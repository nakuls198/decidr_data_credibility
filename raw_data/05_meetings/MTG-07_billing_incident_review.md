# MTG-07 — Billing Integration Incident Review

- **Date:** 2026-02-18
- **Participants:** Lior Ben-David (Head of Engineering), Ana Kowalski (Senior Engineer), Femi Adekunle (Engineer), Sofia Marchetti (QA Lead)
- **Purpose:** Post-incident review of a billing-integration failure that stopped invoice/CRM reconciliation for approximately two days (2026-02-16 to 2026-02-18).

## Discussion

Ana walked through the timeline: a CRM configuration update on 2026-02-16 had an unanticipated interaction with the legacy billing integration, causing invoice status to stop syncing correctly with CRM deal records. She was contacted directly via Slack by Support once customers began reporting stale invoice statuses, rather than via a ticket being raised first, given the urgency. Ana diagnosed and fixed the issue by 2026-02-18. Sofia noted this was the second time in the integration's history that a change elsewhere in the system had unexpectedly affected it, and raised concern about the single-person dependency on Ana for this component.

Lior: *"We can't keep having this be a single point of failure. Femi, can you pair with Ana and get proper documentation written up on how this thing actually works, so it's not just in her head?"*
Femi: *"Yep, happy to — I'll block out time next sprint."*

## Options considered

1. Do nothing differently; treat this as a one-off.
2. Document the integration properly, with Femi leading.
3. Rebuild the integration from scratch to remove the dependency on legacy knowledge.

## Final decision

Option 2 — produce documentation, led by Femi Adekunle with Ana Kowalski's input.

## Decision owner

Lior Ben-David.

## Rationale

Reduce single-person dependency risk without the cost of a full rebuild.

## Conditions or exceptions

None specified regarding priority relative to other engineering work — "next sprint" was not formally scheduled or tracked as a committed deliverable.

## Actions

- Femi Adekunle to pair with Ana Kowalski and produce documentation. **Due:** "next sprint" (no specific date recorded).

## Unresolved matters

No corresponding documentation task was recorded as completed, and no follow-up review of this action item appears in any later meeting record.
