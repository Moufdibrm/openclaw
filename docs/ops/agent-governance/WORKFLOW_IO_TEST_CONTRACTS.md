# Workflow IO Test Contracts

Last updated: `2026-05-06`

This document defines what each governed workflow should receive, produce, and return to Moufdi after deployment/runtime wiring is available.

It is a governance and test contract only.
It does not deploy, restart, edit gateway/runtime code, or mutate Mission Manager.

## Standard Test Render

For every workflow test, the rendered response sent back to Moufdi should include:

- workflow id
- status: `passed`, `passed_with_warnings`, `failed`, or `blocked`
- `brand_scope` when the workflow or deliverable is brand-linked
- exact input summary
- output artifact paths or links
- proof artifact paths
- any approval gate that blocked mutation
- any gap to fix before beta/prod promotion

Do not mark a workflow as passed from a chat answer alone.
A workflow test passes only when the expected artifact/proof exists.

## Common Inputs

| Input class | Examples | Handling |
| --- | --- | --- |
| Request text | prompt, task request, operator question | Store in prompt/request artifact when protocol expects replay. |
| Brand/store scope | `brand_scope.scope_id`, `brand_pack_id`, `focus_mode`, `subject_id` | Must be explicit before business reads/writes and echoed in every brand-linked deliverable; see `BRAND_SCOPE_CONTRACT.md`. |
| Time scope | days, date, end date | Must be explicit for analytics/support/inbox reports. |
| Reviewed artifact | CSV, JSON, report-data bundle, sourcing sheet | Store as governed attachment and include hash/path in proof when possible. |
| Live platform scope | Shopify, PayPal, Zendesk, Klaviyo, Meta Ads, GSC | Read-only unless route explicitly allows mutation and approval is present. |
| Creative attachment | product cutout, source image, style reference | Follow `SKILL_ATTACHMENT_POLICY.md`. |

## Common Outputs

| Output class | Expected shape |
| --- | --- |
| `compact_json` | machine-readable summary with inputs, decisions, blockers, proof paths |
| `verification_json` | route validation result, source checks, assumptions, replay markers |
| `report_bundle` | HTML/PDF/JSON or equivalent report package |
| `generated_media` | local media path plus manifest |
| `memory_candidate` | source-scoped memory candidate, confidence, freshness, owner |
| `mission_patch` | proposed Mission Manager change, not applied unless owner/runtime route allows |
| `delivery_json` | delivery/readback record, approval-gated if external |
| `final_summary` | concise operator-readable result |

Every brand-linked output class must carry `brand_scope` directly or through a sidecar manifest. Missing `brand_scope` is a validation gap, not a harmless omission.

## Workflow Contracts

### Jack

| Workflow | Status | Inputs to test | Expected outputs | Render sent here |
| --- | --- | --- | --- | --- |
| `jack.protocol-missing` | beta | `request_text`, `target_agent`, optional `source_channel`, `reason_code` | `compact_json`, protocol candidate bundle, `final_summary` | candidate path, target agent, missing route reason, next decision |
| `jack.capability-missing` | beta | `request_text`, `capability_slug`, optional label/coverage hints | `compact_json`, capability coverage matrix, suggested agents | coverage summary, missing capability, proposed owner |
| `jack.draft-protocol-runtime` | beta | `bundle_path`, `draft_mode`, optional prompt | `compact_json`, `verification_report` | draft lifecycle status, bundle path, validation gap |
| `jack.direct.mm-supervision` | beta/package | mission context, intended MM change, current state | `decision_json`, `mission_patch`, `final_summary` | proposed patch only; no hidden MM mutation |
| `jack.email-digest` | beta/package | qualified Jack-X mail artifact(s), operator scope | digest summary, `delivery_summary` | digest bullets, source artifact, blocked delivery if no approval |
| `jack.higgsfield-skill-supervision` | draft | creative prompt, source image if any, owner decision | installed skill summary, auth presence, media manifest if run | generated media paths or explicit handoff to Kanye |

### Jack-X

