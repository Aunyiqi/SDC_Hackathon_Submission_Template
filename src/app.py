from __future__ import annotations

import math
import os
import secrets
import time
from datetime import timedelta
from pathlib import Path

from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from werkzeug.exceptions import RequestEntityTooLarge

from ai_extractor import AIExtractionUnavailable, MAX_MESSAGE_CHARS, extract_supplier_message
from demo_security import (
    MIN_SIGNING_KEY_LENGTH,
    OWNER_SESSION_SECONDS,
    AttemptLimiter,
    constant_time_match,
    csrf_token,
    owner_access_configured,
    owner_session_marker,
    owner_unlocked,
    valid_csrf_token,
)
from orbyte_adapter import build_pending_action_summary, filter_cases
from supplier_radar import build_supplier_radar
from workflow import OrderGuardService


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = os.getenv("ORDERGUARD_DB", str(BASE_DIR / "orderguard.db"))
DEMO_ORG = os.getenv("ORDERGUARD_ORG", "Vortex Demo SME")
DEMO_USER = os.getenv("ORDERGUARD_USER", "Owner Demo")

app = Flask(__name__, template_folder="templates", static_folder="static")
configured_signing_key = os.getenv("FLASK_SECRET_KEY", "")
signing_key_configured = len(configured_signing_key) >= MIN_SIGNING_KEY_LENGTH
# An ephemeral key lets unconfigured deployments render read-only pages safely.
# It never enables owner access; there is no built-in owner code or signing secret.
app.secret_key = configured_signing_key if signing_key_configured else secrets.token_hex(32)
app.config.update(
    OWNER_SIGNING_KEY_CONFIGURED=signing_key_configured,
    OWNER_ACCESS_CODE=os.getenv("ORDERGUARD_OWNER_ACCESS_CODE", ""),
    SESSION_COOKIE_NAME="orderguard_session",
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=os.getenv("ORDERGUARD_COOKIE_SECURE", "true").lower() != "false",
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_REFRESH_EACH_REQUEST=False,
    PERMANENT_SESSION_LIFETIME=timedelta(seconds=OWNER_SESSION_SECONDS),
    MAX_CONTENT_LENGTH=64 * 1024,
)
app.extensions["owner_login_limiter"] = AttemptLimiter(5, 60)
app.extensions["ai_extraction_limiter"] = AttemptLimiter(10, 60)
service = OrderGuardService(DB_PATH)


@app.context_processor
def inject_demo_context():
    return {
        "demo_org": DEMO_ORG,
        "demo_user": DEMO_USER if owner_unlocked() else "Read-only visitor",
        "integration_mode": "Simulated Orbyte workspace",
        "owner_unlocked": owner_unlocked(),
        "owner_access_configured": owner_access_configured(),
        "csrf_token": csrf_token,
        "ai_enabled": bool(os.getenv("DEEPSEEK_API_KEY")),
    }


def _error_response(status: int, message: str, retry_after: int = 0):
    if request.path.startswith("/api/"):
        response = app.make_response((jsonify({"ok": False, "error": message}), status))
    else:
        response = app.make_response(
            (render_template("error.html", status=status, message=message), status)
        )
    if retry_after:
        response.headers["Retry-After"] = str(retry_after)
    return response


@app.before_request
def protect_mutating_requests():
    if request.method in {"GET", "HEAD", "OPTIONS"} or request.endpoint is None:
        return None
    if request.endpoint != "owner_logout" and not owner_access_configured():
        return _error_response(
            503, "Owner controls are not configured. This demo is read-only."
        )
    if request.endpoint not in {"owner_login", "owner_logout"} and not owner_unlocked():
        return _error_response(401, "Unlock the demo owner controls before changing data.")
    token = request.headers.get("X-CSRF-Token")
    if not token and not request.is_json:
        token = request.form.get("csrf_token")
    if not valid_csrf_token(token):
        return _error_response(400, "Security token is missing or expired. Reload the page and retry.")
    return None


@app.after_request
def response_safety_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Content-Security-Policy"] = "frame-ancestors 'none'"
    response.headers["Referrer-Policy"] = "same-origin"
    if request.endpoint != "static":
        response.headers["Cache-Control"] = "no-store"
    return response


@app.errorhandler(RequestEntityTooLarge)
def request_too_large(_error):
    return _error_response(413, "Request is too large. Use a shorter message or fewer form values.")


