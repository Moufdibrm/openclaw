# Memory Lifecycle Backlog - 2026-05-08

Scope: Jack-X, LLM Wiki, durable KG, memory reviews, and Mission Manager memory surfaces.

This backlog is based on the live validation after the Mission Manager governance auth fix.

## Current Observed State

Auth and publish:
- `MISSION_MANAGER_GOVERNANCE_API_KEY` is present on local and VPS env.
- `/memory/reviews` returns `200` with `43` MM-visible pending reviews.
- Jack-X DB analysis validation run: `ok`.
- Memory projection publish: `ok`.
- Final memory projection publish: `ok`.
- LLM Wiki compile and publish: `ok`.

Event intake:
- `7090` Jack-X events are marked `processed`.
- No pending event analysis remained in the validation run.

Durable KG:
- `244` durable KG entries.
- `150` entities.
- `94` relations.
- Entity counts: `37 commerce_order`, `20 channel`, `14 operation`, `13 issue`, `13 application`, `12 decision`, `10 task`, `9 product`, `6 artifact_ref`, `4 person`, `4 integration`, `4 pole`, `2 brand`, `1 company`, `1 team`.
- Relation counts: `48 belongs_to`, `22 includes`, `20 uses`, `4 member_of`.

Memory reviews:
- Local review DB has `602` pending reviews:
  - `103` P1 `identity_merge`.
  - `108` P2 `kg_candidate`.
  - `185` P3 `kg_candidate`.
  - `206` P3 `uncertain_relation`.
- Mission Manager currently exposes `43` pending reviews:
  - `33` P1 `identity_merge`.
  - `10` P2 `kg_candidate`.

LLM Wiki:
- Latest compile: `2026-05-08T14:28:20Z`.
- `80` pages.
- `80` KG operations.
- `61` review items.
- `19` operations are `ready`.
- `61` operations are `candidate`.
- Ready operations are mostly existing people and applications.
- Candidate operations are mostly channel, brand, company, operation, product, integration, and person refinements.

Latest DB analysis promotion review:
- `131` object candidates examined.
- `22` already known.
- `0` promoted by promotion review.
- `53` review-required.
- `56` rejected/event-only.

Observed mismatch:
- The latest commit still changed the KG even though promotion review had `promote_count=0`.
- Latest commit changes:
  - inserted `Task :: Hi team , 400765 - FR ticket please take it over Thank you!`
  - inserted `Issue :: Hello @126860465827919, c'est une bonne version meme si elle est un peu longue...`
  - updated `Bigblue`
  - updated `Klaviyo`
  - updated `Meta for Business`
  - updated `Klaviyo` again
- This proves the commit path is not yet governed by the promotion review decision.

Quality risks already visible in KG:
- `commerce_order` contains noisy labels such as `-bottom-style`, `-collapse`, `-left`, `-radius`, `-width`, `Order`, `est`, `s`.
- `decision` and `issue` entries include raw message fragments and HTML-ish text.
- Some task/issue writes are raw conversation snippets, not consolidated durable facts.

## Step-By-Step Backlog

### Step 1 - Lock promotion-gated KG commits

Status: implemented and live-validated on 2026-05-08.

Goal: make promotion review authoritative before durable KG writes.

Required changes:
- Build a filtered graph candidate from promotion review output.
- Commit only:
  - `already_known` updates when the matched durable entity is stable.
  - `promote` candidates.
  - explicitly safe non-sensitive updates.
- Do not commit `review`, `reject`, or event-only candidates.
- If filtered candidate is empty, skip commit and record `kg_commit_skipped_no_promotable_candidates`.

Acceptance:
- A run with `promote_count=0` must not insert new task/issue/order/decision entities.
- Summary must show candidate counts, filtered counts, commit counts, and skip reason.
- Strict KG validation still runs after every non-empty commit.

