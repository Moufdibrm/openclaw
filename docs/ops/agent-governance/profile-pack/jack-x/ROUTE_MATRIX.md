# Jack-X Route Matrix

Last updated: `2026-05-07`

## Current Protocols

| Route | Status | Coverage | Purpose | Proof |
| --- | --- | --- | --- | --- |
| `jack-x.registry-ingest` | `beta` | `package_only` | Governed channel registry ingest. | runtime_summary and verification_json |
| `jack-x.email-intake-pass0` | `beta` | `package_only` | MS365 mail intake into compact memory candidates. | compact_json and memory_candidate |
| `jack-x.lark-message-intake-pass0` | `beta` | `package_only` | Lark message intake into compact memory candidates. | compact_json and memory_candidate |
| `jack-x.lark-table-intake-pass0` | `beta` | `package_only` | Lark table intake into compact memory candidates. | compact_json and memory_candidate |
| `jack-x.whatsapp-intake-pass0` | `beta` | `package_only` | WhatsApp runtime snapshot intake into memory candidates. | compact_json and memory_candidate |
| `jack-x.db-analysis` | `beta` | `package_only` | Memory projection, review and DB analysis. | memory_projection and runtime_summary |
| `jack-x.memory-wiki` | `beta` | `recurring_script` | Compile Jack-X reports and memory projection into readable Memory Wiki pages plus reviewable KG operations. | latest_manifest, page_count, kg_operations, review_items |
| `jack-x.memory-refinement-review` | `draft` | `planned` | Review LLM Wiki KG operation proposals and convert accepted items into governed Jack-X promotion decisions. | refinement_review_artifact, accepted/rejected/deferred counts, KG commit or skip reason |
| `jack-x.memory-feedback-loop` | `draft` | `planned` | Detect later evidence, contradictions, stale facts, and failed retrievals, then propose history-preserving KG corrections. | feedback_event, correction_candidate, review_decision, supersession_or_confirmation_summary, retrieval_proof |
| `jack-x.signal.extract` | `beta` | `package_only` | Extract mission/memory candidates from bounded signal. | handoff_packet, mission_patch, memory_candidate |

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
