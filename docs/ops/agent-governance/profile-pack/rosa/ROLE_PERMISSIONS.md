# Rosa Role Permissions

Last updated: `2026-05-07`

Source of truth: `/Users/moufdi/openclaw-governance-clean/docs/ops/agent-governance/AGENT_PROFILE_STANDARD.md` plus the agent governance matrices listed below.

## Current State

- Agent: `rosa`
- Status: `beta`
- Role: Marketing, offers, performance, market intelligence.
- Canonical environment: `marketing`
- Workdir: `~/.openclaw/workspace-rosa`

## Autonomy

- `audit_read`
- `discussion_approval`
- `autonomous_e2e_validated_route`

## Allowed Skill Families

- `shopify-read`
- `klaviyo-read`
- `hiboo-read`
- `lark-read`
- `ga4-read`
- `gsc-read`
- `dataforseo-read`
- `creative-asset-request-via-kanye`
- `filesystem-reporting`

## Forbidden Or Approval-Gated

- `direct-higgsfield-generation`
- `campaign-publication-without-approval`
- `external-message-send-without-approval`
- `storefront-or-crm-mutation-without-route`

## Global Approval Gates

- `outbound_external_message`
- `customer_visible_support_reply`
- `paypal_or_dispute_message`
- `refund_payment_billing_or_financial_mutation`
- `ambiguous_target_or_delta`

## Platform Access

Summary: `14` visible, `14` read-allowed, `13` write-conditional.

| Platform | Status | Visibility | Read | Write | Approval gates |
| --- | --- | --- | --- | --- | --- |
| `shopify` | `partial` | `primary_owner` | yes | route_or_approval_gated_owner | product_or_theme_publication, storefront_mutation, customer_or_order_mutation |
| `recharge` | `partial` | `secondary_owner` | yes | route_or_approval_gated_secondary | subscription_or_billing_mutation |
| `klaviyo` | `partial` | `secondary_owner` | yes | route_or_approval_gated_secondary | external_email_send, crm_mutation, flow_activation, segment_mutation |
| `hiboo-core` | `beta` | `secondary_owner` | yes | route_or_approval_gated_secondary | collaboration_create_update_archive, supplier_order_purchase_mutation |
| `meta-ads` | `partial` | `secondary_owner` | yes | route_or_approval_gated_secondary | campaign_publication_or_ad_mutation, budget_mutation |
| `google-ads` | `partial` | `secondary_owner` | yes | route_or_approval_gated_secondary | campaign_publication_or_ad_mutation, budget_mutation |
| `hiboo-ads` | `beta` | `secondary_owner` | yes | route_or_approval_gated_secondary | campaign_publication_or_ad_mutation |
| `ga4` | `partial` | `primary_owner` | yes | route_or_approval_gated_owner | analytics_config_mutation |
| `google-search-console` | `prod` | `secondary_owner` | yes | route_or_approval_gated_secondary | site_or_property_mutation |
| `dataforseo` | `prod` | `secondary_owner` | yes | no | costly_bulk_query |
| `lark-messages` | `beta` | `secondary_owner` | yes | route_or_approval_gated_secondary | external_or_team_message_send |
| `lark-tables` | `beta` | `secondary_owner` | yes | route_or_approval_gated_secondary | table_mutation_when_business_effect |
| `anthropic` | `beta` | `secondary_owner` | yes | route_or_approval_gated_secondary | external_send_of_generated_content |
| `brand-packs` | `beta` | `secondary_owner` | yes | route_or_approval_gated_secondary | ambiguous_brand_or_account_mapping_change |

Write-conditional means the agent may write only after route, target, approval gate, and proof target are resolved. Installed skills do not grant permission.