Validation evidence:
- Historical polluting candidate `Task :: Hi team , 400765 - FR ticket please take it over Thank you!` now returns `kg_commit_skipped_no_promotable_candidates`.
- The filtered candidate has `included_entity_count=0`, `blocked_entity_count=1`.
- KG SHA stayed unchanged during the validation replay.
- Normal Jack-X DB analysis still reports `status=ok`, with memory projection publish and final projection publish both `ok`.

### Step 2 - Publish P1/P2 review backlog to MM predictably

Status: implemented and live-validated on 2026-05-08 via the governed MM memory snapshot surface.

Goal: close the local-to-MM review bridge without flooding MM.

Implemented changes:
- `MemoryReviewStore.pending(...)` can now filter by priority.
- `jack_x_memory_projection.py` now selects a bounded review front:
  - P0 max 5.
  - P1 max 25.
  - P2 max 25.
  - P3 max 0 by default.
  - total review front max 50.
- The projection now emits `open_review_summary` and `projection_policy.review_selection`.
- `jack_x_db_analysis_cycle.py` now publishes that bounded review front during its normal memory snapshot publish.
- The older `/missions` review sync remains deferred; this step uses `/memory/snapshot` as the governed source for MM memory review visibility.

Validation evidence:
- Local targeted tests: `13 passed`.
- VPS targeted tests: `13 passed`.
- VPS projection build selected exactly `50` reviews:
  - `P1`: `25`
  - `P2`: `25`
  - `P3`: `0`
- VPS publish validation run:
  - run root: `/home/ubuntu/.openclaw/workspace-jack-x/logs/cron/step2-publish-validation-20260508T145338Z`
  - cycle status: `ok`
  - channel count: `0`
  - processed channel count: `0`
  - memory projection publish: `ok`
  - final memory projection publish: `ok`
- MM `/memory/reviews` before publish:
  - total: `43`
  - `P1`: `33`
  - `P2`: `10`
- MM `/memory/reviews` after publish:
  - total: `68`
  - `P1`: `38`
  - `P2`: `30`
  - `P3`: `0`
- Diff check:
  - projected reviews present in MM: `50/50`
  - projected reviews missing from MM: `0`
  - MM extra persisted reviews outside the current projection front: `18`

Open caveat:
- MM currently appears to expose the union of the current snapshot front plus persisted pending reviews, not only the latest 50 projected reviews. This is acceptable for Step 2 because all projected P1/P2 reviews are present and P3 is excluded, but it should stay visible during Step 3 decision consumption.

### Step 3 - Consume MM decisions into Jack-X actions

Status: implemented and live-validated on 2026-05-08 for the no-terminal-decision path; approved-review mutation is unit-tested and ready for the first real MM approval.

Goal: turn review decisions into deterministic memory mutations.

Implemented changes:
- Map MM statuses to local statuses:
  - approved -> approved.
  - accepted -> approved.
  - rejected -> rejected.
  - needs_iteration -> needs_iteration.
  - superseded -> superseded.
- `MemoryReviewStore.resolve(...)` now records previous status and whether the status actually changed.
- For a newly approved review, Jack-X now:
  - builds a reviewed `brm.graph-candidate.v1`.
  - writes it under `~/.openclaw/workspace-jack-x/runtime/memory-review-actions/...`.
  - commits it through `brm-shared-graph.py commit-candidate --actor-agent-id jack-x --apply`.
- Approved reviews are idempotent: already-consumed approvals do not recommit.
- For rejected/superseded reviews, do not mutate KG; record resolution trail.
- For needs_iteration, keep the review resolved to `needs_iteration`; no KG mutation.

Validation evidence:
- Local targeted tests: `16 passed`.
- VPS targeted tests: `16 passed`.
- Dry-run against live MM memory reviews:
  - path: `/home/ubuntu/.openclaw/workspace-jack-x/logs/cron/step3-sync-dry-run-20260508T150044Z.json`
  - source status: `ok`
  - terminal statuses seen: none
  - updated count: `0`
  - action count: `0`
  - applied action count: `0`
