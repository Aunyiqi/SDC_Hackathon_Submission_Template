# Orbyte Platform Note — Domain 2

This note records the organizer announcement shared with the team on 23 October 2026 and explains how Vortex OrderGuard treats Orbyte in the prototype.

## Correct sandbox for participant familiarization

Organizer-provided participant sandbox:

`https://orbyte-xyz.alphareds.com/`

The public marketing website is not the participant sandbox used for this Domain 2 familiarization step.

## Registration is optional

The organizer announcement explicitly states that registering for the Orbyte sandbox is **not compulsory**. The Domain 2 guide does not require teams to depend on the live platform.

Vortex therefore treats Orbyte access as optional product familiarization, not as a technical dependency or submission prerequisite.

## How OrderGuard uses the Orbyte concept

OrderGuard is designed as a reusable purchasing-exception module that could fit into the Orbyte ecosystem.

For the competition MVP:

- Orbyte login and roles are simulated.
- Purchase orders, supplier data, receiving records and invoices are synthetic.
- No live Orbyte API integration is claimed.
- Interface/API assumptions are team-created and documented.
- The core workflow remains fully demonstrable without an approved Orbyte account.

Potential future integration inputs include purchase orders, supplier records, receiving records, invoice data and user/role information. Potential outputs include exception cases, approval decisions, clarification requests and audit events.

## Credential handling

The organizer provided a temporary shared account for participants while personal accounts are pending approval. Those credentials are intentionally **not committed to this public repository**.

Do not add passwords, temporary account credentials, personal IC details, API keys or session tokens to GitHub. If sandbox access is used during the demo, credentials should be handled outside the repository.

## What we should say in the pitch

Recommended wording:

> OrderGuard is designed for the Orbyte ecosystem, but our prototype does not depend on live Orbyte access. We simulate the required business data, user roles and approval flow, while keeping the module reusable for future integration.

Do not claim that the prototype is already integrated with a live Orbyte API unless the team actually builds and verifies that integration.
