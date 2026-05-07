# Selena Route Matrix

Last updated: `2026-05-07`

## Current Protocols

| Route | Status | Coverage | Purpose | Proof |
| --- | --- | --- | --- | --- |
| `selena.paypal-dispute.phase1-audit` | `prod` | `specialist_route_registry` | PayPal dispute export audit. | paypal_dispute_audit and final_summary |
| `selena.paypal-dispute.phase1-live` | `prod` | `specialist_route_registry` | Live PayPal fetch plus audit replay. | paypal_dispute_live_audit and final_summary |
| `selena.zendesk-feedback-review` | `prod` | `specialist_route_registry` | Reviewed Zendesk export analysis. | zendesk_feedback_review and final_summary |
| `selena.zendesk-feedback-live` | `prod` | `specialist_route_registry` | Live Zendesk fetch plus review replay. | zendesk_feedback_live_review and final_summary |

## Common Proof Rules

### Discussion

- short confirmation of actions taken
- explicit blocker or assumption when present

### Protocol

- route/package id
- structured artifact or report bundle
- validation/replay evidence for prod route claims

### External Mutation

- resolved target before mutation
- explicit approval
- post-mutation readback or platform confirmation

### Voice

- OpenAI whisper-1 transcript for input voice
- Higgsfield job id and local audio artifact for output voice once validated
- approval record before external audio send

## Missing Route Behavior

- If the request is repeated and no route exists, open or route through `jack.protocol-missing`.
- If the tool/platform capability does not exist, open or route through `jack.capability-missing`.
- Do not silently convert an exploratory direct action into a production protocol claim.
