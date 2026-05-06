# Phase 0 Fixture Inventory

Last updated: `2026-05-06`

This inventory records the real local fixtures available before post-deploy workflow tests.

Scope is governance only. It does not deploy, restart services, edit gateway/runtime code, mutate Mission Manager, or contact external parties.

## Summary

Fixture readiness:

- `available`: 12
- `partial`: 3
- `needed`: 1

Important distinction:

- Input fixtures are safe materials that can be fed to a workflow runner.
- Golden output fixtures are prior deliverables used to verify expected output shape.

A prior deliverable is useful evidence, but it does not always prove that the exact runner input is ready.

## Brand Scopes

| Fixture | Status | Canonical data | Notes |
|---|---:|---|---|
| `brand_scope_maybe_paris` | available | `/Users/moufdi/clawd/config/brand-packs/maybe-paris.json` | `brand_id=maybe-paris`, `store_key=maybe-paris`, `canonical_domain=maybe-paris.co`. Brand pack itself remains `partial`, mainly around some marketing/analytics/Hiboo surfaces. |
| `brand_scope_blinx` | available | `/Users/moufdi/clawd/config/brand-packs/blinx.json` | `brand_id=blinx`, `store_key=blinx`, `canonical_domain=blinxunderwear.com`. Logistics remains unknown. |
| `brand_scope_botanic` | available | `/Users/moufdi/clawd/config/brand-packs/botanic.json` | `brand_id=botanic`, `store_key=botanic`, `canonical_domain=trybotanic.com`. GA4, Hiboo ids, and logistics are incomplete. |

Rule: missing brand surfaces block only that surface, not unrelated work on the same brand.

## Business Ops

| Agent | Workflow / fixture | Status | Evidence path | Test meaning |
|---|---|---:|---|---|
| Selena | `paypal_reviewed_dispute_export` | available | `/Users/moufdi/.openclaw/workspace-selena/fixtures/paypal-dispute-audit-001.json` | Input fixture exists for `selena.paypal-dispute.phase1-audit`; no PayPal/dispute message is allowed without approval. |
| Selena | `zendesk_reviewed_export` | available | `/Users/moufdi/.openclaw/workspace-selena/fixtures/zendesk-feedback-review-001.json` | Input fixture exists for `selena.zendesk-feedback-review`; no customer-visible reply is allowed without approval. |
| Naya | `reviewed_sourcing_sheet` | partial | `/Users/moufdi/.openclaw/workspace-naya-test/deliverables/maybe-paris/naya-product-sourcing/2026/2026-04-14__sourcing-accessories__mm-none__run-2026-04-03-accessories/manifest.json` | Golden output bundle exists, but a reviewed runner input sheet/path is not isolated yet. |
| Naya | `stock_snapshot_or_known_sku` | partial | `/Users/moufdi/.openclaw/jack-handoff-sweep-2026-04-14-full/naya__stock-check/dispatch.json` | Dispatch/transcript exists, but no reviewed stock snapshot or known SKU/product query was found. |
| Alfred | `seo_report_data_bundle` | available | `/Users/moufdi/.openclaw/workspace-alfred/reports/maybe_paris/2026-03-22-visibility-audit/visibility-audit.report-data.reviewed.json` | Reviewed report-data fixture exists for `alfred.visibility-audit`. |
| Jeff | `creator_profile_fixture` | available | `/Users/moufdi/.openclaw/workspace-jeff/deliverables/maybe-paris/jeff-analyse-profil/2026/2026-04-15__analyse-profil-romi-allata__mm-176__run-20260415t110759z/manifest.json` | `creator_handle=romi_allata`, `store=maybe-paris` is usable for profile analysis. |
| Safir | `safir_email_workflow_brief` | needed | none | No business brief fixture found. Needs `brand`, `campaign_goal`, `offer`, `audience`. |

Additional golden outputs available:

