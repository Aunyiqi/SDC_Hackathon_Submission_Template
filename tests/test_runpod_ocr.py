import math
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from runpod_ocr import (
    ALLOWED_IMAGE_MIME_TYPES,
    MAX_OCR_IMAGE_BYTES,
    RunPodOCRUnavailable,
    ocr_invoice,
)


class TestRunPodOCR(unittest.TestCase):
    def test_missing_credentials_fails_safely(self):
        with patch.dict(
            os.environ,
            {"RUNPOD_API_KEY": "", "RUNPOD_ENDPOINT_ID": ""},
            clear=False,
        ):
            with self.assertRaisesRegex(RunPodOCRUnavailable, "not configured"):
                ocr_invoice(b"fake-image", "image/png")

    def test_rejects_unsupported_mime_before_provider_call(self):
        with patch("runpod_ocr.requests.post") as provider:
            with self.assertRaisesRegex(ValueError, "PNG, JPEG or WebP"):
                ocr_invoice(b"fake-image", "application/pdf")
            provider.assert_not_called()
        self.assertEqual(ALLOWED_IMAGE_MIME_TYPES, {"image/png", "image/jpeg", "image/webp"})

    def test_rejects_empty_and_oversized_images_before_provider_call(self):
        with patch("runpod_ocr.requests.post") as provider:
            with self.assertRaisesRegex(ValueError, "not empty"):
                ocr_invoice(b"", "image/png")
            with self.assertRaisesRegex(ValueError, "5 MB"):
                ocr_invoice(b"x" * (MAX_OCR_IMAGE_BYTES + 1), "image/png")
            provider.assert_not_called()

    def test_successful_runsync_response_is_normalized(self):
        response = Mock()
        response.raise_for_status.return_value = None
        response.json.return_value = {
            "status": "COMPLETED",
            "output": {
                "ok": True,
                "gpu_used": True,
                "gpu_name": "NVIDIA GeForce RTX 5090",
                "ocr_text": "Supplier: FreshFarm\nItem: Chicken\nQuantity: 10",
                "fields": {
                    "supplier_name": "FreshFarm",
                    "item": "Chicken",
                    "quantity": 10,
                    "unit": "kg",
                    "unit_price": 13,
                    "invoice_total": 130,
                    "ignored": "do not expose",
                },
            },
        }
        with patch.dict(
            os.environ,
            {"RUNPOD_API_KEY": "secret-key", "RUNPOD_ENDPOINT_ID": "endpoint-123"},
            clear=False,
        ), patch("runpod_ocr.requests.post", return_value=response) as provider:
            result = ocr_invoice(b"image-bytes", "image/png")

        self.assertTrue(result["ok"])
        self.assertTrue(result["gpu_used"])
        self.assertEqual(result["gpu_name"], "NVIDIA GeForce RTX 5090")
        self.assertEqual(result["provider_status"], "COMPLETED")
        self.assertEqual(
            result["fields"],
            {
                "supplier_name": "FreshFarm",
                "item": "Chicken",
                "quantity": 10.0,
                "unit": "kg",
                "unit_price": 13.0,
                "invoice_total": 130.0,
            },
        )
        self.assertNotIn("ignored", result["fields"])
        args, kwargs = provider.call_args
        self.assertEqual(args[0], "https://api.runpod.ai/v2/endpoint-123/runsync")
        self.assertEqual(kwargs["headers"]["Authorization"], "Bearer secret-key")
        encoded = kwargs["json"]["input"]["image_base64"]
        self.assertTrue(encoded.startswith("data:image/png;base64,"))
        self.assertGreater(kwargs["timeout"], 0)

    def test_invalid_numeric_fields_are_dropped_not_trusted(self):
        response = Mock()
        response.raise_for_status.return_value = None
        response.json.return_value = {
            "status": "COMPLETED",
            "output": {
                "ok": True,
                "gpu_used": False,
                "gpu_name": None,
                "ocr_text": "synthetic",
                "fields": {
                    "quantity": -4,
                    "unit_price": float("inf"),
                    "invoice_total": "not-a-number",
                },
            },
        }
        with patch.dict(
            os.environ,
            {"RUNPOD_API_KEY": "secret-key", "RUNPOD_ENDPOINT_ID": "endpoint-123"},
            clear=False,
        ), patch("runpod_ocr.requests.post", return_value=response):
            result = ocr_invoice(b"image-bytes", "image/jpeg")
        self.assertIsNone(result["fields"]["quantity"])
        self.assertIsNone(result["fields"]["unit_price"])
        self.assertIsNone(result["fields"]["invoice_total"])

    def test_provider_timeout_is_safe_manual_fallback(self):
        with patch.dict(
            os.environ,
            {"RUNPOD_API_KEY": "secret-key", "RUNPOD_ENDPOINT_ID": "endpoint-123"},
            clear=False,
        ), patch("runpod_ocr.requests.post", side_effect=requests.Timeout("cold start timeout")):
            with self.assertRaisesRegex(RunPodOCRUnavailable, "unavailable"):
                ocr_invoice(b"image-bytes", "image/webp")

    def test_failed_provider_output_is_not_treated_as_success(self):
        response = Mock()
        response.raise_for_status.return_value = None
        response.json.return_value = {
            "status": "COMPLETED",
            "output": {"ok": False, "error": "OCR model failed"},
        }
        with patch.dict(
            os.environ,
            {"RUNPOD_API_KEY": "secret-key", "RUNPOD_ENDPOINT_ID": "endpoint-123"},
            clear=False,
        ), patch("runpod_ocr.requests.post", return_value=response):
            with self.assertRaisesRegex(RunPodOCRUnavailable, "OCR model failed"):
                ocr_invoice(b"image-bytes", "image/png")


if __name__ == "__main__":
    unittest.main()
