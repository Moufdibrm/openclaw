# Jeff Role Permissions

Last updated: `2026-05-07`

Source of truth: `docs/ops/agent-governance/AGENT_PROFILE_STANDARD.md` plus the agent governance matrices listed below.

## Current State

- Agent: `jeff`
- Status: `beta`
- Role: Influence, creator operations, outreach, collaboration analysis.
- Canonical environment: `influence/creator-ops`
- Workdir: `~/.openclaw/workspace-jeff`

## Autonomy

- `audit_read`
- `discussion_approval`
- `autonomous_e2e_validated_route`

## Allowed Skill Families

- `hiboo-creators`
- `creator-profile-read`
- `inbox-signal-read`
- `candidate-registry`
- `filesystem-reporting`
- `google-drive-approval-gated`

## Forbidden Or Approval-Gated

- `creator-contact-send-without-approval`
- `collaboration-mutation-without-approval`
- `payment-or-contract-mutation-without-approval`

## Global Approval Gates

- `outbound_external_message`
- `customer_visible_support_reply`
- `paypal_or_dispute_message`
- `refund_payment_billing_or_financial_mutation`
- `ambiguous_target_or_delta`

## Platform Access

Summary: `5` visible, `5` read-allowed, `5` write-conditional.

| Platform | Status | Visibility | Read | Write | Approval gates |
| --- | --- | --- | --- | --- | --- |
| `hiboo-core` | `beta` | `secondary_owner` | yes | route_or_approval_gated_secondary | collaboration_create_update_archive, supplier_order_purchase_mutation |
| `instagram-public` | `beta` | `primary_owner` | yes | route_or_approval_gated_owner | creator_contact_send, collaboration_create_update_archive |
| `instagram-graph` | `partial` | `primary_owner` | yes | route_or_approval_gated_owner | external_message_send, publication_or_account_mutation |
| `apify` | `partial` | `primary_owner` | yes | route_or_approval_gated_owner | costly_or_unbounded_actor_run |
| `google-drive` | `partial` | `secondary_owner` | yes | route_or_approval_gated_secondary | drive_upload_or_external_delivery |

Write-conditional means the agent may write only after route, target, approval gate, and proof target are resolved. Installed skills do not grant permission.
