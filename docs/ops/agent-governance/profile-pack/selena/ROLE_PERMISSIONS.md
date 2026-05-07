# Selena Role Permissions

Last updated: `2026-05-07`

Source of truth: `docs/ops/agent-governance/AGENT_PROFILE_STANDARD.md` plus the agent governance matrices listed below.

## Current State

- Agent: `selena`
- Status: `beta`
- Role: Support risk, PayPal disputes, Zendesk feedback review.
- Canonical environment: `support-risk`
- Workdir: `~/.openclaw/workspace-selena`

## Autonomy

- `audit_read`
- `discussion_approval`
- `autonomous_e2e_validated_route`

## Allowed Skill Families

- `paypal-read`
- `zendesk-read`
- `reviewed-export-analysis`
- `filesystem-reporting`

## Forbidden Or Approval-Gated

- `zendesk-reply-without-approval`
- `paypal-dispute-message-without-approval`
- `refund-or-payment-mutation-without-approval`

## Global Approval Gates

- `outbound_external_message`
- `customer_visible_support_reply`
- `paypal_or_dispute_message`
- `refund_payment_billing_or_financial_mutation`
- `ambiguous_target_or_delta`

## Platform Access

Summary: `4` visible, `4` read-allowed, `4` write-conditional.

| Platform | Status | Visibility | Read | Write | Approval gates |
| --- | --- | --- | --- | --- | --- |
| `recharge` | `partial` | `secondary_owner` | yes | route_or_approval_gated_secondary | subscription_or_billing_mutation |
| `zendesk` | `prod` | `primary_owner` | yes | route_or_approval_gated_owner | customer_visible_support_reply, ticket_mutation |
| `paypal` | `prod` | `primary_owner` | yes | route_or_approval_gated_owner | dispute_message, refund_payment_billing_financial_mutation |
| `anthropic` | `beta` | `secondary_owner` | yes | route_or_approval_gated_secondary | external_send_of_generated_content |

Write-conditional means the agent may write only after route, target, approval gate, and proof target are resolved. Installed skills do not grant permission.
