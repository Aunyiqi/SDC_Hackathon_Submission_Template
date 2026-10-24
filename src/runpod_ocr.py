from __future__ import annotations

import base64
import math
import os
from typing import Any

import requests


MAX_OCR_IMAGE_BYTES = 5 * 1024 * 1024
ALLOWED_IMAGE_MIME_TYPES = {"image/png", "image/jpeg", "image/webp"}
RUNPOD_TIMEOUT_SECONDS = 90
MAX_OCR_TEXT_CHARS = 4000
MAX_TEXT_FIELD_CHARS = 200


class RunPodOCRUnavailable(RuntimeError):
    """Raised when RunPod OCR cannot safely return usable suggestions."""


def _clean_text(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    value = value.strip()
    return value[:MAX_TEXT_FIELD_CHARS] if value else None


def _clean_number(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(number) or number < 0:
        return None
    return number


def _normalize_output(payload: dict[str, Any]) -> dict[str, Any]:
    status = _clean_text(payload.get("status")) or "UNKNOWN"
    output = payload.get("output")
    if not isinstance(output, dict):
        raise RunPodOCRUnavailable("RunPod OCR returned no usable output. Use manual entry instead.")
    if output.get("ok") is not True:
        message = _clean_text(output.get("error")) or "RunPod OCR failed. Use manual entry instead."
        raise RunPodOCRUnavailable(message)

    raw_fields = output.get("fields") if isinstance(output.get("fields"), dict) else {}
    fields = {
        "supplier_name": _clean_text(raw_fields.get("supplier_name")),
        "item": _clean_text(raw_fields.get("item")),
        "quantity": _clean_number(raw_fields.get("quantity")),
        "unit": _clean_text(raw_fields.get("unit")),
        "unit_price": _clean_number(raw_fields.get("unit_price")),
        "invoice_total": _clean_number(raw_fields.get("invoice_total")),
    }
    ocr_text = output.get("ocr_text") if isinstance(output.get("ocr_text"), str) else ""

    return {
        "ok": True,
        "provider_status": status,
        "gpu_used": output.get("gpu_used") is True,
        "gpu_name": _clean_text(output.get("gpu_name")),
        "ocr_text": ocr_text.strip()[:MAX_OCR_TEXT_CHARS],
        "fields": fields,
    }


def ocr_invoice(image_bytes: bytes, mime_type: str) -> dict[str, Any]:
    """Send a bounded synthetic invoice image to the configured RunPod OCR endpoint.

    The function returns suggestions only. It never changes OrderGuard records or
    performs any approval, discrepancy or supplier decision.
    """

    normalized_mime = (mime_type or "").strip().lower()
    if normalized_mime not in ALLOWED_IMAGE_MIME_TYPES:
        raise ValueError("Invoice image must be PNG, JPEG or WebP.")
    if not image_bytes:
        raise ValueError("Invoice image must not be empty.")
    if len(image_bytes) > MAX_OCR_IMAGE_BYTES:
        raise ValueError("Invoice image must be 5 MB or smaller.")

    api_key = os.getenv("RUNPOD_API_KEY", "").strip()
    endpoint_id = os.getenv("RUNPOD_ENDPOINT_ID", "").strip()
    if not api_key or not endpoint_id:
        raise RunPodOCRUnavailable("RunPod OCR is not configured. Use manual entry instead.")

    encoded = base64.b64encode(image_bytes).decode("ascii")
    data_url = f"data:{normalized_mime};base64,{encoded}"
    url = f"https://api.runpod.ai/v2/{endpoint_id}/runsync"

    try:
        response = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={"input": {"image_base64": data_url}},
            timeout=RUNPOD_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        payload = response.json()
    except (requests.RequestException, ValueError) as exc:
        raise RunPodOCRUnavailable("RunPod OCR is temporarily unavailable. Use manual entry instead.") from exc

    if not isinstance(payload, dict):
        raise RunPodOCRUnavailable("RunPod OCR returned an invalid response. Use manual entry instead.")
    return _normalize_output(payload)
