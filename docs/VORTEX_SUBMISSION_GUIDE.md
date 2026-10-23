# Vortex submission preparation guide

Reviewed on 23 October 2026 against the supplied documents. This is a working checklist, not a completed official proposal, tools declaration or signed certification.

Research and implementation evidence were updated on **24 October 2026**. This update does not independently re-verify the organizer rules or complete any team declaration.

## Source documents and interpretation

- Online Orientation Slides: preliminary deliverables, deadline, AI policy, Replit/RunPod requirements, public submission and repository freeze.
- Official Participant Handbook: Sections 6.3, 9 and 10 cover deliverables, resources and submission.
- Official Terms & Conditions: Sections 5 and 6 cover development, AI assistance, declarations and freeze; these take precedence in a conflict.
- Official Handbook: eligibility, AI-use guidance and general rules.
- Domain 2 brief: six must-have features, synthetic-data-only boundary, Orbyte assumptions and preliminary marking rubric.
- Preliminary Submission Template: official proposal fields, word limits, impact baseline, readiness and declarations.
- Technical Tools Declaration Template: reviewed both PDF and DOCX; declarations must reflect actual usage.
- Online Orientation Recording: unavailable; not reviewed.

The broader orientation allows several data sources, but Domain 2 specifically requires team-created synthetic records. Follow that narrower requirement for the prototype.

## Current status

Previously recorded: team name Vortex; selected project direction OrderGuard; public template fork; English project documentation; ChatGPT-assisted ideation and writing.

