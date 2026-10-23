from __future__ import annotations

from collections import Counter
from typing import Any, Dict, Iterable, List


OPEN_ACTION_STATUSES = {"PENDING_APPROVAL", "NEEDS_CLARIFICATION"}
EXCEPTION_STATUSES = {"PENDING_APPROVAL", "NEEDS_CLARIFICATION", "APPROVED", "REJECTED"}


def _safe_money_at_risk(case: Dict[str, Any]) -> float:
    difference = case.get("comparison", {}).get("difference")
    if difference is None:
        return 0.0
    try:
        return round(abs(float(difference)), 2)
    except (TypeError, ValueError):
        return 0.0


def _is_exception_case(case: Dict[str, Any]) -> bool:
    if str(case.get("status", "")).upper() in EXCEPTION_STATUSES:
        return True
    return bool(case.get("comparison", {}).get("discrepancies", []))


def build_priority_queue(cases: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Sort open work by transparent operational urgency, never by AI judgment.

    The queue only recommends what an owner should review first. It does not
    approve, reject, blacklist a supplier, or change Trust Gate permissions.
    """
    items = list(cases)
    supplier_exception_counts = Counter(
        (case.get("supplier_name") or "Demo Supplier").strip().lower()
        for case in items
        if _is_exception_case(case)
    )

    queue: List[Dict[str, Any]] = []
    for case in items:
        status = str(case.get("status", "")).upper()
        if status not in OPEN_ACTION_STATUSES:
            continue

        score = 0
        reasons: List[str] = []

        if status == "NEEDS_CLARIFICATION":
            score += 40
            reasons.append("Trust Gate is blocked until a person clarifies the evidence.")
        else:
            score += 30
            reasons.append("An owner decision is waiting.")

        money_at_risk = _safe_money_at_risk(case)
        if money_at_risk >= 100:
            score += 35
            reasons.append(f"RM{money_at_risk:.2f} open risk signal.")
        elif money_at_risk >= 50:
            score += 25
            reasons.append(f"RM{money_at_risk:.2f} open risk signal.")
        elif money_at_risk >= 20:
            score += 15
            reasons.append(f"RM{money_at_risk:.2f} open risk signal.")
        elif money_at_risk > 0:
            score += 5
            reasons.append(f"RM{money_at_risk:.2f} open risk signal.")

        supplier_key = (case.get("supplier_name") or "Demo Supplier").strip().lower()
        supplier_exception_count = supplier_exception_counts[supplier_key]
        if supplier_exception_count > 1:
            score += 20
            reasons.append(
                f"This supplier has {supplier_exception_count} exception cases in the current synthetic history."
            )

        discrepancy_count = len(case.get("comparison", {}).get("discrepancies", []))
        if discrepancy_count >= 2:
            score += 10
            reasons.append(f"{discrepancy_count} discrepancy types need review.")
        elif discrepancy_count == 1:
            score += 5

        priority = "P1" if score >= 60 else "P2" if score >= 30 else "P3"
        enriched = dict(case)
        enriched.update(
            {
                "priority": priority,
                "priority_score": score,
                "priority_reasons": reasons,
                "money_at_risk": money_at_risk,
            }
        )
        queue.append(enriched)

    priority_rank = {"P1": 0, "P2": 1, "P3": 2}
    queue.sort(
        key=lambda case: (
            priority_rank.get(case["priority"], 9),
            -int(case["priority_score"]),
            -int(case.get("id", 0)),
        )
    )
    return queue


def build_pending_action_summary(cases: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    items = list(cases)
    return {
        "all": sum(case.get("status") in {"NEEDS_CLARIFICATION", "PENDING_APPROVAL", "APPROVED"} for case in items),
        "clarify": sum(case.get("status") == "NEEDS_CLARIFICATION" for case in items),
        "review": sum(case.get("status") == "PENDING_APPROVAL" for case in items),
        "approved": sum(case.get("status") == "APPROVED" for case in items),
        "queue": build_priority_queue(items),
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
