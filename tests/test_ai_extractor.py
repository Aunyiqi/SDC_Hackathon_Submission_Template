import json
import os
import secrets
import sys
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from ai_extractor import (
    AIExtractionUnavailable,
    MAX_MESSAGE_CHARS,
    _validated_suggestions,
    extract_supplier_message,
)


class TestAIExtractor(unittest.TestCase):
    def test_valid_suggestions_are_whitelisted_and_missing_values_are_null(self):
        result = _validated_suggestions({"item": " Chicken ", "quantity": 8, "extra": "ignored"})
        self.assertEqual(result, {"item": "Chicken", "unit": None, "quantity": 8, "unit_price": None})
        self.assertEqual(_validated_suggestions({"unit": " "})["unit"], None)

    def test_non_object_response_is_rejected(self):
        for value in ([], None, "text", 10):
            with self.subTest(value_type=type(value).__name__), self.assertRaises(ValueError):
                _validated_suggestions(value)

    def test_invalid_numbers_are_rejected(self):
        for field in ("quantity", "unit_price"):
            for value in (-1, float("nan"), float("inf"), True, "8 kg", {}):
                with self.subTest(field=field, value_type=type(value).__name__):
                    with self.assertRaises(ValueError):
                        _validated_suggestions({field: value})

    def test_invalid_or_oversized_text_is_rejected(self):
        for field, size in (("item", 201), ("unit", 41)):
            for value in ("x" * size, 12, [], {}):
                with self.subTest(field=field, value_type=type(value).__name__):
                    with self.assertRaises(ValueError):
                        _validated_suggestions({field: value})

    def test_request_limits_and_response_validation(self):
        response = Mock()
        response.json.return_value = {
            "choices": [{"message": {"content": json.dumps({"item": "Chicken", "quantity": 8, "unit": "kg", "unit_price": 13})}}]
        }
        with patch.dict(os.environ, {"DEEPSEEK_API_KEY": secrets.token_urlsafe(32)}):
            with patch("ai_extractor.requests.post", return_value=response) as provider:
                result = extract_supplier_message("Synthetic received/invoice evidence.")
                self.assertEqual(result["quantity"], 8)
                self.assertEqual(provider.call_args.kwargs["json"]["max_tokens"], 256)
                self.assertEqual(provider.call_args.kwargs["timeout"], (5, 20))
                response.raise_for_status.assert_called_once()
                response.json.return_value = {"choices": [{"message": {"content": '["not an object"]'}}]}
                with self.assertRaises(ValueError):
                    extract_supplier_message("Synthetic evidence.")

    def test_invalid_input_never_calls_provider(self):
        with patch("ai_extractor.requests.post") as provider:
            for message in (None, [], "", " ", "x" * (MAX_MESSAGE_CHARS + 1)):
                with self.subTest(message_type=type(message).__name__), self.assertRaises(ValueError):
                    extract_supplier_message(message)
            provider.assert_not_called()

    def test_missing_configuration_uses_manual_fallback_without_network(self):
        with patch.dict(os.environ, {}, clear=True), patch("ai_extractor.requests.post") as provider:
            with self.assertRaises(AIExtractionUnavailable):
                extract_supplier_message("Synthetic evidence.")
            provider.assert_not_called()


if __name__ == "__main__":
    unittest.main()
