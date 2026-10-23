# Vortex OrderGuard

**Check deliveries. Explain discrepancies. Remember patterns. Keep owners in control.**

Vortex OrderGuard is a functional MVP for the SDC Hackathon 2026 Domain 2 — **Orbyte Smart SME Challenge: Less Busywork, Better Business**. It helps micro and small businesses compare purchase orders, receiving records and supplier invoices, surface explainable exceptions, remember repeated supplier-item issues and keep consequential actions behind human approval.

> **Current MVP status:** The latest competition version is on the `vortex-orderguard-submission` branch. Core comparison, Trust Gate, human clarification, owner approval/rejection, simulated outbox, audit log, Supplier Pattern Memory, Money at Risk, Supplier Exception Radar, judge demo scenarios, optional DeepSeek extraction and automated tests are implemented. Replit deployment and final submission evidence still need to be completed by the team.

## Why OrderGuard

Small businesses often reconcile supplier messages, purchase orders, deliveries and invoices manually. A shortage, wrong unit or price change can be missed when records live in different places. OrderGuard turns that recurring checking into one reviewable workflow without allowing AI to make the final business decision.

## Core Journey

1. **Trigger** — staff submits supplier evidence and connected purchasing records.
2. **Connected data** — purchase order, receiving record and invoice are compared together.
3. **Decision logic** — deterministic rules identify quantity, invoice-quantity, price and unit exceptions.
4. **Supplier intelligence** — repeated issue patterns and open Money at Risk are surfaced for review.
5. **Trust Gate** — a transparent rules-based score shows whether the case is clear, reviewable or blocked.
6. **Human control** — ambiguous units must be clarified by a person; consequential supplier clarification requires owner approval.
7. **Visible outcome** — approved clarification enters a simulated outbox and every step is recorded in the audit trail.

## Innovation

### 1. OrderGuard Trust Gate

The Trust Gate is a reusable safety layer between automation and action.

- `CLEAR` — records match; no supplier action is needed.
- `REVIEW` — records are comparable but discrepancies require owner review.
- `BLOCKED` — data is ambiguous or incompatible, so approval is disabled until a person clarifies it.

The Trust Gate score is a deterministic heuristic, **not an AI confidence probability**.

### 2. Supplier Pattern Memory

For the same supplier + item combination, OrderGuard can surface repeated discrepancy types across prior synthetic cases. This helps the owner notice recurring operational issues without automatically scoring, blacklisting or penalising the supplier.

### 3. Money at Risk

Open discrepancies are translated into a visible RM comparison signal so the owner can prioritize review. This is **not** a payment instruction and is not presented as the final amount owed.

### 4. Supplier Exception Radar

The dashboard aggregates supplier exception activity, repeat patterns and open risk so the owner can see where attention is needed without turning the prototype into an autonomous supplier-rating system.

## Judge Demo Scenarios

The dashboard includes four one-click synthetic scenarios:

| Scenario | What it demonstrates |
| --- | --- |
| `1 · Discrepancy` | 10 kg chicken ordered at RM12/kg, 8 kg received, invoice at RM13/kg |
| `2 · Repeat issue` | Same supplier + item repeats an exception; Pattern Memory surfaces it |
| `3 · Ambiguous unit` | PO/invoice use kg while receiving says “bags”; Trust Gate blocks approval |
| `4 · Clean match` | Connected records match and the system avoids unnecessary follow-up |

Best sequence: run **Discrepancy** first, then **Repeat issue**, then **Ambiguous unit**. For the ambiguous-unit case, confirm the receiving quantity/unit to demonstrate **blocked → human clarification → recalculation → owner review**.

See [`docs/JUDGE_DEMO.md`](docs/JUDGE_DEMO.md) for the full walkthrough.

## Implemented MVP Features

- Source-item identity validation before comparison: missing or mismatched item names block the Trust Gate; case and whitespace differences are normalized without fuzzy matching
- Evidence-linked quantity and price discrepancy detection
- Invoice quantity checks
- Human clarification for incompatible/missing units
- Explainable Trust Gate with `CLEAR`, `REVIEW` and `BLOCKED` states
- Owner-only approval/rejection for consequential actions
- Duplicate-approval protection using a unique outbox case constraint
- Simulated supplier outbox (no real messages/payments)
- Activity/audit history
- Supplier Pattern Memory for repeat supplier-item exceptions
- Money at Risk aggregation for open cases
- Supplier Exception Radar
- Four one-click judge demo scenarios
- Optional DeepSeek supplier-message extraction
- Manual fallback when AI is unavailable
- Human confirmation of AI-extracted fields before rule evaluation
- SQLite demonstration storage
- Responsive Flask/Bootstrap UI
- GitHub Actions automated test workflow on the safe submission branch

## AI Design

AI is used only where unstructured language creates friction: converting informal supplier text into structured suggestions such as item, quantity, unit and price. It does **not** calculate discrepancies, approve actions, infer unit conversions, judge suppliers or send supplier messages.

