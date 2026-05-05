# Mission Autonomy Contract

## Purpose

This phase turns Mission Manager from a passive tracker into an active follow-up system.

Mission Manager remains the business source of truth.
Hermes becomes the wake-and-execute layer on top of that truth.
Curator comes later and optimizes this loop; it does not replace it.
Canonical here means the object model and its invariants are authoritative; it does not imply every clause is fully shipped yet.

## Shipping Matrix

| Area | Status | Notes |
| --- | --- | --- |
| Workflow ledger and task lineage | shipped | `workflow_runs` / `agent_run_events` and `mission_task_id` / `submission_scope` are canonical on governed wake routes, and `MissionTask` exposes `submission_scope` plus `execution_lineage` as read models. |
| Runtime handoff | partial | Hippocampus is now the canonical pre-routing packet for interactive specialist dispatch, `context_packet_ref` remains stable across interactive and wake routes, and `MissionTask` now exposes a task-bound routing summary. Deeper KG/MM-first enrichment and full retirement of older keyword fallbacks remain open. |
| Protocol lifecycle closure | partial | `candidate -> draft_runtime -> validated` is enforced; `validated -> prod` still requires an explicit reviewed promotion path. |
| Autoloop improvement inbox | partial | `MissionTask` now exposes a derived protocol-improvement inbox from curator signals, recommendations, and lifecycle state, but replay, promotion, and monitoring remain open. |

## Core Objects

- `mission`
  - durable business commitment
  - owns `success_criteria`, `due_date`, `current_summary`, `status`
- `mission_task`
  - operational unit inside a mission
  - can be owned by an agent or a human
  - can be scheduled for follow-up
  - can produce drafts, actions, blockers, or info requests
- `workflow_run`
  - execution trace
  - holds lineage, artifacts, costs, and run state
- `mission_task_event`
  - audit trail for task lifecycle, wake attempts, reviews, and feedback

## Source Of Truth

- Canonical mission deadline remains `due_date`
- Canonical mission success field remains `acceptance_criteria`
- Read-model aliases may expose:
  - `deadline_at`
  - `success_criteria`
- `mission.next_check_at` remains derived from open mission tasks
- No second scheduler or task state is allowed outside MM

## Workflow Ledger Contract

`workflow_run` and `agent_run_event` are the canonical execution ledger for lineage-bound runtime truth.

They do not replace mission or mission-task business truth.
They record how work was executed, reviewed, blocked, validated, approved, or failed.

### Canonical Workflow Statuses

Incoming runtime aliases may normalize, but the stored `workflow_run.status` must collapse to one of:

- `queued`
- `planned`
- `running`
- `blocked`
- `waiting_approval`
- `completed`
- `failed`
- `cancelled`
- `validated`
- `rejected`
- `superseded`

Richer execution meaning must live in:

- `current_stage`
- `current_task`
- `event_type`
- workflow `metadata`
- event `metadata`

### Canonical Execution Modes

`workflow_run.execution_mode` must normalize to one of:

- `manual`
- `scheduled`
- `autoloop`
- `draft_protocol`
- `operator`
- `background`

### First-Class Workflow Truth Fields

The canonical `workflow_run` surface is:

- `run_id`
- `parent_run_id`
- `mission_id`
- `agent_id`
- `agent_name`
- `session_id`
- `protocol_id`
- `route_id`
- `dispatch_mode`
- `executor_kind`
- `profile`
- `source`
- `source_channel`
- `source_ref`
- `execution_mode`
- `status`
- `protocol_version`
- `input_ref`
- `context_packet_ref`
- `allowed_tools`
- `validation_result`
- `approval_state`
- `blocker`
- `error`
- `current_stage`
- `current_task`
- `summary`
- `started_at`
- `completed_at`
- `last_event_at`
- `usage`
- `artifacts`
- `metadata`

The canonical `agent_run_event` surface is:

- `event_id`
- `run_id`
- `parent_run_id`
- `agent_id`
- `agent_name`
- `protocol_version`
- `input_ref`
- `context_packet_ref`
- `allowed_tools`
- `validation_result`
- `approval_state`
- `blocker`
- `error`
- `event_type`
- `status`
- `stage_id`
- `tool_name`
- `message`
- `timestamp`
- `received_at`
- `usage`
- `metadata`

### Well-Known Workflow Metadata Keys

The following workflow truth fields are already first-class on `workflow_run`, and may also appear in `workflow_run.metadata` for compatibility:

