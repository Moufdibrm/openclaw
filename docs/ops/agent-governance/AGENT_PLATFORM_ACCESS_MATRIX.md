# Agent Platform Access Matrix

Last updated: `2026-05-07`

This document is the human-readable companion to `agent-platform-access-matrix.yaml`.

It projects the platform registry into operational agent access. It does not grant runtime wiring, gateway edits, Mission Manager implementation, deploy, restart, or systemd work.

## Core Rules

- Jack has all-platform visibility and supervised read access for routing, governance, gap detection, and handoff coordination.
- Jack mutation is never blanket mutation; writes require a governed route or explicit approval plus proof.
- Tony sees every `partial` platform as development/audit context, but this is not business-platform read permission unless Tony owns the relevant technical work.
- Specialist agents see only owned, secondary-owned, route-owned, or explicitly selected platforms.
- Installed skills are not permissions.
- New platforms must select access agents explicitly instead of relying on skill installation.

## Agent Summary

| Agent | Visible platforms | Read-allowed platforms | Write-conditional platforms | Notes |
| --- | ---: | ---: | ---: | --- |
| `jack` | 49 | 49 | 46 | all platforms; mutation gated |
| `jack-x` | 9 | 9 | 9 | specialist-scoped access only |
| `mnemos` | 1 | 1 | 1 | specialist-scoped access only |
| `rosa` | 14 | 14 | 13 | specialist-scoped access only |
| `jeff` | 5 | 5 | 5 | specialist-scoped access only |
| `naya` | 9 | 9 | 9 | specialist-scoped access only |
| `selena` | 4 | 4 | 4 | specialist-scoped access only |
| `alfred` | 9 | 9 | 7 | specialist-scoped access only |
| `cortex` | 8 | 8 | 8 | specialist-scoped access only |
| `tony` | 22 | 13 | 12 | dev owner plus partial observer |
| `kanye` | 6 | 6 | 6 | creative provider selection: higgsfield default, banana/openai selectable |
| `safir` | 8 | 8 | 8 | specialist-scoped access only |

## Platform Addition Standard

When a platform is added, the owner must declare:

- `primary_owner_agent` and optional `secondary_owner_agents`
- selected `explicit_access_agents.read`, `explicit_access_agents.write`, and `visible_only` in the projected matrix
- read surfaces, write surfaces, forbidden surfaces, approval gates, auth metadata, proof targets, and test plan
- whether repeated direct use opens `jack.protocol-missing` or `jack.capability-missing`

## Kanye Creative Provider Policy

Kanye may select:

- `higgsfield`: default for final campaign stills, product shots, motion, and future voice identity work
- `banana`: fast exploratory/edit image provider
- `openai`: premium image route when requested or better suited

Publication, paid delivery, external send, and voice clone paths remain approval-gated.

## Validation Notes

- `partial` does not mean available to every specialist.
- A missing brand-pack platform field blocks only that platform surface.
- Platform write access still needs route/proof/approval; the matrix is not a deploy or runtime wiring document.
