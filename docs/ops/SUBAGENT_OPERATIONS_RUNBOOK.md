# Subagent Operations Runbook

Last updated: `2026-05-05`

## Purpose

This runbook is for another agent working in parallel on the same machine.

It defines:

- where truth lives
- which toolboxes belong to which agents
- where credentials and config live
- how missions connect MM, Hermes, and KG
- how the learning loop is allowed to improve
- the current schema floor
- the DRY/KISS rules
- the safe operational workflow

This document is operational. It should stay factual.

## Executive Rules

1. `MissionTask` owns business scope.
2. `WorkflowRun` owns execution truth.
3. `ProtocolLifecycleRecord` owns protocol state.
4. `Curator` is derived and advisory only.
5. `Hippocampus` is pre-routing, not execution.
6. Prefer derived read models over new tables.
7. Prefer additive machine-readable fields over prose-only summaries.

## Deployment Policy

The VPS is a release mirror, not an authoring checkout.

Allowed in-band runtime actions:

- `gateway_control.status`
- `gateway_control.health_check`
- `gateway_control.restart_gateway`
- `gateway_control.reload_config`
- `gateway_control.release_status`
- `gateway_control.rollback_release`

Forbidden in-band runtime actions:

- `git pull`
- `git checkout`
- self-update to a commit
- building a new release on the live gateway
- mutating the deployed release in place as the normal upgrade path

Rule:

- new code is authored, tested, pushed, and deployed from the operator machine
- the VPS consumes immutable releases under `releases/`
- rollback is agent-callable
- forward deploy is operator-driven

Current BRM policy:

- `/update` is disabled on Jack production deployments
- `update_to_commit` is intentionally not exposed until a separate governed source-of-truth flow exists

## System Truth Map

### Mission Manager

Path:

- `/Users/moufdi/Desktop/ClaudeCode/mission-manager-git`

Owns:

- missions
- mission tasks
- mission task events
- workflow ledger
- protocol lifecycle records
- approvals and review outcomes
- curator snapshot and recommendations

Canonical files:

- [database.js](/Users/moufdi/Desktop/ClaudeCode/mission-manager-git/database.js)
- [server.js](/Users/moufdi/Desktop/ClaudeCode/mission-manager-git/server.js)

Current task-bound read models:

- `submission_scope`
- `execution_lineage`
- `task_workspace_kind`
- `hippocampus_summary`
- `protocol_improvement_inbox`

### Hermes Runtime

Path:

- `/Users/moufdi/hermes-runtime`

Owns:

- gateway sessions
- model and tool execution
- wake-loop scheduling
- Hippocampus packet generation
- specialist dispatch
- runtime truth handoff back into MM

Canonical files:

- [hermes-agent/gateway/run.py](/Users/moufdi/hermes-runtime/hermes-agent/gateway/run.py)
- [hermes-agent/gateway/hippocampus.py](/Users/moufdi/hermes-runtime/hermes-agent/gateway/hippocampus.py)
- [hermes-agent/cron/scheduler.py](/Users/moufdi/hermes-runtime/hermes-agent/cron/scheduler.py)
- [scripts/brm-specialist-dispatch.ts](/Users/moufdi/hermes-runtime/scripts/brm-specialist-dispatch.ts)
- [scripts/mission_manager_runtime.py](/Users/moufdi/hermes-runtime/scripts/mission_manager_runtime.py)

### KG / Memory / Continuity

Path:

- `/Users/moufdi/openclaw`

Owns:

- Jack X channel registry and event DB logic
- KG candidate and review path
- Memory Wiki and projection surfaces
- Mnemos continuity memory
- ops docs and orchestration contract

Rule:

- KG and continuity are not operator mission truth.

## Agent Roles And Boundaries

### Jack

Role:

- supervisor
- operator-facing orchestration
- route handoff or bounded discussion

Must not:

- bypass MM for business work
- improvise silent production execution when no governed route exists

### Hippocampus

Role:

- primary pre-routing packet
- intent detection
- recommended mode selection
- candidate route ordering
- guardrail injection

Must not:

- execute business work
- become a second ledger

### Curator

Role:

- read loops
- count friction
- expose recommendations
- expose protocol improvement candidates

Must not:

- auto-promote protocols to `prod`
- override mission truth

### Specialists

Role:

- bounded production surfaces

Examples:

- `tony.*`
- `naya.*`
- `rosa.*`
- `jeff.*`
- `selena.*`
- `alfred.*`
- `cortex.*`
- `kanye.*`

Must not:

- redefine MM truth locally
- silently mutate protocol state

## Toolboxes Per Agent

Toolbox truth should come from route packages, runtime context, and allowed tools, not from freeform prompting.

### Jack toolbox

- Mission Manager bridge
- WhatsApp/interactive gateway
- bounded specialist dispatch
- protocol-missing and capability-missing openers

### Jack X toolbox

- channel registry
- event DB
- KG candidate/review path
- Memory Wiki compiler

### Specialist toolbox

- per-agent `TOOLS.md`
- route package contract
- specialist runtime context bundle
- governed files/API/web tools only when the route contract allows them

## Access Boundaries

Allowed write surfaces:

- MM APIs or MM backend functions for mission truth
- Hermes runtime and route outputs for execution truth
- governed Jack X candidate/review paths for KG work

Forbidden shortcuts:

- using channel transcripts as business truth
- writing production protocol state outside MM lifecycle records
- hidden local files as production dependencies
- bypassing approval gates on sensitive mutation work

## Credentials And Config

### Hermes live profile truth

Primary Jack live profile:

- `HERMES_HOME=/home/ubuntu/.brm-hermes/profiles/jack`

Typical live config locations:

