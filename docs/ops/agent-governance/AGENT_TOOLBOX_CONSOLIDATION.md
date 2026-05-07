# Agent Toolbox Consolidation

Last updated: `2026-05-06`

This is the working list for consolidating agent toolboxes into usable skills, scripts, and documentation.

Authorization still comes from:

- `platform-registry.yaml`
- `agent-toolbox-matrix.yaml`
- route packages / protocol matrices
- global approval gates

This document is for iteration planning. It does not grant permission by itself.

## Consolidation Rule

Consolidate in this order:

1. agent role and owned business surface
2. platform registry entry and owner
3. platform/toolbox read operations
4. platform/toolbox write operations
5. reusable script or CLI wrapper
6. skill documentation
7. route/protocol proof contract
8. beta/prod promotion evidence

If a tool use happens once, keep it direct and logged.
If it repeats with the same input and proof shape, make it a protocol candidate.

## Agent / Toolbox List

| Agent | Owner scope | Current toolboxes | Write policy | Consolidation focus |
| --- | --- | --- | --- | --- |
| Jack | transversal routing, supervision, governed direct execution | Mission Manager read/supervision, KG, specialist dispatch, governed platform skills, Higgsfield supervision, browser verification, filesystem governance | writes only through governed routes and approval gates | make toolbox changes precise: owner, route, proof, approval gate |
| Jack-X | long-term memory and channel intake | MS365 read, Lark read, WhatsApp snapshot read, MM session read, memory wiki, KG candidate/update | KG/memory updates only through validation path | add refinement/dedup layer after memory validation |
| Mnemos | continuity and compaction | local session state, context metering, continuity artifacts | local continuity artifacts only | keep scope narrow; no external surface |
| Rosa | marketing, offers, performance, market intelligence | Shopify read, Klaviyo read, Hiboo read, Lark read, GA4, GSC, DataForSEO, creative request via Kanye/Jack | campaign/storefront/CRM mutation approval-gated | split analytics reads from campaign mutation; define creative handoff format |
| Jeff | influence, creators, outreach, collaboration ops | Hiboo creators, creator profile read, inbox signals, candidate registry, report artifacts | contact/collaboration/contract mutation approval-gated | standardize creator intake and outreach draft proof |
| Naya | stock, sourcing, supply chain feasibility | Shopify read, BigBlue read, stock telemetry, sourcing sheets, reports | supplier/order/purchase/payment mutation approval-gated | standardize stock evidence and supplier question packs |
| Selena | support risk, PayPal disputes, Zendesk feedback | PayPal read, Zendesk read, reviewed exports, support-risk reports | replies, dispute messages, refunds/payments approval-gated | preserve strict read/write separation and proof before any customer-visible action |
| Alfred | SEO visibility and strategy artifacts | GSC, DataForSEO, GA4, site-audit reads, report artifacts | site/theme/publication mutation approval-gated | standardize report bundle and strategy-plan inputs |
| Cortex | paid-media observation and handoff | Hiboo ads read, Meta Ads read, Google Ads read, creative observation, creative request via Kanye/Jack | live campaign/ad publication approval-gated | turn repeated observation into campaign feedback protocol candidates |
| Tony | development and git | repository filesystem, terminal, git, GitHub, package managers, tests/build/lint, browser dev verification | deploy/restart/release only by explicit delegation outside this governance lane | centralize script hardening and test commands when delegated |
| Kanye | creative generation and reference edits | Hermes `creative_generate`, official Higgsfield CLI skills, image/video providers, reference media, local media artifacts | generated artifacts allowed locally; publication/delivery mutation approval-gated | harden Higgsfield wrappers, manifests, model caveats, product photoshoot validation |
| Safir | email/CRM audit and workflow design | MS365 read, Klaviyo read, email template analysis, email design/draft generation, creative request via Kanye/Jack | external send or CRM mutation approval-gated | reopen email workflow with modern image/design model floor and render proof |

Deferred agents:

