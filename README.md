# Vortex OrderGuard

**Check deliveries. Explain discrepancies. Remember patterns. Keep owners in control.**

Vortex OrderGuard is a functional MVP for the SDC Hackathon 2026 Domain 2 — **Orbyte Smart SME Challenge: Less Busywork, Better Business**. It helps micro and small businesses compare purchase orders, receiving records and supplier invoices, surface explainable exceptions, remember repeated supplier-item issues and keep consequential actions behind human approval.

> **Current MVP status:** The latest competition version is on the `vortex-orderguard-submission` branch. Core comparison, Trust Gate, human clarification, owner approval/rejection, simulated outbox, audit log, Supplier Pattern Memory, Money at Risk, Supplier Exception Radar, judge demo scenarios, optional DeepSeek extraction and automated tests are implemented. Replit deployment and final submission evidence still need to be completed by the team.

## Why OrderGuard

**Problem hypothesis:** micro and small businesses handling purchasing evidence across messages, receiving notes and invoices may benefit from one reviewable exception workflow. OrderGuard is designed to make quantity, unit and price differences visible without allowing AI to make the final business decision. Customer demand and time savings still need measurement.

**Research context:** DOSM reports that MSMEs contributed **39.7% of Malaysia's GDP and 48.7% of employment in 2025**, in a release dated 30 July 2026. These are national context, not OrderGuard's addressable market. [[1]](https://www.dosm.gov.my/portal-main/release-content/micro-small--medium-enterprises-msmes-performance-2025) The World Bank's **2022** assessment found limited use of complex productivity tools and end-to-end digital transactions among Malaysian SMEs; it is historical context, not a current purchasing-error survey. [[2]](https://www.worldbank.org/en/country/malaysia/publication/digitalizing-smes-to-boost-competitiveness)

See [`docs/RESEARCH_AND_REFERENCES.md`](docs/RESEARCH_AND_REFERENCES.md) for the evidence brief, linked sources, limitations and proposed user-validation protocol. Cited proposal wording and pitch notes are included in the [submission guide](docs/VORTEX_SUBMISSION_GUIDE.md) and [pitch content](docs/PITCH_DECK_CONTENT.md).

## Core Journey

1. **Trigger** — the demo operator submits supplier evidence and structured purchasing records.
2. **Connected data** — purchase order, receiving record and invoice are compared together.
3. **Decision logic** — deterministic rules identify quantity, invoice-quantity, price and unit exceptions.
4. **Supplier intelligence** — repeated issue patterns and open Money at Risk are surfaced for review.
5. **Trust Gate** — a transparent rules-based score shows whether the case is clear, reviewable or blocked.
6. **Human control** — ambiguous units must be clarified by a person; consequential supplier clarification requires owner approval.
7. **Visible outcome** — approved clarification enters a simulated outbox and every step is recorded in the audit trail.

## Design Focus

Three-way matching is already documented in established accounting software and institutional workflows. [[3]](https://learn.microsoft.com/en-us/dynamics365/finance/accounts-payable/accounts-payable-invoice-matching) [[4]](https://financialservices.ecu.edu/invoice-matching-ap-team-step-by-step-guide/) OrderGuard's hypothesis is that a focused exception-review experience is useful for its intended users—not that it invented matching or is proven superior to existing tools.

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
- Read-only public demo with private, expiring owner-control sessions and CSRF protection on all mutations
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

The design rationale is consistent with NIST's guidance to evaluate AI output against known truth and OWASP's recommendations to validate output and restrict model authority. These references do not certify this prototype or establish its extraction accuracy. [[5]](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf) [[6]](https://owasp.org/www-project-top-10-for-large-language-model-applications/assets/PDF/OWASP-Top-10-for-LLMs-v2025.pdf)

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

Do not commit or print real keys. Configure these **names** through Replit Secrets or server-side environment variables:

- `FLASK_SECRET_KEY`: an independent, randomly generated signing secret of at least 32 characters.
- `ORDERGUARD_OWNER_ACCESS_CODE`: a private, randomly generated demo-owner code of at least 24 characters.
- `DEEPSEEK_API_KEY`: optional; leave unset to use the manual workflow without external AI calls.

If either required secret is missing or too short, the app stays **read-only**. It has no built-in owner code and no predictable signing-key fallback. The application does not automatically load `.env` files.

Open **Owner access** and enter the private owner code before creating checks, running scenarios, clarifying/approving/rejecting cases, resetting demo data or using AI extraction. Owner access lasts at most 30 minutes from login; activity does not extend that deadline. **Lock owner controls** ends access in the current browser. Rotating the owner code or signing secret invalidates existing owner sessions.

Cookies require HTTPS by default. For local HTTP development only, set `ORDERGUARD_COOKIE_SECURE=false`; do not use that override for a public HTTPS deployment.

Optional AI settings:

```text
DEEPSEEK_MODEL=deepseek-chat
DEEPSEEK_API_URL=https://api.deepseek.com/chat/completions
```

### Demo access boundaries

This is a shared **demo-owner access guard**, not individual user authentication, tenant isolation or live Orbyte RBAC. All public pages remain visible without the code, so **use synthetic records only**. Real customer data requires a proper identity/authorization system and a deployment/storage review first.

Data-changing routes and AI extraction require a signed owner session and a per-session CSRF token. Login and logout also require CSRF. Request bodies are limited to 64 KiB. AI extraction accepts at most 4,000 message characters, requests at most 256 output tokens, validates returned field types and retains a manual fallback.

Login attempts are limited to five per minute and AI extraction to ten per minute, shared across each application process. These bounded in-memory limits are **not distributed or persistent billing quotas**; they reset on process restart and multiply with multiple workers/instances.

**Demo maintenance** requires explicit confirmation before clearing cases, simulated outbox entries and case audit history. Reset runs in one database transaction, preserves the database file and does not reuse old case IDs. It cannot be undone.

## Tests

Run:

```bash
python -m unittest discover -s tests -v
```

Automated coverage includes matching records, quantity/price discrepancies, ambiguous units, Trust Gate blocking, human clarification, owner-only approval, rejection without action, duplicate-action protection, repeat supplier-item issue detection and supplier-risk aggregation.

Item-identity regression tests also cover missing, blank or non-text item names, mismatches in any source record, harmless case/spacing differences, combined item/unit ambiguity and blocked approval through both the service and web routes. Item-blocked cases require corrected source records to be submitted as a new check; quantity/unit clarification cannot bypass the item check.

The current browser form uses a single shared item name for all three records. Per-source item-name mismatch coverage is at the engine/service boundary; independent source ingestion and multi-line invoice matching are not implemented.

Security regression tests cover anonymous writes, CSRF, secret rotation, fixed session expiry, confirmed/atomic resets, concurrent workflow changes, malformed and oversized AI requests, throttling and safe AI failure responses. Tests mock the AI provider; they do not consume live API credits.

The repository also contains a GitHub Actions workflow for automated regression checks on every pull request and pushes to `vortex-orderguard-submission`.

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

Replit Agent has also assisted with code review, item-identity validation, demo-access hardening, regression tests and pull-request preparation; include this assistance in the declaration.

This repository is based on the official SDC Hackathon Submission Template and retains its Apache License 2.0.

## License

Apache License 2.0 — see [LICENSE](LICENSE).

## Research references

All sources accessed **24 October 2026**. Dates below are the source's publication/update or edition dates, not necessarily the data year.

1. Department of Statistics Malaysia. [Micro, Small & Medium Enterprises (MSMEs) Performance 2025](https://www.dosm.gov.my/portal-main/release-content/micro-small--medium-enterprises-msmes-performance-2025) — 30 July 2026; reference year 2025. Tier 1.
2. World Bank. [Digitalizing SMEs to Boost Competitiveness](https://www.worldbank.org/en/country/malaysia/publication/digitalizing-smes-to-boost-competitiveness) — 31 October 2022. Tier 1.
3. Microsoft Learn. [Accounts payable invoice matching overview](https://learn.microsoft.com/en-us/dynamics365/finance/accounts-payable/accounts-payable-invoice-matching) — Updated 15 May 2025. Tier 3.
4. East Carolina University Financial Services. [Invoice Matching – AP Team Step-by-Step Guide](https://financialservices.ecu.edu/invoice-matching-ap-team-step-by-step-guide/) — Publication/update date not stated. Tier 1.
5. National Institute of Standards and Technology. [Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile (NIST AI 600-1)](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf) — July 2024. Tier 1.
6. OWASP. [Top 10 for Large Language Model Applications, 2025 edition](https://owasp.org/www-project-top-10-for-large-language-model-applications/assets/PDF/OWASP-Top-10-for-LLMs-v2025.pdf) — 18 November 2024; edition labelled 2025. Tier 2.
