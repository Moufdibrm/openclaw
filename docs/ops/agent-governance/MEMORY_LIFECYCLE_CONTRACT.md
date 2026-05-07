# Memory Lifecycle Contract

Last updated: `2026-05-07`

This contract separates the durable-memory roles for Jack, Jack-X, LLM Wiki, Mnemos, and the shared KG.

It is a governance contract only. It does not authorize runtime wiring, Mission Manager implementation, service restart, deploy, or gateway changes.

## Current Diagnosis

The memory layer is useful but not production-complete.

Observed locally on `2026-05-07` before repair:

- Jack-X already emits graph candidates under `~/.openclaw/workspace-jack-x/runtime/graph-candidates`.
- Jack-X already stores promotion review state in `~/.openclaw/workspace-jack-x/runtime/memory_reviews.db`.
- The shared graph writer already allows `jack` and `jack-x` as commit actors through `shared-graph-write-policy.json`.
- The local durable KG file `~/.openclaw/knowledge-graph/memory.jsonl` was invalid JSONL at line 65, so recent Jack-X graph commits failed before merge.
- LLM Wiki already compiles Jack-X reports and memory projection into pages under `~/.openclaw/memory-wiki`.
- LLM Wiki emits `kg_operations` and `review_items`, but it does not directly mutate the KG.
- Mnemos is continuity memory only and must not become enterprise truth.

The JSONL corruption was repaired on `2026-05-07`; see `MEMORY_LIFECYCLE_REPAIR_REPORT.md`.
The existing Jack-X event DB was replayed on real processed data in an isolated proof run on `2026-05-07`: DB recording is healthy, memory candidates can be regenerated, promotion review can be rebuilt, and Memory Wiki can compile from the replay projection without mutating the durable KG.
A copied-KG lifecycle rehearsal also passed all states from `signal_observed` through `feedback_loop_reported`; see `MEMORY_LIFECYCLE_PRODUCTION_PROMOTION_RUNBOOK.md`.
The remaining product issue is not that the pieces are absent. The issue is that the loop from "captured signal" to "durable KG fact" to "slow consolidation" to "refined durable update" to "future correction" is not governed end to end.

## Product Roles

| Surface | Owner | Role | May write durable KG? |
| --- | --- | --- | --- |
| Jack | operator/orchestrator | route, ask approval, supervise ambiguous memory decisions | yes, only through governed policy |
| Jack-X | long-term memory agent | capture signals, produce memory candidates, run promotion review, commit governed durable facts, and run the autocorrection feedback loop over time | yes, only after validation gates |
| LLM Wiki | slow consolidation layer | read Jack-X traces, pages, projections, and source refs; consolidate aliases, relations, summaries, open questions, contradictions, staleness, and KG operation proposals | no direct KG write |
| Mnemos | continuity layer | preserve session context, compaction handoff, and reinjection capsules | no |
| Shared KG | durable enterprise memory | canonical facts, stable entities, stable relationships, reviewed metadata | n/a |

## Lifecycle

1. `signal_observed`
   - Owner: Jack-X.
   - Input: MS365, Lark, WhatsApp snapshot, Mission Manager session, or bounded operator signal.
   - Output: source artifact with channel/window/source refs.
   - No durable KG mutation.

2. `candidate_extracted`
   - Owner: Jack-X.
   - Output: `brm.graph-candidate.v1` with entities, relations, confidence, source refs, brand scope when relevant, and dedup key.
   - Example: Najet is observed in messages; Jack-X may create or update a candidate person with role evidence and source refs.

3. `promotion_reviewed`
   - Owner: Jack-X.
   - Output: memory review row and promotion decision: `already_known`, `promote`, `review`, or `reject`.
   - Low-confidence identities, people roles, ownership relations, permissions, and finance/customer facts stay review-gated.

4. `durable_committed`
   - Owner: Jack-X or Jack.
   - Output: valid append/merge in `~/.openclaw/knowledge-graph/memory.jsonl` plus strict validation proof.
   - Blocked while the KG file is invalid.
   - Autonomous commit is allowed only for validated low-risk routes after strict schema validation.
   - Approval/review is required for identity merges, role changes, permission/ownership relations, customer/payment/support facts, stale-data deletion, and ambiguous duplicate resolution.

