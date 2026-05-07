# Kanye Route Matrix

Last updated: `2026-05-07`

## Current Protocols

| Route | Status | Coverage | Purpose | Proof |
| --- | --- | --- | --- | --- |
| `kanye.still-generate` | `beta` | `specialist_route_registry` | Still image generation through selected route. | generated media file and manifest |
| `kanye.reference-edit` | `beta` | `specialist_route_registry` | Reference image edit through selected route. | generated media file and manifest |
| `kanye.higgsfield-skill-exploration` | `beta` | `planned` | Explore the official Higgsfield skill now installed in the Kanye profile. | installed skill surface summary, auth-presence check without secret output, command/help surface, risks and gaps |
| `kanye.higgsfield-skill-validation` | `beta` | `planned` | Bounded test phase for Higgsfield official skill before production use. | test artifacts, manifest, cost/error notes, comparison with current kanye-generate path |
| `kanye.higgsfield-generate.official-cli` | `beta` | `planned` | Official Higgsfield CLI still/video generation through the installed higgsfield-generate skill. | prompt.txt, higgsfield job json, downloaded media, manifest.json |
| `kanye.higgsfield-product-photoshoot.validation` | `beta` | `planned` | Validate product-focused Higgsfield photoshoot modes before beta use. | enhance-only output if used, generated media, manifest.json |
| `kanye.higgsfield-marketplace-cards.validation` | `draft` | `planned` | Validate marketplace card generation and visual compliance before beta use. | generated media set, manifest.json, compliance notes |
| `kanye.higgsfield-soul-id.validation` | `draft` | `planned` | Validate Soul ID only after explicit operator approval, identity consent, and paid-plan check. | approval record, input photo manifest, soul id status, reuse test manifest |

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
