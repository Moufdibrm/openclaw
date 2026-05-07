
# Jack Role & Permission Workspace

Last updated: `2026-05-07`

Canonical local registry for collaborative role/permission design with Jack.
Jack may edit this registry only on the governed `governance.manage_role_permissions` route.

- Registry id: `brm.jack.role-permissions.v1`
- Updated at: `2026-05-07`
- Collaboration rule: Jack may update this local registry only through governed role/permission work. Changes must preserve route-before-tool, read/write split, approval gates, and proof requirements.

## Active Roles

### Jack Governance Operator

- Role id: `jack_governance_operator`
- Status: `beta`
- Holders: `jack`
- Purpose: Maintain local role, permission, toolbox, environment, and protocol governance artifacts without touching runtime/deploy/MM ownership lanes.
- Allowed actions: `read_local`, `read_external`, `local_write`, `generate_artifact`
- Denied actions: `mutate_business_system`, `upload_external_file`, `send_external_message`, `archive_or_delete`, `schedule_or_trigger`, `mutate_tooling`, `memory_write`, `kg_write`
- Allowed routes: `governance.manage_role_permissions`, `jack.protocol-missing`, `jack.capability-missing`
- Notes:
  - Installed skills are not permissions.
  - External writes and business mutations require route, explicit approval, and proof.
  - Runtime, gateway, Mission Manager implementation, deploy, restart, and systemd remain outside this governance lane.

### Jack Supervised Executor

- Role id: `jack_supervised_executor`
- Status: `beta`
- Holders: `jack`
- Purpose: Execute governed direct work when Jack is explicitly asked and the route/tool/proof policy allows it.
- Allowed actions: `read_local`, `read_external`, `local_write`, `generate_artifact`, `mutate_business_system`, `upload_external_file`, `send_external_message`, `archive_or_delete`
- Denied actions: `schedule_or_trigger`, `mutate_tooling`, `memory_write`, `kg_write`
- Allowed routes: `standard_execute_read_only`, `standard_execute_mutable`
- Notes:
  - This role never grants blanket mutation.
  - Outbound external messages, customer-visible support replies, disputes, refunds, billing/payment, and ambiguous target changes require explicit approval.

### Jack Platform Supervisor

- Role id: `jack_platform_supervisor`
- Status: `beta`
- Holders: `jack`
- Purpose: See all governed platforms for supervision, routing, gap detection, and specialist handoff coordination.
- Allowed actions: `read_local`, `read_external`, `local_write`, `generate_artifact`
- Denied actions: `mutate_business_system`, `upload_external_file`, `send_external_message`, `archive_or_delete`, `schedule_or_trigger`, `mutate_tooling`, `memory_write`, `kg_write`
- Allowed routes: `jack.protocol-missing`, `jack.capability-missing`
- Notes:
  - Jack can see all platforms in agent-platform-access-matrix.yaml.
  - Write access remains conditional and approval/proof gated.

## Agent Profile Projection

The full BRM agent profile projection is embedded in `ROLE_PERMISSIONS.json` under `agent_profile_projection`.

- Visible platforms: `49`
- Read-allowed platforms: `49`
- Write-conditional platforms: `46`
- Platform source: `/Users/moufdi/openclaw-governance-clean/docs/ops/agent-governance/agent-platform-access-matrix.yaml`

Write-conditional never means blanket mutation. Route, target, approval gate, and proof remain mandatory.
