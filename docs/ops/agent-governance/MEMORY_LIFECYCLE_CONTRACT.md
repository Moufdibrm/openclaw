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
The remaining product issue is not that the pieces are absent. The issue is that the loop from "captured signal" to "durable KG fact" to "slow consolidation" to "refined durable update" is not governed end to end.

## Product Roles

| Surface | Owner | Role | May write durable KG? |
| --- | --- | --- | --- |
| Jack | operator/orchestrator | route, ask approval, supervise ambiguous memory decisions | yes, only through governed policy |
| Jack-X | long-term memory agent | capture signals, produce memory candidates, run promotion review, commit governed durable facts | yes, only after validation gates |
| LLM Wiki | slow consolidation layer | read Jack-X traces, pages, projections, and source refs; consolidate aliases, relations, summaries, open questions, and KG operation proposals | no direct KG write |
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

For the Najet example, the expected proof is:

- Jack-X source refs where Najet was observed
- candidate person record with aliases and role evidence
- promotion decision for the person and any relationships
- KG commit or review-gated skip
- LLM Wiki page showing consolidated summary, aliases, relationships, and open questions
- refinement operation when the wiki finds a missing or weak relationship

## Current Blockers

- KG JSONL health is repaired locally, but live commit replay still needs supervised proof.
- `~/.openclaw` vs `~/.clawdis` active files are aligned, but the tool/MCP pointers still need source-of-truth cleanup.
- LLM Wiki `kg_operations` need a governed handoff into Jack-X review instead of staying only in the wiki manifest.
- Jack-X DB analysis must gate `commit-candidate --apply` on promotion review, not only record review before commit.
- Memory Wiki pages must include bounded KG relation evidence from memory projection.
- The pending review queue has unresolved items and no operator-grade triage proof.
- Brand-linked memory candidates need native `brand_scope`.
- Retrieval proof is missing: after a commit/refinement, Jack must demonstrate that the updated memory is visible in its bounded context.

## Next Implementation Slice

1. Add promotion-review gating before any Jack-X live `commit-candidate --apply`.
2. Convert wiki `kg_operations` into a Jack-X refinement review artifact without direct KG mutation.
3. Add KG relation evidence to Memory Wiki page seeds/pages.
4. Run one low-risk supervised KG commit after the gate exists.
5. Prove retrieval from Jack's memory context.
