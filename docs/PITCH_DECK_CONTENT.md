# Vortex OrderGuard — Pitch Deck Content

Use this as the content source for the preliminary pitch deck. Keep any measured-impact numbers honest: replace placeholders only after the team has actually timed or tested the prototype.

Research and reference notes were updated on **24 October 2026**. Use the linked citations in slide footers or an appendix; the complete evidence and limitations are in [Research and References](RESEARCH_AND_REFERENCES.md).

## Slide 1 — Vortex OrderGuard

**Catch supplier discrepancies before they become expensive mistakes.**

Domain 2 — Orbyte Smart SME Challenge: Less Busywork, Better Business

One-line pitch:

> Vortex OrderGuard turns scattered supplier messages, purchase orders, receiving records and invoices into one explainable exception workflow, while keeping SME owners in control of every consequential action.

Suggested visual: OrderGuard dashboard with the Money at Risk and Trust Gate cards visible.

## Slide 2 — The SME Problem

**Published context:** Malaysian MSMEs contributed **39.7% of GDP and 48.7% of employment in 2025**; DOSM published these figures on 30 July 2026. These totals are not the product's addressable market. [[1]](https://www.dosm.gov.my/portal-main/release-content/micro-small--medium-enterprises-msmes-performance-2025)

The World Bank's 2022 analysis found limited use of complex productivity solutions and end-to-end digital transactions among Malaysian SMEs. This is dated structural context, not a current survey of invoice errors. [[2]](https://www.worldbank.org/en/country/malaysia/publication/digitalizing-smes-to-boost-competitiveness)

**Problem hypothesis to validate:** some micro/small food-service operators may check purchasing records manually across messages, spreadsheets, receiving notes and invoices. Do not present this as an interview finding.

A staff member may need to answer questions such as:

- Did the delivered quantity match the purchase order?
- Did the invoice use the agreed unit price?
- Are the units actually comparable?
- Has this supplier-item combination had the same issue before?
- Who is allowed to approve the follow-up?

The proposed problem is not only data entry: it is **manual cross-checking, repeated follow-up and inconsistent exception handling**. The frequency and cost of that burden remain to be established.

Do not claim interview or market-validation results until the team has actually collected them.

## Slide 3 — Our Solution

OrderGuard focuses on one complete SME workflow:

**Trigger → Connected records → Decision logic → Supplier pattern memory → Trust Gate → Human approval → Logged outcome**

The prototype currently supports:

- Purchase order, receiving and invoice comparison
- Quantity and unit-price discrepancy detection
- AI-assisted extraction from informal supplier messages
- Human confirmation of AI suggestions
- Trust Gate for ambiguous or unsafe-to-act data
- Owner-only approval/rejection
- Duplicate-action protection
- Simulated supplier outbox
- Activity/audit trail
- Repeat-issue detection for the same supplier and item
- Money at Risk visibility
- Supplier Exception Radar

## Slide 4 — What Makes It Different

