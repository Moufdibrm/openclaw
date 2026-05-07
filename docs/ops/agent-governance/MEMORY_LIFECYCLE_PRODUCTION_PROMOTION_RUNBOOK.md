# Memory Lifecycle Production Promotion Runbook

Date: `2026-05-07`

Scope: Jack-X / LLM Wiki / shared KG production promotion. This is a governance and validation runbook only. Runtime deployment, service restart, gateway changes, VPS release control, and Mission Manager implementation remain owned by the integrator lane.

## Current Gate Status

Ready:

- real Jack-X event DB replay from existing processed data
- memory candidate regeneration from real processed data
- promotion review regeneration
- no-apply KG validation
- isolated review queue generation
- deterministic Memory Wiki compile
- copied-KG lifecycle rehearsal for commit, refinement, correction, and retrieval

Not ready for live autonomous KG writes:

- live `commit-candidate --apply` is not yet gated by promotion-review decisions
- Memory Wiki `kg_operations` are not yet bridged into Jack-X review as a repeatable route
- Memory Wiki pages still miss bounded KG relation context
- feedback-loop route is proven as copied-KG rehearsal, not live route
- Jack retrieval proof from the live runtime context is still missing after a real KG update

## Promotion Sequence

1. `stage_isolated_replay`
   - Status: done.
   - Proof: `/Users/moufdi/.openclaw/workspace-jack-x/replays/db-existing-data-20260507T000135Z`
   - Requirement: active KG hash unchanged.

2. `stage_lifecycle_rehearsal`
   - Status: done.
   - Proof: `/Users/moufdi/.openclaw/workspace-jack-x/replays/lifecycle-e2e-20260507T001119Z/lifecycle-e2e-summary.json`
   - Requirement: all lifecycle states green on copied KG.

3. `close_review_gate`
   - Status: next.
   - Owner: integrator/Tony lane if runtime script changes are required.
   - Required behavior: `commit-candidate --apply` must only apply accepted `promote` items, never the full candidate when promotion review says `review` or `reject`.
   - Required proof: candidate with mixed `promote/review/reject` decisions applies only allowed rows on copied KG.

4. `bridge_wiki_refinement`
   - Status: next.
   - Required behavior: LLM Wiki `kg_operations` become Jack-X memory review artifacts; LLM Wiki still never writes KG directly.
   - Required proof: one wiki operation becomes `pending`, then `approved/rejected/deferred`, then either commits or skips with reason.

5. `relation_rendering`
   - Status: next.
   - Required behavior: Memory Wiki page seeds include bounded relation evidence from memory projection.
   - Required proof: page for an entity with existing KG relation renders relationships in the page and manifest.

6. `supervised_low_risk_live_commit`
   - Status: blocked until review gate exists.
   - Required behavior: one low-risk channel/project/operation update is committed to live KG under supervision.
   - Required proof: strict validation after commit, hash change explained, backup path recorded, Jack retrieval proof present.

7. `feedback_loop_live_fixture`
   - Status: blocked until review gate and wiki bridge exist.
   - Required behavior: previous fact -> later signal -> correction candidate -> review -> history-preserving commit or skip -> retrieval.
   - Required proof: correction metadata includes source refs, confidence, review decision, and supersession/staleness metadata when relevant.

8. `runtime_deploy_restart`
   - Status: handoff required.
   - Owner: integrator.
   - Requirement: deploy only after local copied-KG tests, live supervised commit proof, and rollback notes are complete.

## Deployment Guardrails

- Do not deploy from this governance lane.
- Do not restart services from this governance lane.
- Do not touch gateway, systemd, VPS deploy scripts, or Mission Manager code from this lane.
- Do not allow LLM Wiki direct KG writes.
- Do not allow Mnemos KG writes.
- Do not allow identity, role, permission, support, payment, legal, or destructive corrections without review.
- Treat `.openclaw/knowledge-graph/memory.jsonl` as canonical; `.clawdis` must remain compatibility-only until source-of-truth cleanup is complete.

## Rollback Requirements

Before the first live commit:

- capture SHA-256 of `.openclaw` and `.clawdis` KG files
- write timestamped backups of both files
- record candidate path, review path, commit summary, and strict validation output
- verify `.openclaw` and `.clawdis` remain aligned or record the explicit compatibility reason if they diverge

Rollback means:

- restore both timestamped backups
- run strict validation on both
- rebuild memory projection
- compile deterministic Memory Wiki
- document the reverted candidate and reason
