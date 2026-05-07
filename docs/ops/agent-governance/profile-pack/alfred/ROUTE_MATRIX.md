# Alfred Route Matrix

Last updated: `2026-05-07`

## Current Protocols

| Route | Status | Coverage | Purpose | Proof |
| --- | --- | --- | --- | --- |
| `alfred.visibility-audit` | `prod` | `specialist_route_registry` | SEO visibility audit. | HTML/PDF/JSON report bundle and verification_json |
| `alfred.strategy-plan` | `beta` | `planned` | Strategy plan from phase1 artifacts. | strategy report and workboard |
| `alfred.deployment-feedback-loop` | `beta` | `planned` | Deployment feedback loop artifacts. | feedback report and queue artifacts |

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