- VPS cycle validation:
  - path: `/home/ubuntu/.openclaw/workspace-jack-x/logs/cron/step3-cycle-validation-20260508T150101Z/db-analysis-summary.json`
  - status: `ok`
  - channel count: `0`
  - processed channel count: `0`
  - resolution sync status: `ok`
  - resolution updated count: `0`
  - resolution action count: `0`
  - memory projection publish: `ok`
  - final memory projection publish: `ok`

Open caveat:
- There is not yet a real operator-approved MM memory review in production. The approved mutation path is covered by unit tests and will need one supervised real approval to close the live mutation proof.

### Step 4 - Ingest LLM Wiki refinement operations into review DB

Status: implemented and live-validated on 2026-05-08.

Goal: make LLM Wiki refinements actionable instead of passive manifest items.

Implemented changes:
- Read `latest.json` `kg_operations`.
- Insert or upsert operations with `review_required=true` as memory reviews.
- Treat `ready` operations as low-risk link confirmations only if they refer to existing entities and require no mutation.
- Preserve source page, source refs, operation id, confidence, and semantic notes.
- LLM Wiki review items use:
  - `source_agent=llm-wiki`
  - `review_type=wiki_refinement`
  - `dedup_key=memory_wiki:{operation_id}`
  - default priority `P3`, with only high-confidence strategic merge/review items eligible for `P2`.
- `jack_x_memory_wiki_cycle.py` now runs compile -> publish wiki snapshot -> upsert wiki reviews.

Validation evidence:
- Local targeted tests: `18 passed`.
- VPS targeted tests: `18 passed`.
- VPS Memory Wiki validation:
  - path: `/home/ubuntu/.openclaw/workspace-jack-x/logs/cron/step4-memory-wiki-validation-20260508T150515Z/wiki-cycle-summary.json`
  - cycle status: `ok`
  - compiled pages: `80`
  - compiled review items: `61`
  - wiki publish: `ok`
  - review upsert status: `ok`
  - review upsert count: `61`
  - inserted: `61`
  - updated: `0`
  - skipped ready/non-review ops: `19`
- Review DB before:
  - total reviews: `602`
  - `llm-wiki`: `0`
- Review DB after:
  - total reviews: `663`
  - `jack-x`: `602`
  - `llm-wiki`: `61`
  - `llm-wiki pending`: `61`
  - `llm-wiki P3`: `61`
- Post-check projection still exposes only the P1/P2 operator front:
  - projection path: `/home/ubuntu/.openclaw/workspace-jack-x/logs/cron/step4-post-projection-check-20260508T150536Z.json`
  - open review count: `50`
  - `P1`: `25`
  - `P2`: `25`
  - `P3`: `0`

Open caveat:
- The current live wiki batch produced all wiki refinements as `P3`, which is desirable for not flooding MM. A later curation pass can promote selected wiki refinements to `P2` when they are ready for operator attention.

### Step 5 - Curate existing KG noise

Status: implemented and live-validated on 2026-05-08 as a non-destructive review-gated audit.

Goal: repair already-promoted bad durable facts without silent rewrites.

Implemented changes:
- Add a KG noise audit pass for:
  - commerce order labels not matching order patterns.
  - decisions with raw HTML or long unbounded message text.
  - issues/tasks that are raw user utterances rather than consolidated facts.
- Generate review items:
  - `mark_stale`.
  - `supersede`.
  - `merge_duplicate`.
- All generated cleanup actions are `P3` reviews with `review_type=kg_noise_cleanup`.
- No destructive KG edit occurs in this pass.
- `jack_x_db_analysis_cycle.py` now runs the audit and upserts cleanup reviews idempotently.

Validation evidence:
- Local targeted tests: `21 passed`.
- VPS targeted tests: `21 passed`.
- Standalone KG noise audit:
  - path: `/home/ubuntu/.openclaw/workspace-jack-x/logs/cron/step5-kg-noise-audit-20260508T150931Z.json`
  - candidate count: `8`
  - actions:
    - `mark_stale`: `6`
    - `supersede`: `2`
  - entity types:
    - `commerce_order`: `6`
    - `decision`: `1`
    - `task`: `1`
  - review upsert: `ok`
  - inserted: `8`
  - updated: `0`
