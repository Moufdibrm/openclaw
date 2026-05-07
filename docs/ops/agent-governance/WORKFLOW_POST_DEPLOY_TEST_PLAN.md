# Workflow Post-Deploy Test Plan

Last updated: `2026-05-06`

This plan explains how to test governed BRM/Hermes workflows after runtime deployment is handled by the integrator lane.

This governance lane does not deploy, restart, edit gateway/runtime services, or mutate Mission Manager.

## Objective

After deployment, each tested workflow must produce a clear render back to Moufdi:

```yaml
workflow_id:
status: passed|passed_with_warnings|failed|blocked
brand_scope: required_when_brand_linked
input_summary:
output_artifacts:
proof_artifacts:
approval_gates:
gaps_or_next_fix:
```

A workflow is not passed until expected artifacts and proof exist.
For brand-linked workflows, proof must include consistent `brand_scope` across runner input, manifest/result, report data, delivery record, and generated media manifest when present.

## Current Coverage

- workflow contracts: `53`
- runtime registry routes: `25`
- protocol package files observed: `35`
- prod workflows: `13`
- beta workflows: `33`
- draft workflows: `7`

Source contracts:

- `docs/ops/agent-governance/workflow-io-test-matrix.yaml`
- `docs/ops/agent-governance/WORKFLOW_IO_TEST_CONTRACTS.md`
- `docs/ops/agent-governance/workflow-runner-input-map.yaml`
- `docs/ops/agent-governance/workflow-test-fixtures.yaml`
- `docs/ops/agent-governance/PHASE0_FIXTURE_INVENTORY.md`
- `docs/ops/agent-governance/release-readiness-matrix.yaml`
- `docs/ops/agent-governance/brand-scope-sidecars.yaml`
- `docs/ops/agent-governance/supervised-production-validation-mission.yaml`
- `docs/ops/agent-governance/supervised-production-validation-ledger.yaml`
- `docs/ops/agent-governance/ads-media-orchestration-matrix.yaml`
- `docs/ops/agent-governance/ads-media-test-ledger.yaml`
- `docs/ops/agent-governance/alfred-orchestration-matrix.yaml`
- `docs/ops/agent-governance/alfred-test-ledger.yaml`

## Lanes

### Lane A: Technical / Memory

Agents:

- Jack
- Jack-X
- Mnemos
- Tony

Goal:

- validate protocol creation, memory extraction, continuity, and dev workflows on fixtures only

Hard constraints:

- no Mission Manager mutation
- no KG merge
- no live WhatsApp/VPS snapshot
- no cursor writes
- Tony uses fixture repo/snapshot only

### Lane B: Business Ops

Agents:

- Rosa
- Jeff
- Naya
- Selena
- Alfred
- Cortex
- Safir

Goal:

- validate report, audit, support, stock, SEO, influence, ads, and email workflows from reviewed fixtures first, then bounded live reads

Hard constraints:

- no external messages
- no refunds/payments/dispute messages
- no supplier sends
- no campaign/ad mutation
- no CRM/send mutation
- uploads disabled unless explicitly approved

### Lane C: Creative

Agents:

- Kanye
- Jack only for supervision/handoff

Goal:

- validate still/reference/Higgsfield/product/marketplace workflows with manifests and local media

Hard constraints:

- no publication
- no paid delivery mutation
- no identity/Soul workflow without explicit approval and consent
- no retries before `generate get` recovery checks

## Phase Order

### Phase 0: Fixture Prep

Prepare:

- brand/store fixture set: Maybe Paris, Blinx, Botanic
- reviewed PayPal export
- reviewed Zendesk export
- reviewed sourcing sheet
- SEO report-data bundle
- known creator handle/profile fixture
- stock SKU/product query fixture
- bounded live read defaults
- Jack-X memory/channel fixtures
- Tony fixture repo snapshot
- Kanye safe image fixtures
- Safir email workflow fixture

Output:

- fixture paths and hashes where applicable
- fixture readiness matrix
- unresolved fixture gaps

Current Phase 0 readiness is documented in `PHASE0_FIXTURE_INVENTORY.md`.
The remaining blockers are Naya sourcing input isolation, Naya stock SKU/snapshot selection, Safir email brief creation, and Jack fresh post-deploy proof.

### Phase 1: Prod Artifact-Fed, No Mutation

