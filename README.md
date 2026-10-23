# Vortex OrderGuard

**Check deliveries. Explain discrepancies. Keep owners in control.**

Vortex OrderGuard is a proposed automation product for Malaysian micro and small businesses. It compares purchase orders, delivery records and supplier invoices, then prepares discrepancy reports for human review. The first demonstration will focus on restaurant purchasing.

> **Project status:** Concept agreed; implementation pending. This repository currently contains the competition starter template and project documentation. The features below are planned, not completed or deployed.

## Team Information

| Field | Details |
| --- | --- |
| Team name | Vortex |
| Project name | Vortex OrderGuard |
| Domain | Domain 2 — Orbyte Smart SME Challenge: Less Busywork, Better Business |
| Primary SDG | SDG 8 — Decent Work and Economic Growth |
| Relevant targets | 8.2: productivity through technological upgrading; 8.3: support for micro and small enterprises |
| Team leader | To be confirmed |
| University / institutions | To be confirmed for all members |
| Number of members | To be confirmed |

## Problem

Small businesses may need to compare supplier messages, purchase orders, receiving records and invoices manually. Differences in quantities, prices, product names and units can make this work difficult.

Our initial hypothesis is that a focused checking and approval workflow can reduce repeated checking and help staff resolve discrepancies consistently. The team still needs to validate this problem with SME owners or staff; no customer research results are claimed here.

## Proposed Solution

OrderGuard will bring relevant records into one comparison, explain each discrepancy and prepare a proposed clarification request. An authorized owner will review, edit, approve or reject that request before it enters a simulated outbox.

AI will help extract structured information from informal supplier messages. Program rules will perform calculations, validate units, enforce permissions and control workflow transitions. Missing or ambiguous information will require clarification instead of a guessed answer.

## Core Automated Journey

| Stage | Planned behavior |
| --- | --- |
| Trigger | Staff submits a synthetic supplier message or delivery record. |
| Connected data | The app loads the matching purchase order, agreed prices, receiving record and invoice. |
| Decision logic | Rules compare quantities and prices; AI assists with extracting message content. |
| Human approval | An owner reviews the evidence and approves, edits or rejects the proposed clarification. |
| Visible outcome | An approved request appears in a simulated outbox; the case status and activity log update. |

A corrected supplier record will be checked again. The owner will confirm the resolution before the case closes.

## Demonstration Scenario

All records in this example are synthetic.

| Record | Details |
| --- | --- |
| Purchase order | Chicken: 10 kg at RM12/kg |
| Receiving record | 8 kg received |
| Supplier invoice | 10 kg at RM13/kg = RM130 |

The comparison will flag:

- A 2 kg difference between ordered and received quantities.
- An invoiced unit price RM1/kg above the agreed price.
- A received-goods comparison amount of RM96, calculated as 8 kg × RM12.
- An RM34 difference between the invoice and that comparison amount, requiring review.

RM96 is a comparison reference, not an automatic payment instruction or a determination of the final amount owed. Partial deliveries, delivery charges and other agreed terms may require further review.

The owner can approve a clarification request asking the supplier to explain or correct the discrepancies. No real message or payment will be sent in the demo.

## Planned MVP Features

1. **Evidence-linked comparison:** Each flag identifies the source values and the rule that produced it.
2. **Clarification for ambiguous inputs:** “Two bags” cannot be compared with kilograms until a person confirms the conversion.
3. **Owner approval:** Staff can submit records; only an authorized owner can approve a consequential action.
4. **Resolution tracking:** Cases remain open until corrected information is checked and the owner confirms resolution.
5. **Activity history:** Record submissions, proposed actions, approvals, rejections and closure.
6. **Duplicate-action protection:** Repeated approval clicks must not create duplicate outbox entries.

### MVP Boundaries

The first version will focus on one restaurant purchasing journey. It will not process real payments, submit statutory filings, provide legal or financial advice, or connect to live Orbyte or WhatsApp services.

Roles and Orbyte interfaces may be simulated. The demo will use only team-created synthetic business records.

## Orbyte Fit and Reuse

OrderGuard is intended as a purchasing exception module within a shared business hub. Assumed interfaces would provide purchase orders, supplier records and role information, while the module returns discrepancy cases, approval decisions and activity records.

These are proposed integration assumptions, not verified live Orbyte APIs. A later version could adapt product mappings, units and review rules for retailers, cafes or other small businesses without rebuilding the core approval workflow.

## Proposed Technical Approach

