# BRM Orchestration Unified Plan

Last updated: `2026-05-05`

Status: canonical plan for the next orchestration hardening wave.

## Purpose

This document unifies the active plan for subagents, protocols, workflow lifecycle, scheduler/autoloop, Jack X memory, Mnemos continuity, Hippocampus preprocessing, and Mission Manager visibility.

It supersedes older local interpretations when they conflict with the current orchestration target. `STATUS.md` remains the factual production status log. `MASTERPLAN.md` remains the long-term migration plan. This file owns the current execution architecture.

## Executive Verdict

The system is usable, but not yet production-ready as a unified orchestration platform.

Approximate current maturity: `75%`.

Main blocker:

- the first canonical `WorkflowRun` / `AgentRunEvent` ledger is now live for Mission Manager recurring runtime reports, Jack interactive turns, and first specialist child runs, but protocol stages, approvals, validation, KG commits, and external tool cost events are not yet all lineage-bound to it.

Current instruction:

- do not add new primary agents before the orchestration substrate is unified
- do not loosen Jack by simply reopening tools
- replace hard locks with knowledge-first routing and typed execution modes
- make every run observable and replayable before calling it production-ready
- standardize toolboxes before widening route coverage; prefer upstream Hermes optional skills when they reduce custom integration debt

## Shipping Matrix

| Area | Status | Notes |
| --- | --- | --- |
| Workflow ledger and task lineage | shipped | The first canonical `WorkflowRun` / `AgentRunEvent` slice is live, and `mission_task_id` / `submission_scope` now remain machine-readable through the wake path. |
| Runtime handoff | partial | Hippocampus preprocessing is live and now feeds a task-bound routing summary through the same canonical `context_packet_ref` contract on interactive and wake-loop paths; broader MM/KG-first enrichment and fallback retirement remain open. |
| Protocol lifecycle closure | partial | Protocol-missing and draft-protocol runtime exist as lifecycle bridges; reviewed promotion to `prod` is still explicit work. |
| Autoloop improvement inbox | partial | The first task-bound improvement inbox is now derived from curator signals, recommendations, and lifecycle state; observation -> replay -> validation -> promotion remains the next closure wave. |

## Target Architecture

```text
Operator / Board / Channels
  | WhatsApp / Lark / MS365 / MM UI
  v
Hermes Gateway
  | auth, session isolation, pairing, channel runtime, cron ticker
  |
  +--> Hippocampus preprocessing
  |      input: message + ordered conversation + KG + protocol graph + MM state
  |      output: route packet + useful context + execution mode
  |
  +--> Jack supervisor
  |      mode: direct safe read
  |      mode: exploratory draft
  |      mode: validated protocol execute
  |      mode: mutation requires approval
  |
  +--> WorkflowRun ledger in Mission Manager
  |      run_id / parent_run_id / mission_id / route_id / protocol_id
  |      stage / status / artifacts / cost / validation / blocker
  |
  +--> Specialist routes
  |      Rosa / Jeff / Naya / Selena / Alfred / Tony / Cortex / future agents
  |
  +--> Jack X memory loop
  |      channel registry -> event DB -> per-channel reports
  |      -> KG candidate/review -> governed commit -> MM memory projection
  |      -> readable Memory Wiki pages + reviewable KG operations
  |
  +--> Mnemos continuity loop
  |      watch-threshold snapshot -> continuity journal
  |      context pressure / compaction -> continuity capsule
  |      session expiry reset -> pending capsule handoff -> session reinjection
  |
  +--> Autoloop controller
         observation -> failure/retour terrain -> draft protocol
         -> replay/test -> human validation -> promotion -> monitoring
```

## Ownership Model

Hermes owns runtime execution:

- model/provider calls
- gateway sessions and transcripts
- tool execution
- cron ticking
- channel adapters
- low-level logs

BRM Harness owns governance:

- protocol definitions
- route gates
- anti-variance rules
- execution modes
- validation contracts
- KG write policy

Mission Manager owns operator truth:

- missions
- recurring task intent
- workflow run ledger
- approvals
- protocol promotion status
- KG review queue
- visible run/activity state

Agents own reasoning and artifacts:

- Jack owns supervision and action orchestration
- Jack X owns diffuse memory and KG ingestion
- Mnemos owns active continuity and compaction survival
- Hippocampus owns pre-routing and context injection, not execution
- specialists own their bounded protocols and reviewable outputs

Messenger channels own signal only:

