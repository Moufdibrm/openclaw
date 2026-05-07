# Jeff Route Matrix

Last updated: `2026-05-07`

## Current Protocols

| Route | Status | Coverage | Purpose | Proof |
| --- | --- | --- | --- | --- |
| `jeff.analyse-profil` | `prod` | `specialist_route_registry` | Creator profile analysis. | pass0 bundle, report_bundle, verification_json |
| `jeff.performance-report` | `prod` | `specialist_route_registry` | Influence portfolio performance report. | report_bundle, verification_json, delivery_json |
| `jeff.candidate-intake` | `beta` | `specialist_route_registry` | Creator candidate intake and graph-oriented enrichment. | candidate_intake_bundle and verification_json |
| `jeff.email-digest` | `beta` | `planned` | Influencer inbox signal reading. | digest artifact |
| `jeff.outreach-pipeline` | `beta` | `planned` | Outreach preparation and follow-up decisions. | outreach artifact |
| `jeff.ajout-collaboration` | `beta` | `planned` | Create collaboration, approval-gated. | pre/post mutation evidence |
| `jeff.collab-management` | `beta` | `planned` | Update/archive collaboration, approval-gated. | pre/post mutation evidence |

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
