from __future__ import annotations

import json
import math
import os
from typing import Any, Dict

import requests


MAX_MESSAGE_CHARS = 4000


class AIExtractionUnavailable(RuntimeError):
    pass


def _validated_suggestions(data: Any) -> Dict[str, Any]:
    if not isinstance(data, dict):
        raise ValueError("AI suggestions must be an object")
    result: Dict[str, Any] = {}
    for key, maximum in (("item", 200), ("unit", 40)):
        value = data.get(key)
        if value is not None:
            if not isinstance(value, str) or len(value) > maximum:
                raise ValueError("AI suggestion text is invalid")
            value = value.strip() or None
        result[key] = value
    for key in ("quantity", "unit_price"):
        value = data.get(key)
        if value is not None and (
            isinstance(value, bool)
            or not isinstance(value, (int, float))
            or not math.isfinite(value)
            or value < 0
        ):
            raise ValueError("AI suggestion number is invalid")
        result[key] = value
    return result


def extract_supplier_message(message: str) -> Dict[str, Any]:
    if not isinstance(message, str) or not message.strip() or len(message) > MAX_MESSAGE_CHARS:
        raise ValueError("Supplier message must be nonempty text within the length limit")
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        raise AIExtractionUnavailable("DEEPSEEK_API_KEY is not configured. Use the human-confirmed fields instead.")

    api_url = os.getenv("DEEPSEEK_API_URL", "https://api.deepseek.com/chat/completions")
    model = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
    prompt = (
        "Extract purchasing facts from the supplier message. Return JSON only with keys: "
        "item, quantity, unit, unit_price. Use null for missing or ambiguous values. "
        "quantity means the delivered/received quantity, not the ordered or invoiced quantity. "
        "unit is the delivered/received unit; unit_price is the invoiced unit price. "
        "Do not infer unit conversions or invent values.\n\nSupplier message: " + message
    )
    response = requests.post(
        api_url,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": "You extract structured purchasing data. Never invent missing facts."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0,
            "max_tokens": 256,
            "response_format": {"type": "json_object"},
        },
        timeout=(5, 20),
    )
    response.raise_for_status()
    content = response.json()["choices"][0]["message"]["content"]
    data = json.loads(content)
    return _validated_suggestions(data)
