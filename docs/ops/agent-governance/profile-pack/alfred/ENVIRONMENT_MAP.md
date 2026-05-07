# Alfred Environment Map

Last updated: `2026-05-07`

## Canonical Files

- Profile: `/Users/moufdi/.brm-hermes/profiles/alfred`
- Config: `/Users/moufdi/.brm-hermes/profiles/alfred/config.yaml`
- Workdir: `~/.openclaw/workspace-alfred`
- Canonical environment: `seo`

## Readable External Surfaces

- `gsc`
- `dataforseo`
- `ga4`
- `site-rendering`

## Mutable External Surfaces

- `local-report-artifacts`

## Approval-Gated Surfaces

- `drive-upload`
- `site-or-theme-mutation`

## Platform Projection

Platform permissions are projected from `docs/ops/agent-governance/agent-platform-access-matrix.yaml`.

- Visible platforms: `9`
- Read-allowed platforms: `9`
- Write-conditional platforms: `7`

## Environment Rules

- Resolve brand/account/tenant before reading a brand-scoped platform.
- A missing surface blocks only that surface, not unrelated brand work.
- Never print, copy, or commit secret values.
- External mutation requires route/approval/proof even when a platform is visible.
