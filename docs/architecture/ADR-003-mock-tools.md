# ADR-003: Isolated Mock Tools

## Status

Accepted

## Decision

The prototype will use simulated tools instead of
real external systems.

## Reasons

- Prevent accidental real-world actions.
- Avoid privacy risks.
- Enable deterministic experiments.
- Enable controlled tool-abuse scenarios.

## Examples

- search_customer
- get_account
- send_email
- delete_record

The tools will not communicate with real customer,
financial or external production systems.