# Alfred Role Permissions

Last updated: `2026-05-07`

Source of truth: `docs/ops/agent-governance/AGENT_PROFILE_STANDARD.md` plus the agent governance matrices listed below.

## Current State

- Agent: `alfred`
- Status: `beta`
- Role: SEO visibility, strategy plan, deployment feedback artifacts.
- Canonical environment: `seo`
- Workdir: `~/.openclaw/workspace-alfred`

## Autonomy

- `audit_read`
- `discussion_approval`
- `autonomous_e2e_validated_route`

## Allowed Skill Families

- `gsc-read`
- `dataforseo-read`
- `ga4-read`
- `site-audit-read`
- `filesystem-reporting`
- `google-drive-approval-gated`

## Forbidden Or Approval-Gated

- `site-or-theme-mutation-without-route`
- `external-publication-without-approval`

## Global Approval Gates

- `outbound_external_message`
- `customer_visible_support_reply`
- `paypal_or_dispute_message`
- `refund_payment_billing_or_financial_mutation`
- `ambiguous_target_or_delta`

## Platform Access

Summary: `9` visible, `9` read-allowed, `7` write-conditional.

| Platform | Status | Visibility | Read | Write | Approval gates |
| --- | --- | --- | --- | --- | --- |
| `shopify` | `partial` | `secondary_owner` | yes | route_or_approval_gated_secondary | product_or_theme_publication, storefront_mutation, customer_or_order_mutation |
| `ga4` | `partial` | `secondary_owner` | yes | route_or_approval_gated_secondary | analytics_config_mutation |
| `google-search-console` | `prod` | `primary_owner` | yes | route_or_approval_gated_owner | site_or_property_mutation |
| `dataforseo` | `prod` | `primary_owner` | yes | no | costly_bulk_query |
| `public-site-rendering` | `beta` | `primary_owner` | yes | no | site_or_theme_mutation |
| `google-drive` | `partial` | `secondary_owner` | yes | route_or_approval_gated_secondary | drive_upload_or_external_delivery |
| `brand-packs` | `beta` | `secondary_owner` | yes | route_or_approval_gated_secondary | ambiguous_brand_or_account_mapping_change |
| `cloudflare` | `partial` | `secondary_owner` | yes | route_or_approval_gated_secondary | dns_or_edge_mutation |
| `godaddy` | `partial` | `secondary_owner` | yes | route_or_approval_gated_secondary | domain_or_dns_mutation |

Write-conditional means the agent may write only after route, target, approval gate, and proof target are resolved. Installed skills do not grant permission.