- `context_packet_ref`
- `allowed_tools`
- `approval_state`
- `validation_result`
- `blocker`
- `error`

Until they are promoted further, these same facts may appear in `agent_run_event.metadata` as machine-readable keys.

Rules:

- these keys must not exist only inside free-text summaries
- `approval_state` on `workflow_run` should remain a normalized machine-readable state label
- if richer approval context is needed, it may live in `workflow_run.metadata.approval_state` or `agent_run_event.metadata.approval_state`
- `validation_result`, `blocker`, and `error` should remain objects or null
- `context_packet_ref` should remain a stable reference, not an ad hoc narrative string
- task state may summarize these facts, but the workflow ledger remains the canonical execution trace

### Wake Submission Lineage Keys

Wave 0+1 wake-loop submissions must keep the task binding machine-readable without introducing new MM business objects.

Minimum metadata/runtime-truth keys:

- `mission_task_id`
- `submission_scope`

Rules:

- `mission_task_id` identifies the MM task that originated the submission when the wake-loop dispatches a governed route
- `submission_scope` identifies the submission boundary, with `mission_task` as the canonical Wave 0+1 value
- these keys may live in workflow/event metadata and runtime truth even when they are not first-class workflow columns
- child route payloads emitted from Hermes should preserve them so downstream bridge/audit artifacts do not lose task lineage
- interactive Hippocampus packets and specialist-runtime packets may keep different payload schemas, but they should converge on the same machine-readable `context_packet_ref` contract

### Approval And Validation Lineage

Approval, validation, and protocol-governance facts must be lineage-bound to the same workflow ledger.

Minimum expectation:

- approval request -> `agent_run_event`
- approval resolution -> `agent_run_event`
- validation result -> `agent_run_event`
- blocker emission -> `agent_run_event`
- runtime error emission -> `agent_run_event`
- protocol lifecycle stage change -> linked by `run_id` or `origin_run_id`

If a route is approval-gated:

- `workflow_run.status` may remain `blocked`
- the reason must be recoverable from `blocker` / `approval_state`
- completion must not silently bypass an MM-visible approval decision

If a route is validation-gated:

- the validation verdict must be recoverable from `validation_result`
- `prod` promotion must not be inferred from a successful run alone

### Protocol Lifecycle Truth

Protocol lifecycle remains a governance read/write surface anchored to MM truth.

Canonical lifecycle states:

- `candidate`
- `draft_runtime`
- `validated`
- `prod`
- `deprecated`
- `superseded`

Canonical lineage-bearing lifecycle fields include:

- `protocol_key`
- `mission_id`
- `origin_run_id`
- `parent_run_id`
- `requested_route_id`
- `target_agent`
- `bundle_path`
- `protocol_path`
- `registry_entry_path`
- `review_root`
- `draft_artifact_path`
- `feedback_artifact_path`
- `allowed_actions`
- `recommended_next_action`
- `validated_at`
- `promoted_at`
- `deprecated_at`
- `metadata`

Lifecycle rules:

- `candidate` and `draft_runtime` may be machine-generated, but remain reviewable
- `validated` requires lineage-bound validation evidence
- `prod`, `deprecated`, and `superseded` remain explicit governance outcomes, not silent runtime side effects

## Mission Task Contract

### Engagement Mode

Every mission task must declare one canonical engagement mode:

- `direct_discussion`
  - broad, tool-bounded exploration
  - clarification, comparison, diagnosis, synthesis, draft preparation
  - must not claim final governed completion by itself
- `extraction`
  - structured collection and pre-analysis
  - can prepare facts, inventories, and bounded evidence packets
  - must not claim final business completion by itself
- `governed_route`
  - repeatable, auditable, route-backed execution
  - required for mutations, deliverables, validation, or safety-sensitive work

Rule:

- ambiguity starts in `direct_discussion` or `extraction`
- stable, executable work promotes to `governed_route`
- no task may silently shift from discussion to governed execution without an explicit task update

### Canonical Statuses

- `todo`
- `scheduled`
- `in_progress`
- `draft_ready`
- `waiting_review`
- `changes_requested`
- `waiting_external`
- `blocked`
- `done`
- `canceled`

### Review Modes

- `draft_only`
  - agent prepares output only
  - no final action without human validation
- `approval_required`
  - agent may prepare or partially execute
  - final state change requires explicit approval
- `auto_execute_safe`
  - route may execute automatically if explicitly marked safe
- `manual_only`
  - tracked in MM, but never auto-dispatched to Hermes

