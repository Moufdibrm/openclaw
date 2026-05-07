# Safir Role Permissions

Last updated: `2026-05-07`

Source of truth: `docs/ops/agent-governance/AGENT_PROFILE_STANDARD.md` plus the agent governance matrices listed below.

## Current State

- Agent: `safir`
- Status: `beta`
- Role: Email and CRM audit, email workflow design and drafting.
- Canonical environment: `email-crm`
- Workdir: `~/.openclaw/workspace-safir`

## Autonomy

- `audit_read`
- `discussion_approval`
- `autonomous_e2e_validated_route`

## Allowed Skill Families

- `ms365-mail-read`
- `klaviyo-read`
- `email-template-analysis`
- `image-design-for-email`
- `creative-asset-request-via-kanye`
- `filesystem-reporting`

## Forbidden Or Approval-Gated

- `direct-higgsfield-generation`
- `external-email-send-without-approval`
- `crm-mutation-without-route-and-approval`

## Global Approval Gates

- `outbound_external_message`
- `customer_visible_support_reply`
- `paypal_or_dispute_message`
- `refund_payment_billing_or_financial_mutation`
- `ambiguous_target_or_delta`

## Platform Access

Summary: `8` visible, `8` read-allowed, `8` write-conditional.

| Platform | Status | Visibility | Read | Write | Approval gates |
| --- | --- | --- | --- | --- | --- |
| `klaviyo` | `partial` | `primary_owner` | yes | route_or_approval_gated_owner | external_email_send, crm_mutation, flow_activation, segment_mutation |
| `ms365-mail` | `beta` | `secondary_owner` | yes | route_or_approval_gated_secondary | external_email_send |
| `lark-messages` | `beta` | `secondary_owner` | yes | route_or_approval_gated_secondary | external_or_team_message_send |
| `lark-tables` | `beta` | `secondary_owner` | yes | route_or_approval_gated_secondary | table_mutation_when_business_effect |
| `openai` | `beta` | `secondary_owner` | yes | route_or_approval_gated_secondary | external_send_of_generated_content |
| `anthropic` | `beta` | `secondary_owner` | yes | route_or_approval_gated_secondary | external_send_of_generated_content |
| `google-gemini` | `beta` | `secondary_owner` | yes | route_or_approval_gated_secondary | external_send_of_generated_content |
| `brand-packs` | `beta` | `secondary_owner` | yes | route_or_approval_gated_secondary | ambiguous_brand_or_account_mapping_change |

Write-conditional means the agent may write only after route, target, approval gate, and proof target are resolved. Installed skills do not grant permission.
