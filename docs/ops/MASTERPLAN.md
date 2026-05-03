# BRM Hermes Master Plan

Last updated: `2026-05-03`

## Current Canonical Orchestration Plan

The active orchestration plan now lives in:

- `docs/ops/ORCHESTRATION_UNIFIED_PLAN.md`

This master plan remains the long-term migration document. If an older section below conflicts with `ORCHESTRATION_UNIFIED_PLAN.md`, the unified orchestration plan is the current execution truth.

Current architecture priority:

- unify Hermes, BRM Harness, Mission Manager, scheduler, protocols, subagents, Jack X, Mnemos, and Hippocampus around a canonical `WorkflowRun` / `AgentRunEvent` ledger
- replace hard keyword-first Jack routing with Hippocampus KG/protocol/MM-first preprocessing
- keep Jack bounded through typed execution modes instead of blanket tool locks
- close the protocol lifecycle from missing protocol to draft runtime, validation, promotion, monitoring, and autoloop feedback
- converge the live runtime code path toward `hermes-runtime` so Hermes owns process, state, bridges, hooks, and route execution
- keep `hermes-runtime` as a standalone production repo, not a deploy-only working tree

## Objective

Replace `OpenClaw` as the active runtime with a BRM-controlled system:

- `Hermes` for runtime execution
- `BRM Harness` for protocol enforcement, anti-variance, memory policy, and validation
- `Mission Manager` for supervised operator workflow
- `Messenger ingress` for real-world input channels

Target outcome:

- no active dependence on `OpenClaw` for runtime orchestration
- no silent model/timeout drift
- no fake `done`
- no channel ingress without BRM gates

## Strategic Decision

`OpenClaw` is no longer the target runtime.

It remains useful only as:

- script archive
- protocol archive
- migration shim layer
- legacy channel reference

Rule from now on:

- no new runtime capability should be added to `OpenClaw` unless it directly helps the migration
- new execution truth must land in `Hermes + BRM Harness`

Current runtime-consolidation order:
1. freeze the migration contract and parity gates
2. extract central bridges into `hermes-runtime`
3. reroute Hermes hooks / deploy / bootstrap / validation to the Hermes bridge surface
4. normalize `hermes-runtime` as a standalone repo with its own remote and backupable provenance
5. migrate live route runners in bounded tranches
6. fail hard on remaining runtime-critical `OpenClaw` path debt

## Architecture Target

### Hermes owns

- model/provider runtime
- sessions and transcripts
- tool execution
- profile-local memory
- messaging/webhook runtime
- transport and agent execution substrate

### BRM owns

- protocol definitions
- protocol packages
- launch gates and stage gates
- anti-variance rules
- mission status rules
- runtime observation and validation
- shared graph memory
- operator truth

### Mission Manager owns

- supervised mission lifecycle
- operator visibility
- backlog / todo / in_progress / review / blocked / done state
- attachments and deliverable routing

### Messenger owns

- inbound operator/customer/team signal
- never business truth by itself
- always routed through BRM intake and mission rules

## Non-Negotiables

- `protocol first`
- `script first`
- `production truth first`
- `route before tool`
- `no business tool call before environment + route classification`
- `no mutable governed route without a plan artifact`
- `no fake done`
- `no silent override`
- `no hidden blocker`
- `no secret leakage`
- `no agent chooses its own model or timeout on a governed route`
- `no specialist work is silently absorbed by Jack when a governed specialist route exists`
- `no browser-or-shell first on backend-owned business routes`

## Current State

### Already closed enough to build on

- `jack` local supervised Hermes runtime
- `jack-x` local supervised Hermes runtime
- `jack-x` first structured reporting layer:
  - every bounded memory-update slice now emits a machine-readable `channel report`
  - a macro `worldstate consolidator` now surfaces actual missing KG contract families from observed intake outputs
  - every canonical Hermes cycle now appends a `worldstate_consolidate` post-step artifact on the VPS
  - current contracted floor on the VPS now closes the first durable extension slice:
    - `channel`
    - `operation`
    - `product`
    - `reported_in`
    - `mentions`
  - latest consolidated worldstate on the live VPS shows `missing_durable_entity_types = []` and `missing_durable_relation_types = []` for the current floor
  - the canonical weekend floor was re-run on `2026-04-12` and left back on Hermes timers with the scheduler state green again after clearing a temporary validation-time lock collision
- `rosa` first direct route
- `jeff` first two direct routes
- `alfred` reviewed-bundle route
- `naya` first wave plus live stock pilot
- `selena` artifact-fed PayPal and Zendesk routes
- `tony` exploration / plan / development split runtime
- Mission Manager hosted mutation gates
- Mission Manager first canonical workflow ledger slice:
  - `workflow_runs` and `agent_run_events`
  - API surface for run/event creation, lookup, and update
  - recurring runtime reports auto-mirrored into workflow runs
  - Live view now prefers canonical workflow events for mirrored recurring reports
  - production E2E proof on `jack-x.db-analysis` at `2026-04-22T23:48:26Z`
  - direct specialist chat now creates lineage-bound child runs with `parent_run_id` on the live floor
  - first cost truth layer now exists:
    - `billing_mode`
    - `cost_status`
    - `cost_source`
  - Mission Manager now has a visible `Costs` surface for LLM run usage and cost coverage
  - cost semantics are now separated enough to operate on:
    - `subscription-handled`
    - `out-of-subscription llm`
    - `external_tool_costs`
    - `operational / synthetic excluded`
- shared graph normalization and governed write path
- centralized local credential pattern:
  - `auth-profiles.json`
  - `~/.brm-hermes/.env`
  - `~/.brm-hermes/credentials/`
- first Hermes WhatsApp VPS cutover:
  - runtime deployed on `54.76.101.182`
  - paired session stored in `HERMES_HOME`
  - Hermes systemd gateway active
  - legacy OpenClaw gateway service disabled
  - root/profile runtime ambiguity on the VPS is now hardened:
    - live state is explicitly profile-backed
    - legacy root state is archived out of the audit path
    - `/status` now exposes active gateway home, session store, channel directory, and WhatsApp mode
- specialist direct chat runtime now has a real floor, not just a prompt overlay:
  - bound sessions now isolate `user + agent`
  - active specialists now run profile-backed Hermes runtimes
  - `/jack` and `/specialist <agent>` now rebind to real agent sessions instead of sharing one mixed transcript