- WhatsApp, Lark, and mail are not business truth by themselves
- all business work must resolve through MM, protocol gates, or explicit read-only context paths

## Current Reality

Working now:

- Hermes gateway, sessions, WhatsApp runtime, and cron are deployed on the VPS.
- `jack.email-digest` runs via Hermes recurring jobs.
- `jack-x.registry-ingest`, `jack-x.db-analysis`, and `jack-x.memory-wiki` run via Hermes recurring jobs.
- Jack X has a real channel registry, event DB ingestion, DB-first analysis, KG candidate/review path, and MM memory projection.
- Jack X Memory Wiki now compiles channel reports and the latest memory projection into readable enterprise memory pages under `~/.openclaw/memory-wiki`; it does not directly mutate the KG.
- The semantic layer is now wired in bounded mode: `deterministic`, `shadow`, `active`. Production cron now runs `active` on `Gemini` with a shared semantic cache, so the first backfill writes fresh semantic outputs and subsequent runs reuse cached semantics for unchanged pages.
- Mnemos exists as a working continuity subsystem:
  - proactive watch-threshold snapshots once the configured watch band is crossed
  - compaction-time reinjection capsule generation
  - auto-reset continuity capture for daily/idle resets
  - one-shot prompt reinjection into the next session
  - durable continuity journal per profile under `~/.openclaw/workspace-mnemos/journal`
- Mnemos is intentionally not a KG writer. Its output is continuity memory and operator-grade handoff state, not enterprise truth.
- Mission Manager has missions, recurring tasks, Capabilities, Live, Activity, Memory KG, KG review operations, and the first `WorkflowRun` / `AgentRunEvent` ledger.
- Mission Manager now has a visible `Costs` surface on top of the activity ledger:
  - LLM and external tool cost truth are operator-visible
  - `billing_mode`, `cost_status`, and `cost_source` are surfaced
  - `subscription-handled` vs `out-of-subscription` is explicit
  - remaining gap is pricing contract quality for `unknown` / `credit-based` providers
- Hermes recurring runtime reports now auto-create canonical workflow runs in Mission Manager; validated on production with `jack-x.db-analysis` at `2026-04-22T23:48:26Z`.
- Jack interactive turns now create Mission Manager workflow runs via Hermes hook `brm-mm-workflow-ledger`; production synthetic proof exists for `interactive:synthetic:synthetic-hippocampus-session:synthetic-hippocampus-validation-20260423-001`.
- Specialist direct chat now creates first lineage-bound child runs in Mission Manager with `parent_run_id`.
- Hermes cron transport now has a standard prod floor:
  - `delivery.targets`
  - multi-target fan-out
  - persisted delivery receipts
- Runtime-state ambiguity on the VPS is now hardened:
  - live Jack and Jack-x gateways are explicitly profile-backed
  - root legacy state is archived out of the audit path
  - Jack `/status` exposes active gateway home, session store, channel directory, and WhatsApp mode
- Hippocampus is now a mandatory Jack runtime preprocessor for the Jack WhatsApp toolset. It injects a bounded packet into the prompt: identity, channel, ordered conversation window, KG hits, candidate protocol routes, recommended execution mode, guardrails, and LLM refiner status.
- Specialist route registry exists and multiple routes have validation artifacts.
- Specialist route registry now carries a first canonical executor contract:
  - `executor.kind` is live
  - local/VPS path drift is reduced through portable `~/...` registry paths plus bridge-side expansion
- Active specialist routes now share the first bounded specialist runtime context layer:
  - per-specialist `TOOLS.md` and protocol index are present for the active floor
  - route bundles persist `specialist-context.json` and `specialist-context.md`
  - LLM-backed specialist routes inject the bounded packet into their prompt instead of reasoning on an unbounded ask
- Protocol-missing and draft-protocol runtime exist as partial lifecycle bridges.
- The first toolbox-standardization slice is now closed and usable as a base:
  - Hermes upstream optional skill:
    - `optional-skills/productivity/shopify/SKILL.md`
  - standardized role:
    - standardized Shopify Admin/Storefront GraphQL capability for commerce routes
  - current floor:
    - standardized around the live `shopify-stores` backend already used in prod
    - tenant/auth contract now follows `clawd/skills/shopify-stores/stores.json`, and the capability registry references that source instead of duplicating tenants
    - live read validation now covers `maybe-paris` admin, `us-maybe-paris` admin via `client_credentials`, `maybe-paris` theme, and `blinx` admin
    - the local skill doc is aligned with the command surface actually implemented in `shopify.py`
  - residuals:
    - `blinx-us` auth declared but not ready
    - `nailz` brand metadata still references a missing Shopify store
