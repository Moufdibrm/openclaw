# Safir Environment Map

Last updated: `2026-05-07`

## Canonical Files

- Profile: `/Users/moufdi/.brm-hermes/profiles/safir`
- Config: `/Users/moufdi/.brm-hermes/profiles/safir/config.yaml`
- Workdir: `~/.openclaw/workspace-safir`
- Canonical environment: `email-crm`

## Readable External Surfaces

- `ms365-mail`
- `klaviyo`
- `email-template-inputs`

## Mutable External Surfaces

- `local-report-artifacts`
- `local-email-drafts`

## Approval-Gated Surfaces

- `external-email-send`
- `crm-mutation`

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