- first bounded work-policy floor is live across the active specialist runtime:
  - `extraction`
  - `reasoning`
  - `action`
  - `follow_up`
  - `/status` now exposes the default work type plus the effective model lanes behind it
- current provider floor is materially usable on the live runtime:
  - `zai`
  - `kimi-coding`
  - `anthropic`
  - `openai-codex` for text lanes
  - `openai` direct for image lanes
  - `higgsfield`
- Hermes recurring cutover for `jack` and `jack-x`:
  - canonical manifest:
    - `/Users/moufdi/hermes-runtime/contracts/hermes-recurring-jobs.v1.json`
- `jack.email-digest` now runs on Hermes cron (`4` jobs)
- Hermes cron delivery now has a production-grade transport floor:
  - structured `delivery.targets`
  - multi-target WhatsApp fan-out
  - persisted delivery receipts
  - backward-compatible legacy `deliver`
- `jack.email-digest` WhatsApp delivery is now proven end-to-end on the VPS, and the digest prompt has been upgraded from a dry audit template to an operator-grade WhatsApp digest built from curated support / follow-up / finance / archive slices:
    - first failure exposed bad executor paths (`/Users/moufdi/...`)
    - second failure exposed unstable nested `response_mode`
    - final fix is a stable top-level `response_preview` contract plus Linux-stable executor paths
  - `jack-x` recurring floor now runs on Hermes cron through the current canonical manifest:
    - `4` `jack-x.registry-ingest` jobs
    - `4` `jack-x.db-analysis` jobs
  - legacy `/etc/cron.d/agent-mission-loop` ownership for `jack-x` is explicitly disabled
  - `mnemos` remains intentionally `trigger_only` until a real cadence is defined
  - supervised specialist ingress now pre-routes before runtime execution, so `Jack` can stay manager / dispatcheur while the owned specialist route executes
- first audited `WhatsApp -> Hermes -> MM -> specialist -> Drive` proof:
  - inbound message created governed MM missions
  - specialist dispatch stayed owned by `Rosa`
  - deliverables landed on Drive and were attached in MM
  - mission/file traceability now carries creation metadata plus `mission_id` and `run_id`
- first Jack capability-bank proof on the live VPS:
  - machine-readable healthcheck registry exists
  - machine-readable runner exists
  - `33/33` capabilities now have an explicit smoke strategy
  - latest VPS pass is `31 OK / 2 FAIL / 0 SKIP`
  - remaining red auth surfaces are currently limited to:
    - `Cloudflare`
    - `GoDaddy`
- first Jack action-governance slice on the live VPS:
  - action classes, scope profiles, and route action overlays now exist
  - a local role/permissions registry exists and can be edited through a governed Jack route
  - plan mode now explicitly allows local scratch work without silently allowing external side effects
- first MM operator snapshot layer:
  - canonical `Deliverables`, `Drive`, and `Integrations` snapshots now build from live MM + Drive + registry truth
  - the data layer is live locally and on `jack-vps`
  - the snapshot already surfaces the next real gap:
    - the non-empty `Deliverables` view stays empty until route pilots attach real `mission files` back into MM
    - the live blocker is now precise:
      - `jack-vps` has no valid Google Drive user OAuth credential scoped for Drive
      - the readable credential is a service account that can see `DRIVE AGENTS` but cannot publish official files there because it hits the service-account quota limitation
- first usable Kanye creative generation floor is now closed enough to build on:
  - `generation_policy` is live on the `kanye` profile
  - still-image routing now supports:
    - `Nano Banana 2`
    - `GPT Image 2`
    - `Higgsfield` still generation
  - motion generation now supports `Higgsfield / Seedance`
  - still-image reference forwarding is now validated locally and on the VPS for:
    - `Nano Banana 2`
    - `GPT Image 2`
  - image generation is now considered usable as a bounded specialist capability, even though route closeout and tuning remain open
  - reference-image forwarding is now validated on the VPS for:
    - `Nano Banana 2`
    - `GPT Image 2`
  - the surface is considered `usable` for bounded creative generation, not fully industrialized
- first upstream optional-skill adoption target is now identified for toolbox standardization:
  - Hermes optional skill:
    - `optional-skills/productivity/shopify/SKILL.md`
  - role in the next wave:
    - standardized Shopify Admin/Storefront GraphQL capability
    - commerce toolbox surface for product, inventory, order, customer, and metafield routes
  - status:
    - first standardization slice is now closed around the existing `clawd/skills/shopify-stores/scripts/shopify.py` backend
    - production contract now includes:
      - `clawd/skills/shopify-stores/stores.json` is the source of truth for tenant/auth resolution
      - Hermes capability registry now references that source instead of duplicating tenant lists
      - Hermes readiness/audit visibility for all declared Shopify tenants, with `shared_env_presence_only` made explicit
      - live-read proof validated on the VPS for:
        - `maybe-paris` admin read
        - `us-maybe-paris` admin read via `client_credentials`
        - `maybe-paris` theme read
    - current live tenant set is `7` stores
    - residuals remain explicit:
      - `blinx-us` auth declared but not ready
      - `nailz` brand metadata still references a `store_key` absent from `stores.json`
- first Safir route-backed closeout slice is now closed enough to build on:
  - canonical package root now exists under `hermes-runtime/adapters/agents/safir/packages`
  - first live canonical routes now exist:
    - `safir.email-audit`
    - `safir.mail-pole-audit`
  - both routes are live on `executor.kind=command`
  - both routes were smoke-validated on the VPS in render-only mode on `2026-05-02`
  - explicit residual:
    - `email-workflow` remains open and intentionally out of this closeout slice

### Not closed yet

- `jack` mission-digest remains unclosed as a live MM-backed route; the operator email digest is now a separate live cron surface on explicit `zai/glm-5.1`, and must stay distinct from the Jack X memorization protocol
- `jack-x` per-channel worker model is not closed yet:
  - channel reports exist
  - macro consolidation exists
  - the email slice now covers `MS365 inbox + sent`
  - the mail tooling surface now supports:
    - bulk search
    - bounded search by folder/date/read-state
    - targeted extraction with body / headers / attachment metadata
  - sender classification on the email slice is now bounded:
    - `person`
    - `organization`
    - `store sender`
    - `system sender`
  - `application` / `domain` extraction is live, and sent-recipient correspondents now flow through the same review-gated policy, but durable promotion must stay policy-gated
  - scheduler/runtime still need to move from source-family slices to true per-channel worker truth