- `/home/ubuntu/.brm-hermes/profiles/jack/.env`
- `/home/ubuntu/.brm-hermes/profiles/jack/config.yaml`
- `/home/ubuntu/.brm-hermes/profiles/jack/whatsapp/session/`

### Local authoring roots

- `/Users/moufdi/hermes-runtime`
- `/Users/moufdi/Desktop/ClaudeCode/mission-manager-git`
- `/Users/moufdi/openclaw`

### Hippocampus provider overrides

Prefer env overrides before editing profile config when testing a provider/model change:

- `HIPPOCAMPUS_AUX_PROVIDER=openrouter`
- `HIPPOCAMPUS_AUX_MODEL=google/gemini-3-flash-preview`
- optional:
  - `HIPPOCAMPUS_AUX_BASE_URL=https://openrouter.ai/api/v1`
  - `HIPPOCAMPUS_LLM_TIMEOUT=4`
  - `HIPPOCAMPUS_TOTAL_TIMEOUT=6`
  - `HIPPOCAMPUS_PACKET_CACHE_TTL_SECONDS=60`

Credential source for the OpenRouter path:

- `OPENROUTER_API_KEY`

### MM hosted truth

- ALB `mission-manager-prod-alb`
- ECS service `mission-manager-prod-backend`

Rule:

- local Mac behavior is never production proof by itself.

## Mission Connection Model

1. user or operator intent reaches Jack
2. Hippocampus builds a bounded routing packet
3. Jack or wake-loop resolves or creates a `MissionTask`
4. Hermes executes a governed route or keeps the task operator-owned
5. runtime emits `WorkflowRun` and `AgentRunEvent`
6. MM derives:
   - `submission_scope`
   - `execution_lineage`
   - `hippocampus_summary`
   - `curator_snapshot`
   - `curator_recommendations`
   - `protocol_improvement_inbox`
7. if memory/KG work is involved, Jack X remains the governed candidate path
8. protocol state remains in MM lifecycle truth

## Current Schema Floor

### MissionTask

Important current derived fields:

- `submission_scope`
- `execution_lineage`
- `task_workspace_kind`
- `hippocampus_summary`
- `protocol_improvement_inbox`

### WorkflowRun

Important execution fields:

- `run_id`
- `parent_run_id`
- `mission_id`
- `mission_task_id`
- `route_id`
- `protocol_id`
- `dispatch_mode`
- `input_ref`
- `context_packet_ref`
- `approval_state`
- `validation_result`
- `blocker`
- `error`
- `allowed_tools`
- `metadata`

### ProtocolLifecycleRecord

Important state fields:

- `protocol_key`
- `mission_id`
- `mission_task_id`
- `origin_run_id`
- `parent_run_id`
- `requested_route_id`
- `state`
- `phase_state`
- `recommended_next_action`
- `validated_at`
- `promoted_at`
- `deprecated_at`

## Learning Loop

Allowed improvement path:

1. observe task friction
2. derive curator signals
3. derive recommendations
4. expose protocol improvement inbox
5. open or enrich a lifecycle `candidate`
6. move through `draft_runtime`
7. validate with lineage-bound evidence
8. explicitly review promotion to `prod`

Not allowed:

- silent auto-promotion
- implicit protocol state from a single successful run
- replacing MM lifecycle truth with side files

## DRY / KISS Policy

Prefer:

- derived read models
- small helpers
- compact UI panels
- reuse of `workflow_runs`, `agent_run_events`, and `protocol_lifecycle`

Avoid:

- new tables for packet, scope, or inbox unless proved necessary
- duplicate truth in MM and runtime
- a separate Curator scheduler
- speculative abstractions before operational need

## Safe Operational Workflow

### Before coding

1. audit current truth in MM, runtime, and docs
2. decide whether the need is a new write surface or only a derived read model
3. freeze owned files per lane

### During parallel work

1. keep write sets disjoint
2. do not revert unrelated dirty changes
3. avoid broad refactors across MM/runtime/docs at once
4. prefer additive machine-readable fields over free-text summaries

### Before push

Mission Manager:

- `node --check server.js`
- `node --check database.js`
- targeted backend tests

Frontend:

- `pnpm exec tsc --noEmit`
- `pnpm build`

Hermes runtime:

- targeted `pytest`
- targeted Node tests
- `python3 scripts/validate-jack-standardization.py`

### After push

1. deploy only changed surfaces
2. replay VPS validations
3. run a production-shaped smoke:
   - create temporary mission
   - create direct-discussion task
   - create governed task
   - verify routing summary, lineage, approval, lifecycle state
   - verify protocol improvement inbox if touched
4. cleanup temporary mission/project
5. send WhatsApp confirmation from the real Jack/Hermes path

## Shipped / Partial / Next

### Shipped

- task-centric workflow lineage
- canonical `context_packet_ref`
- Hippocampus routing packet transport
- operator execution inspector
- curator snapshot and recommendations
- first derived protocol improvement inbox

### Partial

- richer MM/KG-first Hippocampus enrichment
- full retirement of older keyword-first routing behavior
- reviewed promotion to `prod`
- unified lineage for every approval, validation, KG, and cost event
- replay and monitoring closure for the protocol improvement loop

### Next

- stronger MM/KG-first Hippocampus enrichment
- replay pipeline for protocol candidates
- reviewed promotion and monitoring closeout
- deeper convergence between native Hermes delegation and BRM specialist dispatch

## Missing Operational Gaps

Still open:

- not every protocol stage and external tool event is lineage-bound yet
- Hippocampus still coexists with older fallback routing paths
- reviewed promotion to `prod` remains explicit operator work
- protocol improvement replay and monitoring are not yet closed as a full autoloop
- native Hermes delegation and BRM specialist dispatch are still parallel systems
