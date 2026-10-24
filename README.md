# Vortex OrderGuard

**Check deliveries. Explain discrepancies. Remember patterns. Keep owners in control.**

> **SDC Hackathon 2026 — Domain 2: Orbyte Smart SME Challenge · Less Busywork, Better Business**

Vortex OrderGuard is a functional SME purchasing-exception MVP that compares purchase orders, receiving records and supplier invoices, highlights explainable mismatches, remembers repeated supplier-item issues and keeps consequential actions behind human approval.

## Quick Links

| Resource | Link | Status |
| --- | --- | --- |
| **Live Demo** | https://sdc-hackathon-submission-template.replit.app | ✅ Published |
| **Demo Video** | https://www.youtube.com/watch?v=Mn3d2Ra77_Q | ✅ Available |
| **GitHub Repository** | https://github.com/Aunyiqi/SDC_Hackathon_Submission_Template | ✅ Public |
| **RunPod Serverless API** | `POST https://api.runpod.ai/v2/ojf4e2o9yj00cy/runsync` | ✅ Working authenticated API |
| **Slide Deck** | Pending final public link | ⏳ Pending |

### Submission PDFs

- [`SDC2026_Vortex_Preliminary.pdf`](submission/SDC2026_Vortex_Preliminary.pdf)
- [`SDC2026_Vortex_Replit_POU.pdf`](submission/SDC2026_Vortex_Replit_POU.pdf)
- [`SDC2026_Vortex_Runpod_POU.pdf`](submission/SDC2026_Vortex_Runpod_POU.pdf)
- [`SDC2026_Vortex_TechDeclaration.pdf`](submission/SDC2026_Vortex_TechDeclaration.pdf)

## Project Snapshot

The competition build is maintained on the **`vortex-orderguard-submission`** branch and is deployed as a public Replit demo.

**Core workflow** — OrderGuard compares purchase orders, receiving records and supplier invoices using deterministic rules, then explains quantity, price, item and unit exceptions through the Trust Gate.

**Supplier intelligence** — Money at Risk, Supplier Pattern Memory and Supplier Exception Radar help owners prioritize cases and recognize recurring supplier-item issues without automatically penalising suppliers.

**Human control** — ambiguous evidence requires clarification, consequential actions require owner approval or rejection, and every simulated action is recorded in the audit history and outbox.

**Prototype & evidence** — the project includes a published Replit demo, optional DeepSeek-assisted extraction, RunPod GPU OCR proof of use, GitHub Actions regression tests, the required submission PDFs and a YouTube demo video.

## The Problem

Small businesses often receive purchasing information across messages, purchase orders, delivery / receiving records and supplier invoices. When quantities, units or prices do not match, staff must manually compare multiple records before deciding what to do.

OrderGuard focuses on the **exception-review step**: make mismatches visible, explain why they matter, surface recurring supplier-item issues and ensure a person remains responsible for the final action.

## The Solution

```text
Supplier message / documents
          |
          v
Optional AI / OCR extraction
          |
          v
Human-confirmed structured fields
          |
          v
PO + Receiving + Invoice
          |
          v
Deterministic comparison engine
       /                 \
      v                   v
 Trust Gate        Pattern Memory
      |                   |
      +------> Money at Risk / Radar
      |
BLOCKED / REVIEW / CLEAR
      |
Human clarify OR owner approve / reject
      |
      v
Simulated outbox + audit log
```

## What Makes OrderGuard Different

### 1. Explainable Trust Gate

The Trust Gate separates automation from business action.

- **CLEAR** — connected records match; no supplier action is needed.
- **REVIEW** — records are comparable but a discrepancy requires owner review.
- **BLOCKED** — information is ambiguous or incompatible, so approval is disabled until a person clarifies it.

The Trust Gate is a deterministic rules-based heuristic, **not an AI confidence score**.

### 2. Supplier Pattern Memory

