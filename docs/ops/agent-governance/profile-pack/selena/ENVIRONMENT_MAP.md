# Selena Environment Map

Last updated: `2026-05-07`

## Canonical Files

- Profile: `/Users/moufdi/.brm-hermes/profiles/selena`
- Config: `/Users/moufdi/.brm-hermes/profiles/selena/config.yaml`
- Workdir: `~/.openclaw/workspace-selena`
- Canonical environment: `support-risk`

## Readable External Surfaces

- `paypal`
- `zendesk`
- `reviewed-support-exports`

## Mutable External Surfaces

- `local-report-artifacts`

## Approval-Gated Surfaces

- `zendesk-reply`
- `paypal-dispute-message`
- `refund-or-payment-mutation`

## Platform Projection

Platform permissions are projected from `/Users/moufdi/openclaw-governance-clean/docs/ops/agent-governance/agent-platform-access-matrix.yaml`.

- Visible platforms: `4`
- Read-allowed platforms: `4`
- Write-conditional platforms: `4`

## Environment Rules

- Resolve brand/account/tenant before reading a brand-scoped platform.
- A missing surface blocks only that surface, not unrelated brand work.
- Never print, copy, or commit secret values.
- External mutation requires route/approval/proof even when a platform is visible.
