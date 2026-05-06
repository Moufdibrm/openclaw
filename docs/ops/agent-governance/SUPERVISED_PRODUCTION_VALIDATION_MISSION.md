# Supervised Production Validation Mission

Last updated: `2026-05-06`

Mission id: `spv-2026-05-06`

This mission prepares the V1 BRM/Hermes agents for a supervised production phase.

It is a governance, audit, fixture, and proof mission. It does not authorize deploy, restart, gateway/runtime wiring, Mission Manager code changes, VPS release control, external message sending, payment/refund/dispute mutation, CRM mutation, Shopify publication, campaign publication, or Drive delivery.

## Objective

Validate all V1 agents today for supervised production start by proving:

- each agent has a clear allowed route/toolbox surface
- each selected route has explicit inputs, outputs, proof, and approval gates
- each brand-linked deliverable carries `brand_scope` natively or through sidecar
- every mutation-capable surface is blocked unless explicit approval exists
- each agent produces a render Moufdi can inspect
- unresolved blockers are named and scoped instead of hidden

Supervised production does not mean every agent is fully autonomous or globally prod-ready.

It means each agent can operate only inside a validated route/mode with reviewable proof and hard mutation gates.

## Entry Criteria

The mission can start when these conditions are true:

| Criterion | Required | Current prep |
| --- | --- | --- |
| V1 agent inventory fixed | yes | `12` agents in `release-readiness-matrix.yaml` |
| brand-linked proof mapping | yes | `brand-scope-sidecars.yaml` created for legacy proofs |
| runner/input contract reference | yes | `workflow-runner-input-map.yaml` |
| workflow IO/proof reference | yes | `workflow-io-test-matrix.yaml` |
| fixture reference | yes | `workflow-test-fixtures.yaml` |
| no deploy/MM/runtime mutation | yes | mission-level hard block |
| approval gates explicit | yes | route-level and global gates documented |

## Exit Criteria

The mission is complete when each V1 agent has one of these final statuses:

- `supervised_ready`
- `supervised_ready_with_caveats`
- `blocked_with_named_owner`

No agent may be marked `supervised_ready` without:

- a tested route or fixture mode
- input summary
- output artifact/proof path
- approval gate state
- `brand_scope` if brand-linked
- final render ready for Moufdi

## Workstreams

### W0: Governance And Repo Hygiene

Owner: governance lane

Goal:

- keep changes restricted to governance docs and local proof artifacts
- avoid dirty-worktree mixing with runtime/integrator changes
- validate YAML/JSON/path/hash/secret checks

Required proof:

- YAML parse OK
- JSON parse OK where applicable
- referenced paths exist
- sidecar hashes match
- no raw secrets in docs
- no reserved runtime/gateway/deploy/MM files touched

### W1: Business Prod Route Smoke

Agents:

- Rosa
- Jeff
- Selena
- Cortex
- Alfred Phase 1 only

Goal:

- run or verify prod read/report routes with upload off
- attach sidecar `brand_scope` for legacy proofs
- return concise business render for Moufdi

Default gates:

- `upload_drive=false`
- no external message
- no customer reply
- no dispute/refund/payment
- no campaign mutation
- no site/theme mutation

Pass condition:

- route proof exists
- report or summary is inspectable
- `brand_scope` is native or sidecar-mapped
- no external mutation occurred

### W2: Naya Supply Chain Unblock

Agents:

- Naya

Goal:

- isolate a reviewed sourcing input sheet
- choose one reviewed SKU/product query or stock snapshot
- run only read/report validation

Current blockers:

- `reviewed_sourcing_sheet` is partial
- `stock_snapshot_or_known_sku` is partial

Pass condition:

- one sourcing input fixture with hash
- one stock fixture or known SKU/query with source
- `naya.product-sourcing` and `naya.stock-check` can be smoked without supplier/order/payment mutation

### W3: Alfred SEO/AEO Unblock

Agents:

- Alfred
- Tony as implementation owner for code/theme/file fixes only
- Rosa for marketing context if needed

Goal:

- resolve the Alfred Phase 2 gate by separating `brand_pack_id` from `runtime_store_key`
- rerun `alfred.strategy-plan` with `skip-drive`
- prepare Phase 3 only after Phase 2 passes

Current blocker:

- Phase 2 strict input gate compares `maybe-paris` and `maybe_paris` as one raw store field

Pass condition:

- Phase 2 returns report/workboard/manifest/result with no Drive upload
- `brand_scope` is present or sidecar-mapped
- site/theme/content mutations remain blocked until explicit approval