- durable shared-graph taxonomy extension beyond the first closed slice is not closed yet and must follow observed channel-report evidence, not prompt intuition:
  - first closed slice:
    - `channel`
    - `operation`
    - `product`
    - `reported_in`
    - `mentions`
  - still open:
    - `issue`
    - `task`
- `cortex` wider route surface beyond the closed Phase 1 path
- `hermes -> mm` final bridge for direct sessions, child runs, approvals, validation results, protocol stages, and KG commit events
- Mission Manager cost truth is not fully closed yet:
  - LLM and external tool costs are now separated and visible
  - `subscription-handled` vs `out-of-subscription` semantics are now explicit
  - remaining gap is pricing contract quality for `unknown` / `credit-based` providers, not the absence of a cost surface
- toolbox standardization is not closed yet:
  - some routes still rely on local custom surfaces where a governed standardization pass is still needed
  - the first Shopify commerce slice is now closed around the live `shopify-stores` backend
  - the next work is broader route ownership and adjacent tooling standardization, not Shopify floor discovery
  - explicit residuals on the current floor are:
    - `blinx-us` auth not ready
    - `nailz` still references a missing `store_key`
  - the next implementation order is:
    - the MM reflection closeout slice so the cockpit keeps reflecting canonical specialist truth across dashboard / org / member / mission surfaces without heuristic drift
    - the MM frontend slice for `mission_tasks / mission_task_events / next_check_at`, now that the first backend substrate is live
    - broader commerce route ownership after the Shopify floor, including explicit treatment of draft brands like `nailz`
- `drive + mm + channels` ecosystem wave
- MM operator truth beyond the data layer:
  - the snapshot layer exists
  - the non-empty `Deliverables` view is still not truthful on the live floor because `mission files` attachment is not generalized yet
- `lark`-backed ops route closeout inside the v1 perimeter
- remaining partially validated business integrations
- remaining red auth in the Jack capability bank:
  - `Cloudflare`
  - `GoDaddy`
- remaining materially unclosed agent surfaces:
  - `mnemos` first route is now packaged on Hermes as a `trigger_only` technical surface; real-session VPS sweeps are green, forced `compact_now` and `handoff_required` proofs are green on a real Jack session, and artifact collision was fixed; only a natural live high-saturation Jack turn remains unobserved
  - `jhin` remains an internal visual capability, not an exposed specialist closeout target
  - `kanye` now has a first governed creative route floor:
    - `kanye.still-generate`
    - `kanye.reference-edit`
    - both are canonical `executor.kind=command` routes with green local tests, VPS dispatch replay, and real VPS smoke proof
    - delivery hardening, MM lineage, tuning, and wider motion coverage remain open
  - `safir` now has a first canonical route-backed mail floor, but is not yet fully industrialized:
    - `safir.email-audit` and `safir.mail-pole-audit` are now validated on the VPS as render-only canonical routes
    - `email-workflow` remains open
  - `walter` stays draft
- the mission-autonomy substrate is now partially live:
  - backend MM truth exists for:
    - `mission_tasks`
    - `mission_task_events`
    - derived `mission.next_check_at`
  - first live CRUD/API proof is green on prod
  - UI reflection, operator wake-loop ownership, and Hermes follow-up execution are still open
- the specialist route registry now has a first canonical executor contract:
  - `executor.kind` is live
  - the registry uses portable `~/...` paths and the dispatch bridge expands them per host
  - live route coverage is currently closed for `command`; `specialist_runtime`, `api_pipeline`, and `comfyui` remain future route kinds
- Mission Manager reflection is now materially live enough to build on:
  - Capabilities and Live now project:
    - `executor.kind`
    - `dispatch_mode`
    - route contracts
    - specialist runtime bindings
  - Dashboard, Org Chart, Member Profile, Member Dialog, Project Board, Mission Card, and Mission Dialog now surface canonical specialist signals:
    - `route-backed` vs `profile-backed`
    - `registry_stage`
    - `profile`
    - `work_surface`
    - route / protocol counts
  - hardening closed on this slice:
    - `agent.member`-aware binding in the MM frontend projection layer
    - specialist metadata cleanup in member editing
    - richer canonical summary rendering
    - mobile mission-card visibility for specialist signals
    - Member Profile mission creation now locks assignee by context instead of exposing a fake reassignment path
  - remaining MM reflection residuals are now narrow:
    - some surfaces still summarize protocol truth too lightly
    - broader lineage/event projection remains a backend/MM ledger problem, not a frontend discovery problem

## Immediate Next Wave

The current next wave should stay narrow:

1. keep repo/VPS/runtime truth stable before widening coverage
   - local worktrees remain the canonical code truth
   - VPS checkouts remain deploy mirrors and must not drift on route packages, tests, or docs
   - current exact drift snapshot:
     - VPS `openclaw` worktree is heavily dirty
     - VPS `clawd` worktree is heavily dirty
     - VPS `hermes-runtime` is deployed as a working tree, not a clean git checkout
   - no phase is considered closed unless:
     - local targeted tests are green
     - the same critical test slice replays on the VPS when the checkout actually contains that slice
     - live service restart is green when runtime-bearing files changed
     - operator confirmation is sent over the real Jack WhatsApp bridge
2. keep specialist/MM lineage hardening on the same ledger
   - approvals
   - protocol stages
   - validation results
   - KG commit events
3. finish the remaining Mission Manager reflection residuals before autonomy schema
   - the first two MM reflection slices are now live:
     - runtime/API alignment across `Capabilities`, `Live`, and workflow-facing surfaces
     - canonical specialist projection across dashboard / org / member / mission surfaces
   - keep the residual slice narrow:
     - fuller protocol/capability summary on the remaining views
     - stronger direct use of canonical member linkage where the registry already knows the member
4. open the mission-autonomy substrate only after the MM runtime/API contract is explicit enough
   - current exact floor:
     - `workflow_runs` and `agent_run_events` exist
     - `recurring_tasks` and `recurring_task_events` exist
     - `mission_tasks` and `mission_task_events` now exist on the MM backend
     - `next_check_at` is now derived on the mission read model from open mission tasks
   - first slice must stay narrow:
     - create/update task truth
     - event trail
     - dedicated task API surface
     - no live/activity pollution
   - next slice remains:
     - one-shot wake path
     - no self-improving autoloop
5. keep commerce/toolbox work on the already-closed Shopify floor
   - do not build a second Shopify executor
   - current exact residuals:
     - `blinx-us` auth not ready
     - `nailz` still references a `store_key` absent from `stores.json`
     - route ownership and production smoke coverage remain the next real work, not floor discovery
   - next commerce work is route ownership and metadata/auth cleanup, not Shopify floor discovery