- The first Safir route-backed closeout slice is now live:
  - `safir.email-audit`
  - `safir.mail-pole-audit`
  - both are canonical `executor.kind=command` routes with VPS render-only smoke proof
  - `email-workflow` remains intentionally open outside this slice
- The next execution order is now constrained by exact remaining truth, not preference:
  - `kanye` phase1 is now closed:
    - canonical routes now exist:
      - `kanye.still-generate`
      - `kanye.reference-edit`
    - `package_root` is live
    - route packages exist under `hermes-runtime/adapters/agents/kanye/packages`
    - local tests, VPS dispatch replay, and real VPS smoke are green
  - the first two `Mission Manager reflection` slices are now live:
    - the cockpit now projects current runtime truth directly on runtime-facing surfaces:
      - `executor.kind`
      - `dispatch_mode`
      - direct specialist chat vs route-backed runs
      - toolbox health
      - Hermes cron delivery receipts
    - canonical specialist truth now also surfaces across dashboard / org / member / mission views
    - the remaining low-blast-radius writer slice is now limited to:
      - stronger direct canonical member linkage where the registry already knows the member
      - fuller protocol/capability summary on the remaining surfaces
  - `mission autonomy` stays immediately after that:
    - `workflow_runs` / `agent_run_events` are live
    - `recurring_tasks` / `recurring_task_events` are live
    - `mission_tasks` / `mission_task_events` are now live on the MM backend
    - `next_check_at` is now derived on the mission read model
    - the Hermes wake path is now live
    - the remaining work is to encode one explicit business split across MM + runtime:
      - `direct_discussion`
      - `extraction`
      - `governed_route`
    - the remaining work also includes:
      - standardized route outcomes
      - first-class `data_check_report`
      - curator-ready signals bound to runs / task events
  - `Shopify` no longer blocks floor discovery:
    - standardization is done on the live `shopify-stores` backend
    - remaining work is auth/metadata cleanup plus route ownership
  - `repo/VPS drift` is a standing gate:
    - some targeted test slices are portable and replayable on both hosts
    - broader auxiliary specialist coverage still requires a wider sync before it can be treated as VPS-replayable truth
    - the VPS must still be treated as a deploy mirror, not as the canonical authoring checkout

Execution method for this next wave is now explicit:
- `mission autonomy truth gate` is the remaining sequential writer slice before parallel work
- once that contract is frozen:
  - `MM mission-task contract`
  - `MM operator review workspace`
  - `Hermes outcome normalization`
  - `Shopify residuals`
  - `deploy/test normalization`
    can run in parallel on disjoint write sets
- every implementation slice must end with:
  - local targeted tests
  - VPS replay of the exact synced slice
  - live smoke on the real runner
  - service restart when runtime-bearing files changed
  - operator confirmation over the real Jack WhatsApp bridge

Not production-ready yet:

- Jack orchestration is not trusted for critical autonomous work.
- Hippocampus is live for Jack WhatsApp turns, but the first slice still depends on deterministic prefiltering plus a short LLM refiner; it is not yet a full protocol-graph planner with replay feedback.
- Native Hermes `delegate_task` and BRM specialist dispatch are parallel systems, not one lineage-aware subagent orchestration model.
- Mission Manager does not yet receive every Hermes direct session, specialist child run, protocol stage, approval, validation result, and KG commit as `AgentRunEvent`.
- Mission Manager still does not receive every protocol stage, approval, validation result, KG commit, and external tool cost event as first-class `AgentRunEvent`.
- Mission tasks still do not yet encode the explicit boundary between:
  - `direct_discussion`
  - `extraction`
  - `governed_route`
- route outcomes are not yet uniformly comparable enough for Curator-grade analysis
- Protocol lifecycle is modeled as `candidate -> draft_runtime -> validated -> prod -> deprecated`, but reviewed promotion and later governance stages are still partial.
- Autoloop is not closed: the first task-bound protocol improvement inbox is now live, but replay, promotion, and monitoring remain open.
- Docs and snapshots have drifted across local/VPS and across older protocol status files.
- Toolbox standardization is not closed:
  - the first Shopify commerce slice is now closed on the live `shopify-stores` backend
  - remaining work is broader route ownership, adjacent tools, and prod route coverage
  - explicit current residuals are:
    - `blinx-us` auth not ready
    - `nailz` still lacks a canonical Shopify store mapping
  - skill presence alone is not enough; each widened surface still needs auth, bounded operations, and VPS smoke

