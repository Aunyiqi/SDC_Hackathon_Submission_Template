# RunPod OCR + Competition Readiness Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Integrate the existing RunPod GPU OCR worker into the OrderGuard New Check flow and strengthen judge-facing documentation without giving OCR any decision authority.

**Architecture:** Replit/Flask keeps RunPod credentials server-side and exposes one owner-only `/api/ocr-invoice` route. The browser uploads a synthetic invoice image to Flask; Flask base64-encodes it and calls RunPod Serverless `/runsync`; extracted invoice fields are returned as suggestions and filled into the existing form. The current deterministic discrepancy engine, Trust Gate, human clarification and owner approval remain authoritative.

**Tech Stack:** Flask, requests, vanilla JavaScript, Jinja/Bootstrap, RunPod Serverless, EasyOCR, SQLite.

**Spec:** User-selected B+C scope in this conversation: competition-scoring README/docs enhancement plus real RunPod OCR integration in the product UI.

## Global Constraints

- Never expose `RUNPOD_API_KEY` in HTML or JavaScript.
- Require owner session and CSRF for OCR requests, matching the existing mutation/AI protection model.
- OCR may suggest supplier, item, invoice quantity, unit and unit price only; it must not change PO/receiving values or approve/reject a case.
- Human confirmation remains required before the normal New Check form is submitted.
- Accept only synthetic demo invoice images; reject unsupported types and oversized files.
- Preserve existing DeepSeek/manual fallback, Trust Gate, audit log, Pattern Memory and owner approval behavior.
- RunPod outage or missing configuration must fail safely back to manual entry.

## Review Focus

- Missing RunPod secrets must return a safe manual-fallback response without leaking configuration.
- Empty, non-image or oversized uploads must be rejected before any provider call.
- RunPod HTTP/provider failures must not crash the Flask app or create cases.
- OCR response fields must be validated and bounded before returning to the browser.
- Existing anonymous/CSRF protections must cover the OCR endpoint.

---

### Task 1: RunPod OCR client

**Files:**
- Create: `src/runpod_ocr.py`
- Create: `tests/test_runpod_ocr.py`

**Interfaces:**
- Produces: `RunPodOCRUnavailable`, `MAX_OCR_IMAGE_BYTES`, `ALLOWED_IMAGE_MIME_TYPES`, `ocr_invoice(image_bytes: bytes, mime_type: str) -> dict`.

- [ ] Write tests for missing credentials, unsupported MIME type, oversized image, successful `/runsync` response normalization and provider failure.
- [ ] Verify tests fail before `src/runpod_ocr.py` exists.
- [ ] Implement the minimal client using `https://api.runpod.ai/v2/{RUNPOD_ENDPOINT_ID}/runsync` and `Authorization: Bearer ...`.
- [ ] Verify client tests pass.

### Task 2: Owner-only OCR API route

**Files:**
- Modify: `src/app.py`
- Create: `tests/test_runpod_ocr_route.py`

**Interfaces:**
- Consumes: `ocr_invoice(...)` from Task 1.
- Produces: `POST /api/ocr-invoice` multipart route returning `{ok, data, requires_human_confirmation}`.

- [ ] Write route tests for anonymous access, missing file, successful normalized result and safe provider failure.
- [ ] Verify route tests fail before route implementation.
- [ ] Increase Flask request limit enough for bounded invoice images while keeping existing text-length checks.
- [ ] Add an OCR request limiter and the owner/CSRF-protected route.
- [ ] Expose only a boolean `runpod_ocr_enabled` to templates; never expose credentials.
- [ ] Verify route tests pass.

### Task 3: New Check GPU OCR UX

**Files:**
- Modify: `src/templates/new_case.html`
- Modify: `src/static/orderguard.js`
- Modify: `src/static/new_check.css`
- Modify: `tests/test_orbyte_routes.py`

**Interfaces:**
- Consumes: `POST /api/ocr-invoice` from Task 2.
- Produces: invoice upload control, `Read invoice with RunPod GPU` action, OCR evidence/result panel, human-confirmed field suggestions.

- [ ] Extend the New Check route contract test to require RunPod OCR UI copy and controls.
- [ ] Add PNG/JPEG/WebP file input in the Supplier invoice card.
- [ ] Add client-side upload request with CSRF header and clear loading/error/success states.
- [ ] Populate only supplier/item/invoice quantity/unit/price suggestions; never overwrite PO or receiving data.
- [ ] Show GPU name/usage and a bounded OCR text preview as judge-visible evidence.
- [ ] Refresh the existing Live Evidence Preview after suggestions are loaded.

### Task 4: Competition-facing documentation

**Files:**
- Modify: `README.md`
- Modify: `docs/JUDGE_DEMO.md`
- Modify: `docs/PITCH_DECK_CONTENT.md`
- Modify: `.env.example`

- [ ] Document `RUNPOD_API_KEY` and `RUNPOD_ENDPOINT_ID` as server-side-only secrets.
- [ ] Add the real demo flow: invoice image → RunPod GPU OCR → human confirmation → deterministic comparison → Trust Gate → owner action → audit log.
- [ ] Add a judge quick path and explicitly state that RunPod performs OCR only, not business decisions.
- [ ] Update pitch content so GPU OCR is presented as functional utilisation, not a fabricated dependency.

### Task 5: Regression verification

**Files:**
- No production changes unless failures require a root-cause fix.

- [ ] Run the full `python -m unittest discover -s tests -v` suite in GitHub Actions.
- [ ] Confirm the branch workflow is green and no existing Trust Gate/security/supplier-intelligence test regressed.
