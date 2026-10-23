import copy
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import app as app_module
from discrepancy_engine import compare_records
from security_support import authenticate_owner, configure_owner_access
from workflow import OrderGuardService


def matching_records():
    return [
        {"item": "Chicken", "quantity": 10, "unit": "kg", "unit_price": 12},
        {"item": "Chicken", "quantity": 10, "unit": "kg"},
        {"item": "Chicken", "quantity": 10, "unit": "kg", "unit_price": 12},
    ]


class TestItemIdentityComparison(unittest.TestCase):
    def assert_item_blocked(self, result):
        self.assertEqual(result["status"], "NEEDS_CLARIFICATION")
        self.assertEqual(result["trust_gate"]["level"], "BLOCKED")
        self.assertFalse(result["trust_gate"]["approval_allowed"])
        self.assertIsNone(result["comparison_amount"])
        self.assertIsNone(result["invoice_amount"])
        self.assertIsNone(result["difference"])
        self.assertIn(
            "ITEM_CLARIFICATION",
            {entry["type"] for entry in result["discrepancies"]},
        )
        self.assertTrue(
            any("item" in reason.lower() for reason in result["trust_gate"]["reasons"])
        )

    def test_different_item_in_any_record_blocks_comparison(self):
        evidence_keys = ("purchase_order_item", "received_item", "invoice_item")
        for record_index in range(3):
            with self.subTest(record_index=record_index):
                records = matching_records()
                records[record_index]["item"] = "Beef"
                original = copy.deepcopy(records)

                result = compare_records(*records)

                self.assert_item_blocked(result)
                self.assertEqual(
                    result["discrepancies"][0]["evidence"],
                    dict(zip(evidence_keys, (record["item"] for record in records))),
                )
                self.assertEqual(records, original)

    def test_missing_item_in_any_record_blocks_comparison(self):
        for record_index in range(3):
            with self.subTest(record_index=record_index):
                records = matching_records()
                del records[record_index]["item"]
                self.assert_item_blocked(compare_records(*records))

    def test_blank_or_non_text_item_in_any_record_blocks_comparison(self):
        for invalid_item in ("", " \t\n ", None, 123, ["Chicken"], {}):
            for record_index in range(3):
                with self.subTest(item=invalid_item, record_index=record_index):
                    records = matching_records()
                    records[record_index]["item"] = invalid_item
                    self.assert_item_blocked(compare_records(*records))

    def test_all_blank_items_are_not_a_match(self):
        records = matching_records()
        for record in records:
            record["item"] = " "
        self.assert_item_blocked(compare_records(*records))

    def test_case_and_whitespace_differences_are_accepted_without_mutation(self):
        records = matching_records()
        records[0]["item"] = " Free Range Chicken "
        records[1]["item"] = "free  range\tchicken"
        records[2]["item"] = "FREE RANGE CHICKEN"
        original = copy.deepcopy(records)

        result = compare_records(*records)

        self.assertEqual(result["status"], "MATCH")
        self.assertEqual(result["discrepancies"], [])
        self.assertEqual(records, original)

    def test_similar_item_names_are_not_fuzzy_matched(self):
        records = matching_records()
        records[0]["item"] = records[2]["item"] = "Rice"
        records[1]["item"] = "Rice flour"
        self.assert_item_blocked(compare_records(*records))

    def test_item_and_unit_issues_are_both_reported(self):
        records = matching_records()
        records[1].update(item="Beef", unit="bags")

        result = compare_records(*records)

        self.assert_item_blocked(result)
        self.assertEqual(
            {entry["type"] for entry in result["discrepancies"]},
            {"ITEM_CLARIFICATION", "UNIT_CLARIFICATION"},
        )
        self.assertTrue(
            any("unit" in reason.lower() for reason in result["trust_gate"]["reasons"])
        )

    def test_matching_items_preserve_quantity_and_price_checks(self):
        records = matching_records()
        records[1].update(item=" chicken ", quantity=8)
        records[2].update(item="CHICKEN", unit_price=13)

        result = compare_records(*records)

        self.assertEqual(result["status"], "REVIEW_REQUIRED")
        self.assertEqual(
            {entry["type"] for entry in result["discrepancies"]},
            {"QUANTITY_MISMATCH", "PRICE_MISMATCH"},
        )
        self.assertEqual(result["difference"], 34.0)
        self.assertTrue(result["trust_gate"]["approval_allowed"])


