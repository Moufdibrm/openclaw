# Tony Role Permissions

Last updated: `2026-05-07`

Source of truth: `/Users/moufdi/openclaw-governance-clean/docs/ops/agent-governance/AGENT_PROFILE_STANDARD.md` plus the agent governance matrices listed below.

## Current State

- Agent: `tony`
- Status: `beta`
- Role: Development owner: codebase exploration, planning, implementation, tests, git.
- Canonical environment: `development`
- Workdir: `~/.openclaw/workspace-tony`

## Autonomy

- `audit_read`
- `discussion_approval`
- `autonomous_e2e_validated_route`

## Allowed Skill Families

- `repository-filesystem`
- `terminal`
- `git`
- `github`
- `package-managers`
- `tests-build-lint`
- `browser-dev-verification`

## Forbidden Or Approval-Gated

- `production-deploy-or-restart-without-explicit-delegation`
- `gateway-runtime-systemd-edits-in-this-governance-lane`
- `mission-manager-product-lane-ownership`
- `business-system-mutation`
- `external-message-sending`

## Global Approval Gates

- `outbound_external_message`
- `customer_visible_support_reply`
- `paypal_or_dispute_message`
- `refund_payment_billing_or_financial_mutation`
- `ambiguous_target_or_delta`

## Platform Access

Summary: `22` visible, `13` read-allowed, `12` write-conditional.

| Platform | Status | Visibility | Read | Write | Approval gates |
| --- | --- | --- | --- | --- | --- |
| `shopify` | `partial` | `secondary_owner` | yes | route_or_approval_gated_secondary | product_or_theme_publication, storefront_mutation, customer_or_order_mutation |
| `recharge` | `partial` | `partial_observer` | no | no | subscription_or_billing_mutation |
| `klaviyo` | `partial` | `partial_observer` | no | no | external_email_send, crm_mutation, flow_activation, segment_mutation |
| `meta-ads` | `partial` | `partial_observer` | no | no | campaign_publication_or_ad_mutation, budget_mutation |
| `google-ads` | `partial` | `partial_observer` | no | no | campaign_publication_or_ad_mutation, budget_mutation |
| `ga4` | `partial` | `partial_observer` | no | no | analytics_config_mutation |
| `public-site-rendering` | `beta` | `secondary_owner` | yes | no | site_or_theme_mutation |
| `instagram-graph` | `partial` | `partial_observer` | no | no | external_message_send, publication_or_account_mutation |
| `apify` | `partial` | `partial_observer` | no | no | costly_or_unbounded_actor_run |
| `google-drive` | `partial` | `partial_observer` | no | no | drive_upload_or_external_delivery |
| `openai` | `beta` | `primary_owner` | yes | route_or_approval_gated_owner | external_send_of_generated_content |
| `kimi` | `beta` | `primary_owner` | yes | route_or_approval_gated_owner |  |
| `route-registry` | `prod` | `secondary_owner` | yes | route_or_approval_gated_secondary | runtime_registry_mutation |
| `protocol-packages` | `beta` | `secondary_owner` | yes | route_or_approval_gated_secondary | package_promotes_external_mutation |
| `hippocampus` | `partial` | `partial_observer` | no | no | runtime_wiring_change |
| `local-repositories` | `prod` | `primary_owner` | yes | route_or_approval_gated_owner | forbidden_path_change, destructive_change |
| `git-github` | `beta` | `primary_owner` | yes | route_or_approval_gated_owner | push_or_pr_when_not_requested, destructive_git_operation |
| `package-registries` | `partial` | `primary_owner` | yes | route_or_approval_gated_owner | broad_dependency_or_executable_install |
| `aws` | `prod` | `secondary_owner` | yes | route_or_approval_gated_secondary | infra_dns_secret_deploy_restart_mutation |
| `aws-secrets-manager` | `prod` | `secondary_owner` | yes | route_or_approval_gated_secondary | secret_value_read, secret_write, secret_rotation |
| `cloudflare` | `partial` | `primary_owner` | yes | route_or_approval_gated_owner | dns_or_edge_mutation |
| `godaddy` | `partial` | `primary_owner` | yes | route_or_approval_gated_owner | domain_or_dns_mutation |

Write-conditional means the agent may write only after route, target, approval gate, and proof target are resolved. Installed skills do not grant permission.
