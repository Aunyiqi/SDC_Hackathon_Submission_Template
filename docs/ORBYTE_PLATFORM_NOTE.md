# Orbyte Platform Note — Domain 2

This note records the organizer announcement and participant-provided sandbox screenshots shared with the team on 23 October 2026. It separates **observed platform patterns** from **future integration assumptions** so Vortex does not overclaim live Orbyte integration.

## Correct sandbox for participant familiarization

Organizer-provided participant sandbox:

`https://orbyte-xyz.alphareds.com/`

The public marketing website is not the participant sandbox used for this Domain 2 familiarization step.

## Registration is optional

The organizer announcement explicitly states that registering for the Orbyte sandbox is **not compulsory**. The Domain 2 guide does not require teams to depend on the live platform.

Vortex therefore treats Orbyte access as optional product familiarization, not as a technical dependency or submission prerequisite.

## Observed Orbyte patterns

The team reviewed participant-sandbox screenshots showing these UI/workflow patterns:

- A persistent **current organization** context in the left navigation.
- Main navigation grouped around **Dashboard, Organization, Workspace, Talent Hub, Reports and Settings**.
- A Dashboard **Pending Actions** area with workflow categories and due items.
- Organization records displayed as searchable CRUD tables with status and action controls.
- Review-oriented pages using **search, status filters, approve/reject-style workflow states and empty-state messaging**.
- Strong use of clear blue navigation states, white cards, compact status badges and action links.

These observations are used only to make OrderGuard feel compatible with the host product's interaction model. The prototype does not copy private backend behavior or claim access to Orbyte source code/APIs.

## How the MVP now reflects those patterns

OrderGuard uses an Orbyte-aligned shell with:

- a simulated current-organization selector;
- `Workspace > Supplier Checks` and `New Check` navigation;
- Dashboard Pending Actions for `Clarify`, `Review` and `Approved` states;
- a searchable/filterable Supplier Checks table;
- a Reports page containing Supplier Exception Radar and exception analytics;
- status badges, review links and explicit human-control states.

The OrderGuard-specific workflow remains its own product logic: Trust Gate, deterministic discrepancy checks, Supplier Pattern Memory, Money at Risk, owner approval and audit logging.

## Integration assumptions — not observed live APIs

Potential future Orbyte integration inputs may include purchase orders, supplier records, receiving records, invoice data and user/role information. Potential outputs may include exception cases, approval decisions, clarification requests and audit events.

For the competition MVP:

- Orbyte login, organization and roles are simulated.
- Purchase orders, supplier data, receiving records and invoices are synthetic.
- No live Orbyte API integration is claimed.
- Interface/API assumptions are team-created and documented.
- The core workflow remains fully demonstrable without an approved Orbyte account.

## Credential handling

The organizer provided a temporary shared account for participants while personal accounts are pending approval. Those credentials are intentionally **not committed to this public repository**.

Do not add passwords, temporary account credentials, personal IC details, API keys or session tokens to GitHub. If sandbox access is used during the demo, credentials should be handled outside the repository.

## Recommended pitch wording

> We reviewed the Orbyte participant sandbox to understand its organization context, Pending Actions, CRUD and review patterns. OrderGuard adopts those interaction patterns as a potential Workspace module, while the hackathon prototype keeps Orbyte data and roles simulated and does not depend on a live Orbyte API.

Do not claim that the prototype is already integrated with a live Orbyte API unless the team actually builds and verifies that integration.
