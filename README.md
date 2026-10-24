# Vortex OrderGuard

> **AI-assisted supplier discrepancy control for smarter SME purchasing**

**Team:** Vortex  
**Challenge:** SDC Hackathon 2026 — Domain 2: Orbyte Smart SME Challenge  
**Theme:** Less Busywork, Better Business

## Project Links

- **Live demo:** [Open Vortex OrderGuard](https://sdc-hackathon-submission-template.replit.app)
- **Video presentation:** [Watch on YouTube](https://www.youtube.com/watch?v=Mn3d2Ra77_Q)
- **GitHub repository:** [View source code](https://github.com/Aunyiqi/SDC_Hackathon_Submission_Template)
- **RunPod proof:** [View RunPod proof of use](docs/RUNPOD_PROOF_OF_USE.md)

## 1. Project Overview

### The problem

Small and micro businesses often receive purchasing information across supplier messages, purchase orders, receiving records and invoices. When quantities, units or prices do not match, staff must manually compare multiple records before deciding what needs attention.

The challenge is not only detecting a mismatch. Owners also need to understand **why** a case is risky, which cases should be reviewed first, whether the same supplier-item problem has happened before, and when human clarification is required before any action is taken.

OrderGuard focuses on this exception-review gap by turning disconnected purchasing evidence into one explainable workflow.

### Target users

- **Primary users:** SME owners and staff who review supplier deliveries, purchase orders and invoices.
- **Operational users:** Staff responsible for receiving goods, checking invoices or preparing supplier follow-up.
- **Decision maker:** The owner remains responsible for consequential approval or rejection.

### Our solution

Vortex OrderGuard is a functional purchasing-exception MVP that compares purchase orders, receiving records and supplier invoices using deterministic rules.

It highlights quantity, price, item and unit discrepancies, calculates a visible **Money at Risk** signal, remembers repeated supplier-item issues through **Supplier Pattern Memory**, and uses an explainable **Trust Gate** to decide whether a case is clear, reviewable or blocked pending human clarification.

AI and OCR reduce data-entry friction, but they do not make the final business decision.

### Core feature set

| Feature | What OrderGuard does |
| --- | --- |
| **Dashboard & Priority Queue** | Shows cases that need attention, open money at risk and review priority. |
| **Supplier Checks** | Compares purchase-order, receiving and invoice evidence in one place. |
| **Trust Gate** | Classifies cases as `CLEAR`, `REVIEW` or `BLOCKED` using explainable deterministic rules. |
| **Human Clarification** | Stops approval when units or evidence are ambiguous until a person confirms the information. |
| **Money at Risk** | Converts open discrepancies into an RM comparison signal for prioritisation. |
| **Supplier Pattern Memory** | Surfaces repeated issue patterns for the same supplier and item. |
| **Supplier Exception Radar** | Aggregates recurring exceptions and open risk across suppliers. |
| **Owner Approval** | Keeps consequential actions behind explicit human approval or rejection. |
| **Audit History** | Records case activity and simulated outcomes for traceability. |
| **Optional AI / OCR** | Uses DeepSeek and RunPod OCR only as extraction assistance with manual fallback. |

## 2. User Flow and Demo

### Core workflow

`Capture Evidence -> Compare Records -> Explain Exceptions -> Trust Gate -> Human Clarification -> Owner Decision -> Audit`

The end-to-end flow is:

1. A user enters a supplier message and structured purchasing evidence.
2. OrderGuard connects the purchase order, receiving record and invoice.
3. Deterministic rules compare quantity, price, item identity and unit consistency.
4. The system explains every detected exception.
5. Money at Risk and supplier history help prioritise the case.
6. The Trust Gate classifies the case as `CLEAR`, `REVIEW` or `BLOCKED`.
7. Ambiguous information must be clarified by a person.
8. The owner approves or rejects the consequential action.
9. Approved demo actions enter a simulated outbox and every step remains visible in the audit trail.

### Judge demo scenarios

| Scenario | What it demonstrates |
| --- | --- |
| **Discrepancy** | 10 kg chicken ordered at RM12/kg, 8 kg received, invoice at RM13/kg. |
| **Repeat issue** | The same supplier and item repeat an exception, triggering Pattern Memory. |
| **Ambiguous unit** | PO and invoice use kg while receiving says `bags`; Trust Gate blocks approval. |
| **Clean match** | Connected records match and no unnecessary follow-up is created. |

Recommended demo sequence:

`Discrepancy -> Repeat Issue -> Ambiguous Unit -> Clean Match`

Full walkthrough: [`docs/JUDGE_DEMO.md`](docs/JUDGE_DEMO.md)

## 3. What Makes OrderGuard Different

### Explainable Trust Gate

The Trust Gate separates automation from business action.

- **CLEAR** — connected records match and no supplier action is needed.
- **REVIEW** — records are comparable but a discrepancy requires owner review.
- **BLOCKED** — information is ambiguous or incompatible, so approval is disabled until a person clarifies it.

The Trust Gate is a deterministic rules-based heuristic, not an AI confidence score.

### Supplier Pattern Memory

OrderGuard remembers repeated discrepancy types for the same supplier-item combination. This helps owners notice recurring operational problems without automatically blacklisting or penalising suppliers.

### Money at Risk

Open discrepancies are translated into a visible RM comparison signal so owners can prioritise which cases deserve attention first. It is not a payment instruction or final amount owed.

### Supplier Exception Radar

Reports combine supplier exception activity, repeated patterns and open risk so the owner can see where attention is concentrated.

### AI assists, humans decide

AI and OCR are used only to reduce data-entry friction. They do **not** approve cases, calculate final business decisions, infer unsafe unit conversions, blacklist suppliers or send real supplier messages.

`Extract -> Validate -> Compare -> Explain -> Human Decides`

## 4. Prototype and Deployment

### Live prototype

The functional prototype is publicly deployed on Replit:

**https://sdc-hackathon-submission-template.replit.app**

Public visitors can inspect the synthetic demo in read-only mode. Data-changing actions require a private, expiring owner-control session.

### Replit deployment

Replit is used to host and publish the competition prototype. The deployed application runs the Flask web application and exposes the live judge demo.

Proof of use: [`docs/REPLIT_PROOF_OF_USE.md`](docs/REPLIT_PROOF_OF_USE.md)

### RunPod GPU OCR

RunPod Serverless provides the optional GPU-assisted OCR path used for document extraction.

| Item | Implementation |
| --- | --- |
| Provider | RunPod Serverless |
| OCR library | EasyOCR |
| Verified GPU test | NVIDIA GeForce RTX 5090 |
| Endpoint role | Extraction only |
| Decision authority | OrderGuard deterministic rules + human approval |

Authenticated invocation format:

```text
POST https://api.runpod.ai/v2/ojf4e2o9yj00cy/runsync
Authorization: Bearer <RUNPOD_API_KEY>
Content-Type: application/json
```

The API key is stored only as a server-side secret and is not committed to the repository.

Proof of use: [`docs/RUNPOD_PROOF_OF_USE.md`](docs/RUNPOD_PROOF_OF_USE.md)

## 5. Technical Architecture and Feasibility

OrderGuard uses a lightweight web architecture that deliberately separates extraction, deterministic comparison and human approval.

### Tech stack

| Layer | Technology | Purpose |
| --- | --- | --- |
| Frontend | HTML, CSS, JavaScript | Web interface and interaction. |
| Backend | Python 3 + Flask | Routes, validation, workflow and business logic. |
| Database | SQLite | Stores synthetic cases, findings, audit history and supplier patterns. |
| AI extraction | DeepSeek API | Optional supplier-message extraction into structured suggestions. |
| GPU OCR | RunPod Serverless + EasyOCR | Optional document text extraction. |
| Hosting | Replit | Public live prototype deployment. |
| Version control | GitHub | Source control and submission repository. |
| CI / testing | GitHub Actions + Python `unittest` | Automated regression and security checks. |

### System architecture

```text
Supplier message / documents
          |
          v
     Flask Web UI
      /        \
     v          v
DeepSeek     RunPod OCR
(optional)   (optional)
      \        /
       v      v
Human-confirmed structured fields
          |
          v
PO + Receiving + Invoice
          |
          v
Deterministic Comparison Engine
       /                   \
      v                     v
 Trust Gate          Pattern Memory
      |                     |
      +------> Money at Risk / Radar
      |
CLEAR / REVIEW / BLOCKED
      |
Human clarify or owner approve / reject
      |
      v
Simulated Outbox + Audit Log
      |
    SQLite
```

The architecture ensures AI output remains input to the workflow rather than the authority that decides what happens next.

## 6. Safety and Human Control

OrderGuard is intentionally conservative around consequential actions.

- Synthetic business data is used for the public demo.
- Public visitors are read-only by default.
- Owner controls use a private, expiring session.
- Data-changing routes use CSRF protection.
- Ambiguous units block approval until human clarification.
- Duplicate approval is prevented by workflow constraints.
- AI output is validated and can be replaced with manual input.
- No real payments are processed.
- No real supplier messages are sent.
- No supplier is automatically blacklisted or penalised.
- No API keys or organiser credentials are committed.

## 7. Orbyte Alignment

OrderGuard is designed as a reusable purchasing-exception module for the **Orbyte ecosystem**.

For this hackathon MVP:

- Orbyte organisation context and roles are simulated.
- No live Orbyte API integration is claimed.
- The prototype operates independently with synthetic data.
- Potential future inputs include suppliers, purchase orders, receiving records, invoices and role information.
- Potential outputs include exception cases, clarification requests, approval decisions and audit events.

See [`docs/ORBYTE_PLATFORM_NOTE.md`](docs/ORBYTE_PLATFORM_NOTE.md).

## 8. Repository and Testing

### Run locally

```bash
python -m venv .venv
.venv/bin/python -m pip install -r requirements.web.txt
.venv/bin/python src/main.py
```

Then open:

```text
http://127.0.0.1:5000
```

Required server-side environment variables:

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

### Tests

```bash
python -m unittest discover -s tests -v
```

Regression coverage includes clean matches, quantity and price discrepancies, item-identity checks, ambiguous units, Trust Gate blocking, human clarification, owner-only actions, duplicate-action protection, supplier-pattern detection and security controls.

## 9. Submission Materials

The official competition files are stored in [`submission/`](submission/):

- [`SDC2026_Vortex_Preliminary.pdf`](submission/SDC2026_Vortex_Preliminary.pdf)
- [`SDC2026_Vortex_Replit_POU.pdf`](submission/SDC2026_Vortex_Replit_POU.pdf)
- [`SDC2026_Vortex_Runpod_POU.pdf`](submission/SDC2026_Vortex_Runpod_POU.pdf)
- [`SDC2026_Vortex_TechDeclaration.pdf`](submission/SDC2026_Vortex_TechDeclaration.pdf)

Recorded prototype walkthrough: [YouTube Demo](https://www.youtube.com/watch?v=Mn3d2Ra77_Q)

## 10. Technical and AI Disclosure

ChatGPT and Replit Agent were used for substantial ideation, documentation and development assistance. The team remains responsible for reviewing, understanding, testing and adapting generated material.

External AI services, cloud platforms, libraries, models and development-assistance tools used by the project are declared in the official Technical Tools Declaration.

This repository is based on the official SDC Hackathon Submission Template and retains the **Apache License 2.0**.

## 11. Research References

1. Department of Statistics Malaysia — [MSMEs Performance 2025](https://www.dosm.gov.my/portal-main/release-content/micro-small--medium-enterprises-msmes-performance-2025)
2. World Bank — [Digitalizing SMEs to Boost Competitiveness](https://www.worldbank.org/en/country/malaysia/publication/digitalizing-smes-to-boost-competitiveness)
3. Microsoft Learn — [Accounts payable invoice matching overview](https://learn.microsoft.com/en-us/dynamics365/finance/accounts-payable/accounts-payable-invoice-matching)
4. East Carolina University Financial Services — [Invoice Matching Guide](https://financialservices.ecu.edu/invoice-matching-ap-team-step-by-step-guide/)
5. NIST — [AI RMF Generative AI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)
6. OWASP — [Top 10 for Large Language Model Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/assets/PDF/OWASP-Top-10-for-LLMs-v2025.pdf)

## License

Apache License 2.0 — see [LICENSE](LICENSE).