### Parallel Execution Discipline

Every phase after this point should use the same operating pattern:

1. `read-only audit wave`
   - launch bounded explorer subagents in parallel
   - one subagent per axis (`route closeout`, `autonomy substrate`, `toolbox/auth`, `repo/VPS drift`)
   - the parent agent consolidates and decides sequence
2. `single-owner implementation wave`
   - one writing owner per canonical file surface
   - helper subagents stay read-only or prepare tests only
   - do not allow two writers on the same registry or protocol surface
3. `regression wave`
   - one dedicated regression subagent or parent-owned pass replays:
     - local targeted tests
     - VPS targeted tests
     - live smoke when applicable
   - phase stays open until the regression wave is green
4. `repo/VPS truth gate`
   - local repos remain the only canonical code truth
   - VPS checkouts are deploy mirrors plus live runtime state, not authoring truth
   - each phase must declare:
     - synced file set
     - restart requirements
     - the exact VPS-replayable test slice
   - no phase is counted closed without:
     - local tests green
     - VPS replay green on the synced slice
     - service restart green when runtime-bearing files changed
     - operator confirmation over the real Jack WhatsApp bridge

This keeps subagents useful without creating parallel truths or conflicting edits.

The exact next execution order is now:

1. `Mission autonomy truth gate`
   - freeze:
     - `engagement_mode`
     - `outcome_type`
     - `data_check_report`
     - `curator_signals`
   - keep one canonical semantic split:
     - `direct_discussion`
     - `extraction`
     - `governed_route`
2. `Mission autonomy MM contract + review workspace`
   - encode the split above on `mission_task`
   - make review the primary operator surface
3. `Mission autonomy runtime outcome normalization`
   - keep the live wake-loop route-backed only
   - attach `data_check_report` and curator-ready signals to task events / workflow runs
4. `Shopify residuals` as parallel audit/readiness
5. `deploy/test normalization` as a transverse hardening lane across every slice
- specialist child-run lineage is still not unified end-to-end into the MM workflow ledger:
  - direct specialist chat is real
  - bounded runtime context is real
  - but specialist child runs, approvals, protocol stages, and validation results are still not all canonical `AgentRunEvent`s
- final OpenClaw runtime retirement

Current perimeter decision:

- `Telegram` is explicitly deferred from the `v1` closeout perimeter
- `WhatsApp` stays in-scope for `v1`
- `Lark` stays in-scope for `v1`
- `Mnemos` is in-scope as a technical trigger surface, not as an MM-triggered operator route
- the governed `jack` runtime now compacts at `60%` with a `Mnemos` continuity capsule layered on top of Hermes native compaction

Operator rule for the remaining channel migration:

- `Jack` owns transversal coordination, protocol co-design, governance fallback, and dispatch
- specialist agents own execution on their governed routes

## Operating Insights From The Current Wave

These are now design rules, not just observations.

### Fix Jack with runtime discipline, not robotic language

- the main failures came from:
  - unresolved route reuse
  - terminal over-freedom
  - scope inflation after the first useful step
- the right fix is not a more bureaucratic tone
- the right fix is:
  - route resolution
  - action-class governance
  - scope-aware tool exposure
  - better separation between local scratch and external side effects

### Production Readiness Depends On Separating Discovery From Execution

- the current protocol feedback is valid:
  - some routes feel rigid because they are entered too early
- the correct response is not to soften governed routes blindly
- the correct response is to keep one explicit split:
  - `direct_discussion`
    - broad, tool-bounded exploration
    - clarification, comparison, draft preparation
  - `extraction`
    - structured collection and pre-analysis
    - no business `done` by itself
  - `governed_route`
    - mutation, deliverable, validation, safety-sensitive execution
- Curator must later optimize this boundary:
  - when discussion should stay discussion
  - when extraction should precede protocol
  - when repeated discussion deserves protocol promotion
  - when a governed route is being applied too early

### Plan mode must stay productive, but only locally

- plan mode should allow:
  - local notes
  - HTML/PDF/report drafts
  - intermediate files
  - structured artifacts
- plan mode should not silently allow:
  - business mutations
  - Drive publication
  - archiving / deletion
  - external sends
  - tooling/codebase mutation
- this is the practical middle ground between chaos and bureaucracy

### Stable ecosystem context should be always available before live reads

- Jack should not have to rediscover the ecosystem on every turn
- brand workspace cards, the global ecosystem index, action governance, and role permissions are now the stable context layer
- live reads should only be used for volatile facts:
  - current theme
  - inventory
  - channel messages
  - current deliverables

### Jack X, digest, and Mnemos must stay separated

- `Jack X` = world-state intake and KG candidate production
- `jack.email-digest` = operator-facing summarization
- `Mnemos` = continuity / compaction
- these surfaces may read the same underlying signals, but they must not collapse into one mixed protocol

### MM should be the readable control plane, not the place where raw runtime state leaks

- local workspace = production
- Drive = publication
- MM = operator truth
- the new MM snapshot layer confirms the structure is right
- the next useful MM work is not more snapshot code
- the next useful MM work is making sure real route pilots attach `mission files` so the Deliverables view becomes live and useful

### Jack X should evolve toward per-channel workers, not toward a bigger generic blob

- the contracted floor is now good enough to build on
- the next Jack X step should be:
  - per-channel workers
  - per-channel state / cursor / dedup
  - macro consolidator
- it should not be:
  - uncontrolled ontology growth
  - semantic auto-promotion by prompt intuition
  - conversation-scale improvisation

## System Operating Model

- `Jack` is the transversal manager:
  - reads operator intent
  - chooses the governed route or opens `protocol-missing` / `capability-missing`
  - keeps MM honest
- `Jack X` is the bounded world-state intake layer:
  - ingests mail, chat, and ops surfaces on schedule
  - extracts objects, relations, and KG candidates
  - never becomes the source of business truth by itself
- `Mnemos` is the continuity and compaction layer:
  - checks context pressure
  - prepares continuity capsules
  - keeps long-running work from dying in the context window
- specialists own execution:
  - they run bounded protocols
  - they produce reviewable artifacts
  - they do not redefine governance

## Jack Standardization Layer

`Jack` is still under-standardized as an interactive runtime.
The next hardening wave must stop treating "better prompt text" as sufficient.

Target operating shape:

1. `preprocess`
   - classify:
     - `environment`
     - `brand`
     - `tenant`
     - `surface`
     - `route`
   - hydrate known context before tool choice