5. `wiki_compiled`
   - Owner: LLM Wiki.
   - Input: Jack-X channel reports, latest memory projection, source refs, and optionally the semantic cache.
   - Output: readable memory pages, summaries, facts, relationships, recent signals, open questions, and `kg_operations`.
   - No direct KG mutation.

6. `wiki_refinement_proposed`
   - Owner: LLM Wiki.
   - Output: reviewable KG operation proposals such as `link_existing`, `upsert_candidate`, `merge_candidate`, `add_relation`, `mark_stale`, or `needs_human`.
   - Example: after Jack-X captures Najet, LLM Wiki can consolidate aliases, infer grounded BRM/brand/channel relationships, and propose a relationship update with evidence.

7. `refinement_reviewed`
   - Owner: Jack-X.
   - Output: accepted/rejected/deferred refinement decision, with provenance to the wiki page and source evidence.
   - LLM Wiki remains advisory; Jack-X owns the promotion queue.

8. `refinement_committed`
   - Owner: Jack-X or Jack.
   - Output: durable KG update and validation proof.
   - Same write gates as `durable_committed`.

9. `retrieval_ready`
   - Owner: Jack plus routed agents.
   - Input: valid KG, Memory Wiki latest manifest, and agent-scoped memory excerpt.
   - Output: bounded context packet for the mission or conversation.

10. `feedback_observed`
   - Owner: Jack-X.
   - Input: later signals, repeated source evidence, operator correction, failed retrieval, specialist feedback, external surface drift, or Memory Wiki contradiction.
   - Output: feedback event linked to the original KG entity/relation and source evidence.
   - No direct destructive mutation.

11. `correction_candidate`
   - Owner: Jack-X or LLM Wiki.
   - Output: proposed correction operation: `confirm`, `add_observation`, `add_relation`, `update_attribute`, `merge_duplicate`, `mark_stale`, `supersede`, `deprecate`, or `needs_human`.
   - LLM Wiki may propose; Jack-X owns the durable review queue.

12. `correction_reviewed`
   - Owner: Jack-X, with Jack/operator approval when ambiguity or risk requires it.
   - Output: accepted/rejected/deferred correction with reason, confidence, and source refs.
   - Contradictions do not overwrite silently. They become an explicit correction candidate.

13. `correction_committed`
   - Owner: Jack-X or Jack.
   - Output: durable KG update, strict validation proof, and metadata linking the update to the previous version.
   - Destructive replacement must use `supersedes`, `superseded_by`, `valid_from`, `valid_until`, or equivalent metadata instead of silent deletion.

14. `feedback_loop_reported`
   - Owner: Jack-X.
   - Output: periodic memory health report: promoted facts, corrected facts, stale candidates, unresolved contradictions, open review backlog, and retrieval quality.

## Future-Time Model

The KG must support memory improving over time.

Rules:

- durable entries should keep provenance, confidence, and review metadata
- corrections should preserve history instead of silently replacing facts
- stale facts should be marked stale or superseded before removal
- repeated corroboration should increase confidence only when sources are independent enough
- contradictions should lower confidence or open review, not auto-delete prior truth
- time-sensitive facts should carry `observed_at`, `valid_from`, `valid_until`, `last_seen_at`, or equivalent metadata when available
- a future signal may correct a past KG entry, but must leave a reviewable trail
- Jack-X owns this feedback loop; LLM Wiki proposes slow corrections; Jack/operator resolves ambiguous or risky cases

Autocorrection is allowed for:

- typo/normalization fixes where stable identity is unchanged
- alias additions with repeated evidence
- non-destructive relation additions with strong source refs
- confidence refresh from new corroborating evidence
- marking stale when a better source clearly supersedes old information

Autocorrection is review-gated for:

- person identity merge or split
- role/responsibility change
- brand ownership/access/permission relation
- customer/support/payment/legal facts
- destructive deletion
- source conflict between two plausible facts
- any correction that would affect an agent permission, external action, or business decision

## Source Of Truth

Canonical durable KG path:

- `~/.openclaw/knowledge-graph/memory.jsonl`

Canonical Jack-X runtime paths:

