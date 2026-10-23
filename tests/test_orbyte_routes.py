import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import app as app_module
from workflow import OrderGuardService


class TestOrbyteAlignedRoutes(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        app_module.service = OrderGuardService(str(Path(self.tmp.name) / "routes.db"))
        app_module.app.config.update(TESTING=True)
        self.client = app_module.app.test_client()

    def tearDown(self):
        self.tmp.cleanup()

    def valid_form(self):
        return {
            "supplier_name": "FreshFarm Foods",
            "item": "Chicken",
            "supplier_message": "Delivered 8 kg chicken. Invoice 10 kg at RM13/kg.",
            "po_quantity": "10",
            "po_unit": "kg",
            "po_price": "12",
            "received_quantity": "8",
            "received_unit": "kg",
            "invoice_quantity": "10",
            "invoice_unit": "kg",
            "invoice_price": "13",
        }

    def test_dashboard_renders_pending_actions(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Pending Actions", response.data)
        self.assertIn(b"Supplier Checks", response.data)

    def test_checks_support_search_and_status_filter(self):
        app_module.service.create_case(
            "Delivered 8 kg chicken.",
            {"item": "Chicken", "quantity": 10, "unit": "kg", "unit_price": 12},
            {"item": "Chicken", "quantity": 8, "unit": "kg"},
            {"item": "Chicken", "quantity": 10, "unit": "kg", "unit_price": 13},
            "staff-demo",
            supplier_name="FreshFarm Foods",
        )
        response = self.client.get("/checks?q=freshfarm&status=PENDING_APPROVAL")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"FreshFarm Foods", response.data)

    def test_reports_renders_supplier_exception_radar(self):
        response = self.client.get("/reports")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Supplier Exception Radar", response.data)

    def test_new_check_renders_live_evidence_preview(self):
        response = self.client.get("/cases/new")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Live Evidence Preview", response.data)
        self.assertIn(b"Browser preview only", response.data)
        self.assertIn(b"orderguard.js", response.data)
        self.assertIn(b"new_check.css", response.data)

        css_response = self.client.get("/static/new_check.css")
        self.assertEqual(css_response.status_code, 200)
        self.assertIn(b".check-stepper", css_response.data)
        self.assertIn(b".record-card", css_response.data)
        self.assertIn(b".preview-state", css_response.data)

    def test_new_case_rejects_negative_numeric_values(self):
        data = self.valid_form()
        data["po_quantity"] = "-1"
        response = self.client.post("/cases/new", data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Purchase order quantity cannot be negative", response.data)
        self.assertEqual(app_module.service.list_cases(), [])

    def test_new_case_rejects_non_finite_numbers(self):
        data = self.valid_form()
        data["invoice_price"] = "nan"
        response = self.client.post("/cases/new", data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Invoice unit price must be a finite number", response.data)
        self.assertEqual(app_module.service.list_cases(), [])

    def test_new_case_rejects_blank_required_text(self):
        data = self.valid_form()
        data["supplier_name"] = "   "
        response = self.client.post("/cases/new", data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Supplier name is required", response.data)
        self.assertEqual(app_module.service.list_cases(), [])


if __name__ == "__main__":
    unittest.main()