2. `plan`
   - user-facing
   - local scratch allowed, external side effects blocked
   - produces a short plan artifact on mutable, ambiguous, or multi-system work
3. `execute`
   - runs only on locked target, locked route, allowed tools, and proof target
4. `replan`
   - any contradiction, missing standard route, or missing target returns to planning or opens governance fallback

Required supporting artifacts:

- a baseline `capability registry`
- governed `brand packs`
- a `route template` library
- a `tool adapter` layer between business language and raw scripts
- an `action governance` layer:
  - action classes
  - scope profiles
  - route action overlays
  - role / permission workspace
- an `execution policy` that filters tools by route
- an `operating doctrine` that removes action-first improvisation from professional work

Reference design docs:

- [jack-standardized-runtime.md](/Users/moufdi/hermes-runtime/docs/jack-standardized-runtime.md)
- [jack-action-governance-plan.md](/Users/moufdi/hermes-runtime/docs/jack-action-governance-plan.md)
- [capability-registry-baseline.md](/Users/moufdi/hermes-runtime/docs/integrations/capability-registry-baseline.md)
- [jack-capability-bank.md](/Users/moufdi/hermes-runtime/docs/integrations/jack-capability-bank.md)

## Production-Ready Operating Contract

The target production path is now explicit:

1. `Moufdi -> Jack`
   - operator enters through a governed surface:
     - WhatsApp
     - Mission Manager
     - later approved ingress surfaces
2. `Jack -> Mission Manager`
   - Jack identifies the intended business outcome
   - checks the governed route registry and current MM/workspace truth
   - creates or updates the MM mission when the work is business-relevant
3. `Mission Manager -> specialist route`
   - MM becomes the operator spine:
     - assignment
     - status
     - dependencies
     - attachments
     - calendar / recurring work
4. `specialist -> bounded execution`
   - the specialist executes only its owned protocol
   - artifacts, logs, and blockers are written under a deterministic workspace shape
5. `specialist -> MM`
   - the run updates mission truth
   - deliverables attach to the mission
   - failure is surfaced as `blocked` or `review`, never hidden
6. `MM -> Jack -> Moufdi`
   - Jack returns a short recap
   - Jack includes the MM mission link
   - Jack includes delivery links when the route allows them

Rules:

- no business-relevant specialist execution without MM, except surfaces explicitly marked:
  - `trigger_only`
  - `internal`
  - `cron` operator digest surfaces
- a nominative ask for a specialist is a routing hint, not permission to improvise execution
- if no governed route exists, Jack must stop and open:
  - `protocol-missing` for a named specialist gap
  - `capability-missing` for a transversal business gap

## Autonomy Contract

### Jack

Jack is the assistant de direction, not a hidden freeform worker.

Allowed:

- interpret operator intent
- route to the correct protocol or specialist
- open MM missions
- ask only the minimum missing clarification needed for safe routing
- coordinate dependencies between specialists
- refuse work when the protocol floor is missing

Forbidden:

- silently absorbing specialist work that has an owned governed route
- inventing a new production process in the middle of execution
- choosing uncontrolled model/provider/timeouts for governed routes
- reporting success when the protocol truth is still `review` or `blocked`

### Specialists

Specialists are bounded production surfaces.

Allowed:

- execute owned protocol steps
- produce reviewable artifacts
- emit explicit blockers, validation results, and logs

Forbidden:

- widening their own scope
- changing process shape mid-run without protocol support
- writing durable shared memory outside the governed path
- choosing creativity where deterministic execution is expected

### Jack X

Jack X is world-state intake, not a business decision-maker.

Allowed:

- scheduled ingestion
- bounded extraction
- object/relation candidate creation
- dedup candidate generation
- KG candidate preparation

Forbidden:

- creating operator truth by itself
- mutating business mission state without the governed bridge
- becoming a second Mission Manager

### Mnemos

Mnemos is continuity and memory hygiene, not a business executor.

Allowed:

- context checks
- compaction
- continuity capsule generation
- bounded reinjection planning

Forbidden:

- inventing mission logic
- changing operator truth
- free-writing shared graph memory outside the governed candidate path

## Anti-Variance Contract

The system must default to low variance.

Rules:

- no protocol is production-ready unless its bounded execution shape is explicit
- `pass0` / extraction absorbs context-heavy collection whenever the live input would otherwise bloat the main run
- creativity is allowed only in the protocol phases marked exploratory, generative, or strategy-oriented
- the operator runtime must prefer classification and plan artifacts over first-tool impulse
- deterministic phases must prefer:
  - scripts
  - bounded tools
  - frozen artifacts
  - subagents or sidecars for heavy collection
- no phase may silently skip render, validation, or blocker emission
- a protocol must block cleanly rather than improvise around missing prerequisites

## Protocol Contract

Every production-shaped protocol must define all of the following:

- owner agent
- route id
- activation mode:
  - `on_demand`
  - `cron`
  - `dependent`
  - `trigger_only`
  - `internal`
- governance mode:
  - `mission_required`
  - `approval_gated`
  - `trigger_managed`
  - `callable`
- required inputs and prerequisites
- dependent artifacts and upstream protocols
- explicit stage flow:
  - `pass0 / extraction`
  - `analysis / planning`
  - `production / render`
  - `verification / feedback`
- allowed models, tools, and sidecars
- output contract:
  - artifact classes
  - MM updates
  - delivery rules
  - blocker rules
- validation evidence root

No route counts as production-ready if one of those fields is implicit.

## Workspace And Artifact Contract

Mission and artifact truth must stay navigable by both humans and agents.

Rules:

- each governed run must be traceable by:
  - `mission_id`
  - `route_id`
  - `run_id`
  - `stage`
- artifacts must be named so an agent can infer:
  - what they are
  - who owns them
  - when they were created
  - whether they are inputs, working files, reports, deliverables, or verification outputs
- a protocol must know when to request a refresh of an upstream artifact instead of silently using a stale document
- if another specialist or annex file is required, the dependency must be explicit in MM and/or the protocol contract
- no hidden one-off local file may become a de facto production dependency

Target workspace logic:

- MM is the operator index
- deterministic workspace paths hold the execution artifacts
- Jack reads mission truth and reviewable artifacts, not random local context
- relaunching a protocol must be an explicit governed action, not an accidental side effect of a stale workspace

## Deliverable Classes

The production system is expected to produce only reviewable classes of output:

