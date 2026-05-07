# Jeff Environment Map

Last updated: `2026-05-07`

## Canonical Files

- Profile: `/Users/moufdi/.brm-hermes/profiles/jeff`
- Config: `/Users/moufdi/.brm-hermes/profiles/jeff/config.yaml`
- Workdir: `~/.openclaw/workspace-jeff`
- Canonical environment: `influence/creator-ops`

## Readable External Surfaces

- `hiboo`
- `creator-profile-inputs`
- `inbox-signal-inputs`
- `candidate-registry`

## Mutable External Surfaces

- `local-report-artifacts`
- `candidate-registry-local`

## Approval-Gated Surfaces

- `creator-contact-send`
- `collaboration-create-update-archive`

## Platform Projection

Platform permissions are projected from `docs/ops/agent-governance/agent-platform-access-matrix.yaml`.

- Visible platforms: `5`
- Read-allowed platforms: `5`
- Write-conditional platforms: `5`

## Environment Rules

- Resolve brand/account/tenant before reading a brand-scoped platform.
- A missing surface blocks only that surface, not unrelated brand work.
- Never print, copy, or commit secret values.
- External mutation requires route/approval/proof even when a platform is visible.