**Positioning boundary:** three-way matching and exception handling already exist in Microsoft Dynamics and institutional AP workflows. [[3]](https://learn.microsoft.com/en-us/dynamics365/finance/accounts-payable/accounts-payable-invoice-matching) [[4]](https://financialservices.ecu.edu/invoice-matching-ap-team-step-by-step-guide/) We are testing the usefulness of a focused review experience, not claiming a new accounting method or proven superiority.

### 1. AI where it adds value
AI helps transform informal supplier text into structured suggestions. It does not decide payments, calculate discrepancies or approve actions.

### 2. Deterministic financial checks
Quantity, unit and price comparisons use transparent program rules that can be explained from the source records.

### 3. Trust Gate
When inputs are not safely comparable, such as `2 bags` versus `10 kg`, OrderGuard blocks approval instead of guessing a conversion.

### 4. Supplier Pattern Memory
OrderGuard remembers recurring exception types for the same supplier and item, helping the owner notice repeated operational issues without automatically blacklisting the supplier.

### 5. Money at Risk
Open discrepancies are translated into a visible RM comparison amount so the owner can prioritize review. This is a review indicator, not a payment instruction or final amount owed.

## Slide 5 — Live Demo Story

### Demo 1: Discrepancy
FreshFarm Foods:

- PO: Chicken, 10 kg at RM12/kg
- Received: 8 kg
- Invoice: 10 kg at RM13/kg

OrderGuard flags quantity and price discrepancies and shows a RM34 comparison difference.

### Demo 2: Repeat Issue
Run the same supplier + item pattern again.

OrderGuard shows **Repeat issue detected** and displays prior exception context in the Supplier Exception Radar.

### Demo 3: Ambiguous Unit
RiceHub Supply:

- PO: 10 kg
- Receiving record: 2 bags

Trust Gate blocks the workflow. A human confirms the receiving record before recalculation and any approval.

### Demo 4: Clean Match
Golden Egg Trading:

- 30 trays ordered
- 30 trays received
- 30 trays invoiced at the agreed price

OrderGuard takes no unnecessary consequential action.

## Slide 6 — Architecture

```text
Supplier message / staff input
            |
            v
Optional AI extraction (DeepSeek)
            |
            v
Human-confirmed structured fields
            |
            v
PO + Receiving + Invoice
            |
            v
Deterministic discrepancy engine
            |
            +--> Trust Gate
            |
            +--> Supplier Pattern Memory
            |
            +--> Money at Risk / Exception Radar
            |
            v
Owner approve / reject
            |
            v
Simulated outbox + audit log
```

Prototype stack:

- Python
- Flask
- SQLite
- Bootstrap
- DeepSeek API for optional structured extraction
- Replit target for compulsory competition development/deployment evidence
- GitHub for version history and tests

No live Orbyte API is required for the prototype; integration is represented through reusable purchasing and role interfaces.

## Slide 7 — Human Control, Safety and Reliability

OrderGuard is intentionally not a fully autonomous financial agent.

- The demo operator unlocks data-changing controls; public visitors are read-only.
- Consequential supplier clarification requires owner approval.
- Ambiguous units block approval.
- AI output must be human-confirmed.
- Repeated approval does not create duplicate outbox actions.
- Rejection creates no supplier action.
- Activity history records the workflow.
- The prototype sends no real payment and no real supplier message.
- Synthetic demo data is used.

Automated tests cover core discrepancy, Trust Gate, approval, duplicate-action and supplier-intelligence behavior.

**Research rationale:** NIST discusses confidently incorrect AI output and evaluation against ground truth. [[5]](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf) OWASP recommends output validation, limited permissions and human approval for high-impact actions. [[6]](https://owasp.org/www-project-top-10-for-large-language-model-applications/assets/PDF/OWASP-Top-10-for-LLMs-v2025.pdf) A shared demo-owner code is not production RBAC, and these sources do not certify the application.

## Slide 8 — Orbyte Fit and Reusability

OrderGuard can fit into Orbyte as a reusable purchasing-exception module.

Potential input interfaces:

- Purchase orders
- Supplier records
- Receiving records
- Invoice data
- User/role information

Potential output interfaces:

- Exception case
- Approval/rejection decision
- Clarification request
- Audit/activity event

The same core engine could be configured for restaurants, retailers, small wholesalers and other SMEs without rebuilding the entire approval workflow.

## Slide 9 — Business Impact and SDG

Primary SDG: **SDG 8 — Decent Work and Economic Growth**

Target **8.2** links productivity to technological upgrading and innovation; **8.3** includes productive activity and MSME growth. This is intended alignment, not measured SDG impact. [[7]](https://sdgs.un.org/goals/goal8)

Relevant direction:

- Improve SME operational productivity through digital workflow automation.
- Help micro and small enterprises reduce repetitive manual checking.

### KPI to measure before submission

Recommended primary KPI:

**Average time required to check one supplier order/receiving/invoice case.**

Team action:

1. Define a labeled synthetic task set and start/end rules that include human review.
2. Counterbalance manual-first/app-first order using equivalent sets; retain failed attempts.
3. Report actual baseline/app times, sample size, errors and the percentage difference.

Do not place an invented percentage on this slide. Insert the measured value only after testing.

Secondary measurements can include discrepancy-detection accuracy, unnecessary alerts, owner-control tests and time required for a new tester to learn the workflow.

The [validation protocol](RESEARCH_AND_REFERENCES.md#5-proposed-validation--not-completed-research) proposes a small pilot. It has **not** been conducted. Passing regression tests is not proof of operating-time savings or market demand.

## Slide 10 — Why Vortex OrderGuard

Closing message:

> Small businesses do not need another chatbot that tells them what might be wrong. They need a reliable workflow that connects the evidence, explains the exception, remembers repeated issues and still lets the owner make the final decision.

**Vortex OrderGuard: Check. Explain. Remember. Approve.**

End the pitch by returning to the live dashboard and showing the Supplier Exception Radar, Trust Gate and activity log together.

## Research references

All sources accessed **24 October 2026**. Dates below are the source's publication/update or edition dates, not necessarily the data year.

1. Department of Statistics Malaysia. [Micro, Small & Medium Enterprises (MSMEs) Performance 2025](https://www.dosm.gov.my/portal-main/release-content/micro-small--medium-enterprises-msmes-performance-2025) — 30 July 2026; reference year 2025. Tier 1.
2. World Bank. [Digitalizing SMEs to Boost Competitiveness](https://www.worldbank.org/en/country/malaysia/publication/digitalizing-smes-to-boost-competitiveness) — 31 October 2022. Tier 1.
3. Microsoft Learn. [Accounts payable invoice matching overview](https://learn.microsoft.com/en-us/dynamics365/finance/accounts-payable/accounts-payable-invoice-matching) — Updated 15 May 2025. Tier 3.
4. East Carolina University Financial Services. [Invoice Matching – AP Team Step-by-Step Guide](https://financialservices.ecu.edu/invoice-matching-ap-team-step-by-step-guide/) — Publication/update date not stated. Tier 1.
5. National Institute of Standards and Technology. [Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile (NIST AI 600-1)](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf) — July 2024. Tier 1.
6. OWASP. [Top 10 for Large Language Model Applications, 2025 edition](https://owasp.org/www-project-top-10-for-large-language-model-applications/assets/PDF/OWASP-Top-10-for-LLMs-v2025.pdf) — 18 November 2024; edition labelled 2025. Tier 2.
7. United Nations Department of Economic and Social Affairs. [Goal 8](https://sdgs.un.org/goals/goal8) — Target wording publication date not stated on the page. Tier 1.