@app.route("/owner/login", methods=["GET", "POST"])
def owner_login():
    if owner_unlocked():
        return redirect(url_for("dashboard"))
    if request.method == "POST":
        retry_after = app.extensions["owner_login_limiter"].consume()
        if retry_after:
            return _error_response(429, "Too many owner-access attempts. Try again shortly.", retry_after)
        if not constant_time_match(
            request.form.get("access_code"), app.config["OWNER_ACCESS_CODE"]
        ):
            return render_template("owner_login.html", error="Access code not accepted."), 401
        session.clear()
        session.permanent = True
        session["owner_session"] = owner_session_marker()
        session["owner_expires_at"] = time.time() + OWNER_SESSION_SECONDS
        csrf_token()
        flash("Demo owner controls unlocked for up to 30 minutes.", "success")
        return redirect(url_for("dashboard"))
    return render_template("owner_login.html")


@app.post("/owner/logout")
def owner_logout():
    session.clear()
    flash("Owner controls locked. Public viewing remains available.", "info")
    return redirect(url_for("dashboard"))


def _required_text(name: str, label: str) -> str:
    value = request.form.get(name, "").strip()
    if not value:
        raise ValueError(f"{label} is required.")
    return value


def _number(name: str, label: str) -> float:
    raw = request.form.get(name, "").strip()
    try:
        value = float(raw)
    except (TypeError, ValueError):
        raise ValueError(f"{label} must be a number.") from None
    if not math.isfinite(value):
        raise ValueError(f"{label} must be a finite number.")
    if value < 0:
        raise ValueError(f"{label} cannot be negative.")
    return value


@app.get("/")
def dashboard():
    cases = service.list_cases()
    return render_template(
        "dashboard.html",
        cases=cases,
        outbox=service.get_outbox(),
        summary=service.get_dashboard_summary(),
        pending_actions=build_pending_action_summary(cases),
        supplier_radar=build_supplier_radar(cases, service.get_supplier_insight),
        ai_enabled=bool(os.getenv("DEEPSEEK_API_KEY")),
    )


@app.get("/checks")
def checks():
    query = request.args.get("q", "")
    status = request.args.get("status", "ALL")
    cases = service.list_cases()
    return render_template(
        "checks.html",
        cases=filter_cases(cases, query=query, status=status),
        query=query,
        selected_status=status.upper(),
        pending_actions=build_pending_action_summary(cases),
    )


@app.get("/reports")
def reports():
    cases = service.list_cases()
    return render_template(
        "reports.html",
        summary=service.get_dashboard_summary(),
        supplier_radar=build_supplier_radar(cases, service.get_supplier_insight),
    )


@app.post("/api/extract")
def extract_message():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict) or not isinstance(payload.get("message"), str):
        return _error_response(400, "Send a JSON object with a text message.")
    message = payload["message"].strip()
    if not message:
        return jsonify({"ok": False, "error": "Supplier message is required."}), 400
    if len(message) > MAX_MESSAGE_CHARS:
        return _error_response(413, f"Supplier message must be at most {MAX_MESSAGE_CHARS} characters.")
    retry_after = app.extensions["ai_extraction_limiter"].consume()
    if retry_after:
        return _error_response(429, "AI extraction limit reached. Use the manual fields or retry shortly.", retry_after)
    try:
        data = extract_supplier_message(message)
    except AIExtractionUnavailable as exc:
        return jsonify({"ok": False, "error": str(exc), "fallback": "manual"}), 503
    except Exception:
        return jsonify(
            {
                "ok": False,
                "error": "AI extraction failed. Please confirm the structured fields manually.",
                "fallback": "manual",
            }
        ), 502
    return jsonify({"ok": True, "data": data, "requires_human_confirmation": True})


@app.route("/cases/new", methods=["GET", "POST"])
def new_case():
    if request.method == "GET" and not owner_unlocked():
        return redirect(url_for("owner_login"))
    if request.method == "POST":
        try:
            supplier_name = _required_text("supplier_name", "Supplier name")
            item = _required_text("item", "Item")
            supplier_message = _required_text("supplier_message", "Supplier message")
            po_unit = _required_text("po_unit", "Purchase order unit")
            received_unit = _required_text("received_unit", "Receiving unit")
            invoice_unit = _required_text("invoice_unit", "Invoice unit")

            purchase_order = {
                "item": item,
                "quantity": _number("po_quantity", "Purchase order quantity"),
                "unit": po_unit,
                "unit_price": _number("po_price", "Agreed unit price"),
            }
            received = {
                "item": item,
                "quantity": _number("received_quantity", "Received quantity"),
                "unit": received_unit,
            }
            invoice = {
                "item": item,
                "quantity": _number("invoice_quantity", "Invoice quantity"),
                "unit": invoice_unit,
                "unit_price": _number("invoice_price", "Invoice unit price"),
            }
        except ValueError as exc:
            flash(str(exc), "danger")
            return redirect(url_for("new_case"))

        case_id = service.create_case(
            supplier_message=supplier_message,
            purchase_order=purchase_order,
            received=received,
            invoice=invoice,
            submitted_by="owner-demo",
            supplier_name=supplier_name,
        )
        return redirect(url_for("case_detail", case_id=case_id))
    return render_template("new_case.html")


