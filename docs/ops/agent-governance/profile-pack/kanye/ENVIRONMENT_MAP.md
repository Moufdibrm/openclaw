# Kanye Environment Map

Last updated: `2026-05-07`

## Canonical Files

- Profile: `/Users/moufdi/.brm-hermes/profiles/kanye`
- Config: `/Users/moufdi/.brm-hermes/profiles/kanye/config.yaml`
- Workdir: `~/.openclaw/workspace-kanye`
- Canonical environment: `creative-generation`

## Readable External Surfaces

- `reference-media`
- `creative-inputs`
- `higgsfield-api-auth-presence`

## Mutable External Surfaces

- `generated-media-artifacts`
- `higgsfield-generated-media-test-artifacts`

## Approval-Gated Surfaces

- `external-publication`
- `paid-delivery-platform-mutation`

## Platform Projection

Platform permissions are projected from `docs/ops/agent-governance/agent-platform-access-matrix.yaml`.

- Visible platforms: `6`
- Read-allowed platforms: `6`
- Write-conditional platforms: `6`

## Environment Rules

- Resolve brand/account/tenant before reading a brand-scoped platform.
- A missing surface blocks only that surface, not unrelated brand work.
- Never print, copy, or commit secret values.
- External mutation requires route/approval/proof even when a platform is visible.
