# Kanye Role Permissions

Last updated: `2026-05-07`

Source of truth: `docs/ops/agent-governance/AGENT_PROFILE_STANDARD.md` plus the agent governance matrices listed below.

## Current State

- Agent: `kanye`
- Status: `beta`
- Role: Creative generation and reference edits.
- Canonical environment: `creative-generation`
- Workdir: `~/.openclaw/workspace-kanye`

## Autonomy

- `audit_read`
- `discussion_approval`
- `autonomous_e2e_validated_route`

## Allowed Skill Families

- `creative-generation`
- `image-edit`
- `video-generation`
- `higgsfield-ai-official-skill`
- `reference-media-read`
- `filesystem-media-artifacts`

## Forbidden Or Approval-Gated

- `external-campaign-publication-without-approval`
- `paid-delivery-or-platform-mutation-without-approval`

## Global Approval Gates

- `outbound_external_message`
- `customer_visible_support_reply`
- `paypal_or_dispute_message`
- `refund_payment_billing_or_financial_mutation`
- `ambiguous_target_or_delta`

## Platform Access

Summary: `6` visible, `6` read-allowed, `6` write-conditional.

| Platform | Status | Visibility | Read | Write | Approval gates |
| --- | --- | --- | --- | --- | --- |
| `hiboo-ads` | `beta` | `secondary_owner` | yes | route_or_approval_gated_secondary | campaign_publication_or_ad_mutation |
| `higgsfield` | `beta` | `primary_owner` | yes | route_or_approval_gated_owner | external_publication, paid_delivery_platform_mutation, voice_clone_without_consent |
| `banana` | `beta` | `primary_owner` | yes | route_or_approval_gated_owner | external_publication, paid_delivery_platform_mutation |
| `seedance` | `draft` | `primary_owner` | yes | route_or_approval_gated_owner | external_publication |
| `openai` | `beta` | `secondary_owner` | yes | route_or_approval_gated_secondary | external_send_of_generated_content |
| `package-registries` | `partial` | `secondary_owner` | yes | route_or_approval_gated_secondary | broad_dependency_or_executable_install |

Write-conditional means the agent may write only after route, target, approval gate, and proof target are resolved. Installed skills do not grant permission.

## Creative Provider Policy

- Default provider: `higgsfield`
- Selectable providers: `higgsfield`, `banana`, `openai`
- Route aliases: `higgsfield_image`, `higgsfield_video`, `nanobanana_2`, `openai_premium`
- Publication, external send, paid delivery mutation, and voice clone work remain approval-gated.