Default rule:
- if a task has `owner_agent_id` or `route_id`, default to `approval_required`
- otherwise default to `manual_only`

### Ownership

- `owner_agent_id`
  - canonical agent identifier, e.g. `jack`, `kanye`, `safir`
- `owner_member_id`
  - optional MM member owner when a human owns the task

### Execution Fields

- `engagement_mode`
- `route_id`
- `executor_kind`
- `protocol_id`
- `source_run_id`
- `last_run_id`
- `iteration_count`

### Scheduling And Blocking

- `next_check_at`
- `due_at`
- `blocked_reason`

### Data Check Report

When a task or run depends on non-trivial analysis, the execution payload should expose a comparable `data_check_report`:

- `source_provenance`
- `freshness_ok`
- `completeness_ok`
- `conflict_detected`
- `sample_size`
- `blocking_anomalies`
- `human_assumptions_required`

This is not a second business object.
It is execution metadata used for review, validation, and later Curator analysis.

### Curator Signals

The first Curator substrate must be readable from task/run metadata without introducing Curator-owned state:

- `iteration_count`
- `review_cycles`
- `blocked_cycles`
- `data_gaps_detected`
- `cost_per_iteration`
- `escalation_count`

These signals may be stored directly or derived from task events and workflow runs.
The important rule is that they remain lineage-bound to MM truth.

### Workspace Kind

Every task read model may expose one canonical `task_workspace_kind` derived from task truth:

- `review`
- `operator`
- `wake`
- `blocked`
- `completed`

Derivation priority:

- closed task -> `completed`
- `blocked` or `waiting_external` -> `blocked`
- `draft_ready` or `waiting_review` -> `review`
- `manual_only`, `direct_discussion`, or `extraction` -> `operator`
- otherwise -> `wake`

### Curator Snapshot

Mission read models may expose one canonical `curator_snapshot` derived from task truth:

- `tracked_tasks`
- `iterations`
- `review_cycles`
- `blocked_cycles`
- `data_gaps`
- `escalations`
- `avg_cost_per_iteration`
- `workspace_summary`

Rules:

- counters remain additive over lineage-bound task truth
- `avg_cost_per_iteration` is a weighted average by `iteration_count`
- `workspace_summary` counts the canonical `task_workspace_kind` buckets
- no second persistent Curator store is introduced

### Curator Recommendations

Mission read models may expose read-only `curator_recommendations` with:

- `type`
- `severity`
- `confidence`
- `reason`
- `evidence`
- `suggested_action`
- `task_ids`
- `route_ids`

Initial recommendation taxonomy:

- `route_underperforming`
- `insert_extraction_step`
- `keep_as_direct_discussion`
- `escalate_human_earlier`
- `manual_only_candidate`

Curator remains non-authoritative:

- no auto-dispatch
- no auto-close
- no auto-reschedule
- no second scheduler
- no alternate task state

### Wake / Claim Fields

- `lease_owner`
- `lease_expires_at`
- `wake_attempt_count`
- `last_wake_attempt_at`

## Agent Outcome Contract

Agent executions must end with one canonical `outcome_type`:

- `draft`
- `action`
- `blocked`
- `info_request`

Expected output payload:

- `outcome_type`
- `summary`
- `artifacts`
- `recommended_next_check_at`
- `requires_review`
- `blocked_reason`
- `data_check_report`
- `curator_signals`

This payload belongs in task-event metadata and run metadata.
It does not create a second persistent business object.

### Canonical Envelope Rules

- `outcome_type` must always be one of:
  - `draft`
  - `action`
  - `blocked`
  - `info_request`
- `summary` must be a short human-readable result summary.
- `artifacts` must be a list of stable references, even when empty.
- `recommended_next_check_at` is optional, but when present it must be a valid ISO timestamp.
- `requires_review` must be explicit when the route or operator flow needs review.
- `blocked_reason` must be present for `blocked` and `info_request` outcomes when the reason is known.
- `data_check_report` must remain an object or null, never an ad hoc string.
- `curator_signals` must remain an object or null, never a second business object.

## Task Event Taxonomy

- `created`
- `updated`
- `status_changed`
- `claimed`
- `claim_released`
- `wake_attempted`
- `wake_failed`
- `draft_ready`
- `review_requested`
- `approved`
- `changes_requested`
- `rescheduled`
- `blocked`
- `completed`
- `canceled`

### Allowed Transitions

#### Wake And Claim

