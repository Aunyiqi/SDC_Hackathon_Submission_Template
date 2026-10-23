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


if __name__ == "__main__":
    unittest.main()
