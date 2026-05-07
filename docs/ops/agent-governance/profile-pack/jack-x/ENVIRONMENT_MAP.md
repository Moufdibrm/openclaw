# Jack-X Environment Map

Last updated: `2026-05-07`

## Canonical Files

- Profile: `/Users/moufdi/.brm-hermes/profiles/jack-x`
- Config: `/Users/moufdi/.brm-hermes/profiles/jack-x/config.yaml`
- Workdir: `/Users/moufdi/.openclaw/workspace-jack-x`
- Canonical environment: `memory/intake`

## Readable External Surfaces

- `ms365-mail-prod-slices`
- `lark-prod-slices`
- `whatsapp-remote-snapshot`
- `mission-manager-agent-sessions`

## Mutable External Surfaces

- `local-memory-artifacts`
- `memory-wiki`
- `kg-memory-update-governed`

## Approval-Gated Surfaces

- none declared

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
