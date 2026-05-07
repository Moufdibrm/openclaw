# Jack-X Role Permissions

Last updated: `2026-05-07`

Source of truth: `/Users/moufdi/openclaw-governance-clean/docs/ops/agent-governance/AGENT_PROFILE_STANDARD.md` plus the agent governance matrices listed below.

## Current State

- Agent: `jack-x`
- Status: `beta`
- Role: Long-term memory, channel intake, KG and memory updates, plus review of Memory Wiki refinement proposals.
- Canonical environment: `memory/intake`
- Workdir: `/Users/moufdi/.openclaw/workspace-jack-x`

## Autonomy

- `audit_read`
- `autonomous_e2e_validated_route`

## Allowed Skill Families

- `ms365-mail-read`
- `lark-read`
- `whatsapp-snapshot-read`
- `mission-manager-agent-session-read`
- `memory-wiki`
- `kg-memory-update-governed`
- `memory-refinement-review`
- `filesystem-memory-artifacts`

## Forbidden Or Approval-Gated

- `external-message-send`
- `payment-or-support-mutation`
- `business-system-mutation`
- `llm-wiki-direct-kg-write`

## Global Approval Gates

- `outbound_external_message`
- `customer_visible_support_reply`
- `paypal_or_dispute_message`
- `refund_payment_billing_or_financial_mutation`
- `ambiguous_target_or_delta`

## Platform Access

Summary: `9` visible, `9` read-allowed, `9` write-conditional.

| Platform | Status | Visibility | Read | Write | Approval gates |
| --- | --- | --- | --- | --- | --- |
| `ms365-mail` | `beta` | `primary_owner` | yes | route_or_approval_gated_owner | external_email_send |
| `whatsapp` | `beta` | `secondary_owner` | yes | route_or_approval_gated_secondary | outbound_external_message, multi_target_fanout |
| `lark-messages` | `beta` | `primary_owner` | yes | route_or_approval_gated_owner | external_or_team_message_send |
| `lark-tables` | `beta` | `primary_owner` | yes | route_or_approval_gated_owner | table_mutation_when_business_effect |
| `google-gemini` | `beta` | `secondary_owner` | yes | route_or_approval_gated_secondary | external_send_of_generated_content |
| `kimi` | `beta` | `secondary_owner` | yes | route_or_approval_gated_secondary |  |
| `mission-manager` | `beta` | `secondary_owner` | yes | route_or_approval_gated_secondary | product_implementation_or_schema_change |
| `knowledge-graph` | `beta` | `primary_owner` | yes | route_or_approval_gated_owner | high_risk_memory_commit, ambiguous_identity_merge |
| `memory-wiki` | `beta` | `primary_owner` | yes | route_or_approval_gated_owner | promotion_to_durable_kg |

Write-conditional means the agent may write only after route, target, approval gate, and proof target are resolved. Installed skills do not grant permission.