- `todo` -> `scheduled`
- `scheduled` -> `in_progress`
- `in_progress` -> `draft_ready`
- `in_progress` -> `waiting_review`
- `in_progress` -> `blocked`
- `waiting_external` -> `scheduled`

## Wake-Loop Rules

There is one Hermes wake-loop for mission autonomy.

It must:

1. fetch due tasks from MM
2. ignore closed tasks
3. ignore `manual_only` tasks
4. claim one task with a lease before dispatch
5. create a linked workflow run
6. dispatch using canonical `route_id` and `executor_kind`
7. write task events and update `last_run_id`
8. release or renew the lease on completion/failure

When the wake-loop dispatches a route, the child runtime submission must carry:

- `mission_task_id`
- `submission_scope=mission_task`

### Due Task Eligibility

A task is due when:

- `next_check_at <= now`
- `status` is not one of:
  - `done`
  - `canceled`
- lease is absent or expired

### Anti-Duplication Rule

Claim is authoritative.

No runner may execute a task unless:

- claim succeeded
- lease is still owned by that runner

## Review Loop Rules

### Approve

- allowed from:
  - `draft_ready`
  - `waiting_review`
  - `changes_requested`
- default result:
  - task becomes `done`
  - lease cleared

### Request Changes

- allowed from:
  - `draft_ready`
  - `waiting_review`
- result:
  - task becomes `changes_requested`
  - feedback stored as task event
  - `next_check_at` set to immediate or provided follow-up time
  - lease cleared

### Reschedule

- allowed from any non-closed state
- result:
  - task becomes `scheduled`
  - `next_check_at` updated

### Block

- allowed from any non-closed state
- result:
  - task becomes `blocked`
  - `blocked_reason` required
  - lease cleared

#### Review Transition Matrix

- `draft_ready` or `waiting_review` -> `approve` -> `done`
- `draft_ready` or `waiting_review` -> `request_changes` -> `changes_requested`
- any non-closed state -> `reschedule` -> `scheduled`
- any non-closed state -> `block` -> `blocked`

### Validation Expectations

Mission Manager and Hermes must validate the same canonical contract.

- `manual_only` tasks remain tracked in MM but must not be auto-dispatched.
- `draft_only` tasks may produce drafts but may not silently complete sensitive work.
- `approval_required` remains the default when a task has `owner_agent_id` or `route_id`.
- review payloads must reject invalid `action` values, invalid timestamps, and non-object `data_check_report` / `curator_signals` values.
- wake-loop outcomes must preserve the canonical envelope in task events and workflow run metadata.
- Curator signals remain lineage-bound to mission/task truth and do not introduce a second scheduler or an alternate state store.

## API Surface To Add

### Mission Task Discovery

- `GET /api/mission-tasks/due`
  - filters:
    - `due_before`
    - `owner_agent_id`
    - `limit`

### Claim Lifecycle

- `POST /api/missions/:id/tasks/:taskId/claim`
- `POST /api/missions/:id/tasks/:taskId/release`

### Review Lifecycle

- `POST /api/missions/:id/tasks/:taskId/review`
- `POST /api/missions/:id/tasks/:taskId/feedback`

### Curator Read Surface

- `GET /api/missions/:id/curator`
  - returns:
    - `mission_id`
    - `curator_snapshot`
    - `curator_recommendations`
    - `task_summary`
    - `tasks`

## UI Reflection

Mission UI must show:

- open tasks
- review-required tasks
- next check
- task owner
- engagement mode
- route / executor
- latest run
- latest task event
- data check summary

Review UI must support:

- approve
- request changes
- reschedule
- block

The operator must also be able to distinguish clearly between:

- discussion work
- extraction work
- governed execution work

No `done` claim should look equally trustworthy across those three modes.

## Parallelization Boundaries

### Writer A: MM backend

- `database.js`
- `server.js`
- backend tests

### Writer B: Hermes wake-loop

- Hermes cron/wake runtime only
- MM bridge calls
- runtime tests

### Writer C: MM frontend

- mission/task/review surfaces only
- frontend types
- build/type checks

### Writer D: regression

- integration and smoke scripts
- no canonical business logic ownership

## Success Criteria

- a due task can be claimed exactly once
- a claimed task produces a linked workflow run
- agent output can produce:
  - draft
  - action
  - blocked
  - info request
- human review can:
  - approve
  - request changes
  - reschedule
  - block
- every step is visible in MM
- no second task scheduler exists outside MM
