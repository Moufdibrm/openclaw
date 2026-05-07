# Memory Review Gate - Tony Handoff

Date: `2026-05-07`

Owner for implementation: `tony` / integrator lane.

Scope: close the live Jack-X KG write gate before any production `commit-candidate --apply`.

This handoff does not authorize this governance lane to edit runtime scripts, restart services, deploy to VPS, or change gateway/Mission Manager code.

## Problem

The lifecycle rehearsal is green on copied KG, but the live Jack-X DB analysis path still has an unsafe commit shape:

1. memory update script writes a graph candidate
2. `jack-x-kg-promotion-review.py` classifies candidate objects into:
   - `already_known`
   - `promotion_candidates`
   - `review_required`
   - `reject_or_event_only`
3. `jack_x_memory_reviews.py upsert-from-promotion-review` stores review items
4. the runtime cycle still calls `brm-shared-graph.py commit-candidate --apply` on the full graph candidate

That means the review exists, but it does not yet gate what is applied.

## Known Apply Sites

Primary:

- `/Users/moufdi/hermes-runtime/scripts/jack_x_db_analysis_cycle.py`
  - function: `commit_graph_candidate`
  - current behavior: applies the full candidate after review/upsert

Also present:

- `/Users/moufdi/hermes-runtime/scripts/jack_x_lark_message_cycle.py`
- `/Users/moufdi/hermes-runtime/scripts/jack_x_email_intake_cycle.py`
- `/Users/moufdi/hermes-runtime/scripts/jack_x_whatsapp_cycle.py`
- `/Users/moufdi/hermes-runtime/scripts/jack_x_lark_table_cycle.py`

These should converge on the same gated helper instead of each script inventing its own policy.

## Required Behavior

`commit-candidate --apply` must not receive the original full candidate unless the promotion review says every durable row is safe to apply.

Expected policy:

- `already_known`: no new durable write required
- `promotion_candidates`: eligible for an allowlisted candidate rewrite, then apply
- `review_required`: no KG write; create/update memory review only
- `reject_or_event_only`: no KG write; keep in reports only

If there are zero `promotion_candidates`, the graph commit step must return:

```json
{
  "status": "skipped",
  "reason": "no_review_approved_promotions",
  "apply": false
}
```

Pending dedup finalization must only happen after the durable KG effect is safe:

- if no allowed promotions were applied, do not finalize dedup as promoted
- if only a filtered allowed candidate was applied and validated, finalize only the source rows attached to that filtered candidate

## Minimal Patch Shape

Add a shared helper, preferably in a small runtime-local module:

- input:
  - original graph candidate path
  - promotion review JSON
  - output path for filtered candidate
- output:
  - `filtered_candidate_path` when there are allowed promotions
  - skip reason when there are none
  - counts for `already_known`, `promote`, `review`, `reject`

The helper must:

- map `promotion_candidates[*].candidate_id` to graph candidate analysis object ids
- include only entities/relations that are explicitly allowed by the promotion decision
- fail closed if mapping is ambiguous
- preserve original candidate metadata/source refs
- emit a machine-readable filter report

Do not implement destructive correction, identity merge, role change, permission relation, support/payment/legal fact, or stale deletion in this gate. Those remain review-gated.

## Required Tests

Run on copied KG first.

1. Mixed candidate test
   - Input: one candidate with `promote`, `review`, and `reject` decisions.
   - Expected: filtered candidate contains only promoted rows.
   - Expected: review rows are upserted.
   - Expected: rejected rows are not in KG.

2. No-promote test
   - Input: Maybe Paris Lark table replay where deterministic review produced `19` review items and `0` promote.
   - Expected: commit skipped with `no_review_approved_promotions`.
   - Expected: KG hash unchanged.
   - Expected: dedup not finalized as promoted.

3. Real DB replay regression
   - Source: `/Users/moufdi/.openclaw/workspace-jack-x/replays/db-existing-data-20260507T000135Z`
   - Expected: all replay candidates validate in no-apply mode.
   - Expected: the gated live path skips all non-promoted rows.

4. Copied-KG lifecycle regression
   - Source: `/Users/moufdi/.openclaw/workspace-jack-x/replays/lifecycle-e2e-20260507T001119Z`
   - Expected: all `14` lifecycle states stay green.

5. Active KG safety
   - Expected before/after SHA-256 of active KG stays unchanged for all dry-run/copied-KG tests.

## Promotion Gate Before Deploy

Do not deploy or restart until:

- copied-KG tests pass
- one low-risk `promotion_candidates` fixture applies only the filtered candidate
- one `0 promote / many review` fixture skips commit
- strict KG validation passes after copied-KG apply
- rollback instructions and backup paths are recorded

After deploy, first live run must be supervised and low risk.