## Parallel Planning Rule

The remaining waves should use bounded parallelism:

1. parallel explorer subagents for read-only audits
2. one writing owner per canonical surface during implementation
3. one regression pass after each phase, replaying local + VPS + live smoke where applicable

This is now the default execution rule for `Kanye`, `mission autonomy`, and the wider commerce cleanup.

Phase gate rule:

- no implementation phase advances without:
  - local targeted tests
  - local validation scripts
  - VPS targeted tests
  - VPS smoke on the real runner path
  - live restart proof when runtime-bearing files changed
  - operator confirmation over the real Jack WhatsApp bridge

## Canonical State Objects To Add

### WorkflowRun

Required fields:

- `run_id`
- `parent_run_id`
- `mission_id`
- `source_channel`
- `source_thread_id`
- `actor_id`
- `agent_id`
- `route_id`
- `protocol_id`
- `protocol_version`
- `execution_mode`
- `stage_id`
- `status`
- `input_ref`
- `context_packet_ref`
- `allowed_tools`
- `started_at`
- `completed_at`
- `artifacts`
- `validation_result`
- `cost`
- `token_usage`
- `blocker`
- `error`

Implemented first slice:

- persisted in Mission Manager as `workflow_runs` and `agent_run_events`
- API routes:
  - `GET /api/workflow-runs`
  - `GET /api/workflow-runs/:runId`
  - `POST /api/workflow-runs`
  - `PATCH /api/workflow-runs/:runId`
  - `POST /api/workflow-runs/:runId/events`
  - `POST /api/workflow-runs/events`
- `/api/recurring-tasks/runtime` mirrors recurring runtime reports into canonical workflow events
- Live uses the canonical workflow event when a recurring event is mirrored, preventing duplicate Live rows

Allowed statuses:

- `planned`
- `running`
- `waiting_approval`
- `blocked`
- `failed`
- `completed`
- `validated`
- `rejected`
- `superseded`

### ProtocolLifecycle

Allowed states:

- `discovered`
- `candidate`
- `draft_runtime`
- `validated`
- `prod`
- `deprecated`

Promotion requirements:

- owner agent
- protocol YAML/package
- input/output contract
- tool allowlist
- model/timeout policy
- replay corpus
- validation result
- MM-visible approval
- rollback path

### AgentRunEvent

Purpose:

- append-only event stream for every workflow run and subagent child run
- source for Live/Activity instead of reconstructed mission logs only

Minimum event types:

- `run.created`
- `run.started`
- `stage.started`
- `tool.called`
- `artifact.created`
- `approval.requested`
- `approval.resolved`
- `stage.completed`
- `run.completed`
- `run.failed`
- `kg.review.created`
- `kg.commit.applied`

## Jack Modes

Jack must not be one generic mode.

`direct_safe_read`:

- read-only, known capability, low risk
- KG/MM/canonical tools first
- no broad exploration

`exploratory_draft`:

- no validated protocol exists or context is ambiguous
- Jack proposes a short plan
- operator approves bounded steps
- output becomes protocol candidate evidence

`validated_protocol_execute`:

- known route/protocol exists
- stage machine and tool allowlist apply
- specialist owns work when route exists

`mutation_requires_approval`:

- any high-risk write, external publication, payment, customer-visible action, production deploy, or KG durable merge
- explicit approval event required before tool execution

## Hippocampus Runtime Contract

Hippocampus should run before Jack action selection.

Inputs:

- current message
- ordered conversation window
- user identity and channel identity
- KG relevant objects
- protocol graph
- capability registry
- specialist route registry
- MM active missions
- recent workflow runs

Outputs:

- `intent_type`
- `known_entities`
- `candidate_routes`
- `recommended_route`
- `execution_mode`
- `required_clarifications`
- `context_packet`
- `tool_policy`
- `risk_level`
- `confidence`

Default model policy:

- low-cost routing model is acceptable for Hippocampus when schema compliance is stable
- long-context exploration should use the exploration profile
- critical implementation remains on the governed implementation profile
- no agent may choose its own model or timeout on governed routes

## Subagent Orchestration Target

Current problem:

- Hermes native delegation and BRM specialist dispatch are separate.
- Jack WhatsApp currently removes native delegation for safety.
- Mission Manager cannot show true parent/child subagent lineage.

Target:

