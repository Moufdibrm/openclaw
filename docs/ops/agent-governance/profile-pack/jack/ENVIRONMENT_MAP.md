# Jack Environment Map

Last updated: `2026-05-07`

## Canonical Files

- Profile: `/Users/moufdi/.brm-hermes/profiles/jack`
- Config: `/Users/moufdi/.brm-hermes/profiles/jack/config.yaml`
- Workdir: `~/clawd`
- Canonical environment: `operator/control-plane`

## Readable External Surfaces

- `mission-manager`
- `kg`
- `brand-packs`
- `route-registry`
- `platform-skills-when-governed`
- `higgsfield-skill-surface-when-governed`

## Mutable External Surfaces

- `mission-manager-governed`
- `kg-governed`
- `platform-skills-route-governed`
- `higgsfield-generated-media-artifacts-when-requested`

## Approval-Gated Surfaces

- `external-message-send`
- `payment-or-billing-mutation`
- `customer-visible-support-action`
- `external-publication`

## Platform Projection

Platform permissions are projected from `docs/ops/agent-governance/agent-platform-access-matrix.yaml`.

- Visible platforms: `49`
- Read-allowed platforms: `49`
- Write-conditional platforms: `46`

## Environment Rules

- Resolve brand/account/tenant before reading a brand-scoped platform.
- A missing surface blocks only that surface, not unrelated brand work.
- Never print, copy, or commit secret values.
- External mutation requires route/approval/proof even when a platform is visible.
