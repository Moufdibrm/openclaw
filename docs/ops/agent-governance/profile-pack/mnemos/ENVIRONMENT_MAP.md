# Mnemos Environment Map

Last updated: `2026-05-07`

## Canonical Files

- Profile: `/Users/moufdi/.brm-hermes/profiles/mnemos`
- Config: `/Users/moufdi/.brm-hermes/profiles/mnemos/config.yaml`
- Workdir: `/Users/moufdi/.openclaw/workspace-mnemos`
- Canonical environment: `continuity/local-session`

## Readable External Surfaces

- none declared

## Mutable External Surfaces

- `continuity-journal`
- `compaction-capsules`

## Approval-Gated Surfaces

- none declared

## Platform Projection

Platform permissions are projected from `/Users/moufdi/openclaw-governance-clean/docs/ops/agent-governance/agent-platform-access-matrix.yaml`.

- Visible platforms: `1`
- Read-allowed platforms: `1`
- Write-conditional platforms: `1`

## Environment Rules

- Resolve brand/account/tenant before reading a brand-scoped platform.
- A missing surface blocks only that surface, not unrelated brand work.
- Never print, copy, or commit secret values.
- External mutation requires route/approval/proof even when a platform is visible.
