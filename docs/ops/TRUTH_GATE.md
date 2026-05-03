# Truth Gate

## Purpose
This file defines the execution truth model that every production slice must obey.

## Canonical Truth
- local code truth:
  - `~/openclaw`
  - `~/hermes-runtime`
  - `~/clawd`
- live deploy mirrors:
  - `/home/ubuntu/openclaw`
  - `/home/ubuntu/hermes-runtime`
  - `/home/ubuntu/clawd`
- live runtime state:
  - profile-backed state under `HERMES_HOME`
  - operator floor currently anchored on `/home/ubuntu/.brm-hermes/profiles/jack`

## Rule
- code is authored locally
- VPS checkouts are deployment mirrors plus live runtime state
- no production conclusion is based on VPS checkout state alone when local code disagrees

## Runtime Consolidation Rule
- target runtime process family: `Hermes`
- target runtime state root: `~/.brm-hermes/profiles/*`
- target runtime code root: `~/hermes-runtime`
- target runtime repo root: `~/hermes-runtime/.git`
- `OpenClaw` may remain during migration as:
  - authoring surface
  - docs / protocol archive
  - temporary shim layer
- `OpenClaw` must not keep gaining new runtime-critical responsibilities

Allowed intermediate state:
- a migrated slice may coexist with legacy `OpenClaw` code
- but only if:
  - the Hermes slice preserves the same contract
  - the Hermes slice has local parity proof
  - the VPS replay is green
  - the live smoke is green
  - the next tranche removes additional runtime-critical `OpenClaw` surface

Forbidden:
- moving logic without parity proof
- introducing new shared contracts with `OpenClaw`-only runtime paths
- keeping two live runtime code paths for the same capability once Hermes parity is proven
- relying on `/Users/moufdi/.git` or any home-directory parent repo as runtime source control truth

## Portable Contract Rule
Shared execution contracts must not embed machine-specific absolute paths.

Allowed:
- `~/...`
- runtime-relative expansion
- documented runtime-local state schemes such as `jack-x-state://...`

Forbidden in shared contracts:
- `/Users/...`
- `/home/ubuntu/...`

Historical evidence, generated artifacts, and archived reviews are excluded from this rule.

Operational reference:

- `~/hermes-runtime/docs/runtime-portability-contract.md`

Interpretation rule:

- `~/openclaw` and `~/.openclaw/*` may still appear in historical corpora, archived reviews, or bounded legacy workspace dependencies
- they are not the default runtime roots for new or migrated slices

## Required Validation Floor
Every slice must close with:
1. local targeted tests
2. VPS replay of the exact synced slice
3. live smoke on the real runner
4. service restart when runtime-bearing files changed
5. operator confirmation over the real Jack WhatsApp bridge

## Consolidation Waves
1. contract freeze
2. central bridge extraction
3. Hermes rerouting for hooks, deploy, bootstrap, and validation
4. live route migration by bounded tranches
5. strict gate against runtime-critical `OpenClaw` path debt

## Audit Command
Use:

```bash
python3 ~/openclaw/scripts/runtime_truth_gate.py
```

Use strict mode to fail when portability violations remain:

```bash
python3 ~/openclaw/scripts/runtime_truth_gate.py --strict
```