Run first:

1. `selena.paypal-dispute.phase1-audit`
2. `selena.zendesk-feedback-review`
3. `naya.product-sourcing`
4. `alfred.visibility-audit`
5. `naya.stock-check` with reviewed snapshot

Pass condition:

- report/audit/verdict artifact exists
- final render sent here
- no platform mutation

### Phase 2: Prod Decision / Reports, Uploads Off

Run:

1. `rosa.offer-strategy.direct`
2. `rosa.audit-performance-marketing`
3. `rosa.veille-concurrentielle`
4. `jeff.analyse-profil`
5. `jeff.performance-report`

Pass condition:

- report or decision proof exists
- `upload_drive=false` unless approved
- `delivery_json` is either produced or explicitly marked not applicable

### Phase 3: Prod Live Reads, Tiny Limits

Run:

1. `selena.paypal-dispute.phase1-live`
2. `selena.zendesk-feedback-live`
3. `cortex.ads-observation`
4. `naya.stock-check` live if needed

Default live limits:

- `days`: `7`
- `case_limit`: `3`
- `ticket_limit`: `5`
- `skip_comments`: `true` for first Zendesk smoke
- `upload_drive`: `false`

Pass condition:

- readback/report exists
- fetched count is reported
- no customer reply, dispute message, refund, payment, campaign mutation, or upload

### Phase 4: Beta Technical Fixtures

Run:

1. `jack.protocol-missing`
2. `jack.capability-missing`
3. `jack.draft-protocol-runtime`
4. `mnemos.context-check`
5. `tony.codebase-exploration`
6. `tony.development-plan`
7. `tony.development`
8. `jack-x.registry-ingest`
9. `jack-x.email-intake-pass0`
10. `jack-x.lark-message-intake-pass0`
11. `jack-x.lark-table-intake-pass0`
12. `jack-x.whatsapp-intake-pass0`
13. `jack-x.db-analysis`
14. `jack-x.signal.extract`

Pass condition:

- fixture/snapshot only
- no cursor writes
- no MM mutation
- no KG commit
- Tony changes fixture repo only

### Phase 5: Creative Beta

Run:

1. `kanye.still-generate`
2. `kanye.reference-edit`
3. `kanye.higgsfield-generate.official-cli`
4. `kanye.higgsfield-product-photoshoot.validation`
5. `kanye.higgsfield-marketplace-cards.validation`
6. `kanye.higgsfield-soul-id.validation`

Pass condition:

- local media exists
- manifest exists
- source attachment provenance exists when applicable
- publication blocked
- Soul ID remains blocked unless approval and consent artifacts exist

### Phase 6: Draft / Planned Dry-Runs

Run only as dry-run or blocked render:

- `safir.email-workflow`
- `naya.supplier-comm`
- `jeff.email-digest`
- `jeff.outreach-pipeline`
- `jeff.ajout-collaboration`
- `jeff.collab-management`
- `cortex.campaign-management`
- `cortex.feedback-loop`
- `jack.higgsfield-skill-supervision`

Dedicated ads/media release candidate:

- `ads-media.cortex-kanye.rc1`
- source plan: `ADS_MEDIA_ORCHESTRATION_PLAN.md`
- source matrix: `ads-media-orchestration-matrix.yaml`
- execution ledger: `ads-media-test-ledger.yaml`

Dedicated Alfred SEO/AEO release candidate:

- `alfred.seo-aeo.rc1`
- source plan: `ALFRED_ORCHESTRATION_PLAN.md`
- source matrix: `alfred-orchestration-matrix.yaml`
- execution ledger: `alfred-test-ledger.yaml`
- current gate: `alfred.strategy-plan` is locally blocked until the Phase 1 store identifier mismatch is normalized

Pass condition:

- draft artifact or blocked render exists
- approval gate is explicit
- no external mutation

## Open Fixes Before Automation

1. Add a normalized approval-gate vocabulary.
2. Complete `contract_input -> runner_arg` mapping for package-only and planned workflows.
3. Finish the remaining partial/needed fixtures from `PHASE0_FIXTURE_INVENTORY.md`.
4. Clarify whether `delivery_json` is mandatory when upload is disabled.
5. Keep route status as authority over global agent status.
6. For Jack/MM and Jack-X/KG routes, add explicit dry-run/sandbox proof before any live test.