- Mission Manager seeds and truthful mission/task transitions
- structured observation packs and audit summaries
- HTML / PDF / JSON deliverables plus Drive attachments when the route allows delivery
- execution boards, queues, and task seeds
- code/config/deployment artifacts on technical routes
- KG candidates:
  - objects
  - relations
  - confidence hints
  - continuity capsules
- protocol bundles when a governed route does not exist yet

Rule:

- a deliverable class exists only when the owning route, artifacts, and validation evidence exist together

## Harness+ Phase Model

`Harness+` must now be treated as the canonical 3-phase protocol shape:

1. `Phase 1 audit / observation`
   - intake
   - bounded extraction
   - factual diagnosis
   - mission/task seed in MM
2. `Phase 2 creation / production`
   - plan
   - asset/code/report/workboard generation
   - governed execution against the approved scope
3. `Phase 3 verification / iterative feedback loop`
   - delivery review
   - blocker detection
   - quality / performance feedback
   - explicit loop-back inputs into Phase 1 and Phase 2

Rules:

- the MM mission is the operator spine across the 3 phases
- Phase 3 is not a cosmetic “final step”; it is the control loop that reopens Phase 1 or Phase 2 when reality diverges
- no route is production-live if it skips Phase 3 on a surface where truth can drift after production
- if a channel message explicitly targets a specialist but no governed route resolves, the ingress must block or open governance work instead of letting `Jack` improvise the specialist execution

## Canonical Tracking Files

- status: [STATUS.md](/Users/moufdi/openclaw/docs/ops/STATUS.md)
- validation backlog: [HERMES_BRM_VALIDATION_BACKLOG.md](/Users/moufdi/openclaw/docs/ops/HERMES_BRM_VALIDATION_BACKLOG.md)
- collaborator handoff package: [README.md](/Users/moufdi/openclaw/docs/handoff/hermes-brm-v1/README.md)
- integration truth: [status-matrix.md](/Users/moufdi/hermes-runtime/docs/integrations/status-matrix.md)
- agent dependency map: [agent-map.md](/Users/moufdi/hermes-runtime/docs/integrations/agent-map.md)
- rollout order: [agent-channel-rollout.md](/Users/moufdi/hermes-runtime/docs/agent-channel-rollout.md)
- integration migration plan: [openclaw-to-hermes-integrations-plan.md](/Users/moufdi/hermes-runtime/docs/openclaw-to-hermes-integrations-plan.md)
- capability registry baseline: [capability-registry-baseline.md](/Users/moufdi/hermes-runtime/docs/integrations/capability-registry-baseline.md)
- Jack capability bank: [jack-capability-bank.md](/Users/moufdi/hermes-runtime/docs/integrations/jack-capability-bank.md)
- Jack standardized runtime: [jack-standardized-runtime.md](/Users/moufdi/hermes-runtime/docs/jack-standardized-runtime.md)
- codebase layout: [CODEBASE_LAYOUT.md](/Users/moufdi/openclaw/docs/ops/CODEBASE_LAYOUT.md)
- v1 architecture view: [HERMES_BRM_V1_ARCHITECTURE.md](/Users/moufdi/openclaw/docs/ops/HERMES_BRM_V1_ARCHITECTURE.md)

## Documentation And Projection Rule

Canonical local truth lives in:

- `~/openclaw/docs/ops/`
- `~/hermes-runtime/docs/`

The VPS copies under:

- `/home/ubuntu/openclaw/docs/ops/`
- `/home/ubuntu/hermes-runtime/docs/`

are projections, not an independent source of truth.

No wave may be marked closed while these files disagree:

- `MASTERPLAN.md`
- `STATUS.md`
- `HERMES_BRM_VALIDATION_BACKLOG.md`
- `status-matrix.md`
- `agent-map.md`
- `agent-channel-rollout.md`

## Master Milestones

### Milestone 1: Hermes Runtime Foundation

Status: `active / mostly closed`

Scope:

- Hermes install and isolated state
- auth centralization
- BRM protocol gates
- Jack and Jack X validation
- local brains and shared graph bridge

Exit criteria:

- `jack` and `jack-x` stable on supervised Hermes runtime
- centralized credential floor exists
- BRM protocol gate path exists
- shared graph writes are governed

Current verdict:

- functionally reached for local runtime
- still needs hard-enforcement removal of legacy inline-secret paths

### Milestone 2: Specialist Integration Floor

Status: `active`

Scope:

- close remaining live integrations needed by specialist agents
- ensure each specialist route is either:
  - live and validated
  - artifact-fed and explicitly marked
  - non-runnable

Priority order:

1. final `Hermes -> MM` bridge
2. `Jack -> MM -> subagent` handoff truth
3. first `Lark`-backed governed route
4. remaining partial business integrations:
   - `Klaviyo`
   - `Lark`
   - `Shopify` wider live scope
   - `Meta Ads`
   - `Google Ads`
   - `GA4`
   - `Recharge`
   - `Cloudflare`
   - `GoDaddy`

Exit criteria:

- no specialist depends on an undocumented or half-wired integration
- every required client/skill exists locally
- every specialist route is truthfully classified `OK / PARTIAL / ABSENT`
- no route is described as live if the credential source is still missing from canonical stores

### Milestone 3: Operator Fabric

Status: `active`

Scope:

- `Hermes -> Mission Manager` lifecycle bridge
- `Drive` delivery pattern
- `WhatsApp`
- mail intake surfaces

Current truth:

- first live `Hermes -> MM` bridge path is now proven
- first `Jack -> MM -> specialist` handoff is now proven
- first `workspace delivery -> Drive gate -> MM blocked` proof is now proven
- the canonical `workspace local -> official Drive -> MM` delivery standard is now deployed on `jack-vps`:
  - standard `manifest` and `delivery` contracts exist
  - MM bridge now consumes standardized `delivery.json` records
  - mission-manager helper resolves the local bundle path and MM Drive deliverables target
- hosted MM board clean-slate reset is now proven
- first Hermes WhatsApp production cutover is now proven technically on the VPS:
  - paired session exists
  - Hermes system service is active
  - legacy OpenClaw gateway service is disabled
- first audited `WhatsApp -> Hermes -> BRM observation -> MM -> specialist -> Drive` path is now proven
- `Telegram` is now explicitly frozen out of `v1`; no further migration work is required to close `v1`
- remaining work is ecosystem closeout, not proof existence

Order:

