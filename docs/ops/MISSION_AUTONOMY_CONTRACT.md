# Mission Autonomy Contract

## Purpose

This phase turns Mission Manager from a passive tracker into an active follow-up system.

Mission Manager remains the business source of truth.
Hermes becomes the wake-and-execute layer on top of that truth.
Curator comes later and optimizes this loop; it does not replace it.

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
