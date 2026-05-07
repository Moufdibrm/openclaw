# Rosa Environment Map

Last updated: `2026-05-07`

## Canonical Files

- Profile: `/Users/moufdi/.brm-hermes/profiles/rosa`
- Config: `/Users/moufdi/.brm-hermes/profiles/rosa/config.yaml`
- Workdir: `~/.openclaw/workspace-rosa`
- Canonical environment: `marketing`

## Readable External Surfaces

- `shopify`
- `klaviyo`
- `hiboo`
- `lark`
- `ga4`
- `gsc`
- `dataforseo`

## Mutable External Surfaces

- `local-report-artifacts`

## Approval-Gated Surfaces

- `campaign-publication`
- `external-message-send`
- `crm-or-storefront-mutation`

## Platform Projection

Platform permissions are projected from `docs/ops/agent-governance/agent-platform-access-matrix.yaml`.

- Visible platforms: `14`
- Read-allowed platforms: `14`
- Write-conditional platforms: `13`

## Environment Rules

- Resolve brand/account/tenant before reading a brand-scoped platform.
- A missing surface blocks only that surface, not unrelated brand work.
- Never print, copy, or commit secret values.
- External mutation requires route/approval/proof even when a platform is visible.