The following choices are proposals for implementation, not claims about the current starter code.

| Component | Proposed approach |
| --- | --- |
| User interface | Simple web screens for input, comparison, approval and case history |
| Application | Python web backend, building on the starter repository |
| Storage | SQLite for the demonstration |
| Decision rules | Deterministic quantity, unit and price checks |
| AI | Structured extraction from supplier messages; model choice pending |
| Development / hosting | Replit; setup and proof of use pending |
| GPU workload | RunPod if a GPU-based model is used; configuration pending |

If AI extraction is unavailable, the user will be able to enter and confirm structured fields manually. Any fallback will be visibly labeled.

## Validation Plan

Test the same synthetic records manually and with the prototype. Record measured results rather than presenting estimates as achieved savings.

| Measure | Planned method |
| --- | --- |
| Time per check | Compare manual and prototype completion times |
| Discrepancy detection | Compare results with a hand-labeled set of known discrepancies |
| Unnecessary alerts | Count flags on records that should match |
| Ease of learning | Observe whether a new tester completes a check without formal training |
| Approval control | Confirm that staff cannot approve and rejected actions do not execute |
| Reliability | Test missing units, incomplete messages, repeat clicks and corrected records |

Results: not yet measured.

## Data and Privacy

The demo will use synthetic supplier, order and invoice data only. API keys must be stored in server-side secrets and must not be committed.

A real deployment would require business-level data isolation, role-based access, suitable retention and deletion controls, and a review of applicable Malaysian privacy requirements before handling real records.

## Repository and Submission Resources

| Resource | Link / status |
| --- | --- |
| GitHub repository | https://github.com/Aunyiqi/SDC_Hackathon_Submission_Template |
| Official submission templates | https://drive.google.com/drive/folders/1xw7c2aN8N-at8hPEULzkcU76e_FFb0Ef |
| Replit project | Not yet configured |
| Live demo | Not yet deployed |
| RunPod endpoint | Not yet configured |
| Pitch deck | Not yet prepared |
| Demonstration video | Not yet recorded |

The existing starter folders are intended for source code (`src/`), supporting documentation (`docs/`), tests (`tests/`), GPU integration (`runpod/`) and submission files (`submission/`). Starter files are not evidence that the OrderGuard features have been implemented.

## How to Run

OrderGuard does not yet have verified run instructions. Setup, environment variables and test commands will be documented after the implementation is working and tested.

## Technical and AI Disclosure

This README was drafted with assistance from ChatGPT following the team's discussion of the challenge and selection of the project direction. The team must review, adapt and understand the proposal and accurately disclose AI assistance.

The repository is based on the official [SDC Hackathon Submission Template](https://github.com/michaelzhngg/SDC_Hackathon_Submission_Template). Preserve its attribution and license. Document additional tools, models, APIs, libraries and reused materials as they are introduced.

Replit use and proof are pending. The template labels RunPod use as required, while the supplied Participant Handbook ties mandatory RunPod use to GPU workloads. Confirm the applicable requirement with the organizers before finalizing the compute plan and declaration.

## Risks and Next Steps

- Validate the purchasing problem with SME owners or staff.
- Confirm team membership, responsibilities and organizer requirements.
- Finalize the implementation design.
- Build one complete comparison-to-resolution journey.
- Keep AI extraction reviewable and provide manual entry for unclear inputs.
- Measure accuracy, time and usability with synthetic test cases.
- Prepare the required submission materials and verify access to every link.

## Future Improvements

- Additional product aliases and confirmed unit conversions.
- More supplier document formats and languages.
- Configurable rules for different SME sectors.
- Real business-system connectors following permission and privacy review.

## Submission Checklist

- [x] Team name and project direction documented.
- [ ] Team details and responsibilities confirmed.
- [ ] Problem validation completed.
- [ ] Working prototype and user interface available.
- [ ] Core journey and exception cases tested.
- [ ] Replit used and proof of use attached.
- [ ] RunPod requirement confirmed; actual usage and proof documented as applicable.
- [ ] Product requirements completed using the official template.
- [ ] Technical and tools declaration completed.
- [ ] Pitch deck completed.
- [ ] 5–7 minute pitching video with prototype demonstration uploaded.
- [ ] Demonstration links and repository access verified.
- [ ] API keys and sensitive information excluded.
- [ ] Submission documents renamed for Vortex and submitted through the official portal.

## License

This repository retains the [Apache License 2.0](LICENSE) from the official starter template.
