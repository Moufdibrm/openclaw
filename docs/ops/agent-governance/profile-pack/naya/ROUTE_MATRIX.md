# Naya Route Matrix

Last updated: `2026-05-07`

## Current Protocols

| Route | Status | Coverage | Purpose | Proof |
| --- | --- | --- | --- | --- |
| `naya.stock-check` | `prod` | `specialist_route_registry` | SKU stock and reorder risk check. | stock_check_json and final_summary |
| `naya.product-sourcing` | `prod` | `specialist_route_registry` | Sourcing report from reviewed sourcing sheet. | report_bundle and verification_json |
| `naya.campaign-support` | `beta` | `planned` | Campaign feasibility under stock constraints. | campaign support artifact |
| `naya.supplier-comm` | `draft` | `planned` | Supplier communication, approval-gated. | draft and explicit approval |

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
