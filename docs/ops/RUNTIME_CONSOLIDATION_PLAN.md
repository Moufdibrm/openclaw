# Runtime Consolidation Plan

Last updated: `2026-05-03`

## Target

The production target is:

- `Hermes` as the only live runtime process family
- `~/.brm-hermes/profiles/*` as the only live runtime state root
- `~/hermes-runtime` as the only live runtime code root

`OpenClaw` remains acceptable only as:

- authoring surface
- docs and protocol archive
- temporary migration shim

## Non-Negotiables

- no logic rewrite during extraction unless parity is proven
- no new runtime-critical surface lands in `OpenClaw`
- no shared contract may embed `/Users/...` or `/home/ubuntu/...`
- no tranche closes without local tests, VPS replay, live smoke, and operator confirmation

## Waves

### Wave 0
- freeze the migration contract
- define bounded write sets
- define parity gates

### Wave 1
- extract central bridges into `hermes-runtime`
- current scope:
  - `brm-specialist-dispatch`
  - `brm-mm-bridge`
  - `brm-protocol-enforcement`
  - `mission-manager-client`
  - `brm-protocol-gate-check`

### Wave 2
- reroute Hermes callers to the Hermes bridge root
- current scope:
  - wake-loop
  - gateway specialist dispatch
  - MM WhatsApp ingress hook
  - validation scripts
  - deploy / bootstrap

### Wave 3
- migrate live route tranche A
- priority:
  - `kanye`
  - `safir`
  - `jeff`
  - `jack`

### Wave 4
- migrate live route tranche B
- priority:
  - `naya`
  - `rosa`
  - `alfred`
  - `selena`
  - `tony`
  - `cortex`

### Wave 5
- remove secondary and misleading legacy runtime surfaces
- priority:
  - `jack-x`
  - `mnemos`
  - examples
  - residual healthchecks
  - residual docs

## Validation Gates

Each tranche must prove:

1. same launch plan for the migrated capability
2. same gate behavior
3. same structured outcome semantics
4. same artifacts / lineage / MM review behavior
5. no new runtime-critical `OpenClaw` dependency

## Definition Of Done

A consolidation tranche is done only if:

- the migrated runtime surface executes from `hermes-runtime`
- local targeted tests are green
- VPS replay of the exact synced slice is green
- live smoke on the real runner is green
- deploy/bootstrap/validation are aligned for that tranche
- operator confirmation is sent over the real Jack WhatsApp bridge