- `~/.openclaw/workspace-jack-x/runtime/graph-candidates`
- `~/.openclaw/workspace-jack-x/runtime/channel-reports`
- `~/.openclaw/workspace-jack-x/runtime/memory_reviews.db`
- `~/.openclaw/workspace-jack-x/logs/cron`

Canonical LLM Wiki paths:

- `~/.openclaw/memory-wiki/latest.json`
- `~/.openclaw/memory-wiki/pages`
- `~/.openclaw/memory-wiki/runs`

Optional generated LLM Wiki cache path:

- `~/.openclaw/semantic-cache/jack-x-semantic-cache.json`
  - created on first active semantic run; not required for deterministic wiki compilation.

Legacy or ambiguous paths:

- `~/.clawdis/knowledge-graph/memory.jsonl`
- `~/.openclaw/kg`

These must not be treated as independent sources of truth. They need either compatibility reads or explicit deprecation, but no split-brain writes.

## Promotion Rules

Auto-eligible after KG repair:

- stable brand/project/application/channel entities with source refs
- non-sensitive product or operation entities with brand scope
- non-destructive relation additions with confidence at or above the route threshold
- exact update to an already known entity where dedup key and source refs match

Review-gated:

- person identity creation or merge
- person role, ownership, access, or responsibility changes
- duplicate consolidation
- stale-data deletion or destructive correction
- finance, payment, dispute, support, refund, customer-risk, or legal facts
- any ambiguous brand scope or tenant scope
- any correction that changes a previously durable person, permission, ownership, support, payment, or business-critical fact

Forbidden:

- LLM Wiki direct KG mutation
- Mnemos KG mutation
- raw telemetry/runtime batch entities in durable KG
- provenance-only links such as `derived_from` or `reported_in` as durable graph relations
- committing when KG validation fails

## Proof Contract

Every memory lifecycle run must be able to produce:

- source artifact path and channel/window scope
- graph candidate path
- promotion review summary
- KG commit summary or explicit skip reason
- strict KG validation result
- Memory Wiki manifest path when the wiki ran
- `kg_operations` count and review item count
- retrieval proof showing Jack can read the updated fact or the open question
- feedback loop proof when a prior fact is confirmed, corrected, superseded, or marked stale

For the Najet example, the expected proof is:

- Jack-X source refs where Najet was observed
- candidate person record with aliases and role evidence
- promotion decision for the person and any relationships
- KG commit or review-gated skip
- LLM Wiki page showing consolidated summary, aliases, relationships, and open questions
- refinement operation when the wiki finds a missing or weak relationship
- future correction trail if a later signal changes Najet's role, aliases, team relation, or confidence

## Current Blockers

- KG JSONL health is repaired locally, and real DB replay works through no-apply validation, but live commit replay still needs supervised proof after the review gate exists.
- `~/.openclaw` vs `~/.clawdis` active files are aligned, but the tool/MCP pointers still need source-of-truth cleanup.
- LLM Wiki `kg_operations` need a governed handoff into Jack-X review instead of staying only in the wiki manifest.
- Jack-X DB analysis must gate `commit-candidate --apply` on promotion review, not only record review before commit.
- Memory Wiki pages must include bounded KG relation evidence from memory projection.
- Future-time feedback loop is specified in governance, but not yet implemented as a repeatable route/protocol.
- The pending review queue has unresolved items and no operator-grade triage proof.
- Brand-linked memory candidates need native `brand_scope`.
- Retrieval proof is missing: after a commit/refinement, Jack must demonstrate that the updated memory is visible in its bounded context.

## Next Implementation Slice

1. Add promotion-review gating before any Jack-X live `commit-candidate --apply`.
2. Convert wiki `kg_operations` into a Jack-X refinement review artifact without direct KG mutation.
3. Add KG relation evidence to Memory Wiki page seeds/pages.
4. Add Jack-X memory feedback loop route for contradiction/staleness/correction review.
5. Run one low-risk supervised KG commit after the gate exists.
6. Prove retrieval from Jack's memory context.
7. Prove one autocorrection fixture: previous fact -> later signal -> correction candidate -> review -> superseded/confirmed KG update -> retrieval.

Production promotion order is governed by `MEMORY_LIFECYCLE_PRODUCTION_PROMOTION_RUNBOOK.md`.
