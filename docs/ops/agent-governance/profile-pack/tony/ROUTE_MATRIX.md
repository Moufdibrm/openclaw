# Tony Route Matrix

Last updated: `2026-05-07`

## Current Protocols

| Route | Status | Coverage | Purpose | Proof |
| --- | --- | --- | --- | --- |
| `tony.codebase-exploration` | `beta` | `specialist_route_registry` | Bounded codebase read and topology extraction. | compact_json and final_summary |
| `tony.development-plan` | `beta` | `specialist_route_registry` | Implementation plan from exploration artifact. | compact_json and verification_report |
| `tony.development` | `beta` | `specialist_route_registry` | Code changes and validation. | code_delta, verification_report, final_summary |

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
