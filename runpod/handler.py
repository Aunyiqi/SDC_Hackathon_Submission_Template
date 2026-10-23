"""RunPod Serverless GPU OCR worker for Vortex OrderGuard.

Purpose
-------
Accept a synthetic invoice / delivery-note image as either a base64 string or
an HTTPS image URL. EasyOCR runs on the RunPod GPU when CUDA is available.
The worker returns the OCR text plus a small set of fields extracted from
clearly labelled demo documents.

Important: this worker performs document reading only. It never approves,
rejects, or scores a supplier. OrderGuard performs the deterministic business
comparison and keeps the final consequential action behind human approval.
"""

from __future__ import annotations

import base64
import io
import re
from typing import Any
from urllib.parse import urlparse

import easyocr
import numpy as np
import requests
import runpod
import torch
from PIL import Image

MAX_IMAGE_BYTES = 8 * 1024 * 1024
_READER: easyocr.Reader | None = None


def _reader() -> easyocr.Reader:
    global _READER
    if _READER is None:
        # EasyOCR will use CUDA when the RunPod worker has a compatible GPU.
        _READER = easyocr.Reader(["en"], gpu=torch.cuda.is_available())
    return _READER


def _decode_image(job_input: dict[str, Any]) -> Image.Image:
    image_base64 = (job_input.get("image_base64") or "").strip()
    image_url = (job_input.get("image_url") or "").strip()

    if bool(image_base64) == bool(image_url):
        raise ValueError("Provide exactly one of image_base64 or image_url.")

    if image_base64:
        if image_base64.startswith("data:"):
            try:
                image_base64 = image_base64.split(",", 1)[1]
            except IndexError as exc:
                raise ValueError("Invalid data URL.") from exc
        try:
            raw = base64.b64decode(image_base64, validate=True)
        except Exception as exc:  # noqa: BLE001 - return a safe validation error
            raise ValueError("image_base64 is not valid base64.") from exc
    else:
        parsed = urlparse(image_url)
        if parsed.scheme not in {"http", "https"}:
            raise ValueError("image_url must use http or https.")
        response = requests.get(image_url, timeout=20)
        response.raise_for_status()
        raw = response.content

    if not raw or len(raw) > MAX_IMAGE_BYTES:
        raise ValueError("Image must be between 1 byte and 8 MB.")

    try:
        return Image.open(io.BytesIO(raw)).convert("RGB")
    except Exception as exc:  # noqa: BLE001
        raise ValueError("The supplied file is not a readable image.") from exc


def _capture(patterns: list[str], text: str) -> str | None:
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return match.group(1).strip(" :-")
    return None


def _number(value: str | None) -> float | None:
    if not value:
        return None
    cleaned = value.replace(",", "")
    match = re.search(r"-?\d+(?:\.\d+)?", cleaned)
    return float(match.group(0)) if match else None


def _extract_labelled_fields(text: str) -> dict[str, Any]:
    """Parse the labelled synthetic documents used in the hackathon demo."""
    supplier = _capture([r"supplier\s*[:\-]\s*([^\n]+)"], text)
    item = _capture([r"item\s*[:\-]\s*([^\n]+)"], text)
    quantity_raw = _capture([r"(?:quantity|qty)\s*[:\-]\s*([^\n]+)"], text)
    unit = _capture([r"unit\s*[:\-]\s*([a-zA-Z]+)"], text)
    unit_price_raw = _capture(
        [r"unit\s*price\s*[:\-]\s*(?:RM\s*)?([^\n]+)", r"price\s*[:\-]\s*(?:RM\s*)?([^\n]+)"],
        text,
    )
    total_raw = _capture([r"(?:invoice\s*)?total\s*[:\-]\s*(?:RM\s*)?([^\n]+)"], text)

    return {
        "supplier_name": supplier,
        "item": item,
        "quantity": _number(quantity_raw),
        "unit": unit.lower() if unit else None,
        "unit_price": _number(unit_price_raw),
        "invoice_total": _number(total_raw),
    }


def handler(job: dict[str, Any]) -> dict[str, Any]:
    try:
        job_input = job.get("input") or {}
        image = _decode_image(job_input)
        lines = _reader().readtext(np.asarray(image), detail=0, paragraph=False)
        ocr_text = "\n".join(str(line).strip() for line in lines if str(line).strip())
        fields = _extract_labelled_fields(ocr_text)

        return {
            "ok": True,
            "gpu_used": bool(torch.cuda.is_available()),
            "gpu_name": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
            "ocr_text": ocr_text,
            "fields": fields,
            "note": "OCR/extraction only. OrderGuard performs deterministic comparison and human approval.",
        }
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "error": str(exc)}


runpod.serverless.start({"handler": handler})
