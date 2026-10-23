from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from typing import Any, Dict, Iterator, List

from discrepancy_engine import compare_records


class OrderGuardService:
    def __init__(self, db_path: str = "orderguard.db") -> None:
        self.db_path = db_path
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    @contextmanager
    def _db(self) -> Iterator[sqlite3.Connection]:
        conn = self._connect()
        try:
            with conn:
                yield conn
        finally:
            conn.close()

    def _init_db(self) -> None:
        with self._db() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS cases (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    supplier_message TEXT NOT NULL,
                    purchase_order TEXT NOT NULL,
                    received TEXT NOT NULL,
                    invoice TEXT NOT NULL,
                    comparison TEXT NOT NULL,
                    proposed_action TEXT NOT NULL,
                    status TEXT NOT NULL,
                    submitted_by TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS activity_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    case_id INTEGER NOT NULL,
                    actor TEXT NOT NULL,
                    action TEXT NOT NULL,
                    details TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS outbox (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    case_id INTEGER NOT NULL UNIQUE,
                    message TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                """
            )

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).isoformat()

    def _log(self, conn: sqlite3.Connection, case_id: int, actor: str, action: str, details: str) -> None:
        conn.execute(
            "INSERT INTO activity_log(case_id, actor, action, details, created_at) VALUES (?, ?, ?, ?, ?)",
            (case_id, actor, action, details, self._now()),
        )

    def create_case(
        self,
        supplier_message: str,
        purchase_order: Dict[str, Any],
        received: Dict[str, Any],
        invoice: Dict[str, Any],
        submitted_by: str,
    ) -> int:
        comparison = compare_records(purchase_order, received, invoice)
        proposed_action = self._propose_action(comparison)
        with self._db() as conn:
            cur = conn.execute(
                """INSERT INTO cases
                (supplier_message, purchase_order, received, invoice, comparison, proposed_action, status, submitted_by, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    supplier_message,
                    json.dumps(purchase_order),
                    json.dumps(received),
                    json.dumps(invoice),
                    json.dumps(comparison),
                    proposed_action,
                    "PENDING_APPROVAL" if comparison["status"] != "MATCH" else "MATCHED",
                    submitted_by,
                    self._now(),
                ),
            )
            case_id = int(cur.lastrowid)
            self._log(conn, case_id, submitted_by, "CASE_SUBMITTED", "Records submitted for comparison")
            self._log(conn, case_id, "system", "COMPARISON_COMPLETED", comparison["status"])
        return case_id

    @staticmethod
    def _propose_action(comparison: Dict[str, Any]) -> str:
        if comparison["status"] == "MATCH":
            return "No supplier clarification is required."
        if comparison["status"] == "NEEDS_CLARIFICATION":
            return "Confirm the unit conversion or missing information before any supplier action."
        labels = [d["type"].replace("_", " ").title() for d in comparison["discrepancies"]]
        return "Please verify the following discrepancy/discrepancies: " + ", ".join(labels) + "."

    def get_case(self, case_id: int) -> Dict[str, Any]:
        with self._db() as conn:
            row = conn.execute("SELECT * FROM cases WHERE id = ?", (case_id,)).fetchone()
        if row is None:
            raise KeyError(f"Case {case_id} not found")
        result = dict(row)
        for field in ("purchase_order", "received", "invoice", "comparison"):
            result[field] = json.loads(result[field])
        return result

    def list_cases(self) -> List[Dict[str, Any]]:
        with self._db() as conn:
            rows = conn.execute("SELECT id, status, submitted_by, created_at, proposed_action FROM cases ORDER BY id DESC").fetchall()
        return [dict(row) for row in rows]

    def approve_case(self, case_id: int, actor: str, role: str) -> None:
        if role != "owner":
            raise PermissionError("Only an owner may approve a consequential action")
        with self._db() as conn:
            row = conn.execute("SELECT status, proposed_action FROM cases WHERE id = ?", (case_id,)).fetchone()
            if row is None:
                raise KeyError(f"Case {case_id} not found")
            if row["status"] == "APPROVED":
                return
            if row["status"] != "PENDING_APPROVAL":
                raise ValueError(f"Case cannot be approved from status {row['status']}")
            conn.execute("UPDATE cases SET status = 'APPROVED' WHERE id = ?", (case_id,))
            conn.execute(
                "INSERT OR IGNORE INTO outbox(case_id, message, created_at) VALUES (?, ?, ?)",
                (case_id, row["proposed_action"], self._now()),
            )
            self._log(conn, case_id, actor, "APPROVED", "Owner approved the proposed clarification")
            self._log(conn, case_id, "system", "OUTBOX_CREATED", "Simulated supplier message added to outbox")

    def reject_case(self, case_id: int, actor: str, role: str, reason: str) -> None:
        if role != "owner":
            raise PermissionError("Only an owner may reject a consequential action")
        with self._db() as conn:
            row = conn.execute("SELECT status FROM cases WHERE id = ?", (case_id,)).fetchone()
            if row is None:
                raise KeyError(f"Case {case_id} not found")
            if row["status"] != "PENDING_APPROVAL":
                raise ValueError(f"Case cannot be rejected from status {row['status']}")
            conn.execute("UPDATE cases SET status = 'REJECTED' WHERE id = ?", (case_id,))
            self._log(conn, case_id, actor, "REJECTED", reason or "No reason provided")

    def get_outbox(self) -> List[Dict[str, Any]]:
        with self._db() as conn:
            rows = conn.execute("SELECT id, case_id, message, created_at FROM outbox ORDER BY id DESC").fetchall()
        return [dict(row) for row in rows]

    def get_activity(self, case_id: int) -> List[Dict[str, Any]]:
        with self._db() as conn:
            rows = conn.execute(
                "SELECT actor, action, details, created_at FROM activity_log WHERE case_id = ? ORDER BY id ASC",
                (case_id,),
            ).fetchall()
        return [dict(row) for row in rows]
