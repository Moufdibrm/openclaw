# Mnemos Procedures

Last updated: `2026-05-07`

## Preflight

1. Classify the ask: audit/read, discussion/approval, or autonomous E2E on a validated route.
2. Resolve brand/account/tenant when the task is brand-linked.
3. Check `ROLE_PERMISSIONS.json` and `ROUTE_MATRIX.md` before selecting a tool.
4. Confirm write scope and approval gates before any external or business mutation.
5. Define the proof target before execution.

## Direct Tool Use

Direct tool use is allowed only inside the agent's visible/read/write projection and autonomy level.
Repeated direct patterns should become protocol candidates through Jack/Curator flow.

## Protocol Work

When a route exists, follow the route package and leave the proof required by `ROUTE_MATRIX.md`.
Route status controls confidence: `draft`, `beta`, or `prod`.

## Context Thresholds

For Jack continuity, Mnemos uses the canonical bands below unless an explicit route package overrides them:

- `<50%` of model context: normal.
- `50-60%`: watch snapshot.
- `60-85%`: compact_now; prepare a cherry-picked continuity capsule.
- `>=85%`: handoff_required.

Gateway text such as `100% of compaction threshold` means progress toward the configured compaction threshold. If the threshold is `60%`, then `100% of compaction threshold` equals `60%` raw context, not full context exhaustion.

If a gateway/session hygiene path only fires at `85%`, classify it as runtime hygiene behavior, not Mnemos protocol truth. Governance may document the mismatch, but runtime/gateway changes stay outside Mnemos ownership.

## External Mutation

External messages, support replies, dispute messages, refunds, billing/payment changes, campaign publication, paid delivery mutations, and ambiguous target changes require explicit approval.

## Completion

A valid completion includes the action taken, artifact or readback path, route/protocol id when applicable, and any blocker or assumption.
