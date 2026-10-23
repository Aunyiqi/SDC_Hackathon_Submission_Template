from __future__ import annotations

from typing import Any, Dict, Iterable, List


def build_pending_action_summary(cases: Iterable[Dict[str, Any]]) -> Dict[str, int]:
    items = list(cases)
    return {
        "all": sum(case.get("status") in {"NEEDS_CLARIFICATION", "PENDING_APPROVAL", "APPROVED"} for case in items),
        "clarify": sum(case.get("status") == "NEEDS_CLARIFICATION" for case in items),
        "review": sum(case.get("status") == "PENDING_APPROVAL" for case in items),
        "approved": sum(case.get("status") == "APPROVED" for case in items),
    }


def filter_cases(
    cases: Iterable[Dict[str, Any]],
    query: str = "",
    status: str = "ALL",
) -> List[Dict[str, Any]]:
    query_norm = (query or "").strip().lower()
    status_norm = (status or "ALL").strip().upper()
    result: List[Dict[str, Any]] = []

    for case in cases:
        supplier = str(case.get("supplier_name", "")).lower()
        case_label = f"case #{case.get('id', '')}".lower()
        if query_norm and query_norm not in supplier and query_norm not in case_label:
            continue
        if status_norm != "ALL" and str(case.get("status", "")).upper() != status_norm:
            continue
        result.append(case)

    return result
