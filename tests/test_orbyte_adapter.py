import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from orbyte_adapter import build_pending_action_summary, filter_cases


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


if __name__ == "__main__":
    unittest.main()
