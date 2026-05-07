# Safir Route Matrix

Last updated: `2026-05-07`

## Current Protocols

| Route | Status | Coverage | Purpose | Proof |
| --- | --- | --- | --- | --- |
| `safir.email-audit` | `beta` | `specialist_route_registry` | Email audit report. | safir_email_audit and final_summary |
| `safir.mail-pole-audit` | `beta` | `specialist_route_registry` | Mail pole audit. | safir_mail_pole_audit and final_summary |
| `safir.email-workflow` | `draft` | `planned` | Email workflow generation and design. Reopen with improved GPT Image / Claude design model floor. | draft email workflow artifact, render proof, approval before send |

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
