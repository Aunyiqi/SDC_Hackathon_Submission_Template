# Live Evidence Preview Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the New Supplier Check easier to learn by adding an HTML/CSS/JavaScript guided workflow and a live, non-authoritative evidence preview before submission.

**Architecture:** Keep Flask/Python as the authoritative backend for persistence, permissions and discrepancy decisions. Add a browser-only JavaScript preview that mirrors the main quantity, price and unit checks for instant user feedback. Clearly label it as a preview so no consequential action depends on client-side calculations.

**Tech Stack:** HTML/Jinja, Bootstrap, vanilla JavaScript, Flask, SQLite.

**Spec:** Existing OrderGuard competition MVP plus the Orbyte-aligned UX observed from the participant sandbox.

## Global Constraints

- Never expose API keys or credentials in browser JavaScript.
- Browser preview is informational only; backend remains authoritative.
- Ambiguous/incompatible units must be shown as requiring clarification, never guessed.
- AI extraction remains optional and human-confirmed.
- Preserve existing Trust Gate, owner approval, Pattern Memory and audit behavior.

## Review Focus

- Empty or partially typed numeric fields must not crash the preview.
- Different units must show clarification required rather than a numeric mismatch conclusion.
- Matching records must show a clean preview without an exception.
- Price and quantity changes must update the preview immediately.
- Existing server-side routes and tests must continue to pass.

---

### Task 1: Route/UI contract test

**Files:**
- Modify: `tests/test_orbyte_routes.py`

- [ ] Add a test that `/cases/new` renders `Live Evidence Preview`, `Browser preview only`, and the external `orderguard.js` script reference.
- [ ] Run the test to verify it fails before implementation.

### Task 2: Guided New Check UI

**Files:**
- Modify: `src/templates/new_case.html`
- Modify: `src/static/style.css`
- Create: `src/static/orderguard.js`

- [ ] Add a three-step visual guide and grouped evidence sections.
- [ ] Add a live preview panel with unit, quantity, price, amount-difference and readiness indicators.
- [ ] Add vanilla JS listeners that update the preview on every relevant input change.
- [ ] Keep the existing AI extraction button and ensure extracted values trigger preview refresh.
- [ ] Label all browser calculations as preview-only and state that the backend recalculates after submission.

### Task 3: Verify regression

**Files:**
- No production file changes unless failures require them.

- [ ] Run `python -m unittest discover -s tests -v` through GitHub Actions.
- [ ] Confirm all existing Trust Gate, approval, supplier-intelligence and Orbyte-aligned route tests remain green.