- every child agent run is a `WorkflowRun` with `parent_run_id`
- Jack never silently absorbs specialist work when a specialist route exists
- specialists receive bounded context packets, not full unbounded chats
- child outputs are typed artifacts
- parent run cannot close until validation gates pass
- subagents are allowed in exploratory draft mode only with bounded plan and operator approval

## Autoloop Target

Autoloop is not just cron.

Current:

- Hermes recurring jobs schedule known commands.
- Jack X and digest cycles run.
- There is no full automatic protocol improvement loop.

Target loop:

```text
runtime observation
  -> classify failure / variance / missing protocol / user correction
  -> create MM approval or protocol todo
  -> generate draft protocol candidate
  -> replay against corpus
  -> validation result
  -> human approve promotion
  -> update registry/package/scheduler
  -> monitor next runs
```

Autoloop must never directly promote a protocol to prod without approval.

## Immediate Implementation Plan

P0 - Documentation and truth alignment:

- make this document the active orchestration plan
- update `STATUS.md` to remove stale executive contradictions
- sync local docs to VPS
- mark known drifts explicitly instead of hiding them

P1 - WorkflowRun foundation:

- done: add MM storage/API for `workflow_runs` and `agent_run_events`
- done: mirror Hermes recurring runtime reports into run events through `/api/recurring-tasks/runtime`
- done: update Live/Activity to read canonical run events and avoid mirrored recurring duplicates
- next: attach Jack interactive sessions, specialist child runs, protocol stages, approvals, validation, and KG commit events
- next: expose parent/child lineage and validation state in the UI

P2 - Hippocampus runtime:

- build route packet generator from message + KG + protocol graph + MM state
- replace keyword-only Jack routing as the primary decision path
- keep keyword rules as fallback diagnostics, not the main system

P3 - Protocol lifecycle:

- add protocol lifecycle state in MM
- connect protocol-missing and draft runtime to promotion workflow
- require replay/validation artifacts before prod

P4 - Subagent unification:

- wrap BRM specialist dispatch and Hermes native delegation into the same `WorkflowRun` model
- re-enable bounded subagent work for Jack only through execution modes and approvals

P5 - Autoloop:

- create protocol improvement inbox
- classify failures and user corrections
- generate draft candidates
- replay, validate, request approval, promote, monitor

## Current Progress Estimate

| Area | Estimate | Notes |
| --- | ---: | --- |
| Hermes runtime foundation | 80-82% | Gateway and cron are real; OpenClaw shim remains. |
| Specialist routes | 70-75% | Several routes validated; live scope remains partial. |
| Protocol corpus | 70% | Many packages exist; lifecycle/promotion incomplete. |
| Mission Manager cockpit | 76-78% | First canonical run ledger is live; direct sessions and child lineage still missing. |
| Scheduler truth | 70-73% | Cron exists, reports into WorkflowRun for recurring jobs, and now includes active Gemini-backed Memory Wiki cache reuse; protocol/MM drift remains. |
| Jack X memory/KG | 78-83% | Structured pipeline plus readable Memory Wiki compiler, shared semantic cache, and active Gemini layer are live; KG commit/review quality still improving. |
| Mnemos continuity | 65-70% | Trigger-only and useful; natural saturation proof still weak. |
| Jack orchestration | 45-52% | Main risk: rigid keyword routing and tool lock. |
| Hippocampus runtime | 25-35% | Index/schema exists; not mandatory runtime path. |
| Autoloop | 30-35% | Concept and cron exist; improvement loop not closed. |
| Overall | 74-75% | Good base, first workflow ledger slice closed, active memory semantics now live; not yet enterprise-grade orchestration. |

## Non-Negotiables

- `route before tool`
- `KG/MM/canonical backend before browser or raw terminal`
- `no business mutation without execution mode and approval when required`
- `no hidden blocker`
- `no fake done`
- `no specialist work silently absorbed by Jack`
- `no protocol promotion without replay evidence`
- `no durable KG merge without governed review policy`
- `no new primary agent before WorkflowRun and routing foundation are stable`

## Closeout Definition

This orchestration wave is closed only when:

- local and VPS docs match
- `WorkflowRun` exists and receives Hermes cron + Jack interactive + specialist child events
- Hippocampus route packets are used before Jack action selection
- Jack has bounded exploratory draft mode without blanket tool unlocking
- protocol lifecycle is visible in MM
- autoloop creates reviewable improvement candidates instead of silent changes
- Live/Activity can show parent/child subagent lineage and validation state
