from __future__ import annotations

import math
import os
from pathlib import Path

from flask import Flask, flash, jsonify, redirect, render_template, request, url_for

from ai_extractor import AIExtractionUnavailable, extract_supplier_message
from orbyte_adapter import build_pending_action_summary, filter_cases
from supplier_radar import build_supplier_radar
from workflow import OrderGuardService


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = os.getenv("ORDERGUARD_DB", str(BASE_DIR / "orderguard.db"))
DEMO_ORG = os.getenv("ORDERGUARD_ORG", "Vortex Demo SME")
DEMO_USER = os.getenv("ORDERGUARD_USER", "Owner Demo")

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = os.getenv("FLASK_SECRET_KEY", "vortex-orderguard-demo")
service = OrderGuardService(DB_PATH)


@app.context_processor
def inject_demo_context():
    return {
        "demo_org": DEMO_ORG,
        "demo_user": DEMO_USER,
        "integration_mode": "Simulated Orbyte workspace",
    }


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
    message = (request.get_json(silent=True) or {}).get("message", "").strip()
    if not message:
        return jsonify({"ok": False, "error": "Supplier message is required."}), 400
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
            submitted_by="staff-demo",
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
        "demo-staff",
        supplier_name=data["supplier"],
    )
    return redirect(url_for("case_detail", case_id=case_id))


@app.get("/cases/<int:case_id>")
def case_detail(case_id: int):
    return render_template(
        "case_detail.html",
        case=service.get_case(case_id),
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
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    global service
    service = OrderGuardService(DB_PATH)
    flash("Demo data reset.", "info")
    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=False)