OrderGuard remembers repeated discrepancy types for the same supplier + item combination. It helps the owner notice recurring operational issues without automatically blacklisting or penalising suppliers.

### 3. Money at Risk

Open discrepancies are translated into a visible RM comparison signal so the owner can prioritize which cases deserve attention first. It is not a payment instruction or final amount owed.

### 4. Supplier Exception Radar

Reports aggregate supplier exception activity, open risk and repeated patterns so owners can see where attention is needed.

### 5. AI Assists — Humans Decide

AI and OCR are used only to reduce data-entry friction. They do **not** approve cases, calculate final business decisions, infer unsafe unit conversions, blacklist suppliers or send live supplier messages.

## Main Demo Flow

1. Open the published Replit demo.
2. Unlock the synthetic demo controls using the private owner code.
3. Show the **Dashboard** and priority queue.
4. Open **Supplier Checks** or create a **New Check**.
5. Compare PO, receiving and invoice evidence.
6. Explain quantity / price / unit discrepancies.
7. Show **Trust Gate** result.
8. If blocked, perform human clarification and recalculate.
9. Approve or reject as the owner.
10. Show the simulated outbox and audit history.
11. Open **Reports** to show supplier patterns and Money at Risk.

Full walkthrough: [`docs/JUDGE_DEMO.md`](docs/JUDGE_DEMO.md)

## Judge Demo Scenarios

| Scenario | What it demonstrates |
| --- | --- |
| **1 · Discrepancy** | 10 kg chicken ordered at RM12/kg, 8 kg received, invoice at RM13/kg |
| **2 · Repeat issue** | Same supplier + item repeats an exception; Pattern Memory surfaces it |
| **3 · Ambiguous unit** | PO / invoice use kg while receiving says `bags`; Trust Gate blocks approval |
| **4 · Clean match** | Records match and the system avoids unnecessary follow-up |

Recommended presentation sequence: **Discrepancy → Repeat issue → Ambiguous unit → Clean match**.

## Implemented Features

- Evidence-linked quantity and price discrepancy detection
- Invoice quantity checks
- Source-item identity validation
- Human clarification for incompatible or missing units
- Trust Gate with `CLEAR`, `REVIEW` and `BLOCKED`
- Owner-only approval and rejection
- Read-only public demo with expiring owner-control sessions
- CSRF protection on mutations
- Duplicate-approval protection
- Simulated supplier outbox
- Activity / audit history
- Supplier Pattern Memory
- Money at Risk aggregation
- Supplier Exception Radar
- Four one-click synthetic demo scenarios
- Optional DeepSeek supplier-message extraction
- Manual fallback when AI is unavailable
- Human confirmation before rule evaluation
- SQLite demonstration storage
- Responsive Flask UI
- GitHub Actions automated regression tests

## RunPod GPU OCR

OrderGuard includes a server-side RunPod OCR integration path for document extraction.

- **Provider:** RunPod Serverless
- **OCR:** EasyOCR
- **Verified GPU test:** NVIDIA GeForce RTX 5090
- **Role:** extraction only
- **Final decision authority:** deterministic OrderGuard rules + human approval

Authenticated invocation format:

```text
POST https://api.runpod.ai/v2/ojf4e2o9yj00cy/runsync
Authorization: Bearer <RUNPOD_API_KEY>
Content-Type: application/json
```

The API key is intentionally not committed to the repository.

Proof: [`docs/RUNPOD_PROOF_OF_USE.md`](docs/RUNPOD_PROOF_OF_USE.md)

## Replit Deployment

**Live demo:** https://sdc-hackathon-submission-template.replit.app

The application is publicly deployed on Replit. Public visitors can inspect the synthetic demo in read-only mode. Data-changing actions require the private demo-owner access code.

Proof: [`docs/REPLIT_PROOF_OF_USE.md`](docs/REPLIT_PROOF_OF_USE.md)

## Technology Stack