1. generalize the approval-gated Drive/workspace pattern beyond the first Jeff proof
2. close the broader `Hermes -> MM -> Drive -> channel reply` ecosystem
3. keep `Telegram` frozen out of `v1`, reopen it only post-`v1` if still needed
4. close the remaining mail/channel edges that still sit outside the audited path

Exit criteria:

- inbound signal can create/update a mission through BRM gates
- runtime facts reach MM without fake `done`
- operator approval remains explicit on deliveries
- channel ingress is supervised and auditable
- hosted MM board can be started from a genuinely clean mission state

### Milestone 3B: Jack Standardized Operating Layer

Status: `active`

Scope:

- publish the baseline `capability registry` across runtime, channel, business, and support surfaces
- define governed `brand packs` so a brand mention resolves to its known ecosystem instead of ad hoc reconstruction
- define `route templates` for standard business asks:
  - `check`
  - `plan`
  - `update`
  - `audit`
  - `verify`
- separate `preprocess -> plan -> execute` as an explicit runtime contract
- define `tool exposure policy` so Jack does not see every tool on every turn
- rewrite the Jack doctrine away from `action > discussion` toward `standard > impulse`

Current truth:

- machine-readable `capability registry` exists
- machine-readable `brand packs` exist for the current brands
- machine-readable `route templates` exist
- machine-readable capability smoke registry exists
- a canonical VPS capability bank is now generated from live checks:
  - latest pass: `31 OK / 2 FAIL / 0 SKIP`
  - the remaining known red auth surfaces are:
    - `Cloudflare`
    - `GoDaddy`
- the capability bank already caught and forced closure of multiple drift issues:
  - broken `mission-manager` path on the VPS
  - missing skill directories on the VPS
  - missing `GA4` credential file on the VPS
  - missing browser binary on the VPS
- Jack now has a generated always-on workspace helper:
  - `GLOBAL_ECOSYSTEM_INDEX.md`
  - per-brand workspace cards under `BRAND_WORKSPACES/`
  - these are rebuilt during deploy/bootstrap and surfaced in the live session gate
- the live gateway now exposes a compact stable workspace map when a brand resolves:
  - Shopify tenants and storefronts
  - coordination surfaces
  - major business systems

Immediate next order:

1. make `plan` a real runtime gate for:
   - mutable routes
   - ambiguous targets
   - multi-system asks
2. harden route-based tool filtering:
   - current first slice hides `browser` on backend-owned routes like `shopify.check_theme`
   - next slice must lock writes behind a true plan artifact instead of prompt-only discipline
3. persist plan state across turns:
   - accepted plan decisions must survive into execution
   - Jack must resume from the validated route instead of replanning the whole task
4. rewrite Jack doctrine / `SOUL` projection so the live runtime stops favoring first-tool impulse
5. keep the capability bank green on every VPS deployment

Exit criteria:

- a governed brand mention can resolve to its standard ecosystem without freeform reconstruction
- a governed brand mention can load a stable workspace helper before live discovery
- no mutable business route starts without a plan artifact and target lock
- `browser` and generic shell execution are no longer first-hop defaults on backend-owned business routes
- action classes and scope profiles are explicit in the live Jack runtime
- governance work on roles / permissions / whitelists lands in a local role-permissions registry instead of prompt-only memory
- non-standard asks return a gap report or `capability-missing` / `protocol-missing`, not creative experimentation
- Jack doctrine explicitly says:
  - `route before tool`
  - `standard before improvisation`
  - `no papillonnage around missions`

### Milestone 4: Remaining Agents

Status: `next`

Scope:

- close agents not yet materially migrated:
  - `mnemos`
  - `jhin`
  - `kanye`
  - `walter`

Priority order:

1. `mnemos`
2. `jhin`
3. `kanye` and `walter` remain draft unless the `v1` perimeter changes

Rule:

- no agent is “present” just because a profile scaffold exists
- an agent counts only when:
  - protocol root exists
  - package root exists
  - canonical route exists
  - integration floor exists
  - validation evidence exists

### Milestone 5: Production Cutover

Status: `later`

Scope:

- stop using OpenClaw as active runtime
- keep only archive / shim / deterministic scripts that are still needed
- push Hermes + BRM + MM + Messenger as the sole active operating system

Exit criteria:

- no critical workflow depends on OpenClaw runtime orchestration
- MM reflects Hermes runtime truth
- channels feed Hermes, not OpenClaw
- operator team uses BRM/Hermes as the primary system

## V1 Closeout Gates

| Layer | Current state | Required closeout proof |
| --- | --- | --- |
| `Runtime / infra` | Hermes is live on the VPS, WhatsApp is paired, gateway is active on the `jack` profile | stable service + health + paired session on `/home/ubuntu/.brm-hermes/profiles/jack` |
| `Auth / secrets` | centralized floor exists for the active Hermes runtime | no missing credential on any v1 surface except items explicitly deferred from v1 |
| `BRM / harness` | protocol ownership and governed graph writes are live | all active v1 routes remain under explicit BRM gates with no fake `done` path |
| `Mission Manager` | API, first bridge proofs, and first audited WhatsApp ingress proof are live | broader `Hermes -> MM` ecosystem closeout |
| `Channels` | WhatsApp has a first audited governed ingress proof; Telegram is explicitly deferred post-v1 | keep the WhatsApp path stable and close the governed reply ecosystem |
| `Agents / business routes` | core agents are mixed `OK / PARTIAL / OPEN` | every v1 agent/route classified truthfully as `OK`, `approval_gated`, `mission_only`, or `non-runnable` |

## Production Closeout Order

The only valid production-ready closeout order is now:

1. `Control plane / office truth`
   - Mission Manager as the readable office of work
   - protocol taxonomy
   - cron truth
   - runtime observability
2. `Toolbox and capability standardization`
   - standardize active tool surfaces before widening route coverage
   - prefer upstream Hermes optional skills when they reduce custom integration debt
   - first commerce slice now closed:
     - Shopify GraphQL Admin/Storefront capability from `optional-skills/productivity/shopify/SKILL.md`
     - standardized on the existing multi-store backend instead of a parallel implementation
     - live contract now follows `stores.json` plus brand-pack routing
     - remaining commerce standardization work now moves to broader route ownership and adjacent tools, not Shopify floor discovery
3. `Entry points and governed replies`
   - WhatsApp
   - Lark in-scope channel surfaces
   - no message path without BRM + MM truth
4. `Agent protocol truth`
   - each route classified cleanly
   - each route bounded by protocol contract
   - each route validated under MM where business work is involved