@app.post("/demo/scenario/<scenario>")
def demo_scenario(scenario: str):
    scenarios = {
        "discrepancy": {
            "supplier": "FreshFarm Foods",
            "message": "Delivered 8 kg chicken. Invoice 10 kg at RM13/kg.",
            "po": {"item": "Chicken", "quantity": 10, "unit": "kg", "unit_price": 12},
            "received": {"item": "Chicken", "quantity": 8, "unit": "kg"},
            "invoice": {"item": "Chicken", "quantity": 10, "unit": "kg", "unit_price": 13},
        },
        "repeat": {
            "supplier": "FreshFarm Foods",
            "message": "Second delivery: 8 kg chicken received. Invoice still 10 kg at RM13/kg.",
            "po": {"item": "Chicken", "quantity": 10, "unit": "kg", "unit_price": 12},
            "received": {"item": "Chicken", "quantity": 8, "unit": "kg"},
            "invoice": {"item": "Chicken", "quantity": 10, "unit": "kg", "unit_price": 13},
        },
        "match": {
            "supplier": "Golden Egg Trading",
            "message": "Delivered 30 trays eggs as ordered at RM8 per tray.",
            "po": {"item": "Eggs", "quantity": 30, "unit": "tray", "unit_price": 8},
            "received": {"item": "Eggs", "quantity": 30, "unit": "tray"},
            "invoice": {"item": "Eggs", "quantity": 30, "unit": "tray", "unit_price": 8},
        },
        "ambiguous": {
            "supplier": "RiceHub Supply",
            "message": "Delivered two bags rice. Invoice remains 10 kg at RM4/kg.",
            "po": {"item": "Rice", "quantity": 10, "unit": "kg", "unit_price": 4},
            "received": {"item": "Rice", "quantity": 2, "unit": "bags"},
            "invoice": {"item": "Rice", "quantity": 10, "unit": "kg", "unit_price": 4},
        },
    }
    data = scenarios.get(scenario)
    if data is None:
        flash("Unknown demo scenario.", "danger")
        return redirect(url_for("dashboard"))
    case_id = service.create_case(
        data["message"],
        data["po"],
        data["received"],
        data["invoice"],
        "owner-demo",
        supplier_name=data["supplier"],
    )
    return redirect(url_for("case_detail", case_id=case_id))


@app.get("/cases/<int:case_id>")
def case_detail(case_id: int):
    try:
        case = service.get_case(case_id)
    except KeyError:
        return _error_response(404, "This case does not exist or was cleared by a demo reset.")
    return render_template(
        "case_detail.html",
        case=case,
        activity=service.get_activity(case_id),
        supplier_insight=service.get_supplier_insight(case_id),
    )


@app.post("/cases/<int:case_id>/clarify")
def clarify_case(case_id: int):
    try:
        service.clarify_case(
            case_id,
            actor="owner-demo",
            received_quantity=_number("received_quantity", "Confirmed received quantity"),
            received_unit=_required_text("received_unit", "Confirmed unit"),
        )
        flash("Human clarification recorded. The case was recalculated.", "success")
    except (ValueError, KeyError) as exc:
        flash(str(exc), "danger")
    return redirect(url_for("case_detail", case_id=case_id))


@app.post("/cases/<int:case_id>/approve")
def approve_case(case_id: int):
    try:
        service.approve_case(case_id, actor="owner-demo", role="owner")
        flash("Approved. The clarification was added to the simulated outbox.", "success")
    except (PermissionError, ValueError, KeyError) as exc:
        flash(str(exc), "danger")
    return redirect(url_for("case_detail", case_id=case_id))


@app.post("/cases/<int:case_id>/reject")
def reject_case(case_id: int):
    try:
        service.reject_case(
            case_id,
            actor="owner-demo",
            role="owner",
            reason=request.form.get("reason", "Owner rejected the proposed action"),
        )
        flash("Rejected. No supplier action was created.", "warning")
    except (PermissionError, ValueError, KeyError) as exc:
        flash(str(exc), "danger")
    return redirect(url_for("case_detail", case_id=case_id))


@app.post("/demo/reset")
def reset_demo():
    if request.form.get("confirmation") != "reset-synthetic-data":
        return _error_response(400, "Confirm that all synthetic cases, outbox entries and case audit history may be cleared.")
    service.reset_demo(role="owner")
    flash("Demo data reset.", "info")
    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=False)