- Review DB before:
  - total reviews: `663`
  - `kg_noise_cleanup`: `0`
- Review DB after:
  - total reviews: `671`
  - `kg_noise_cleanup`: `8`
  - cleanup priority: `P3`
- Integrated cycle validation:
  - path: `/home/ubuntu/.openclaw/workspace-jack-x/logs/cron/step5-cycle-validation-20260508T150950Z/db-analysis-summary.json`
  - status: `ok`
  - channel count: `0`
  - processed channel count: `0`
  - audit candidates: `8`
  - inserted on rerun: `0`
  - updated on rerun: `8`
  - memory projection publish: `ok`
  - final memory projection publish: `ok`

Open caveat:
- Approved cleanup mutation is intentionally not automatic yet. Cleanup reviews are now visible in the review store; a separate reviewed KG cleanup mutation path should apply approved `mark_stale`, `supersede`, or `merge_duplicate` decisions.

### Step 6 - Add memory lifecycle health report

Status: implemented and live-validated on 2026-05-08.

Goal: make production readiness observable at a glance.

Implemented fields:
- event processing count.
- KG entry counts.
- latest commit counts by result.
- local review counts by status/type/priority.
- MM review counts by status/type/priority.
- LLM Wiki pages, operations, review items, semantic warnings.
- lifecycle status:
  - `complete` only when all bridges work.
  - `degraded` when auth/publish/review sync fails.
  - `partial` when local runs work but MM or curation loop is open.

Validation evidence:
- Local targeted tests: `24 passed`.
- VPS targeted tests: `24 passed`.
- VPS health report:
  - path: `/home/ubuntu/.openclaw/workspace-jack-x/logs/cron/memory-lifecycle-health-20260508T151245Z.json`
  - lifecycle status: `partial`
  - caveats:
    - no real approved memory review has been consumed yet
    - pending memory reviews remain open during supervised production
  - event total: `7104`
  - event unprocessed: `0`
  - KG entries: `244`
  - KG entities: `150`
  - KG relations: `94`
  - local reviews: `671`
  - local review types:
    - `identity_merge`: `103`
    - `kg_candidate`: `293`
    - `kg_noise_cleanup`: `8`
    - `uncertain_relation`: `206`
    - `wiki_refinement`: `61`
  - local priorities:
    - `P1`: `103`
    - `P2`: `108`
    - `P3`: `460`
  - MM reviews: `68`
  - MM priorities:
    - `P1`: `38`
    - `P2`: `30`
  - Wiki:
    - pages: `80`
    - KG operations: `80`
    - review items: `61`

Current interpretation:
- The memory lifecycle is no longer broken: event ingestion, projection, MM auth, MM publishing, MM decision consumption, wiki refinement ingestion, and cleanup review generation all run.
- It is not yet `complete` because the approved-review mutation path still needs one supervised real operator approval to prove live KG mutation end-to-end.

### Step 7 - Add Memory Curator evidence expansion and reversible KG correction

Status: implemented and locally validated on 2026-05-10; not deployed or applied to the live KG in this pass.

Goal: close the gap between raw Jack-X observations and slow LLM Wiki refinement without making LLM Wiki the mutation owner.

Role split:
- Jack-X observes channels, stores events, creates memory reviews, and keeps the local review workflow current.
- Memory Curator investigates ambiguous reviews, searches local evidence, optionally adds external search evidence, proposes clean durable entities, and can apply strong/reversible KG candidates through the shared graph bridge.
- LLM Wiki remains a read/consolidation surface: it compiles readable pages and low-priority refinement operations from the durable KG and channel artifacts.
- KG remains the durable truth. `memory_reviews.db` remains workflow truth.