Verified code evidence: [item-validation fix #1](https://github.com/Aunyiqi/SDC_Hackathon_Submission_Template/pull/1) and [demo-access hardening #2](https://github.com/Aunyiqi/SDC_Hackathon_Submission_Template/pull/2) are merged into `vortex-orderguard-submission`; the [submission-branch CI run passed](https://github.com/Aunyiqi/SDC_Hackathon_Submission_Template/actions/runs/39985643232). The 70-test suite is functional regression evidence, not measured customer impact. The prototype and its limitations are documented in README.

Not verified or completed by this update: team roster, leader, student eligibility, workshop attendance, independent customer validation, proof of use from the team's Replit project, RunPod use, live application-model configuration, deployment, measured benefits, final slides/video, signed forms or submission.

## Important originality action

ChatGPT proposed the project direction and produced substantial documentation. The orientation says the idea, solution design and technical decisions must come from the team and AI outputs must be reviewed and adapted.

Discuss the actual origin with the organizers before presenting this as an eligible original project. Independently investigate the problem, record the team's own choices and changes, and disclose the assistance honestly. Renaming the project or paraphrasing AI text does not establish independent originality. Do not check or sign an originality declaration that the team cannot substantiate.

## Six preliminary deliverables

| Deliverable | Required preparation |
| --- | --- |
| Product proposal / PRD | Complete the official template; export SDC2026_Vortex_Preliminary.pdf |
| Pitch deck | Match the problem, solution, technical approach and expected-impact story in the video |
| Functional prototype | Working deployed link or accessible build; provide safe demo access and reproducible instructions |
| Technical & tools declaration | Complete all official sections; export SDC2026_Vortex_TechDeclaration.pdf |
| GitHub | Public and accessible; genuine history, Apache 2.0 LICENSE, designated committee collaborators |
| Pitching video | 5–7 minutes on YouTube, with actual prototype demonstration |

Submit at https://sdchack.my before **25 October 2026, 07:59:59 MYT**. Aim to finish on 24 October evening. Verify links in an incognito window. After the deadline, no commits, fixes or repository edits unless explicitly authorized by the organizers.

## Official proposal field mapping

| Section | What Vortex needs to supply | Limit |
| --- | --- | --- |
| 1. Team/project | Vortex, Domain 2, SDG 8, OrderGuard; confirm leader, contacts, institutions and member count | No word cap stated |
| 2.1 Problem context | Specific purchasing task, affected SME users and why the burden matters; distinguish hypothesis from findings | 250 words |
| 2.2 Proposed AI solution | Explain extraction, deterministic checking, approval and logged outcome; mention workshop skills only if actually gained | 300 words |
| 3.1 Conceptual stack | Chosen technologies, architecture and actual/planned sponsor use clearly distinguished | No word cap stated |
| 3.2 Design thinking/deployment | Actual discovery and design work, testing plan and deployment strategy; do not invent interviews | 200 words |
| 4. Impact framework | Exact SDG sub-targets, numeric baseline, core KPI and percentage-based Phase 2 target | Table fields |
| 5. Readiness | Verify mandatory GenAI, Database and Cloud Deployment workshops, problem verification, deployable scope and word limits | Check only true statements |
| 6.1 Prior-owned work | Each member confirms any relevant pre-hackathon work and its ownership | Declaration |
| 6.2 Third-party materials | List template, frameworks, libraries, datasets and models with applicable licenses | Table |
| 6.3 Employment-related IP | Each member confirms any relevant employment/internship/consulting agreement | Declaration |
| 7. Signature/date | Team leader verifies and signs the accurate final document | Human completion |

Do not publish leader phone numbers, signatures or employment details in the public repository by default. Complete required personal fields in the official submission copy for the intended organizers.

## Research-backed wording for team review

These are draft passages, not a completed official form. Check the final template's word counter, retain the citations and distinguish proposals from completed activities. The [full evidence brief](RESEARCH_AND_REFERENCES.md) contains ten checked references and their limits.

The external sources support desk research only. They are not application business records, model-training data or a substitute for customer interviews.

### Section 2.1 — Problem context draft

Malaysia's MSMEs contributed 39.7% of GDP and 48.7% of employment in 2025, according to DOSM's July 2026 release. These figures establish economic context, not demand for OrderGuard. [[1]](https://www.dosm.gov.my/portal-main/release-content/micro-small--medium-enterprises-msmes-performance-2025) The World Bank's 2022 assessment found limited use of complex productivity solutions and end-to-end digital transactions among Malaysian SMEs; it is historical context rather than a current invoice-error survey. [[2]](https://www.worldbank.org/en/country/malaysia/publication/digitalizing-smes-to-boost-competitiveness)

Vortex will investigate whether micro/small food-service operators spend avoidable effort reconciling purchase orders, receiving evidence and invoices. The working hypothesis is that quantity, price or unit exceptions become harder to resolve when evidence is scattered. Three-way matching is an established control, not our invention. [[3]](https://learn.microsoft.com/en-us/dynamics365/finance/accounts-payable/accounts-payable-invoice-matching) We propose a focused, explainable exception workflow with human approval. No interviews, purchasing-error prevalence or time savings have yet been established by this project.

### Section 2.2 — Solution rationale draft

OrderGuard compares one item's purchase-order, receiving and invoice data using deterministic rules, blocks ambiguous inputs and records human clarification or approval before adding a simulated supplier action to an outbox. Optional AI suggests structured fields; a person must verify them. NIST recommends evaluating generated output against known truth, while OWASP recommends validating outputs and restricting AI authority. [[4]](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf) [[5]](https://owasp.org/www-project-top-10-for-large-language-model-applications/assets/PDF/OWASP-Top-10-for-LLMs-v2025.pdf)

The prototype demonstrates source-linked exceptions, repeat supplier-item patterns and a Money at Risk review indicator, not a final payable amount. Current browser input uses a shared item name; independent source ingestion and multi-line reconciliation remain outside scope. All business records are synthetic. The shared demo-owner access guard is not production user authentication or live Orbyte RBAC, and the system sends no real supplier messages or payments.

### Section 3.2 — Validation/deployment draft

Planned discovery will involve 3–5 consenting SME operators or representative testers, with their roles reported separately. A proposed 12-task synthetic set covers matching records, quantity/price exceptions and ambiguous units. Manual and app testing will use equivalent sets and counterbalanced order. We will include human-review time, failed attempts, missed exceptions, false alerts and help requests. These activities are proposed, not completed.

The 70-test regression suite has passed, but this does not establish user benefit or live AI accuracy. Deployment through the team's Replit project, secure configuration, public-link checks and sponsor proof of use still require verification. No measured savings or completed deployment is claimed.

## Impact measurement worksheet

No measured baseline or achieved savings currently exist in this project documentation.

1. Prepare a labeled synthetic set including matching records, shortages, price differences and ambiguous units.
2. Time manual checking using those records and record the method, sample size and individual times.
3. Run the same task with the prototype using a consistent start/end definition. Include human review time.
4. Calculate time reduction: (manual baseline - prototype time) / manual baseline × 100%.
5. Count detected known discrepancies, missed discrepancies and false alerts separately.
6. Set a realistic percentage target based on the baseline and explain why it is feasible.

A baseline may be estimated under the official template, but label it as estimated, explain the assumptions and cite any external source. Do not invent a measured number. Prototype targets must be labeled targets, not results.

SDG 8.2 is the primary productivity/technological-upgrading link; SDG 8.3 includes productive activity and MSME growth. These are intended alignment, not achieved impact. [[6]](https://sdgs.un.org/goals/goal8) Do not equate synthetic task time with the UN's national indicators, or claim quantified food-waste savings without measuring them.

## Technical declaration field mapping

| Section | Required content | Limit |
| --- | --- | --- |
| 1 | Team/leader details, prototype and repository links | Fields |
| 2.1 | Actual end-to-end architecture | 200 words |
| 2.2 | Languages, frameworks and libraries: name, version, purpose, license | Table |
| 3.1 | Every application API, provider, purpose and access tier | Table |
| 3.2 | Cloud providers, purpose, plan and region | Table |
| 4.1 | Application models: name/version, source, usage type, license/terms | Table |
| 4.2 | Training/evaluation/runtime datasets, provenance, license and personal-data indicator | Table |
| 4.3 | Development AI tools, version where known, use and extent; actual team review/testing | Review statement: 100 words |
| 5 | Sponsor resources actually used; whether replaceable | Explanation: 100 words |
| 6.1 | Actual collection, storage, API transmission, protection and retention | 150 words |
| 6.2 | Known AI limitations and implemented mitigations | 150 words |
| 7 | Complete and truthful readiness checks | Checklist |
| 8 | Leader verifies, signs and dates | Human completion |

Declare ChatGPT assistance with ideation and substantial documentation. Do not call it merely spelling correction. Record actual review actions when performed. Distinguish a development assistant from a model called by the application. Do not guess a model/version, dependency license, deployment region or tool-use extent.

Also disclose Replit Agent assistance with repository review, code fixes, regression tests, research, source verification and documentation/PR preparation. The team must independently review and adapt the work; agent activity is not evidence that the team has completed its own review.

Complete every section. Use “None” or “No” only when genuinely inapplicable; unresolved facts must be resolved before final submission, not converted to “None”.

## Sponsor proof of use

- Replit is compulsory. Accepted proof includes a live deployment URL, project link with history or credit-exhaustion evidence from the team's own account/project.
- GPU training, fine-tuning or inference must use RunPod according to the orientation and participant handbook.
- For actual RunPod use, retain a dashboard screenshot with Pod ID (or serverless endpoint), GPU type and runtime as applicable.
- If no GPU work is used, describe non-use accurately and seek organizer clarification if a submission field insists on evidence.
- Never fabricate proof, expose keys, or equate receiving credits with using the service.
- Keep evidence with the declaration. Suggested template filenames: SDC2026_Vortex_Replit_POU.pdf and, if applicable, SDC2026_Vortex_Runpod_POU.pdf.

## Domain 2 coverage and demo acceptance

| Must-have | Planned evidence |
| --- | --- |
| One SME problem | Restaurant purchasing discrepancy checks with a clear target user |
| Automated journey | Input → connected purchase/receipt/invoice data → comparison → owner approval → simulated outcome |
| Accuracy/ease of learning | Source-linked flags, missing-unit clarification and an observed first-time-user task |
| Human control | Protected demo-owner actions, reject path, approval before outbox action, activity history; production staff/owner identities are not implemented |
| Orbyte fit/reuse | Clearly labeled mock interfaces; configurable products/units; no claim of live access |
| Business benefit/SDG | Baseline, time/error measures, realistic target and SDG 8 rationale |

Demonstrate a matching case, a discrepancy case and a missing-information case. Verify that rejection produces no outbox action, repeat approval produces no duplicate, and corrected information is rechecked before owner closure.

The first live workflow should run end-to-end even if rough. Extra languages, document formats, real messaging and predictive analytics can remain roadmap items.

## Ordered work remaining

### 23 October — resolve scope and begin the build

1. Confirm the assigned domain, registered roster, leader, student eligibility and workshop completion.
2. Resolve the AI-origin concern with organizers and record the team's own problem reasoning.
3. Validate the purchasing task; keep all demo business records synthetic.
4. Confirm the narrow MVP, technical stack and AI/runtime choice.
5. Use the team's Replit account, connect the repository and retain real evidence.
6. Build input, comparison, owner approval/rejection, simulated outbox and activity history.

### 24 October — validate and prepare submission

7. Test the complete journey and exception cases; fix failures.
8. Measure the baseline and prototype results or transparently document justified estimates.
9. Fill the official proposal and declaration within word limits.
10. Prepare slides and record a 5–7 minute demonstration video.
11. Verify public repository access, committee collaborators, LICENSE, safe demo access and every link.
12. Have the leader review declarations and sign; submit all six items and retain submission confirmation.

### After the deadline

Freeze the submitted repository until organizer authorization. If shortlisted, the supplied schedule announces finalists on 28 October at 20:00 MYT, with confirmation due 29 October at 12:00 MYT. Follow official Discord updates.

## Suggested six-minute video allocation

This is a proposed structure, not an additional competition rule.

| Time | Content |
| --- | --- |
| 0:00–0:45 | User and purchasing problem |
| 0:45–1:30 | Proposed solution and evidence-linked checking |
| 1:30–3:45 | Working discrepancy, clarification and approval demonstration |
| 3:45–4:30 | Architecture, AI role and Orbyte assumptions |
| 4:30–5:15 | Measured results or clearly labeled targets; SDG |
| 5:15–6:00 | Limitations, reuse and next steps |

## Final honesty check

Do not mark planned features as built, declare tests passed without results, invent SME interviews, claim workshop attendance without confirmation, backdate commits or sign for a team member. This guide and README are AI-assisted working documents for team review.

## Research references

All sources accessed **24 October 2026**. Dates below are the source's publication/update or edition dates, not necessarily the data year.

1. Department of Statistics Malaysia. [Micro, Small & Medium Enterprises (MSMEs) Performance 2025](https://www.dosm.gov.my/portal-main/release-content/micro-small--medium-enterprises-msmes-performance-2025) — 30 July 2026; reference year 2025. Tier 1.
2. World Bank. [Digitalizing SMEs to Boost Competitiveness](https://www.worldbank.org/en/country/malaysia/publication/digitalizing-smes-to-boost-competitiveness) — 31 October 2022. Tier 1.
3. Microsoft Learn. [Accounts payable invoice matching overview](https://learn.microsoft.com/en-us/dynamics365/finance/accounts-payable/accounts-payable-invoice-matching) — Updated 15 May 2025. Tier 3.
4. National Institute of Standards and Technology. [Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile (NIST AI 600-1)](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf) — July 2024. Tier 1.
5. OWASP. [Top 10 for Large Language Model Applications, 2025 edition](https://owasp.org/www-project-top-10-for-large-language-model-applications/assets/PDF/OWASP-Top-10-for-LLMs-v2025.pdf) — 18 November 2024; edition labelled 2025. Tier 2.
6. United Nations Department of Economic and Social Affairs. [Goal 8](https://sdgs.un.org/goals/goal8) — Target wording publication date not stated on the page. Tier 1.
