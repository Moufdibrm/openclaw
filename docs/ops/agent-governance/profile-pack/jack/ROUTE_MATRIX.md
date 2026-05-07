# Jack Route Matrix

Last updated: `2026-05-07`

## Current Protocols

| Route | Status | Coverage | Purpose | Proof |
| --- | --- | --- | --- | --- |
| `jack.protocol-missing` | `beta` | `specialist_route_registry` | Create reviewable protocol candidate when no governed specialist route exists. | compact_json plus final_summary |
| `jack.capability-missing` | `beta` | `specialist_route_registry` | Open capability gap instead of improvising unsupported tool use. | compact_json plus final_summary |
| `jack.draft-protocol-runtime` | `beta` | `specialist_route_registry` | Draft protocol runtime bridge. | compact_json plus verification_report |
| `jack.direct.mm-supervision` | `beta` | `package_only` | Direct canonical Mission Manager supervision. | decision_json, mission_patch, final_summary |
| `jack.email-digest` | `beta` | `package_only` | Operator email digest from qualified Jack-X mail artifacts. | final_summary and delivery_summary |
| `jack.higgsfield-skill-supervision` | `draft` | `planned` | Supervise or directly run bounded Higgsfield creative work when Jack is explicitly asked, while keeping Kanye as preferred specialist owner. | installed skill surface summary, auth-presence check without secret output, generated artifact manifest when tested |
| `voice.openai-whisper-input` | `beta` | `planned` | Standard governed voice input transcription through OpenAI whisper-1. | transcript artifact and no local faster-whisper fallback |
| `voice.higgsfield-agent-output` | `draft` | `planned` | Generate differentiated agent voice output through Higgsfield voice identities. | voice profile id, generated test clip, manifest, QA verdict |

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