Implemented changes:
- Add `scripts/jack_x_memory_curator.py`.
- Add `memory-curator` as an allowed shared-graph commit actor.
- Add durable `business_event` entity support to:
  - KG ontology v2.
  - shared graph strict validator.
  - semantic memory page eligibility.
  - LLM Wiki page routing.
- Curator CLI:
  - `curate --limit N` reads pending reviews and writes dossiers.
  - no mutation without `--apply`.
  - `--external-evidence-file` can inject reviewed browser/mail/search evidence.
  - `--allow-external-search` can use Brave only when `BRAVE_API_KEY` exists.
- Dossiers include:
  - search terms.
  - event/review/KG/wiki/external evidence hits.
  - entity hypotheses with confidence basis.
  - reversible corrections.
  - optional `brm.graph-candidate.v1`.
- Strong composite sender example is handled as:
  - `Patrick Philip Via Docusign` -> person `Patrick Philip`.
  - application `Docusign`.
  - business event `Business event :: Patrick Philip Via Docusign`.
  - relation `business_event uses application`.
  - relation `business_event mentions person`.
  - relation `person related_to application`.
- Existing composite KG entities can be superseded instead of silently deleted.
- Runtime noise such as `go`/`ok` is auto-archived as non-KG material.

Validation evidence:
- Local curator tests: `4 passed`.
- Existing Hermes memory tests: `21 passed`.
- Openclaw graph/wiki/semantic tests: `10 passed`.
- Python compile passed for:
  - `scripts/jack_x_memory_curator.py`.
  - `brm-shared-graph.py`.
  - `jack_x_semantic_memory.py`.
  - `jack-x-memory-wiki-compile.py`.
- JSON parse passed for:
  - `contracts/brm-kg-ontology.v2.json`.
  - `shared-graph-write-policy.json`.
- Real local dry-run against pending reviews:
  - review count: `5`.
  - recommendation counts: `needs_more_evidence: 5`.
  - apply: `false`.
  - result: no KG candidate emitted, so no over-promotion.
- Synthetic strong-evidence KG bridge dry-run:
  - candidate valid: `true`.
  - actor: `memory-curator`.
  - apply: `false`.
  - entities accepted: `Patrick Philip`, `Docusign`, `Business event :: Patrick Philip Via Docusign`.
  - relations accepted: `uses`, `mentions`, `related_to`.

Open caveats:
- This is locally implemented only; no service restart, deploy, push, or live `--apply` occurred in this pass.
- A supervised real approval/apply run is still required to validate live KG mutation end-to-end.
- External evidence remains optional and explicit; internal sensitive relations still need internal proof.
- The curator does not yet run on a schedule. It is an operator/Jack-X callable stage until deployment is handled by the integrator lane.

## Current Priority Order

1. Step 1: promotion-gated commits. This prevents further KG pollution.
2. Step 2: P1/P2 review publishing. This makes the backlog actionable in MM.
3. Step 3: decision consumption. This closes the review loop.
4. Step 4: LLM Wiki refinement ingestion. This makes slow consolidation useful.
5. Step 5: KG cleanup. This repairs existing noise.
6. Step 6: health report. This makes supervised production measurable.
7. Step 7: Memory Curator evidence expansion. This makes ambiguous reviews improve over time without giving LLM Wiki write ownership.

## Current Business Readiness

Ready:
- Event capture and processing.
- Local KG/projection generation.
- MM auth and memory publish.
- LLM Wiki compile and publish.
- Basic review creation.
- Local Memory Curator dossier and KG-candidate generation.

Partial:
- Review backlog exposure to MM.
- LLM Wiki operation feedback into Jack-X.
- Decision-to-KG application.
- Curative cleanup of noisy durable entries.
- Memory Curator live apply/deploy/schedule.

Not ready:
- Claiming the memory lifecycle is complete.
- Letting Jack-X auto-commit all durable KG candidates without promotion filtering.
- Treating MM review count as the full backlog; it is only the P1/P2 visible slice today.
- Treating LLM Wiki as a KG writer; it remains consolidation/read-model unless a future protocol explicitly changes that.
