# Rosa Route Matrix

Last updated: `2026-05-07`

## Current Protocols

| Route | Status | Coverage | Purpose | Proof |
| --- | --- | --- | --- | --- |
| `rosa.offer-strategy.direct` | `prod` | `specialist_route_registry` | Offer strategy direct route. | decision_json, verification_json, final_summary |
| `rosa.audit-performance-marketing` | `prod` | `specialist_route_registry` | Performance marketing audit. | report_bundle and verification_json |
| `rosa.veille-concurrentielle` | `prod` | `specialist_route_registry` | Competitive watch report. | report_bundle and verification_json |
| `rosa.market-graph-refresh` | `beta` | `specialist_route_registry` | Market graph refresh and promotion. | graph_snapshot and verification_json |

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
