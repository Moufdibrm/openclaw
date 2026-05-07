# Naya Role Permissions

Last updated: `2026-05-07`

Source of truth: `docs/ops/agent-governance/AGENT_PROFILE_STANDARD.md` plus the agent governance matrices listed below.

## Current State

- Agent: `naya`
- Status: `beta`
- Role: Stock, sourcing, supply chain and operational feasibility.
- Canonical environment: `supply-chain`
- Workdir: `~/.openclaw/workspace-naya`

## Autonomy

- `audit_read`
- `discussion_approval`
- `autonomous_e2e_validated_route`

## Allowed Skill Families

- `shopify-read`
- `bigblue-read`
- `stock-telemetry`
- `sourcing-sheets`
- `filesystem-reporting`
- `google-drive-approval-gated`

## Forbidden Or Approval-Gated

- `supplier-message-send-without-approval`
- `order-or-purchase-mutation-without-approval`
- `payment-mutation-without-approval`

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
| `shopify` | `partial` | `secondary_owner` | yes | route_or_approval_gated_secondary | product_or_theme_publication, storefront_mutation, customer_or_order_mutation |
| `recharge` | `partial` | `primary_owner` | yes | route_or_approval_gated_owner | subscription_or_billing_mutation |
| `bigblue` | `beta` | `primary_owner` | yes | route_or_approval_gated_owner | order_or_purchase_mutation, supplier_order_purchase_mutation |
| `hiboo-core` | `beta` | `primary_owner` | yes | route_or_approval_gated_owner | collaboration_create_update_archive, supplier_order_purchase_mutation |
| `sourcing-sheets` | `draft` | `primary_owner` | yes | route_or_approval_gated_owner | supplier_message_send, order_or_purchase_mutation |
| `lark-messages` | `beta` | `secondary_owner` | yes | route_or_approval_gated_secondary | external_or_team_message_send |
| `lark-tables` | `beta` | `secondary_owner` | yes | route_or_approval_gated_secondary | table_mutation_when_business_effect |
| `google-drive` | `partial` | `secondary_owner` | yes | route_or_approval_gated_secondary | drive_upload_or_external_delivery |
| `brand-packs` | `beta` | `secondary_owner` | yes | route_or_approval_gated_secondary | ambiguous_brand_or_account_mapping_change |

Write-conditional means the agent may write only after route, target, approval gate, and proof target are resolved. Installed skills do not grant permission.
