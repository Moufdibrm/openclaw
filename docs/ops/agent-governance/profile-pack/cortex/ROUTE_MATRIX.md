# Cortex Route Matrix

Last updated: `2026-05-07`

## Current Protocols

| Route | Status | Coverage | Purpose | Proof |
| --- | --- | --- | --- | --- |
| `cortex.ads-observation` | `prod` | `specialist_route_registry` | Paid ads observation. | report_bundle, verification_json, delivery_json |
| `cortex.campaign-management` | `draft` | `planned` | Campaign management plan and handoff. | campaign-management report and task board |
| `cortex.feedback-loop` | `draft` | `planned` | Post-publication feedback loop. | feedback report and next-cycle input |

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
