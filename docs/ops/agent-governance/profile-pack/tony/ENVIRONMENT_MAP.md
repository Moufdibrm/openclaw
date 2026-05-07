# Tony Environment Map

Last updated: `2026-05-07`

## Canonical Files

- Profile: `/Users/moufdi/.brm-hermes/profiles/tony`
- Config: `/Users/moufdi/.brm-hermes/profiles/tony/config.yaml`
- Workdir: `~/.openclaw/workspace-tony`
- Canonical environment: `development`

## Readable External Surfaces

- `repositories`
- `github-when-requested`
- `package-registries-when-needed`

## Mutable External Surfaces

- `repository-files`
- `git-local`
- `github-when-requested`

## Approval-Gated Surfaces

- `push-or-pr-when-not-requested`
- `production-deploy`
- `service-restart`

## Platform Projection

Platform permissions are projected from `/Users/moufdi/openclaw-governance-clean/docs/ops/agent-governance/agent-platform-access-matrix.yaml`.

- Visible platforms: `22`
- Read-allowed platforms: `13`
- Write-conditional platforms: `12`

## Environment Rules

- Resolve brand/account/tenant before reading a brand-scoped platform.
- A missing surface blocks only that surface, not unrelated brand work.
- Never print, copy, or commit secret values.
- External mutation requires route/approval/proof even when a platform is visible.
