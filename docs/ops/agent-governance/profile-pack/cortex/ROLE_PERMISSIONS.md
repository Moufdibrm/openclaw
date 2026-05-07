# Cortex Role Permissions

Last updated: `2026-05-07`

Source of truth: `docs/ops/agent-governance/AGENT_PROFILE_STANDARD.md` plus the agent governance matrices listed below.

## Current State

- Agent: `cortex`
- Status: `beta`
- Role: Paid media observation and campaign handoff.
- Canonical environment: `paid-media`
- Workdir: `~/.openclaw/workspace-cortex`

## Autonomy

- `audit_read`
- `discussion_approval`
- `autonomous_e2e_validated_route`

## Allowed Skill Families

- `hiboo-ads-read`
- `meta-ads-read`
- `google-ads-read`
- `creative-observation`
- `creative-asset-request-via-kanye`
- `filesystem-reporting`

## Forbidden Or Approval-Gated

- `direct-higgsfield-generation`
- `live-campaign-mutation-without-approval`
- `ad-publication-without-approval`

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
| `meta-ads` | `partial` | `primary_owner` | yes | route_or_approval_gated_owner | campaign_publication_or_ad_mutation, budget_mutation |
| `google-ads` | `partial` | `primary_owner` | yes | route_or_approval_gated_owner | campaign_publication_or_ad_mutation, budget_mutation |
| `hiboo-ads` | `beta` | `primary_owner` | yes | route_or_approval_gated_owner | campaign_publication_or_ad_mutation |
| `instagram-public` | `beta` | `secondary_owner` | yes | route_or_approval_gated_secondary | creator_contact_send, collaboration_create_update_archive |
| `instagram-graph` | `partial` | `secondary_owner` | yes | route_or_approval_gated_secondary | external_message_send, publication_or_account_mutation |
| `google-drive` | `partial` | `secondary_owner` | yes | route_or_approval_gated_secondary | drive_upload_or_external_delivery |
| `google-gemini` | `beta` | `primary_owner` | yes | route_or_approval_gated_owner | external_send_of_generated_content |
| `brand-packs` | `beta` | `secondary_owner` | yes | route_or_approval_gated_secondary | ambiguous_brand_or_account_mapping_change |

Write-conditional means the agent may write only after route, target, approval gate, and proof target are resolved. Installed skills do not grant permission.