| Workflow | Status | Inputs to test | Expected outputs | Render sent here |
| --- | --- | --- | --- | --- |
| `jack-x.registry-ingest` | beta/package | registry source, channel scope | `runtime_summary`, `verification_json` | ingested counts, rejected records, proof path |
| `jack-x.email-intake-pass0` | beta/package | MS365 mailbox/window/store scope | `compact_json`, `memory_candidate` | memory candidates, source refs, freshness |
| `jack-x.lark-message-intake-pass0` | beta/package | Lark channel/window | `compact_json`, `memory_candidate` | extracted decisions/signals, source refs |
| `jack-x.lark-table-intake-pass0` | beta/package | Lark table/view/filter | `compact_json`, `memory_candidate` | rows considered, candidate records |
| `jack-x.whatsapp-intake-pass0` | beta/package | WhatsApp snapshot/window/contact scope | `compact_json`, `memory_candidate` | extracted signals, ambiguity list |
| `jack-x.db-analysis` | beta/package | memory DB/projection scope | `memory_projection`, `runtime_summary` | memory health, conflicts, stale data |
| `jack-x.memory-wiki` | beta/recurring-script | Jack-X channel reports, latest memory projection, semantic mode | Memory Wiki manifest, pages, `kg_operations`, `review_items` | page count, review count, key aliases/relations/open questions |
| `jack-x.memory-refinement-review` | draft/planned | Memory Wiki `kg_operations`, source page, source refs, KG health status | refinement review artifact, accepted/rejected/deferred counts, commit or skip reason | proposed durable deltas and why each was accepted, blocked, or deferred |
| `jack-x.memory-feedback-loop` | draft/planned | previous KG fact, later signal, source refs, correction scope | feedback event, correction candidate, review decision, supersession/confirmation summary, retrieval proof | what changed over time, what was preserved, what was corrected, and why |
| `jack-x.signal.extract` | beta/package | bounded signal artifact | `handoff_packet`, `mission_patch`, `memory_candidate` | extracted action/memory split, proposed patch |

### Mnemos

| Workflow | Status | Inputs to test | Expected outputs | Render sent here |
| --- | --- | --- | --- | --- |
| `mnemos.context-check` | beta/package | session/context snapshot, pressure threshold | `memory_observation`, `verification_json` | pressure state, reinjection need, capsule path |

### Rosa

| Workflow | Status | Inputs to test | Expected outputs | Render sent here |
| --- | --- | --- | --- | --- |
| `rosa.offer-strategy.direct` | prod | `prompt`, optional `store`, optional Drive flag | `decision_json`, `verification_json`, `final_summary` | recommendation, assumptions, artifact paths |
| `rosa.audit-performance-marketing` | prod | `store`, optional `period_days`, `end_date`, upload flag | `report_bundle`, `verification_json` | report link/path, top findings, data gaps |
| `rosa.veille-concurrentielle` | prod | `store`, `domain`, optional `refresh_market_graph` | `report_bundle`, `verification_json` | competitive findings, graph/report paths |
| `rosa.market-graph-refresh` | beta | store/domain/SEO capture scope | `graph_snapshot`, `verification_json` | promoted snapshot path, freshness, blocked gaps |

### Jeff

| Workflow | Status | Inputs to test | Expected outputs | Render sent here |
| --- | --- | --- | --- | --- |
| `jeff.analyse-profil` | prod | `creator_handle`, `store` | pass0 bundle, `report_bundle`, `verification_json` | creator verdict, report path, confidence |
| `jeff.performance-report` | prod | `store`, `period_days`, optional upload flag | `report_bundle`, `verification_json`, `delivery_json` | performance summary, report path, delivery status |
| `jeff.candidate-intake` | beta | candidate profile/source artifact | `candidate_intake_bundle`, `verification_json` | candidate record, graph readiness, gaps |
| `jeff.email-digest` | beta/planned | inbox artifact/window | digest artifact | digest path, contact-send blocked unless approval |
| `jeff.outreach-pipeline` | beta/planned | creator/campaign context | outreach artifact | draft outreach plan, approval gate |
| `jeff.ajout-collaboration` | beta/planned | collaboration target/delta | pre/post mutation evidence | pre-mutation summary; mutation blocked without approval |
| `jeff.collab-management` | beta/planned | collaboration id/action/delta | pre/post mutation evidence | proposed update, approval/readback status |

### Naya

| Workflow | Status | Inputs to test | Expected outputs | Render sent here |
| --- | --- | --- | --- | --- |
| `naya.stock-check` | prod | `store`, `product_query`, optional reviewed stock snapshot | `stock_check_json`, `final_summary` | stock verdict, source snapshot, risk |
| `naya.product-sourcing` | prod | reviewed sourcing sheet, optional upload flag | `report_bundle`, `verification_json` | sourcing recommendation, report path |
| `naya.campaign-support` | beta/planned | campaign/product/SKU scope | campaign support artifact | feasibility verdict, stock blocker |
| `naya.supplier-comm` | draft/planned | supplier target, draft intent | draft and explicit approval | draft only; no supplier send |

### Selena

| Workflow | Status | Inputs to test | Expected outputs | Render sent here |
| --- | --- | --- | --- | --- |
| `selena.paypal-dispute.phase1-audit` | prod | reviewed dispute export, `store` | `paypal_dispute_audit`, `final_summary` | dispute risk summary, artifact path |
| `selena.paypal-dispute.phase1-live` | prod | `store`, optional days/case limit/export | `paypal_dispute_live_audit`, `final_summary` | fetched case count, risk summary, no dispute message |
| `selena.zendesk-feedback-review` | prod | Zendesk export, `store` | `zendesk_feedback_review`, `final_summary` | feedback themes, artifact path |
| `selena.zendesk-feedback-live` | prod | `store`, optional days/ticket limit/comments flag | `zendesk_feedback_live_review`, `final_summary` | fetched ticket count, risks, no customer reply |

