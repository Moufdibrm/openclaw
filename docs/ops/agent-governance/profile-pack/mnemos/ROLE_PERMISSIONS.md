# Mnemos Role Permissions

Last updated: `2026-05-07`

Source of truth: `docs/ops/agent-governance/AGENT_PROFILE_STANDARD.md` plus the agent governance matrices listed below.

## Current State

- Agent: `mnemos`
- Status: `beta`
- Role: Continuity, context pressure, compaction and reinjection capsules.
- Canonical environment: `continuity/local-session`
- Workdir: `/Users/moufdi/.openclaw/workspace-mnemos`

## Autonomy

- `audit_read`
- `autonomous_e2e_validated_route`

## Allowed Skill Families

- `local-session-state`
- `context-metering`
- `continuity-artifacts`
- `filesystem-local`

## Forbidden Or Approval-Gated

- `external-read`
- `external-write`
- `business-execution`
- `durable-kg-ownership`

## Global Approval Gates

- `outbound_external_message`
- `customer_visible_support_reply`
- `paypal_or_dispute_message`
- `refund_payment_billing_or_financial_mutation`
- `ambiguous_target_or_delta`

## Platform Access

Summary: `1` visible, `1` read-allowed, `1` write-conditional.

| Platform | Status | Visibility | Read | Write | Approval gates |
| --- | --- | --- | --- | --- | --- |
| `mnemos-continuity` | `beta` | `primary_owner` | yes | route_or_approval_gated_owner |  |

Write-conditional means the agent may write only after route, target, approval gate, and proof target are resolved. Installed skills do not grant permission.
