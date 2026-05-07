# Production Readiness Checkpoint

Date: `2026-05-07`

Scope: BRM/Hermes V1 agent governance, memory lifecycle readiness, local profile materialization, and supervised production validation status.

This checkpoint is governance-only. It does not authorize deploy, restart, gateway/runtime edits, Mission Manager implementation edits, systemd work, VPS work, external sends, billing/payment mutation, campaign publication, or customer-visible replies.

## Verdict

The system is not globally production-ready yet.

It is ready for supervised production validation on bounded routes, with artifact/proof requirements already defined.

Memory is `beta_validated_not_prod_closed`: Jack-X intake, DB analysis, and LLM Wiki compile are healthy on the latest checked artifacts, but the durable KG write loop is not production-closed until the review gate, wiki-to-review bridge, feedback-loop route, fresh Mnemos proof, and one supervised live KG commit/retrieval proof are complete.

## Latest Memory Evidence Checked

| Surface | Latest evidence | Status | Meaning |
| --- | --- | --- | --- |
| Jack-X WhatsApp pass0 | `whatsapp-intake-pass0-20260507T130712495849Z.json` | `ok`, `0` candidates | Latest scheduled pass did not fail; no new candidates in that pass. |
| Jack-X WhatsApp trend | `2026-05-05` to `2026-05-07` pass0 artifacts | `ok`, candidate counts up to `306` | Intake is alive and recent. |
| Jack-X event DB | `/Users/moufdi/.openclaw/workspace-jack-x/runtime/jack_x_events.db` | `271` events processed, `14` snapshots processed | Existing channel data is recorded and processed. |
| Jack-X surfaces | same DB | `mail=73`, `messages=198` processed | Mail/message analysis path is populated. |
| Jack-X review queue | `/Users/moufdi/.openclaw/workspace-jack-x/runtime/memory_reviews.db` | `61` pending reviews | Review workflow exists, but closure is not done. |
| LLM Wiki | `/Users/moufdi/.openclaw/memory-wiki/latest.json` | run `memwiki_20260506T233525Z_1c3d1c21` | Active semantic compile is fresh. |
| LLM Wiki outputs | same manifest | `40` pages, `40` kg_operations, `37` review_items | Consolidation produces reviewable material. |
| Mnemos | `/Users/moufdi/.openclaw/workspace-mnemos/reports/context-check/...` | latest checked run `20260414t210434302927z-jack-live-compaction-smoke` | Route proof exists, but no May freshness proof was found. |

## Memory Blockers Before Production Closure

1. Add the Jack-X review gate before any live `commit-candidate --apply`.
2. Bridge LLM Wiki `kg_operations` into Jack-X memory review artifacts.
3. Render bounded KG relation evidence inside Memory Wiki pages.
4. Add and prove the Jack-X memory feedback-loop route.
5. Run a fresh Mnemos May 2026 context-check proof.
6. Run one low-risk supervised live KG commit only after the review gate exists.
7. Produce Jack retrieval proof after that live memory update.
8. Clear or deliberately triage the `61` pending memory reviews, at least all `P1`.

## Agent Profile Readiness

All V1 local profiles are materialized and parse correctly:

- Jack
- Jack-X
- Tony
- Mnemos
- Rosa
- Jeff
- Selena
- Naya
- Alfred
- Cortex
- Kanye
- Safir

Required local sidecars exist for all V1 agents:

- `SOUL.md`
- `ROLE_PERMISSIONS.json`
- `ROLE_PERMISSIONS.md`
- `ENVIRONMENT_MAP.md`
- `ROUTE_MATRIX.md`
- `PROCEDURES.md`
- `config.yaml`

The Git profile pack also exists under `docs/ops/agent-governance/profile-pack/` with no secret-bearing config. Jack and Mnemos keep source-owned prompt pointers in the Git pack and full local profiles on the machine.

## Platform Visibility Snapshot

| Agent | Visible platforms | Read platforms | Conditional write platforms | Routes |
| --- | ---: | ---: | ---: | ---: |
| Jack | 49 | 49 | 46 | 8 |
| Jack-X | 9 | 9 | 9 | 10 |
| Tony | 22 | 13 | 12 | 3 |
| Mnemos | 1 | 1 | 1 | 1 |
| Rosa | 14 | 14 | 13 | 4 |
| Jeff | 5 | 5 | 5 | 7 |
| Selena | 4 | 4 | 4 | 4 |
| Naya | 9 | 9 | 9 | 4 |
| Alfred | 9 | 9 | 7 | 3 |
| Cortex | 8 | 8 | 8 | 3 |
| Kanye | 6 | 6 | 6 | 8 |
| Safir | 8 | 8 | 8 | 3 |