| Layer | Technology |
| --- | --- |
| Backend | Python 3, Flask |
| Frontend | HTML, CSS, JavaScript |
| Demo database | SQLite |
| AI extraction | DeepSeek API (optional) |
| GPU OCR | RunPod Serverless + EasyOCR |
| Hosting | Replit |
| Version control | GitHub |
| CI / tests | GitHub Actions + Python `unittest` |

## Orbyte Alignment

OrderGuard is designed as a reusable purchasing-exception module for the **Orbyte ecosystem**.

For this hackathon MVP:

- Orbyte organization context and roles are simulated.
- No live Orbyte API integration is claimed.
- The prototype works independently using synthetic data.
- Potential future inputs include suppliers, purchase orders, receiving records, invoices and role information.
- Potential outputs include exception cases, clarification requests, approval decisions and audit events.

See [`docs/ORBYTE_PLATFORM_NOTE.md`](docs/ORBYTE_PLATFORM_NOTE.md).

## Safety Boundaries

- Synthetic business data only
- No real payment processing
- No real supplier messages
- No statutory filing
- No legal, tax or financial advice
- No automatic supplier blacklist
- No live Orbyte integration claimed
- No API keys or organizer credentials committed
- Consequential actions remain human-controlled

## Run Locally

Install web dependencies:

```bash
python -m venv .venv
.venv/bin/python -m pip install -r requirements.web.txt
```

Run:

```bash
.venv/bin/python src/main.py
```

Then open `http://127.0.0.1:5000`.

Required server-side environment variables for owner controls:

```text
FLASK_SECRET_KEY
ORDERGUARD_OWNER_ACCESS_CODE
```

Optional integrations:

```text
DEEPSEEK_API_KEY
RUNPOD_API_KEY
RUNPOD_ENDPOINT_ID
```

Never commit real secret values.

## Tests

```bash
python -m unittest discover -s tests -v
```

Regression coverage includes matching records, quantity and price discrepancies, ambiguous units, Trust Gate blocking, human clarification, owner-only actions, duplicate-action protection, supplier patterns, item identity validation and security controls.

## Submission Materials

The repository contains the official project proposal, Replit proof of use, RunPod proof of use and Technical Tools Declaration in [`submission/`](submission/). The public demo is hosted on Replit, and the recorded prototype walkthrough is available on [YouTube](https://www.youtube.com/watch?v=Mn3d2Ra77_Q).

The final public Slide Deck link will be added to [`docs/SUBMISSION_LINKS.md`](docs/SUBMISSION_LINKS.md) once published.

## Technical & AI Disclosure

ChatGPT and Replit Agent were used for substantial ideation, documentation and development assistance. The team remains responsible for reviewing, understanding, testing and adapting generated material. External AI, cloud services, tools, libraries and sponsor resources must be declared accurately in the official Technical Tools Declaration.

The repository is based on the official SDC Hackathon Submission Template and retains the **Apache License 2.0**.

## Research References

1. Department of Statistics Malaysia — [MSMEs Performance 2025](https://www.dosm.gov.my/portal-main/release-content/micro-small--medium-enterprises-msmes-performance-2025)
2. World Bank — [Digitalizing SMEs to Boost Competitiveness](https://www.worldbank.org/en/country/malaysia/publication/digitalizing-smes-to-boost-competitiveness)
3. Microsoft Learn — [Accounts payable invoice matching overview](https://learn.microsoft.com/en-us/dynamics365/finance/accounts-payable/accounts-payable-invoice-matching)
4. East Carolina University Financial Services — [Invoice Matching Guide](https://financialservices.ecu.edu/invoice-matching-ap-team-step-by-step-guide/)
5. NIST — [AI RMF Generative AI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)
6. OWASP — [Top 10 for Large Language Model Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/assets/PDF/OWASP-Top-10-for-LLMs-v2025.pdf)

## License

Apache License 2.0 — see [LICENSE](LICENSE).
