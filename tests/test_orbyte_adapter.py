import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from orbyte_adapter import build_pending_action_summary, build_priority_queue, filter_cases


CASES = [
    {"id": 1, "supplier_name": "FreshFarm Foods", "status": "PENDING_APPROVAL"},
    {"id": 2, "supplier_name": "RiceHub Supply", "status": "NEEDS_CLARIFICATION"},
    {"id": 3, "supplier_name": "Golden Egg Trading", "status": "MATCHED"},
    {"id": 4, "supplier_name": "FreshFarm Foods", "status": "APPROVED"},
]


class TestOrbyteAdapter(unittest.TestCase):
    def test_pending_action_summary_separates_clarify_review_and_approved(self):
        summary = build_pending_action_summary(CASES)
        self.assertEqual(summary["all"], 3)
        self.assertEqual(summary["clarify"], 1)
        self.assertEqual(summary["review"], 1)
        self.assertEqual(summary["approved"], 1)

    def test_filter_cases_searches_supplier_case_insensitively(self):
        result = filter_cases(CASES, query="freshfarm", status="ALL")
        self.assertEqual([case["id"] for case in result], [1, 4])

    def test_filter_cases_filters_status_and_query_together(self):
        result = filter_cases(CASES, query="freshfarm", status="APPROVED")
        self.assertEqual([case["id"] for case in result], [4])

    def test_filter_cases_all_status_keeps_all_when_query_empty(self):
        result = filter_cases(CASES, query="", status="ALL")
        self.assertEqual([case["id"] for case in result], [1, 2, 3, 4])

    def test_priority_queue_promotes_recurring_supplier_exception(self):
        cases = [
            {
                "id": 10,
                "supplier_name": "FreshFarm Foods",
                "status": "APPROVED",
                "comparison": {
                    "difference": 34,
                    "discrepancies": [{"type": "QUANTITY_MISMATCH"}],
                },
            },
            {
                "id": 11,
                "supplier_name": "FreshFarm Foods",
                "status": "PENDING_APPROVAL",
                "comparison": {
                    "difference": 34,
                    "discrepancies": [
                        {"type": "QUANTITY_MISMATCH"},
                        {"type": "PRICE_MISMATCH"},
                    ],
                },
            },
            {
                "id": 12,
                "supplier_name": "RiceHub Supply",
                "status": "NEEDS_CLARIFICATION",
                "comparison": {
                    "difference": None,
                    "discrepancies": [{"type": "UNIT_CLARIFICATION"}],
                },
            },
        ]

        queue = build_priority_queue(cases)

        self.assertEqual([case["id"] for case in queue], [11, 12])
        self.assertEqual(queue[0]["priority"], "P1")
        self.assertEqual(queue[0]["money_at_risk"], 34.0)
        self.assertTrue(
            any("exception cases" in reason for reason in queue[0]["priority_reasons"])
        )
        self.assertEqual(queue[1]["priority"], "P2")

    def test_priority_queue_excludes_closed_or_matched_cases(self):
        cases = [
            {"id": 1, "supplier_name": "A", "status": "MATCHED", "comparison": {}},
            {"id": 2, "supplier_name": "B", "status": "APPROVED", "comparison": {}},
            {"id": 3, "supplier_name": "C", "status": "REJECTED", "comparison": {}},
        ]
        self.assertEqual(build_priority_queue(cases), [])


if __name__ == "__main__":
    unittest.main()