| Agent | Status | Handling |
| --- | --- | --- |
| Jackette | draft | keep for later; no V1 toolbox consolidation |
| Jhin | draft | keep for later; no V1 toolbox consolidation |
| Walter | draft | keep for later; no V1 toolbox consolidation |

## Skill Consolidation Queue

| Toolbox / skill family | Owner agent | Current maturity | Backend/script focus | Documentation focus | Proof target |
| --- | --- | --- | --- | --- | --- |
| Higgsfield official CLI `higgsfield-generate` | Kanye | beta | wrap polling recovery and download flow | command surface, model caveats, failure recovery | prompt, job JSON, media, manifest |
| Higgsfield `product-photoshoot` | Kanye | beta | use local helper for attachment provenance, accepted ratios, recovery, downloads, and manifest | input requirements, safe prompts, image constraints, attachment metadata, QA checklist | generated media and manifest |
| Higgsfield `marketplace-cards` | Kanye | draft test pending | validate scoped marketplace generation | compliance notes and forbidden publication paths | media set, manifest, compliance notes |
| Higgsfield `soul-id` | Kanye | draft gated | verify model id and training flow only after approval | consent, photo manifest, cost check | approval record and manifest |
| Email workflow | Safir | draft | renderable email draft pipeline, asset handoff | business requirements, brand voice, approval before send | HTML/PDF/render proof and final summary |
| Shopify read/write split | Rosa/Naya | beta by route | read helpers for product/order/stock, mutation wrappers later | read vs mutation rules and brand scoping | JSON readback or report bundle |
| Klaviyo read/design split | Safir/Rosa | beta/draft | list/fetch/audit helpers, no send by default | CRM mutation and send gates | audit artifact or rendered draft |
| Zendesk/PayPal support surfaces | Selena | prod for reads | keep live fetch/readback stable; no reply/mutation wrapper without approval | customer-visible action checklist | pre/post readback and approval record |
| Paid media observation | Cortex | prod/draft by route | stable read snapshots and report generation | campaign mutation gates and handoff rules | report bundle and delivery JSON |
| SEO/data visibility | Alfred | prod/beta by route | stable report builders and strategy inputs | report bundle requirements | HTML/PDF/JSON bundle |
| Creator/influence ops | Jeff | prod/beta by route | creator profile/candidate intake helpers | outreach and collaboration mutation gates | candidate/report bundle |
| Memory/KG intake | Jack-X | beta | dedup/refinement after validation | source confidence and stale-data rules | memory candidate and validation summary |
| Continuity context | Mnemos | beta | context pressure and capsule scripts | reinjection contract | continuity artifact |
| Dev tooling | Tony | beta | test/build/lint and mechanical doc/script hardening | changed files, tests, limitations | verification report |
| Toolbox governance | Jack | beta | matrix updates and route candidate creation | owner, gates, proof, promotion status | matrix diff and final summary |

## Iteration Template

Use this template for each skill/toolbox consolidation pass:

```yaml
owner_agent: ""
toolbox: ""
business_requirement: ""
backend_surface:
  read_tools: []
  write_tools: []
  forbidden_tools: []
scripts_to_harden: []
docs_to_update: []
approval_gates: []
proof_target: ""
current_status: draft
promotion_target: beta
open_questions: []
```

## Next Recommended Iterations

1. Kanye: harden `higgsfield-generate` into a repeatable beta wrapper and run additional product photoshoot QA variants.
2. Safir: reopen email workflow with modern design/image capabilities, but keep sending approval-gated.
3. Rosa/Naya: normalize Shopify read operations and separate every mutation path.
4. Selena: keep Zendesk/PayPal reads prod-stable and document the exact approval checklist for replies/refunds.
5. Jack-X: define the refinement layer for memory dedup and stale-information cleanup.

## Done Criteria

A toolbox consolidation is done when:

- the owning agent is explicit
- read and write operations are separated
- approval-gated actions are named
- scripts or CLI commands are documented
- output paths and proof target are stable
- route status is `draft`, `beta`, or `prod`
- unresolved ambiguities are listed instead of hidden
