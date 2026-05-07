# Naya Environment Map

Last updated: `2026-05-07`

## Canonical Files

- Profile: `/Users/moufdi/.brm-hermes/profiles/naya`
- Config: `/Users/moufdi/.brm-hermes/profiles/naya/config.yaml`
- Workdir: `~/.openclaw/workspace-naya`
- Canonical environment: `supply-chain`

## Readable External Surfaces

- `shopify`
- `bigblue`
- `stock-telemetry`
- `sourcing-sheets`

## Mutable External Surfaces

- `local-report-artifacts`

## Approval-Gated Surfaces

- `supplier-message-send`
- `order-or-purchase-mutation`
- `payment-mutation`

## Platform Projection

Platform permissions are projected from `/Users/moufdi/openclaw-governance-clean/docs/ops/agent-governance/agent-platform-access-matrix.yaml`.

- Visible platforms: `9`
- Read-allowed platforms: `9`
- Write-conditional platforms: `9`

## Environment Rules

- Resolve brand/account/tenant before reading a brand-scoped platform.
- A missing surface blocks only that surface, not unrelated brand work.
- Never print, copy, or commit secret values.
- External mutation requires route/approval/proof even when a platform is visible.
