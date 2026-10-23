import os
import secrets
import sqlite3
import sys
import tempfile
import threading
import time
import unittest
from concurrent.futures import ThreadPoolExecutor
from contextlib import closing
from html.parser import HTMLParser
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import app as app_module
from ai_extractor import AIExtractionUnavailable, MAX_MESSAGE_CHARS
from demo_security import AttemptLimiter
from security_support import authenticate_owner, configure_owner_access
from workflow import OrderGuardService


class PostFormParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.forms = []
        self.current = None

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "form":
            self.current = values if values.get("method", "").lower() == "post" else None
            if self.current is not None:
                self.current["has_csrf"] = False
                self.forms.append(self.current)
        elif tag == "input" and self.current is not None:
            if values.get("name") == "csrf_token" and values.get("value"):
                self.current["has_csrf"] = True

    def handle_endtag(self, tag):
        if tag == "form":
            self.current = None


class TestDemoSecurity(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        original_service = app_module.service
        self.addCleanup(setattr, app_module, "service", original_service)
        self.service = OrderGuardService(str(Path(self.tmp.name) / "security.db"))
        app_module.service = self.service
        configure_owner_access(self, app_module.app)
        self.client = app_module.app.test_client()

    def create_case(self, received_unit="kg"):
        return self.service.create_case(
            "Synthetic supplier evidence.",
            {"item": "Chicken", "quantity": 10, "unit": "kg", "unit_price": 12},
            {"item": "Chicken", "quantity": 8, "unit": received_unit},
            {"item": "Chicken", "quantity": 10, "unit": "kg", "unit_price": 13},
            "test-staff",
        )

    def login(self):
        token = authenticate_owner(self.client, app_module.app, automatic_csrf=False)
        return {"X-CSRF-Token": token}

    def test_anonymous_visitors_cannot_mutate_or_call_ai(self):
        case_id = self.create_case()
        paths = [
            "/cases/new",
            "/demo/scenario/discrepancy",
            f"/cases/{case_id}/approve",
            f"/cases/{case_id}/reject",
            f"/cases/{case_id}/clarify",
            "/demo/reset",
            "/api/extract",
        ]
        with patch("app.extract_supplier_message") as provider:
            for path in paths:
                with self.subTest(path=path), self.client.post(path) as response:
                    self.assertEqual(response.status_code, 401)
            provider.assert_not_called()
        self.assertEqual(self.service.get_case(case_id)["status"], "PENDING_APPROVAL")
        self.assertEqual(self.service.get_outbox(), [])
        self.assertEqual(len(self.service.list_cases()), 1)

    def test_unconfigured_or_weak_secret_configuration_is_read_only(self):
        original = app_module.app.config.copy()
        for invalid in (
            {"OWNER_SIGNING_KEY_CONFIGURED": False},
            {"SECRET_KEY": "short"},
            {"OWNER_ACCESS_CODE": ""},
            {"OWNER_ACCESS_CODE": "short"},
        ):
            with self.subTest(invalid_setting=next(iter(invalid))):
                app_module.app.config.update(original)
                app_module.app.config.update(invalid)
                with self.client.post("/demo/scenario/match") as response:
                    self.assertEqual(response.status_code, 503)
                with self.client.get("/owner/login") as response:
                    self.assertIn(b"Owner controls are not configured", response.data)
        app_module.app.config.update(original)
        self.assertEqual(self.service.list_cases(), [])

    def test_public_views_are_read_only_and_missing_case_is_404(self):
        case_id = self.create_case()
        with self.client.get("/") as response:
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Read-only visitor", response.data)
            self.assertNotIn(b"Reset synthetic records", response.data)
        with self.client.get(f"/cases/{case_id}") as response:
            self.assertNotIn(b"Approve clarification", response.data)
        with self.client.get("/cases/new") as response:
            self.assertEqual(response.status_code, 302)
            self.assertTrue(response.location.endswith("/owner/login"))
        with self.client.get("/cases/99999") as response:
            self.assertEqual(response.status_code, 404)

    def test_login_rotates_csrf_and_does_not_put_access_code_in_session(self):
        with self.client.get("/owner/login"):
            pass
        with self.client.session_transaction() as session:
            previous_token = session["csrf_token"]
        headers = self.login()
        with self.client.session_transaction() as session:
            self.assertTrue(session.permanent)
            self.assertTrue(bool(session.get("owner_session")))
            self.assertFalse(previous_token == session["csrf_token"])
            self.assertNotIn("access_code", session)
            self.assertFalse(
                any(value == app_module.app.config["OWNER_ACCESS_CODE"] for value in session.values())
            )
        with self.client.post("/demo/scenario/match", headers=headers) as response:
            self.assertEqual(response.status_code, 302)

    def test_login_rejects_wrong_code_and_limits_attempts(self):
        with self.client.get("/owner/login"):
            pass
        with self.client.session_transaction() as session:
            token = session["csrf_token"]
        for attempt in range(6):
            with self.client.post(
                "/owner/login", data={"access_code": "incorrect", "csrf_token": token}
            ) as response:
                self.assertEqual(response.status_code, 401 if attempt < 5 else 429)
                if attempt == 5:
                    self.assertGreater(int(response.headers["Retry-After"]), 0)
        with self.client.session_transaction() as session:
            self.assertNotIn("owner_session", session)

    def test_login_requires_csrf_even_with_correct_code(self):
        with self.client.post(
            "/owner/login", data={"access_code": app_module.app.config["OWNER_ACCESS_CODE"]}
        ) as response:
            self.assertEqual(response.status_code, 400)

    def test_owner_mutations_require_csrf_and_valid_requests_work(self):
        case_id = self.create_case()
        headers = self.login()
        for invalid_headers in ({}, {"X-CSRF-Token": "wrong"}, {"X-CSRF-Token": "非ASCII"}):
            with self.subTest(headers_present=bool(invalid_headers)):
                with self.client.post(f"/cases/{case_id}/approve", headers=invalid_headers) as response:
                    self.assertEqual(response.status_code, 400)
                self.assertEqual(self.service.get_outbox(), [])
        with self.client.post(f"/cases/{case_id}/approve", headers=headers) as response:
            self.assertEqual(response.status_code, 302)
        self.assertEqual(len(self.service.get_outbox()), 1)

    def test_all_rendered_mutating_forms_have_csrf_fields(self):
        self.login()
        pending_id = self.create_case()
        blocked_id = self.create_case(received_unit="bags")
        for path in ("/", "/cases/new", f"/cases/{pending_id}", f"/cases/{blocked_id}"):
            with self.subTest(path=path), self.client.get(path) as response:
                parser = PostFormParser()
                parser.feed(response.get_data(as_text=True))
                self.assertTrue(parser.forms)
                self.assertTrue(all(form["has_csrf"] for form in parser.forms))
        with self.client.get(f"/cases/{blocked_id}") as response:
            self.assertIn(b'name="received_unit" value="bags"', response.data)

    def test_owner_manual_workflow_and_unit_clarification_work_without_ai(self):
        headers = self.login()
        form = {
            "supplier_name": "Synthetic Supplier",
            "item": "Chicken",
            "supplier_message": "Received 8 kg; invoice 10 kg at RM13/kg.",
            "po_quantity": "10", "po_unit": "kg", "po_price": "12",
            "received_quantity": "8", "received_unit": "kg",
            "invoice_quantity": "10", "invoice_unit": "kg", "invoice_price": "13",
        }
        with patch.dict(os.environ, {"DEEPSEEK_API_KEY": ""}), patch("app.extract_supplier_message") as provider:
            with self.client.get("/cases/new") as response:
                self.assertIn(b"AI is not configured", response.data)
            with self.client.post("/cases/new", data=form, headers=headers) as response:
                self.assertEqual(response.status_code, 302)
            case_id = self.service.list_cases()[0]["id"]
            self.assertEqual(self.service.get_case(case_id)["status"], "PENDING_APPROVAL")
            with self.client.post(f"/cases/{case_id}/reject", headers=headers) as response:
                self.assertEqual(response.status_code, 302)
            self.assertEqual(self.service.get_case(case_id)["status"], "REJECTED")
            blocked_id = self.create_case(received_unit="bags")
            with self.client.post(
                f"/cases/{blocked_id}/clarify",
                data={"received_quantity": "8", "received_unit": "kg"},
                headers=headers,
            ) as response:
                self.assertEqual(response.status_code, 302)
            self.assertEqual(self.service.get_case(blocked_id)["status"], "PENDING_APPROVAL")
            with self.client.post(f"/cases/{blocked_id}/approve", headers=headers) as response:
                self.assertEqual(response.status_code, 302)
            self.assertEqual(len(self.service.get_outbox()), 1)
            provider.assert_not_called()

    def test_logout_locks_controls_and_rotated_code_invalidates_sessions(self):
        headers = self.login()
        with self.client.post("/owner/logout", headers=headers) as response:
            self.assertEqual(response.status_code, 302)
        with self.client.post("/demo/scenario/match", headers=headers) as response:
            self.assertEqual(response.status_code, 401)
        headers = self.login()
        app_module.app.config["OWNER_ACCESS_CODE"] = secrets.token_urlsafe(32)
        with self.client.post("/demo/scenario/match", headers=headers) as response:
            self.assertEqual(response.status_code, 401)

    def test_owner_session_expires(self):
        headers = self.login()
        future = time.time() + 31 * 60
        with patch("itsdangerous.timed.time.time", return_value=future):
            with self.client.post("/demo/scenario/match", headers=headers) as response:
                self.assertEqual(response.status_code, 401)

    def test_mutation_does_not_extend_owner_session_past_login_deadline(self):
        headers = self.login()
        now = time.time()
        with patch("itsdangerous.timed.time.time", return_value=now + 20 * 60):
            with self.client.post("/demo/scenario/match", headers=headers) as response:
                self.assertEqual(response.status_code, 302)
        with patch("itsdangerous.timed.time.time", return_value=now + 31 * 60):
            with self.client.post("/demo/scenario/match", headers=headers) as response:
                self.assertEqual(response.status_code, 401)

    def test_secure_cookie_and_response_headers(self):
        app_module.app.config["SESSION_COOKIE_SECURE"] = True
        with self.client.get("/", base_url="https://localhost") as response:
            cookie = response.headers["Set-Cookie"]
            self.assertTrue("Secure;" in cookie and "HttpOnly;" in cookie)
            self.assertIn("SameSite=Lax", cookie)
            self.assertEqual(response.headers["Cache-Control"], "no-store")
            self.assertEqual(response.headers["X-Content-Type-Options"], "nosniff")
            self.assertEqual(response.headers["X-Frame-Options"], "DENY")

    def test_reset_needs_confirmation_and_preserves_database_and_id_sequence(self):
        case_id = self.create_case()
        self.service.approve_case(case_id, "test-owner", "owner")
        db_path = Path(self.service.db_path)
        inode = db_path.stat().st_ino
        headers = self.login()
        with self.client.post("/demo/reset", headers=headers) as response:
            self.assertEqual(response.status_code, 400)
        self.assertEqual(len(self.service.list_cases()), 1)
        with self.client.post(
            "/demo/reset", data={"confirmation": "reset-synthetic-data"}, headers=headers
        ) as response:
            self.assertEqual(response.status_code, 302)
        self.assertEqual(db_path.stat().st_ino, inode)
        self.assertEqual(self.service.list_cases(), [])
        self.assertEqual(self.service.get_outbox(), [])
        self.assertEqual(self.service.get_activity(case_id), [])
        self.assertGreater(self.create_case(), case_id)
        with self.client.get(f"/cases/{case_id}") as response:
            self.assertEqual(response.status_code, 404)

    def test_staff_cannot_reset_and_failed_reset_rolls_back_all_deletes(self):
        case_id = self.create_case()
        self.service.approve_case(case_id, "test-owner", "owner")
        with self.assertRaises(PermissionError):
            self.service.reset_demo("staff")
        with closing(sqlite3.connect(self.service.db_path)) as conn, conn:
            conn.execute(
                "CREATE TRIGGER refuse_test_reset BEFORE DELETE ON cases "
                "BEGIN SELECT RAISE(ABORT, 'test reset failure'); END;"
            )
        with self.assertRaises(sqlite3.IntegrityError):
            self.service.reset_demo("owner")
        self.assertEqual(len(self.service.list_cases()), 1)
        self.assertEqual(len(self.service.get_outbox()), 1)
        self.assertTrue(self.service.get_activity(case_id))

    def test_concurrent_approvals_create_one_outbox_and_one_approval_event(self):
        case_id = self.create_case()
        ready = threading.Barrier(2)

        def approve():
            ready.wait(timeout=5)
            self.service.approve_case(case_id, "test-owner", "owner")

        with ThreadPoolExecutor(max_workers=2) as pool:
            futures = [pool.submit(approve) for _ in range(2)]
            for future in futures:
                future.result(timeout=10)
        self.assertEqual(len(self.service.get_outbox()), 1)
        actions = [entry["action"] for entry in self.service.get_activity(case_id)]
        self.assertEqual(actions.count("APPROVED"), 1)
        self.assertEqual(actions.count("OUTBOX_CREATED"), 1)

    def test_concurrent_reset_and_approval_cannot_leave_orphan_outbox(self):
        case_id = self.create_case()
        ready = threading.Barrier(2)

        def approve():
            ready.wait(timeout=5)
            try:
                self.service.approve_case(case_id, "test-owner", "owner")
            except KeyError:
                pass  # The reset committed first.

        def reset():
            ready.wait(timeout=5)
            self.service.reset_demo("owner")

        with ThreadPoolExecutor(max_workers=2) as pool:
            futures = [pool.submit(approve), pool.submit(reset)]
            for future in futures:
                future.result(timeout=10)
        self.assertEqual(self.service.list_cases(), [])
        self.assertEqual(self.service.get_outbox(), [])
        self.assertEqual(self.service.get_activity(case_id), [])

    def test_extraction_rejects_malformed_or_oversized_payloads_without_provider_call(self):
        headers = self.login()
        invalid_payloads = [[], "text", 42, None, {}, {"message": None}, {"message": 5}, {"message": "  "}]
        with patch("app.extract_supplier_message") as provider:
            for payload in invalid_payloads:
                with self.subTest(payload_type=type(payload).__name__):
                    with self.client.post("/api/extract", json=payload, headers=headers) as response:
                        self.assertEqual(response.status_code, 400)
                        self.assertFalse(response.get_json()["ok"])
            for size in (MAX_MESSAGE_CHARS + 1, 70_000):
                with self.client.post(
                    "/api/extract", json={"message": "x" * size}, headers=headers
                ) as response:
                    self.assertEqual(response.status_code, 413)
                    self.assertFalse(response.get_json()["ok"])
            provider.assert_not_called()

    def test_extraction_requires_csrf_and_is_rate_limited(self):
        headers = self.login()
        suggestions = {"item": "Chicken", "quantity": 8, "unit": "kg", "unit_price": 13}
        with patch("app.extract_supplier_message", return_value=suggestions) as provider:
            with self.client.post("/api/extract", json={"message": "Synthetic message"}) as response:
                self.assertEqual(response.status_code, 400)
            provider.assert_not_called()
            for _ in range(10):
                with self.client.post(
                    "/api/extract", json={"message": "Synthetic message"}, headers=headers
                ) as response:
                    self.assertEqual(response.status_code, 200)
                    self.assertTrue(response.get_json()["requires_human_confirmation"])
            with self.client.post(
                "/api/extract", json={"message": "Synthetic message"}, headers=headers
            ) as response:
                self.assertEqual(response.status_code, 429)
                self.assertGreater(int(response.headers["Retry-After"]), 0)
            self.assertEqual(provider.call_count, 10)

    def test_extraction_failure_keeps_manual_fallback_without_exception_details(self):
        headers = self.login()
        for failure, expected in (
            (AIExtractionUnavailable("AI is not configured."), 503),
            (ValueError("private upstream details must not be exposed"), 502),
        ):
            with self.subTest(status=expected), patch("app.extract_supplier_message", side_effect=failure):
                with self.client.post(
                    "/api/extract", json={"message": "Synthetic message"}, headers=headers
                ) as response:
                    self.assertEqual(response.status_code, expected)
                    self.assertEqual(response.get_json()["fallback"], "manual")
                    self.assertNotIn(b"private upstream details", response.data)


class TestAttemptLimiter(unittest.TestCase):
    def test_rolling_window_is_bounded_and_reopens_without_sleeping(self):
        now = [0.0]
        limiter = AttemptLimiter(2, 60, clock=lambda: now[0])
        self.assertEqual(limiter.consume(), 0)
        now[0] = 10
        self.assertEqual(limiter.consume(), 0)
        self.assertEqual(limiter.consume(), 50)
        now[0] = 60
        self.assertEqual(limiter.consume(), 0)
        self.assertEqual(limiter.consume(), 10)


if __name__ == "__main__":
    unittest.main()