### Alfred

| Workflow | Status | Inputs to test | Expected outputs | Render sent here |
| --- | --- | --- | --- | --- |
| `alfred.visibility-audit` | prod | report-data bundle, `store`, optional date/domain/upload flag | HTML/PDF/JSON bundle, `verification_json` | report paths, top SEO actions, data gaps |
| `alfred.strategy-plan` | beta/planned | phase1 audit artifact, strategy scope | strategy report, workboard | strategy path, workboard summary |
| `alfred.deployment-feedback-loop` | beta/planned | deployment feedback artifacts | feedback report, queue artifacts | feedback summary, next-cycle queue |

### Cortex

| Workflow | Status | Inputs to test | Expected outputs | Render sent here |
| --- | --- | --- | --- | --- |
| `cortex.ads-observation` | prod | `store`, optional workspace/mission/upload fields | `report_bundle`, `verification_json`, `delivery_json` | paid-media findings, report path, delivery status |
| `cortex.campaign-management` | draft/planned | campaign objective, budget/scope, brand | campaign-management report, task board | proposed plan only; no live campaign mutation |
| `cortex.feedback-loop` | draft/planned | post-publication metrics/artifacts | feedback report, next-cycle input | feedback path, next test recommendations |

### Tony

| Workflow | Status | Inputs to test | Expected outputs | Render sent here |
| --- | --- | --- | --- | --- |
| `tony.codebase-exploration` | beta | `prompt`, optional `target_repo`, upload flag | `compact_json`, `final_summary` | topology/findings, files inspected, blockers |
| `tony.development-plan` | beta | `target_repo`, `task_request`, `exploration_artifact`, optional prompt | `compact_json`, `verification_report` | plan path, risk, test plan |
| `tony.development` | beta | repo, task, exploration artifact, dev plan | `code_delta`, `verification_report`, `final_summary` | changed files, tests, remaining risk |

### Kanye

| Workflow | Status | Inputs to test | Expected outputs | Render sent here |
| --- | --- | --- | --- | --- |
| `kanye.still-generate` | beta | prompt, optional route/intent/source image | generated media, manifest | media paths, manifest, route used |
| `kanye.reference-edit` | beta | prompt, source image, optional route | edited media, manifest | media paths, manifest, source image |
| `kanye.higgsfield-skill-exploration` | beta/planned | installed skill/package scope | skill surface summary, auth presence, command surface | installed skills, CLI status, gaps |
| `kanye.higgsfield-skill-validation` | beta/planned | bounded prompt/source media | test artifacts, manifest, cost/error notes | pass/fail, artifact paths, caveats |
| `kanye.higgsfield-generate.official-cli` | beta/planned | prompt, model/route, optional source media | prompt, job JSON, downloaded media, manifest | media path, job id, recovery status |
| `kanye.higgsfield-product-photoshoot.validation` | beta/planned | product image, mode, prompt, safe ratio | attachment metadata, media, manifest | media paths, manifest, caveats |
| `kanye.higgsfield-marketplace-cards.validation` | draft/planned | product image, marketplace scope, brand constraints | media set, manifest, compliance notes | media set paths, compliance verdict |
| `kanye.higgsfield-soul-id.validation` | draft/planned | explicit approval, consent, identity photos, model check | approval record, photo manifest, soul status, reuse test | blocked unless approval/consent; no silent identity run |

### Safir

| Workflow | Status | Inputs to test | Expected outputs | Render sent here |
| --- | --- | --- | --- | --- |
| `safir.email-audit` | beta | `store`, `parent_record_id` | `safir_email_audit`, `final_summary` | audit path, issues, no send |
| `safir.mail-pole-audit` | beta | `store`, optional period days, skip-drive default | `safir_mail_pole_audit`, `final_summary` | audit path, pole summary, no Drive mutation unless approved |
| `safir.email-workflow` | draft/planned | brand, campaign goal, offer, audience, assets | draft email workflow, render proof, approval before send | HTML/PDF/render path, subject/body summary, send blocked |

## Test Execution Order After Deployment

Recommended order:

1. Read-only artifact-fed prod routes: Selena export reviews, Naya sourcing, Alfred visibility render.
2. Read-only live prod routes: Selena live reads, Rosa performance, Cortex ads observation.
3. Creative beta routes: Kanye still/reference/product photoshoot.
4. Dev beta routes: Tony exploration/plan/development with harmless repo fixture.
5. Planned/draft workflows: Safir email-workflow, Kanye marketplace, Jack-X refinement.

## Done Criteria Per Workflow

A workflow is test-complete when:

- required inputs are explicit
- output artifacts exist
- proof artifact exists
- rendered response was sent here with paths
- approval-gated mutations are either blocked or explicitly approved
- status and gaps are updated in the relevant matrix
