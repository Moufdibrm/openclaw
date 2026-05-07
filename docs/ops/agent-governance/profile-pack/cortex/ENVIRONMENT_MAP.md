# Cortex Environment Map

Last updated: `2026-05-07`

## Canonical Files

- Profile: `/Users/moufdi/.brm-hermes/profiles/cortex`
- Config: `/Users/moufdi/.brm-hermes/profiles/cortex/config.yaml`
- Workdir: `~/.openclaw/workspace-cortex`
- Canonical environment: `paid-media`

## Readable External Surfaces

- `hiboo-ads`
- `meta-ads`
- `google-ads`
- `creative-reference-artifacts`

## Mutable External Surfaces

- `local-report-artifacts`

## Approval-Gated Surfaces

- `campaign-mutation`
- `ad-publication`

## Platform Projection

Platform permissions are projected from `docs/ops/agent-governance/agent-platform-access-matrix.yaml`.

- Visible platforms: `8`
- Read-allowed platforms: `8`
- Write-conditional platforms: `8`

## Environment Rules

- Resolve brand/account/tenant before reading a brand-scoped platform.
- A missing surface blocks only that surface, not unrelated brand work.
- Never print, copy, or commit secret values.
- External mutation requires route/approval/proof even when a platform is visible.
