import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import app as app_module
from runpod_ocr import RunPodOCRUnavailable
from security_support import authenticate_owner, configure_owner_access
from workflow import OrderGuardService


class TestRunPodOCRRoute(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        original_service = app_module.service
        self.addCleanup(setattr, app_module, "service", original_service)
        app_module.service = OrderGuardService(str(Path(self.tmp.name) / "ocr-route.db"))
        configure_owner_access(self, app_module.app)
        self.client = app_module.app.test_client()

    def login_headers(self):
        token = authenticate_owner(self.client, app_module.app, automatic_csrf=False)
        return {"X-CSRF-Token": token}

    def test_anonymous_ocr_request_is_rejected_before_provider_call(self):
        with patch("app.ocr_invoice") as provider:
            response = self.client.post(
                "/api/ocr-invoice",
                data={"invoice_file": (io.BytesIO(b"fake"), "invoice.png")},
                content_type="multipart/form-data",
            )
        self.assertEqual(response.status_code, 401)
        provider.assert_not_called()
        self.assertEqual(app_module.service.list_cases(), [])

    def test_missing_file_is_rejected_without_provider_call(self):
        headers = self.login_headers()
        with patch("app.ocr_invoice") as provider:
            response = self.client.post(
                "/api/ocr-invoice",
                data={},
                headers=headers,
                content_type="multipart/form-data",
            )
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.get_json()["ok"])
        provider.assert_not_called()

    def test_successful_ocr_returns_human_confirmed_suggestions(self):
        headers = self.login_headers()
        provider_result = {
            "ok": True,
            "provider_status": "COMPLETED",
            "gpu_used": True,
            "gpu_name": "NVIDIA GeForce RTX 5090",
            "ocr_text": "Supplier: FreshFarm\nItem: Chicken\nQuantity: 10",
            "fields": {
                "supplier_name": "FreshFarm",
                "item": "Chicken",
                "quantity": 10.0,
                "unit": "kg",
                "unit_price": 13.0,
                "invoice_total": 130.0,
            },
        }
        with patch("app.ocr_invoice", return_value=provider_result) as provider:
            response = self.client.post(
                "/api/ocr-invoice",
                data={
                    "invoice_file": (
                        io.BytesIO(b"synthetic-png-bytes"),
                        "invoice.png",
                        "image/png",
                    )
                },
                headers=headers,
                content_type="multipart/form-data",
            )
        self.assertEqual(response.status_code, 200)
        body = response.get_json()
        self.assertTrue(body["ok"])
        self.assertTrue(body["requires_human_confirmation"])
        self.assertEqual(body["data"]["fields"]["quantity"], 10.0)
        self.assertTrue(body["data"]["gpu_used"])
        provider.assert_called_once_with(b"synthetic-png-bytes", "image/png")
        self.assertEqual(app_module.service.list_cases(), [])

    def test_provider_failure_returns_manual_fallback_without_exception_details(self):
        headers = self.login_headers()
        with patch(
            "app.ocr_invoice",
            side_effect=RunPodOCRUnavailable("RunPod OCR is temporarily unavailable. Use manual entry instead."),
        ):
            response = self.client.post(
                "/api/ocr-invoice",
                data={
                    "invoice_file": (
                        io.BytesIO(b"synthetic-png-bytes"),
                        "invoice.png",
                        "image/png",
                    )
                },
                headers=headers,
                content_type="multipart/form-data",
            )
        self.assertEqual(response.status_code, 503)
        body = response.get_json()
        self.assertFalse(body["ok"])
        self.assertEqual(body["fallback"], "manual")
        self.assertIn("manual", body["error"].lower())
        self.assertEqual(app_module.service.list_cases(), [])

    def test_ocr_route_requires_valid_csrf(self):
        self.login_headers()
        with patch("app.ocr_invoice") as provider:
            response = self.client.post(
                "/api/ocr-invoice",
                data={"invoice_file": (io.BytesIO(b"fake"), "invoice.png", "image/png")},
                headers={"X-CSRF-Token": "wrong"},
                content_type="multipart/form-data",
            )
        self.assertEqual(response.status_code, 400)
        provider.assert_not_called()


if __name__ == "__main__":
    unittest.main()
