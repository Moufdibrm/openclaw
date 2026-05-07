# Path Resolution Standard

Date: `2026-05-07`

Scope: path conventions for BRM/Hermes agent governance docs, matrices, profile packs, proof ledgers, and local validation artifacts.

This is governance-only. It does not change runtime wiring, gateway code, deploy scripts, service files, Mission Manager implementation, or production services.

## Standard

Use path classes deliberately:

| Class | Format | Use |
| --- | --- | --- |
| Repo governance source | `docs/ops/agent-governance/...` | Docs, matrices, profile-pack references, MM-readable governance references. |
| Local agent profiles | `/Users/moufdi/.brm-hermes/profiles/...` or `~/.brm-hermes/profiles/...` | Machine-local governed profile materialization and profile health evidence. |
| Local agent workspaces | `/Users/moufdi/.openclaw/...` or `~/.openclaw/...` | Generated reports, manifests, validation runs, memory workspaces. |
| Business config | `/Users/moufdi/clawd/config/...` or `~/clawd/config/...` | Brand packs and local business config already canonical on this machine. |
| Runtime/scripts | `/Users/moufdi/openclaw/scripts/...`, `/Users/moufdi/hermes-runtime/...`, or explicit runner cwd | Only when documenting an executable command or a runtime-owned path. |
| Proof artifacts | absolute machine path | Proof must be directly openable on Moufdi's machine. |
| External assets | URL or absolute downloaded local path | Attachments and generated media references. |

## Rules

1. Do not pin governance source files to one worktree such as `/Users/moufdi/openclaw` or `/Users/moufdi/openclaw-governance-clean`.
2. Use `docs/ops/agent-governance/...` for all governance docs, YAML matrices, profile-pack source references, and Mission Manager contract references.
3. Keep absolute machine paths for proof artifacts, generated outputs, local profiles, local workspaces, env files, and observed runtime paths.
4. Use `~` only in human-facing docs or runner cwd fields where shell expansion is expected. Use absolute paths in proof ledgers.
5. Never store secret values in any path-adjacent config. Credential paths may name key names and source classes only.
6. If a consumer needs an absolute source path, it must resolve repo-relative governance paths against its checked-out repo root.
7. Legacy proof bundles are not rewritten just to change path style; attach sidecars or ledgers with the normalized reference instead.

## Current Machine Notes

Both `/Users/moufdi/openclaw` and `/Users/moufdi/openclaw-governance-clean` exist on this machine. Governance docs must not depend on which one is the active worktree.

The current working copy for this lane is:

- `/Users/moufdi/openclaw-governance-clean`

The canonical governance reference remains repo-relative:

- `docs/ops/agent-governance`

## Validation

Path validation for governance changes should include:

1. YAML parses.
2. JSON parses for profile-pack sidecars.
3. No `/Users/moufdi/openclaw*/docs/ops/agent-governance` references remain in governance docs.
4. Latest proof artifact paths exist when the ledger claims they exist.
5. Reserved runtime/deploy/MM paths are not modified.
6. Secret scan passes.