class TestItemIdentityWorkflow(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.service = OrderGuardService(str(Path(self.tmp.name) / "items.db"))
        records = matching_records()
        records[1].update(item="Beef", quantity=8)
        records[2]["unit_price"] = 13
        self.case_id = self.service.create_case(
            "Source records name different items.", *records, "staff-demo"
        )

    def tearDown(self):
        self.tmp.cleanup()

    def test_item_mismatch_blocks_approval_and_creates_no_outbox(self):
        case = self.service.get_case(self.case_id)
        self.assertEqual(case["status"], "NEEDS_CLARIFICATION")
        self.assertIn("item", case["proposed_action"].lower())
        with self.assertRaises(ValueError):
            self.service.approve_case(self.case_id, "owner-demo", "owner")
        self.assertEqual(self.service.get_outbox(), [])
        actions = [entry["action"] for entry in self.service.get_activity(self.case_id)]
        self.assertIn("TRUST_GATE_BLOCKED", actions)
        self.assertNotIn("APPROVED", actions)
        playbook = self.service.get_supplier_insight(self.case_id)["playbook"]
        self.assertTrue(any("item" in step.lower() for step in playbook))

    def test_quantity_or_unit_clarification_cannot_bypass_item_mismatch(self):
        self.service.clarify_case(
            self.case_id, "owner-demo", received_quantity=10, received_unit="kg"
        )
        case = self.service.get_case(self.case_id)
        self.assertEqual(case["status"], "NEEDS_CLARIFICATION")
        self.assertEqual(case["received"]["item"], "Beef")
        self.assertFalse(case["comparison"]["trust_gate"]["approval_allowed"])
        with self.assertRaises(ValueError):
            self.service.approve_case(self.case_id, "owner-demo", "owner")
        self.assertEqual(self.service.get_outbox(), [])


class TestItemIdentityRoutes(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.original_service = app_module.service
        self.original_testing = app_module.app.config["TESTING"]
        app_module.service = OrderGuardService(str(Path(self.tmp.name) / "routes.db"))
        configure_owner_access(self, app_module.app)
        self.client = app_module.app.test_client()
        authenticate_owner(self.client, app_module.app)

    def tearDown(self):
        app_module.service = self.original_service
        app_module.app.config["TESTING"] = self.original_testing
        self.tmp.cleanup()

    def create_blocked_case(self, missing_item=False):
        records = matching_records()
        records[1].update(item="Beef", quantity=8)
        records[2]["unit_price"] = 13
        if missing_item:
            del records[1]["item"]
        return app_module.service.create_case(
            "Source items need confirmation.", *records, "staff-demo"
        )

    def test_detail_shows_source_items_and_correction_guidance(self):
        case_id = self.create_blocked_case()
        with self.client.get(f"/cases/{case_id}") as response:
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Item identities need correction", response.data)
            self.assertIn(b"Beef", response.data)
            self.assertNotIn(b"Confirm & recalculate", response.data)
            self.assertNotIn(b"Approve clarification", response.data)

    def test_detail_labels_missing_item(self):
        case_id = self.create_blocked_case(missing_item=True)
        with self.client.get(f"/cases/{case_id}") as response:
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Missing item", response.data)
            self.assertIn(b"Item identities need correction", response.data)

    def test_approval_route_cannot_approve_item_mismatch(self):
        case_id = self.create_blocked_case()
        with self.client.post(f"/cases/{case_id}/approve", follow_redirects=True) as response:
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Trust Gate blocks approval", response.data)
        self.assertEqual(app_module.service.get_outbox(), [])
        self.assertEqual(
            app_module.service.get_case(case_id)["status"], "NEEDS_CLARIFICATION"
        )


if __name__ == "__main__":
    unittest.main()