### W4: Technical And Memory Fixture Smoke

Agents:

- Jack
- Jack-X
- Mnemos
- Tony

Goal:

- validate fixture-only technical routes without MM/KG/runtime mutation

Default gates:

- `write_cursor=false`
- `kg_commit=false`
- `mission_manager_mutation=false`
- no live VPS/WhatsApp snapshot mutation
- Tony uses fixture repo/snapshot only

Pass condition:

- Jack produces route/capability/draft proof instead of ad hoc work
- Jack-X produces memory candidates with source refs and no KG commit
- Mnemos produces context pressure/continuity observation
- Tony produces exploration/plan/development proof against fixture repo only

### W5: Creative And Ads Media QA

Agents:

- Kanye
- Cortex
- Alfred as landing/SEO dependency

Goal:

- continue local media proof and ads dry-runs without publication
- standardize Higgsfield polling recovery and product/marketplace evidence

Default gates:

- no publication
- no paid delivery mutation
- no identity/private media use without approval and consent

Pass condition:

- local media manifest exists
- generated assets have source/provenance and `brand_scope` where brand-linked
- Cortex consumes asset/landing readiness only as dry-run

### W6: Safir Email Workflow Prep

Agents:

- Safir
- Rosa for offer/brand context
- Kanye for optional visuals

Goal:

- create a render-only email workflow brief fixture
- produce HTML/PDF/JSON proof in draft mode

Current blocker:

- `safir_email_workflow_brief` is missing

Minimum brief:

```yaml
brand_scope:
  scope_id: "maybe-paris:brand_focus:email-workflow"
  brand_pack_id: "maybe-paris"
  focus_mode: "brand_focus"
  subject_id: "email-workflow"
  runtime_store_key: "maybe-paris"
campaign_goal:
offer:
audience:
primary_template:
assets:
```

Pass condition:

- render-only artifact exists
- no external email send
- no CRM mutation
- approval packet states send/CRM blocked

## Per-Agent Validation Targets

| Agent | Target for supervised start | Required proof |
| --- | --- | --- |
| Jack | `supervised_ready_with_caveats` | fixture proof for protocol/capability/draft route handling |
| Jack-X | `supervised_ready_with_caveats` | fixture memory candidates, no KG commit |
| Mnemos | `supervised_ready` | context-check replay proof |
| Rosa | `supervised_ready` | upload-off report/decision proof with `brand_scope` |
| Jeff | `supervised_ready_with_caveats` | prod profile/report proof; candidate/outreach/collab remain gated |
| Naya | `blocked_with_named_owner` until fixtures isolated | sourcing input and stock fixture |
| Selena | `supervised_ready` | PayPal/Zendesk reviewed and bounded live read proof; no mutation |
| Alfred | `blocked_with_named_owner` until Phase 2 gate fixed | Phase 2 strategy report/workboard |
| Cortex | `supervised_ready_with_caveats` | ads observation proof and campaign dry-run only |
| Tony | `supervised_ready_with_caveats` | fixture repo exploration/plan/dev proof; no deploy/restart |
| Kanye | `supervised_ready_with_caveats` | local media manifest and QA notes; publication blocked |
| Safir | `blocked_with_named_owner` until email brief exists | render-only email workflow proof |

## Implementation Plan

1. Freeze governance scope.
   - do not touch runtime/gateway/deploy/MM files
   - do not edit legacy proof bundles
   - do not push a dirty worktree with unrelated changes

2. Run validation lanes from lowest risk to highest value.
   - W0 governance checks
   - W1 business prod smoke
   - W4 technical fixture smoke
   - W5 creative local QA
   - W2/W3/W6 unblockers in parallel where owners are clear

3. Update the execution ledger after each route.
   - status
   - input summary
   - output/proof path
   - `brand_scope`
   - mutation gates
   - final render sent to Moufdi

4. Decide supervised production scope.
   - start with agents/routes that passed
   - keep blocked agents out of autonomous mode
   - allow blocked agents only in audit/discussion mode until their blocker is closed

## Clean Push Policy

This repository currently has many unrelated dirty and untracked changes outside this governance lane.

Before any git commit or push:

- isolate only `docs/ops/agent-governance/**` changes from this lane
- confirm branch and remote target
- do not include runtime/gateway/deploy/MM changes
- do not include unrelated source changes
- run validation checks again

No git push is part of this mission unless explicitly confirmed after reviewing the final diff.

