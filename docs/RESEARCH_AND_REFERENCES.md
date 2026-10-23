# Vortex OrderGuard — Research and References

**Research date:** 24 October 2026 (Asia/Kuala_Lumpur)

**Scope:** Focused desk-research evidence for the hackathon submission

**External sources cited:** 10

## Recommendation

Position OrderGuard as a focused, human-reviewed purchasing-exception demonstrator. Do not present it as a new accounting method, an independently validated savings product or production-ready financial software. The evidence below supports the problem context and design rationale; it does not replace customer discovery.

Three evidence levels must stay separate: **published findings**, **observed prototype behavior**, and **hypotheses still to test**. This brief uses dated sources and identifies the boundaries of each.

External statistics and guidance inform the documentation only; they are not prototype business records, model-training data or customer interviews. The application demo continues to use synthetic records.

## 1. Malaysian SME context supports investigation, not a demand claim

| Verified context | Evidence date | What it does not establish |
|---|---|---|
| MSMEs generated **39.7% of Malaysia's GDP** and accounted for **48.7% of employment** in 2025. [[1]](https://www.dosm.gov.my/portal-main/release-content/micro-small--medium-enterprises-msmes-performance-2025) | DOSM release: 30 July 2026; data year: 2025 | F&B purchasing-error rates, willingness to pay or OrderGuard's market size |
| Malaysia had **1,292,580 MSMEs**, representing **96.2% of establishments**, in 2025. [[2]](https://smecorp.gov.my/index.php/en/policies/2020-02-11-08-01-24/profile-and-importance-to-the-economy) | SME Corp profile updated August 2026, citing DOSM | A count of potential paying customers for this product |
| Malaysian SMEs used customer-facing digital functions but had limited use of more complex productivity solutions and end-to-end digital transactions in the World Bank's assessment. [[3]](https://www.worldbank.org/en/country/malaysia/publication/digitalizing-smes-to-boost-competitiveness) | 31 October 2022 | A verified 2026 adoption rate or evidence specifically about supplier reconciliation |

The World Bank also identifies capability, information, finance and institutional constraints on digitalization. Its older analysis is useful structural context, but it should not be described as a current survey of this project's intended users. [[3]](https://www.worldbank.org/en/country/malaysia/publication/digitalizing-smes-to-boost-competitiveness)

**Product hypothesis:** some micro/small food-service operators would benefit from a simpler way to reconcile purchasing evidence and handle exceptions. This is deliberately narrower than the national statistics. The team still needs to observe actual workflows and establish how frequent, costly and difficult the problem is. No interviews or customer findings are claimed here.

## 2. Matching is established; usability and exception handling are the hypothesis

Microsoft documents three-way matching that compares invoice prices with purchase-order prices and invoice quantities with product receipts, using configured tolerances. That is direct evidence that the basic matching method already exists in enterprise software. [[4]](https://learn.microsoft.com/en-us/dynamics365/finance/accounts-payable/accounts-payable-invoice-matching)

East Carolina University's operational guide separately describes matching exceptions, manual review, approval restrictions and permission-dependent overrides. It demonstrates a real institutional workflow, not a universal rule that every mismatch always prevents payment. [[5]](https://financialservices.ecu.edu/invoice-matching-ap-team-step-by-step-guide/) The U.S. GAO's 2025 Green Book emphasizes preventive controls and documenting risk assessments; it is control-design context, not a Malaysian SME compliance requirement. [[6]](https://www.gao.gov/products/gao-25-107721)

**Positioning recommendation:** explain what OrderGuard makes visible in its small demonstration: source-linked differences, blocked ambiguous inputs, a human review step, repeat supplier-item patterns and a simulated outcome. Do not claim that these capabilities are unique, that the product replaces an ERP, or that it outperforms existing tools without a direct comparison.

## 3. AI should suggest fields, not decide whether to act

NIST's July 2024 Generative AI Profile describes confidently incorrect outputs and recommends evaluating output against known ground truth (MP-2.3-001). It also cautions against extrapolating capabilities from narrow, anecdotal evaluations (MS-2.5-001). [[7]](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)

OWASP's 2025-edition guidance treats model output as untrusted and recommends validation before downstream use. Its excessive-agency guidance recommends limiting permissions, requiring human approval for high-impact actions and enforcing authorization outside the model. [[8]](https://owasp.org/www-project-top-10-for-large-language-model-applications/assets/PDF/OWASP-Top-10-for-LLMs-v2025.pdf) OECD's 2024-updated AI Principles support human agency, oversight, accountability and traceability. [[9]](https://www.oecd.org/en/topics/ai-principles.html)

**Design interpretation:** optional extraction can reduce retyping, but a person must check suggestions against the evidence. Program rules—not generated prose—should compare records, and the model should not gain authority to send supplier messages or approve financial actions. These are design choices informed by guidance, not certifications from NIST, OECD or OWASP.

## 4. What the prototype currently supports

The implementation evidence is [PR #1: item-identity validation](https://github.com/Aunyiqi/SDC_Hackathon_Submission_Template/pull/1), [PR #2: demo-owner and AI guards](https://github.com/Aunyiqi/SDC_Hackathon_Submission_Template/pull/2), and the [passing submission-branch CI run](https://github.com/Aunyiqi/SDC_Hackathon_Submission_Template/actions/runs/39985643232). Both fixes were merged on 24 October 2026 MYT; the 70-test suite passed. This is functional regression evidence, not a customer benchmark, live-model accuracy study or independent security audit.

| Prototype behavior | Research connection | Important boundary |
|---|---|---|
| Deterministic quantity, price, item and unit checks | Established matching and exception-review practice. [[4]](https://learn.microsoft.com/en-us/dynamics365/finance/accounts-payable/accounts-payable-invoice-matching) [[5]](https://financialservices.ecu.edu/invoice-matching-ap-team-step-by-step-guide/) | One item per case; no OCR, source-system import or ERP-level reconciliation |
| Ambiguous item/unit evidence blocks approval | An explicit project safety choice, rather than a requirement attributed to an external source | The browser form uses one shared item name; mismatch tests exercise the engine/service boundary |
| Optional extraction, typed output checks and human confirmation | Ground-truth evaluation and untrusted-output handling. [[7]](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf) [[8]](https://owasp.org/www-project-top-10-for-large-language-model-applications/assets/PDF/OWASP-Top-10-for-LLMs-v2025.pdf) | Valid field types do not prove the extracted facts are correct |
| Owner-gated simulated actions and activity history | Limited authority and traceability. [[8]](https://owasp.org/www-project-top-10-for-large-language-model-applications/assets/PDF/OWASP-Top-10-for-LLMs-v2025.pdf) [[9]](https://www.oecd.org/en/topics/ai-principles.html) | A shared demo code is not individual accounts or production role-based access |

Public viewing intentionally exposes synthetic records. AI throttles are process-local, not persistent spending quotas. No live Orbyte integration, real supplier messaging, payment approval, tax/e-invoice compliance, fraud-prevention guarantee or deployment verification is claimed.

## 5. Proposed validation — not completed research

Start with **3–5 consenting SME operators or realistic representative testers**, identified separately in the results. Ask each to describe a recent delivery-checking task and the evidence used. Record the workflow and difficulties without putting real supplier/customer records or participant identifiers in the public repository. This is an exploratory sample, not a statistically representative market study.

Use **12 synthetic single-item tasks**: four matching, four quantity/price exceptions and four ambiguous-unit tasks. Evaluate different source-item names separately through engine fixtures because the current form shares one item name across the records. Define the expected outcomes before testing.

Counterbalance manual-first and app-first order, using equivalent task sets to reduce learning effects. Time from opening the evidence to the participant's final decision, including corrections and human review. Keep unsuccessful attempts in the results rather than reporting only successful runs.

| Measure | How to report it |
|---|---|
| Checking time | Per-participant mean/median manual and app time, task count and range; reduction = `(manual − app) / manual × 100%`, only for a positive manual baseline |
| Decision quality | Correct classifications, missed exceptions and false alerts, with denominators and separate blocked-input outcomes |
| Ease of use | Unassisted completion count, help requests and observed points of confusion |
| Optional AI usefulness | Field-level correctness and human corrections against predefined truth; record model/date and include failures |
| Action controls | Separate regression-test outcomes from usability and business-impact results |

Predeclare any prototype target after establishing the manual baseline and before evaluating the app. Until measurements exist, report **“not measured”**, not a made-up percentage. A positive small pilot would justify further testing, not a national savings estimate.

## 6. SDG framing

SDG target **8.2** concerns productivity through technological upgrading and innovation; **8.3** includes productive activity and MSME growth. These support the project's intended productivity direction. [[10]](https://sdgs.un.org/goals/goal8) A reduction in synthetic task time would be a project KPI, not a measurement of the UN's national indicators or proof that the app has achieved an SDG.

## Limitations and source quality

The national figures are directly attributed to official sources; the SME Corp profile also cites DOSM and is not independent replication. No verified study in this evidence set quantifies this specific Malaysian food-service purchasing problem. Error frequency, adoption, willingness to pay and benefits remain unvalidated.

The 2022 World Bank analysis and the cited 2024 NIST/OECD/OWASP editions are older than 18 months. They are used for dated structural or design context, not current adoption estimates. ECU and the UN target page do not state publication dates for the cited content. Frameworks from other jurisdictions are not Malaysian legal advice.

Tier 1 denotes government, multilateral or public academic-institution sources; Tier 2 denotes recognized independent technical guidance; Tier 3 denotes commercial/vendor sources. Microsoft is authoritative about its own documented features, not independent evidence of business outcomes. All references below were fetched and checked; search-only snippets and failed pages were excluded.

## References

All sources accessed **24 October 2026**. Dates below are the source's publication/update or edition dates, not necessarily the data year.

1. Department of Statistics Malaysia. [Micro, Small & Medium Enterprises (MSMEs) Performance 2025](https://www.dosm.gov.my/portal-main/release-content/micro-small--medium-enterprises-msmes-performance-2025) — 30 July 2026; reference year 2025. Tier 1.
2. SME Corporation Malaysia. [Profile of MSMEs in 2015–2025](https://smecorp.gov.my/index.php/en/policies/2020-02-11-08-01-24/profile-and-importance-to-the-economy) — Updated August 2026; reference year 2025. Tier 1.
3. World Bank. [Digitalizing SMEs to Boost Competitiveness](https://www.worldbank.org/en/country/malaysia/publication/digitalizing-smes-to-boost-competitiveness) — 31 October 2022. Tier 1.
4. Microsoft Learn. [Accounts payable invoice matching overview](https://learn.microsoft.com/en-us/dynamics365/finance/accounts-payable/accounts-payable-invoice-matching) — Updated 15 May 2025. Tier 3.
5. East Carolina University Financial Services. [Invoice Matching – AP Team Step-by-Step Guide](https://financialservices.ecu.edu/invoice-matching-ap-team-step-by-step-guide/) — Publication/update date not stated. Tier 1.
6. U.S. Government Accountability Office. [Standards for Internal Control in the Federal Government](https://www.gao.gov/products/gao-25-107721) — 15 May 2025; effective beginning fiscal year 2026. Tier 1.
7. National Institute of Standards and Technology. [Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile (NIST AI 600-1)](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf) — July 2024. Tier 1.
8. OWASP. [Top 10 for Large Language Model Applications, 2025 edition](https://owasp.org/www-project-top-10-for-large-language-model-applications/assets/PDF/OWASP-Top-10-for-LLMs-v2025.pdf) — 18 November 2024; edition labelled 2025. Tier 2.
9. Organisation for Economic Co-operation and Development. [AI principles](https://www.oecd.org/en/topics/ai-principles.html) — Adopted 2019; updated 2024; webpage publication date not stated. Tier 1.
10. United Nations Department of Economic and Social Affairs. [Goal 8](https://sdgs.un.org/goals/goal8) — Target wording publication date not stated on the page. Tier 1.