Installed skills are still not permissions. Platform visibility does not grant blanket mutation.

## Supervised Production Validation Status

Current ledger: `docs/ops/agent-governance/supervised-production-validation-ledger.yaml`

Status: `executed_with_followup_blockers`

Latest run:

- `docs/ops/agent-governance/SUPERVISED_VALIDATION_RUN_20260507T135248Z.md`
- `docs/ops/agent-governance/supervised-validation-run-20260507T135248Z.yaml`

| Ledger state | Count |
| --- | ---: |
| `passed` | 9 |
| `passed_with_warnings` | 5 |
| `blocked` | 3 |
| `blocked_rendering` | 1 |
| `failed` | 1 |

Validated routes from the latest supervised run:

- Rosa: offer strategy, performance audit, competitive watch.
- Jeff: profile analysis, performance report.
- Selena: PayPal dispute audit, Zendesk feedback review.
- Cortex: ads observation.
- Alfred: visibility audit.
- Kanye/Cortex: Higgsfield product photoshoot validation.
- Mnemos: context-check freshness proof.
- Naya: BigBlue-backed stock check after canonical env load.
- Selena: PayPal and Zendesk live-read routes after canonical env load.

Blocked routes need missing inputs, schema alignment, or rendering fixes:

- Naya product sourcing: reviewed sourcing sheet input is not isolated.
- Alfred strategy plan: brand pack id vs runtime store key mismatch.
- Safir email workflow: business brief is missing.
- Safir mail-pole audit: Klaviyo Maybe Paris credential works; PDF rendering failed.
- Tony technical fixture: `tony.codebase-exploration` failed its JSON output contract.

Credential follow-up:

- `docs/ops/agent-governance/CREDENTIAL_STANDARDIZATION_AUDIT_20260507.md`
- `docs/ops/agent-governance/credential-standardization-audit.yaml`

The follow-up confirms that BigBlue, Klaviyo Maybe Paris, PayPal Maybe Paris, and Zendesk Maybe Paris credentials exist and work when `/Users/moufdi/.brm-hermes/.env` is loaded. The remaining issue is source-of-truth and runner env-loading standardization, not missing business credentials.

## Mission, Hypotheses, And Results

The governance contract is ready for Mission Manager consumption:

- `MISSION_MANAGER_AGENT_CONTROL_CONTRACT.md`
- `mission-manager-agent-control-contract.yaml`
- `WORKFLOW_IO_TEST_CONTRACTS.md`
- `supervised-production-validation-ledger.yaml`

What is ready:

- mission/action request fields are defined
- route ids and proof targets are defined
- brand scope is mandatory for brand-linked work
- approval gates are defined for external sends, support replies, disputes, payments, billing, publication, voice clone, and ambiguous deltas
- workflow output/render expectations are defined

What is not validated yet:

- MM-created missions have not been proven against each prepared agent workflow from this ledger
- hypothesis/result artifacts are defined by contract, but not populated for the `prepared` entries
- no agent should be marked `prod_ready` from chat-only output or MM state alone

## Production Readiness Sequence

1. Memory closure slice:
   - close Jack-X review gate
   - bridge LLM Wiki operations into Jack-X review
   - run fresh Mnemos context-check
   - run supervised low-risk live KG commit
   - prove Jack retrieval and one autocorrection/feedback-loop fixture

2. Agent supervised validation wave:
   - run prepared no-mutation/read-only routes first
   - send every rendered result back to Moufdi with paths
   - update ledger entries from `prepared` to `passed`, `passed_with_warnings`, `failed`, or `blocked`

3. Blocked workflow unblock:
   - choose Naya sourcing input
   - choose Naya stock SKU/snapshot
   - normalize Alfred `brand_scope` vs runner store key
   - write Safir email workflow brief fixture

4. MM integration handoff:
   - MM may consume the governance contract and display agent cards
   - MM may create governed requests
   - MM must attach proof artifacts before readiness changes
   - MM must not infer readiness from profile existence alone

## Current Product Decision

Use the platform now for supervised production validation and bounded route tests.

Do not call the memory side production-closed yet.

Do not call all agents production-ready yet.

The next practical move is to close the blockers exposed by the supervised validation wave in this order:

1. Fix Tony route output contract and fixture mapping.
2. Standardize credential loading so all runners load `/Users/moufdi/.brm-hermes/.env` before local skill config fallback.
3. Fix Safir PDF rendering and create an email-workflow brief for render-only testing.
4. Keep Selena live reads in read-only beta; any customer reply, dispute, payment, or billing mutation remains approval-gated.
5. Fix Alfred Hermes wrapper parity with the direct route.
6. Continue Jack-X/Mnemos memory closure once review gate and wiki bridge are implemented.
