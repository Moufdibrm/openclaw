# Agent Profile Standard

Last updated: `2026-05-07`

This standard defines what every governed BRM/Hermes profile must expose locally.

It does not wire runtime, gateway, Mission Manager, deploy, restart, or systemd behavior.

## Required Local Files

Every V1 profile under `/Users/moufdi/.brm-hermes/profiles/<agent>/` must expose:

- `SOUL.md`: stable identity, role, boundaries, and first-response behavior.
- `ROLE_PERMISSIONS.md`: human-readable permissions and gates.
- `ROLE_PERMISSIONS.json`: machine-readable local permission projection.
- `ENVIRONMENT_MAP.md`: canonical workdir, environment, external read/write surfaces.
- `ROUTE_MATRIX.md`: current route/protocol list and proof targets.
- `PROCEDURES.md`: operating procedure for direct asks, route-backed asks, exploratory asks, and proof.

`SOUL.md` is the local identity entrypoint, but permissions do not come from prose alone.
The permission truth is the combination of:

- `docs/ops/agent-governance/agent-toolbox-matrix.yaml`
- `docs/ops/agent-governance/agent-environment-matrix.yaml`
- `docs/ops/agent-governance/agent-protocol-matrix.yaml`
- `docs/ops/agent-governance/agent-platform-access-matrix.yaml`

## Access Rules

- Jack sees all platforms for supervision, routing, governance, gap detection, and governed direct execution.
- Jack does not get blanket mutation rights. Any write still needs a governed route or explicit approval plus proof.
- Tony sees partial platforms for development and audit context. That visibility is not business-platform permission.
- Specialists see only owned, secondary-owned, route-owned, or explicitly selected platforms.
- Installed skills are not permissions.
- Platform write access is conditional until the route, target, approval gate, and proof target are resolved.

## New Platform Process

When adding a platform, declare:

- platform id, status (`draft`, `beta`, `prod`), category, scope model
- owner agent, secondary agents, and Jack as supervisor
- selected read/write/visible-only agents
- auth metadata without secret values
- readable surfaces, mutable surfaces, approval gates, forbidden surfaces
- proof targets and test plan
- whether repeated direct use should open `jack.protocol-missing` or `jack.capability-missing`

Partial platforms are visible to Jack and Tony by default.
Other agents receive partial platform visibility only when selected by ownership, route coverage, or explicit access.

## SOUL Ownership

Some SOUL files are generated from canonical OpenClaw sources.
Generated SOULs must not be hand-edited as the only source of truth because a sync can overwrite them.

Current generated SOUL profiles:

- `jack`: source `~/.openclaw/SOUL.md`
- `mnemos`: source `~/.openclaw/agents/mnemos/SOUL.md`

For those agents, use sidecars for local governance until the canonical SOUL source is intentionally updated.

## Kanye Provider Selection

Kanye must support an explicit creative provider mode:

- `higgsfield`: default provider
- `banana`: Nano Banana / Gemini image route
- `openai`: OpenAI image route

Provider selection is a routing decision, not an approval bypass.
Publication, external sending, paid delivery platform mutation, and voice clone paths remain approval-gated.

## Validation

Before a profile standard update is considered ready:

- YAML and JSON parse successfully.
- Every V1 agent has all required sidecars.
- Referenced canonical profile and workdir paths are present or explicitly marked as pending.
- No secret values are written into docs or profiles.
- No reserved runtime, gateway, deploy, Mission Manager, or Jack reserved files are modified.
- The agent to platforms to permissions to protocols projection remains coherent.