5. `Enterprise memory`
   - Jack X world-state floor
   - Mnemos continuity floor
   - governed KG candidate and commit path
6. `Governance fallback`
   - `protocol-missing`
   - `capability-missing`
   - no silent improvisation
7. `Harness+ Phase 3`
   - verification
   - delivery review
   - feedback loop into Phase 1 and Phase 2
8. `OpenClaw` runtime retirement

Concrete live backlog under that order:

- keep MM runtime truth alive through recurring-task runtime events emitted by the real Hermes cron cycles
- build on the now-standardized Shopify floor before widening commerce route coverage
- keep the audited WhatsApp path stable while closing governed reply truth
- close the first `Lark`-backed governed specialist route
- keep protocol classification stable across all agents
- move Jack X from the contracted floor to per-channel workers plus a macro consolidator, without reopening the already-closed contracted floor
- capture a natural live Mnemos compaction proof
- package the first MM-backed `Harness+ Phase 3` families
- then retire the remaining OpenClaw runtime dependency

## Release Discipline

Before the next wider implementation wave:

1. reconcile local canonical repos and VPS deployed copies
2. review git drift and branch state
3. tag the current hardened VPS baseline
4. only then widen the next prod surface

Rule:

- no broad new prod surface should be opened while repo/deploy drift is still unclear

## Validation Rule

Nothing is considered closed unless:

- the integration exists in the canonical credential store
- the local skill/client exists
- the canonical runner exists
- the route package exists
- the route is replayed under BRM gates
- outputs are reviewable
- the state is written in `STATUS.md`

When the route is live and data can change between runs:

- validate fetch truth live
- freeze the fetched artifact
- replay the governed route on the frozen artifact
- require `3 runs / 0 variance` on the frozen artifact path

## Codebase Rule

The codebase is acceptable by domain roots, but not fully clean yet.

Cleanup truth on `2026-04-09`:

- root-level `tmp-*` and one-off repro files were archived out of `openclaw`
- accidental malformed root entries were archived out of `openclaw`
- local Python cache under `scripts/__pycache__` was removed
- hosted MM backup exports were archived out of the repo
- remaining dirty state is now mostly the active migration working set, not temporary clutter

Required cleanup before final cutover:

1. keep migration truth only in:
   - `openclaw/docs/ops/`
   - `hermes-runtime/docs/`
   - `hermes-runtime/reviews/`
2. normalize the remaining active worktree into intentional code/doc changes instead of mixed local runtime residue
3. keep secrets/auth truth explicit across runtime surfaces:
   - profile `.env`
   - auth store
   - MM-facing API vars
4. avoid new hidden state outside:
   - `.openclaw/workspace-*`
   - `.brm-hermes/profiles/*`
   - `hermes-runtime/reviews/*`

## What We Are Not Doing

- not finishing OpenClaw as if it were the destination runtime
- not migrating channels before the MM/operator bridge is clean
- not calling artifact-fed routes “live”
- not claiming an integration is healthy only because a secret exists
- not letting Jack choose models or timeouts for governed specialist routes
- not relying on prompt prose alone to solve routing or planning discipline

## Immediate Next Actions

1. keep Hermes recurring truth canonical:
   - `jack` digest must stay on `/Users/moufdi/hermes-runtime/contracts/hermes-recurring-jobs.v1.json`
   - `jack-x` recurring intake floor must stay on the same manifest plus its dedicated Hermes gateway
   - `mnemos` must stay explicitly `trigger_only` until a real recurring cadence is intentionally defined
   - remove or refuse any new parallel legacy scheduler ownership
2. close the control-plane/operator surface first:
   - keep MM `Capabilities` as the single readable office view for protocols
   - keep recurring-task runtime truth alive on Hermes cron history / `last_run` / `next_run` visibility
   - keep protocol classification stable across all agents
   - keep the `local workspace -> official Drive -> MM` delivery standard canonical
   - extend route adoption on top of `workspace_delivery.py` instead of adding new ad hoc Drive upload logic
   - the first MM operator snapshot layer is now closed:
     - `Deliverables` snapshot
     - `Drive` snapshot
     - `Integrations` snapshot with allowed agents and access scopes
   - the next MM work after this data layer:
     - attach real `mission files` from the route pilots so the non-empty Deliverables view becomes truthful
     - first unblock official Drive publication on `jack-vps` by installing a real Google user OAuth credential with Drive scope; without that, the delivery standard is structurally correct but cannot close live uploads into the official BRM workspace
     - decide whether the MM frontend consumes these snapshots directly or whether a dedicated MM UI slice is built on top
3. keep the audited `WhatsApp -> Hermes -> BRM observation -> MM` proof stable while closing the governed reply path
4. close the Jack runtime behavior gap on the live governed path:
   - observe `preprocess -> plan -> execute` on real work
   - close the persistent `plan artifact` and write-lock path
   - keep the capability bank in the deploy cycle so tool truth does not drift again
5. keep `jack.email-digest` explicitly separate from `jack-x.email-intake-pass0`:
   - digest = operator cron surface
   - Jack X = memorization / KG candidate surface
   - only decide later whether a distinct MM-backed `mission-digest` surface is worth adding
6. close `mnemos.context-check` on replay evidence and capture one natural live compaction proof
7. package the first `Harness+` Phase 3 loops as first-class MM-backed protocol families tied to MM/task truth
8. keep `protocol-missing` / `capability-missing` as the governed fallback for uncovered work instead of letting Jack improvise
9. keep the `draft protocol runtime` as the bounded bridge between uncovered specialist asks and future governed routes:
   - `protocol-missing` must produce a machine-readable draft runtime payload
   - draft routes may run only through a temporary registry and the existing BRM dispatch engine
   - promotion to a governed route must stay explicit and review-driven
10. open `Jhin` after `Mnemos`, while keeping `Telegram`, `Kanye`, and `Walter` out of `v1`

## Hermes Ecosystem Alignment

The wider Hermes ecosystem must be used selectively.

Adopt:

- Hermes core runtime:
  - gateway
  - profiles
  - tools
  - context compressor
- deploy and packaging patterns that reduce runtime drift
- `hermes-agent-self-evolution`, but only offline and review-driven

Study:

- memory/context helpers that can strengthen `Mnemos`
- retrieval/index helpers that can improve `Jack X`

Do not adopt as control plane:

- swarm / meta-harness / mission-control style layers must not replace `BRM + MM`
- free-writing memory systems must not replace the governed shared graph
- any helper that hides routing, validation, or delivery truth behind runtime magic is out of scope