The application supports DeepSeek through `DEEPSEEK_API_KEY`. If no key is configured, users continue with manual structured fields.

## Architecture

```text
Supplier message / records
          |
          v
Flask web UI ---- optional DeepSeek extraction
          |
          v
Human-confirmed structured fields
          |
          v
PO + Receiving + Invoice
          |
          v
Deterministic discrepancy engine
       /              \
      v                v
Trust Gate      Supplier Pattern Memory
      |                |
      +-------> Money at Risk / Radar
      |
  BLOCKED or REVIEW
      |
Human clarify OR Owner approve/reject
      |
      v
Simulated outbox + audit log
      |
    SQLite
```

## Orbyte Fit — Without Depending on Live Orbyte

OrderGuard is designed as a reusable purchasing-exception module for the **Orbyte ecosystem**.

The Domain 2 guide allows teams to simulate login, profiles and RBAC and to use synthetic data and team-created interface/API assumptions. The organizer announcement also states that participant registration on the Orbyte sandbox is **not compulsory** and is provided for understanding/familiarization.

Organizer-provided participant sandbox:

`https://orbyte-xyz.alphareds.com/`

For this MVP:

- Orbyte roles and business data are simulated.
- No live Orbyte API integration is claimed.
- The core demo works without an approved Orbyte account.
- Potential future inputs include purchase orders, supplier records, receiving records, invoices and user/role information.
- Potential outputs include exception cases, approval decisions, clarification requests and audit events.

The organizer also supplied temporary sandbox credentials to participants. Those credentials are intentionally **not committed to this public repository**.

See [`docs/ORBYTE_PLATFORM_NOTE.md`](docs/ORBYTE_PLATFORM_NOTE.md) for the exact project interpretation and credential-handling note.

## Run Locally / Replit

Install dependencies:

```bash
pip install -r requirements.txt
```

Run:

```bash
python src/main.py
```

Then open the URL provided by Replit, or locally open `http://127.0.0.1:5000`.

### Replit Secrets

Do not commit real keys. Configure these through Replit Secrets when used:

```text
DEEPSEEK_API_KEY=...
FLASK_SECRET_KEY=...
```

Optional:

```text
DEEPSEEK_MODEL=deepseek-chat
DEEPSEEK_API_URL=https://api.deepseek.com/chat/completions
```

## Tests

Run:

```bash
python -m unittest discover -s tests -v
```

Automated coverage includes matching records, quantity/price discrepancies, ambiguous units, Trust Gate blocking, human clarification, owner-only approval, rejection without action, duplicate-action protection, repeat supplier-item issue detection and supplier-risk aggregation.

Item-identity regression tests also cover missing, blank or non-text item names, mismatches in any source record, harmless case/spacing differences, combined item/unit ambiguity and blocked approval through both the service and web routes. Item-blocked cases require corrected source records to be submitted as a new check; quantity/unit clarification cannot bypass the item check.

The repository also contains a GitHub Actions workflow for automated regression checks on `vortex-orderguard-submission`.

## Safety and Competition Boundaries

- Synthetic demo business data only
- No real payment processing
- No statutory filing
- No legal, tax or financial advice
- No live WhatsApp or live Orbyte integration claimed
- Roles and Orbyte interfaces are simulated for the MVP
- No automatic supplier blacklist or supplier quality score
- No organizer temporary-account credentials committed
- No API keys or personal IC details should be committed
- RunPod is only relevant if the team actually uses GPU training, fine-tuning or GPU inference

## Validation Still Required

The team still needs to complete real SME problem validation and measure a defensible baseline/KPI for the official preliminary proposal. Do not present estimated time savings as measured results.

Suggested measurements:

- Manual check time vs prototype check time
- Known discrepancy detection rate
- False-alert count on matching records
- First-time-user task completion
- Approval-control and duplicate-action tests

## Submission Status

Still required before the preliminary deadline:

- Complete official `SDC2026_Vortex_Preliminary.pdf`
- Complete `SDC2026_Vortex_TechDeclaration.pdf`
- Deploy through the team's Replit account and retain proof of use
- Add the official Replit/live prototype link
- Prepare pitch deck
- Record 5–7 minute YouTube pitch with prototype demo
- Verify team details, workshop completion, eligibility and declarations
- Verify all public links in an incognito window

See [`docs/VORTEX_SUBMISSION_GUIDE.md`](docs/VORTEX_SUBMISSION_GUIDE.md) for the detailed requirement mapping and [`docs/PITCH_DECK_CONTENT.md`](docs/PITCH_DECK_CONTENT.md) for the pitch structure.

## Technical & AI Disclosure

The project has used ChatGPT for substantial ideation, documentation and development assistance and this must be disclosed accurately in the Technical & Tools Declaration. The team remains responsible for reviewing, understanding, testing and adapting all generated material. The competition requires the team's own problem framing, solution decisions and explainability; the team should validate the SME problem and document its own decisions before submission.

This repository is based on the official SDC Hackathon Submission Template and retains its Apache License 2.0.

## License

Apache License 2.0 — see [LICENSE](LICENSE).