- Rosa `offer-strategy.direct`: `/Users/moufdi/.openclaw/workspace-rosa/deliverables/maybe-paris/rosa-offer-strategy-direct/2026/2026-04-15__offer-strategy-maybe-paris__mm-156__run-20260415t144822z/manifest.json`
- Rosa `audit-performance-marketing`: `/Users/moufdi/.openclaw/workspace-rosa/data/deliverables/maybe-paris/rosa-audit-performance-marketing/2026/2026-04-15__audit-performance-marketing-maybe-paris__mm-177__run-20260415t013337z/manifest.json`
- Rosa `veille-concurrentielle`: `/Users/moufdi/.openclaw/workspace-rosa/deliverables/maybe-paris/rosa-veille-concurrentielle/2026/2026-04-15__veille-concurrentielle-maybe-paris__mm-178__run-20260415t021027z/manifest.json`
- Jeff `performance-report`: `/Users/moufdi/.openclaw/workspace-jeff/deliverables/maybe-paris/jeff-performance-report/2026/2026-04-14__performance-report-maybe-paris__mm-none__run-20260414t180537z/manifest.json`
- Cortex `ads-observation`: `/Users/moufdi/.openclaw/workspace-cortex/deliverables/maybe-paris/cortex-ads-observation/2026/2026-04-15__ads-observation-maybe-paris__mm-174__run-20260415t162850z/manifest.json`
- Cortex `campaign-management`: `/Users/moufdi/.openclaw/workspace-cortex/reports/campaign-management/2026-04-03T21-04-02Z-maybe-paris/campaign-management.manifest.json`

## Technical / Memory

| Agent | Fixture | Status | Evidence path | Test meaning |
|---|---|---:|---|---|
| Jack | `jack_protocol_fixture_pack` | partial | `/Users/moufdi/hermes-runtime/contracts/jack-protocol-corpus-001.md` | Contracts/corpus exist for protocol/capability tests, but no post-deploy Jack run artifact was found. |
| Jack-X | `jack_x_memory_fixture_pack` | available | `/Users/moufdi/hermes-runtime/contracts/jack-x-batch-3-corpus-001.json` | Contract examples and runtime-baseline slice exist for registry, intake, DB analysis, and signal extraction fixture tests. |
| Mnemos | `mnemos_context_snapshot` | available | `/Users/moufdi/hermes-runtime/contracts/mnemos-context-check.context.example.json` | Context-check input fixture exists; proof result exists under workspace Mnemos. |
| Tony | `tony_fixture_repo` | available | `/Users/moufdi/hermes-runtime/fixtures/tony-dev-fixture-template` | Minimal fixture repo is enough for smoke/dev workflow validation. It is not a rich regression project. |

Jack-X note: live snapshots exist in `/Users/moufdi/.openclaw/workspace-jack-x`, but fixture tests should prefer contract examples and `/Users/moufdi/.openclaw/workspace-jack-x/runtime-baselines/kg-upgrade-slice-001` to avoid noisy live data.

## Creative

| Agent | Fixture | Status | Evidence path | Test meaning |
|---|---|---:|---|---|
| Kanye | `kanye_monoi_product_cutout` | available | `/Users/moufdi/.openclaw/workspace-kanye/higgsfield-product-photoshoot-validation/20260505T222952Z/monoi_love_detoure.png` | Public Monoi Love product cutout is mirrored locally for attachment-safe tests. |
| Kanye | `kanye_reference_edit_safe_image` | available | `/Users/moufdi/.openclaw/workspace-kanye/higgsfield-product-photoshoot-runs/20260505T232850Z/attachments/monoi_love_helper_validation.png` | Same non-private source image can be used for reference-edit smoke tests. |

Existing Higgsfield proof manifests:

- `/Users/moufdi/.openclaw/workspace-kanye/higgsfield-validation/20260505T214148Z/manifest.json`
- `/Users/moufdi/.openclaw/workspace-kanye/higgsfield-product-photoshoot-validation/20260505T222952Z/manifest.json`
- `/Users/moufdi/.openclaw/workspace-kanye/higgsfield-product-photoshoot-qa/20260505T230630Z/manifest.json`
- `/Users/moufdi/.openclaw/workspace-kanye/higgsfield-product-photoshoot-runs/20260505T232850Z/manifest.json`

## Blockers Before Full Phase 1

1. Isolate a reviewed input sheet or request fixture for `naya.product-sourcing`.
2. Choose a reviewed SKU/product query or stock snapshot for `naya.stock-check`.
3. Create a Safir email workflow brief fixture with `brand`, `campaign_goal`, `offer`, and `audience`.
4. Decide whether Jack protocol/capability routes can be tested from contract corpus only, or need a fresh post-deploy artifact.

## Approval Gates

Always block before:

- external messages
- customer-visible support replies
- PayPal/dispute messages
- refunds, payment, billing, dispute, or financial mutations
- supplier messages
- CRM/send mutations
- campaign/ad publication or paid delivery mutation
- public creative publication
- identity/private media use without explicit approval and consent
