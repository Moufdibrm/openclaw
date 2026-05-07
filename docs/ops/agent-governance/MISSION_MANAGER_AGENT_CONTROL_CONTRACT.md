# Mission Manager Agent Control Contract

Last updated: `2026-05-07`

This contract defines what Mission Manager may consume and control about BRM/Hermes agents.

It is a governance handoff only. It does not implement Mission Manager, gateway, runtime, deploy, restart, systemd, or VPS release behavior.

Machine-readable companion:

- `mission-manager-agent-control-contract.yaml`
- `agent-profile-materialization-manifest.yaml`

## Source Of Truth

Mission Manager should treat these files as the governance source for agent control:

- `agent-toolbox-matrix.yaml`: agent role, autonomy, allowed skills, denied/gated skills.
- `agent-environment-matrix.yaml`: profile, config, workdir, canonical environment, external surfaces.
- `agent-protocol-matrix.yaml`: route/protocol ids, route maturity, proof targets.
- `agent-platform-access-matrix.yaml`: platform visibility, read access, write conditions, approval gates.
- `agent-profile-materialization-manifest.yaml`: local profile files that have been materialized on this machine.

Mission Manager should not infer permissions from installed skills or from profile files alone.

## Control Levels

Mission Manager may model these control levels:

| Level | Meaning | External mutation |
| --- | --- | --- |
| `view_governance` | Display agent scope, tools, platforms, routes, proof targets, and profile health. | no |
| `request_audit_read` | Create an audit/read task for an agent. | no |
| `request_discussion_approval` | Create a task that prepares an action or asks for approval. | no |
| `launch_validated_route` | Launch a route that already exists and is mature enough for the requested scope. | only if route and gates allow |
| `record_approval_decision` | Record operator approval or rejection for a gated action. | decision only |
| `request_governance_change` | Ask Jack/governance lane to update permissions/toolbox/protocol docs. | local governance only |

No control level grants direct gateway edit, deployment, restart, systemd action, or Mission Manager product implementation.

## Agent Card

An MM agent card should display:

- agent id, role, status, canonical environment, profile path, config path, workdir
- autonomy levels
- allowed skill families
- forbidden/gated actions
- visible/read/write platform counts
- platform detail with read surfaces, write surfaces, approval gates, and proof targets
- current routes with status and proof target
- required profile sidecars and materialization state
- unresolved gaps or route maturity blockers

## Action Request

Any MM action request toward an agent should carry:

- `mission_id` and `task_id`
- `requested_by`
- `agent_id`
- `autonomy_level`
- `route_id` when route-backed
- `platform_id` when platform-backed
- `brand_scope` when brand-linked
- `read_or_write`
- `external_mutation`
- `approval_gate_refs`
- `input_artifacts`
- `expected_outputs`
- `proof_targets`
- `blocked_reason` when the request cannot run safely

If `route_id` is missing for repeated work, MM should open `jack.protocol-missing`.
If the capability/tool/platform is missing, MM should open `jack.capability-missing`.

## Approval Gates

MM must require explicit approval before:

- outbound external messages
- customer-visible support replies
- PayPal/dispute messages
- refunds, payment, billing, or financial mutations
- external publication or paid delivery platform mutation
- voice clone or external audio send
- ambiguous target or ambiguous delta

Approval should be recorded as a first-class MM event before the route executes the gated step.

## Jack Rule

Jack sees every governed platform for routing, supervision, gap detection, and governed direct execution.
This is not blanket mutation.
Every write still requires target resolution, a route or explicit approval, and proof.

## Tony Rule

Tony sees partial platforms for development and audit context.
That visibility is not business-platform permission.
Business mutation still belongs to the owning agent, route, and approval gate.

## Specialist Rule

Specialists see only owned, secondary-owned, route-owned, or explicitly selected platforms.
If a platform is partial and not assigned to the specialist, MM should not present it as a usable specialist surface.

## Kanye Rule

Kanye may select creative provider mode:

- `higgsfield`: default
- `banana`: Nano Banana / Gemini image route
- `openai`: OpenAI image route

Provider selection never bypasses publication, delivery, external-send, paid-mutation, or voice-clone gates.

## Profile Materialization

The current local Mac profile materialization is described by `agent-profile-materialization-manifest.yaml`.

MM should use it for visibility and health checks, not as a direct write target.
Profile writes should go through a governed sync/apply procedure with dry-run, path allowlist, no secret output, and no reserved-file writes.

## Non-Negotiables

- No fake done from MM state alone.
- Runtime proof and artifact proof must be attached to mission/task truth.
- Installed skills are not permissions.
- Agent status uses only `draft`, `beta`, `prod`.
- Route status uses only `draft`, `beta`, `prod`.
- Missing brand surfaces block only that surface, not unrelated brand work.
- Do not mutate runtime/gateway/deploy/MM files from this governance lane.
