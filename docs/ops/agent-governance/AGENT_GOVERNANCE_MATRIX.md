# Agent Governance Matrix

Last updated: `2026-05-07`

## Current State

The real system has more profiles than governed V1 agents.
The V1 governance scope is:

| Agent | Product status | Real role | Canonical local workdir | Route status |
| --- | --- | --- | --- | --- |
| Jack | beta | transversal operator, routing, direct execution when governed | `~/clawd` | partial, core missing/capability/draft routes exist; Higgsfield skill installed for governed direct/supervised use |
| Jack-X | beta | long-term memory, channel intake, KG/memory updates, Memory Wiki refinement review | `~/.openclaw/workspace-jack-x` | packages exist, Memory Wiki compiles pages, KG commit proof currently blocked by KG health |
| Mnemos | beta | continuity and compaction preservation | `~/.openclaw/workspace-mnemos` | package exists, not in specialist registry |
| Rosa | beta | marketing, offers, performance, market intelligence | `~/.openclaw/workspace-rosa` | several prod route scopes |
| Jeff | beta | influence, creators, outreach, collaboration ops | `~/.openclaw/workspace-jeff` | several prod route scopes, wider nodes partial |
| Naya | beta | stock, sourcing, supply chain decisions | `~/.openclaw/workspace-naya` | validated stock/sourcing floor |
| Selena | beta | support risk, PayPal/Zendesk review | `~/.openclaw/workspace-selena` | V1 phase1 routes production-usable |
| Alfred | beta | SEO visibility and strategy artifacts | `~/.openclaw/workspace-alfred` | phase1 prod, phase2/3 supervised |
| Cortex | beta | paid media observation and campaign handoff | `~/.openclaw/workspace-cortex` | phase1 prod, phase2/3 drafted |
| Tony | beta | development owner: exploration, planning, implementation, tests, git | `~/.openclaw/workspace-tony` | one agent with `explore`/`plan`/`execute`/`review` modes; exploration contract alignment still blocking prod-ready |
| Kanye | beta | creative generation and reference edits | `~/.openclaw/workspace-kanye` | generation floor live; HF API pair configured, official Higgsfield CLI live still test passed |
| Safir | beta | email/CRM audit and workflow design | `~/.openclaw/workspace-safir` | audit floor live, email-workflow to reopen |

Deferred agents:

| Agent | Status | Reason |
| --- | --- | --- |
| Jackette | draft | legacy ops assistant profile, no V1 route/package governance |
| Jhin | draft | legacy creative execution profile, no V1 route/package governance |
| Walter | draft | legacy B2B profile, no V1 route/package governance |

## Common Permission Model

Autonomy levels:

1. `audit_read`
   - read, inspect, summarize, compare, report
   - no business mutation
2. `discussion_approval`
   - discuss, plan, draft, prepare changes
   - ask before external/business mutation
3. `autonomous_e2e_validated_route`
   - execute only if the route is already validated and the route allowlist covers the tools
   - still obeys global approval gates

Global approval gates:

- outbound email or message to an external party
- Zendesk or PayPal customer/dispute communication
- refund, payment, billing, dispute, invoice, subscription, or financial mutation
- mutation with unclear target, unclear tenant, unclear brand, or unclear delta

## Toolboxes By Agent

| Agent | Allowed toolbox families | Forbidden or gated |
| --- | --- | --- |
| Jack | MM, KG, specialist dispatch, governed platform skills, Higgsfield supervised/direct creative use when requested, browser after canonical proof, filesystem/docs governance | hidden prod deploy/restart, gateway/MM code, direct high-risk mutation without route |
| Jack-X | MS365 read, Lark read, WhatsApp snapshot read, MM agent session read, memory/KG candidate/update path, Memory Wiki refinement review | external replies, payments, support replies, business-system mutation, direct LLM Wiki KG writes |
| Mnemos | local session state, context metering, continuity artifacts | external read/write, KG durable truth ownership, business execution |
| Rosa | marketing analytics, Shopify/Klaviyo/Hiboo/GA4/GSC/DataForSEO/Lark reads, report artifacts, creative asset requests via Kanye/Jack | direct Higgsfield generation, external publication or campaign mutation unless route+approval |
| Jeff | creator/portfolio/inbox/Hiboo scripts, outreach artifacts, collaboration drafts | outbound creator contact or collaboration mutation without approval |
| Naya | Shopify/BigBlue/stock telemetry/sourcing sheets, sourcing and stock reports | supplier message, order mutation, purchase/payment without approval |
| Selena | PayPal/Zendesk fetch/review, support-risk reports | customer-visible reply, dispute action, refund/payment mutation without approval |
| Alfred | SEO/GSC/DataForSEO/GA4/site audit scripts, report artifacts | site/theme mutation or Drive delivery without approval |
| Cortex | paid-media observations, Hiboo ads/Meta/Google Ads reads, creative/report artifacts, creative asset requests via Kanye/Jack | direct Higgsfield generation, live campaign mutation without approval and route |
| Tony | repository filesystem, terminal, git, tests/build/lint, package managers, browser dev verification, GitHub when requested | prod deploy/restart/systemd/gateway/MM lane, business-system mutation, external messages unless explicitly delegated |
| Kanye | creative generation routes, image/video providers, local media artifacts, official Higgsfield skills installed in profile | external campaign publication or delivery mutation without approval |
| Safir | email/CRM analysis, Klaviyo/MS365 reads, email design/draft generation, creative asset requests via Kanye/Jack | direct Higgsfield generation, sending external mail or CRM mutation without approval |

## Environments By Agent

Canonical local roots:

- `/Users/moufdi/hermes-runtime`
- `/Users/moufdi/openclaw`
- `/Users/moufdi/clawd`
- `~/.openclaw/workspace-<agent>`
- `~/.brm-hermes/profiles/<agent>`

Canonical production truth:

- Jack/Hermes runtime: VPS profile homes under `/home/ubuntu/.brm-hermes/profiles`
- Mission Manager truth: hosted ECS/ALB, not local Mac behavior
- Business brand truth: `~/clawd/config/brands.json` and `~/clawd/config/brand-packs/*.json`

Legacy or unclear local roots:

- `BRMXHERMES/clawd`
- `BRMXHERMES/clawd/workspace/creative`
- `BRMXHERMES/clawd/workspace/b2b`
- `BRMXHERMES/clawd/workspace/supply-chain`
- `BRMXHERMES/clawd/workspace/tech`

These are not canonical V1 governance roots unless a route says so.

## External Surfaces By Agent

| Agent | Read surfaces | Mutable surfaces |
| --- | --- | --- |
| Jack | MM, KG, platform skills, route registry, brand packs, Higgsfield skill surface when governed | governed MM/KG/platform writes and generated media artifacts only through request/route and approval gates |
| Jack-X | MS365, Lark, WhatsApp snapshot, MM agent sessions, Memory Wiki manifests/pages | local memory, review queue, KG updates through governed validation; LLM Wiki writes pages and proposals only |
| Mnemos | local session/context state | continuity capsules and local continuity journal |
| Rosa | Shopify, Klaviyo, Hiboo, Lark, GA4/GSC/DataForSEO, paid snapshots | local report artifacts; business mutation only if route+approval |
| Jeff | Hiboo, creator/profile data, inbox inputs, registry artifacts | local reports/candidate registry; collaboration/contact mutation approval-gated |
| Naya | Shopify, BigBlue, sourcing sheets, stock telemetry | local reports; supplier/order/business mutation approval-gated |
| Selena | PayPal, Zendesk, reviewed exports | local support-risk reports; support/payment mutation approval-gated |
| Alfred | SEO/search/analytics/site data | local reports; Drive upload approval-gated |
| Cortex | paid media and ad observation sources | local reports; campaign mutation approval-gated |
| Tony | repos, tests, Git/GitHub as requested | code/git artifacts; deploy/restart outside normal lane |
| Kanye | creative inputs, reference media, Higgsfield auth/command surface | generated media artifacts; publication/delivery approval-gated |
| Safir | MS365/Klaviyo/email/template inputs | local email/report artifacts; sending approval-gated |

## Protocols And Routes

Use `agent-protocol-matrix.yaml` as the current machine-readable map.

Important current gaps:

- `jack-x.*`, `jack.email-digest`, `jack.direct.mm-supervision`, and `mnemos.context-check` are package-backed but absent from `specialist-route-registry.json`.
- Jack-X has a KG commit path, but the audited local KG JSONL is invalid and recent commits cannot be trusted until repair/validation is complete.
- LLM Wiki has the right product role as a slow consolidation layer, but its `kg_operations` need a governed Jack-X refinement review bridge before they can affect durable KG.
- `Safir email-workflow` is not closed. It should be reopened as a new beta/draft route using the improved email/design model floor.
- `higgsfield-ai/skills` is installed locally in Jack and Kanye profiles with four skills: `higgsfield-generate`, `higgsfield-marketplace-cards`, `higgsfield-product-photoshoot`, and `higgsfield-soul-id`. The HF API pair is configured for the existing Hermes generation tool, and the official Higgsfield CLI is installed/authenticated locally. A bounded GPT Image 2 still test passed with manifest `/Users/moufdi/.openclaw/workspace-kanye/higgsfield-validation/20260505T214148Z/manifest.json`; a bounded Monoi Love product-shot test passed with manifest `/Users/moufdi/.openclaw/workspace-kanye/higgsfield-product-photoshoot-validation/20260505T222952Z/manifest.json`. Remaining gaps: standardize polling failure recovery, refine product lifestyle prompt-safety after one `nsfw` false-positive, and QA more owner-run variants before prod.
- Jack direct Higgsfield execution remains an explicit exception because `jack.higgsfield-skill-supervision` is still draft. Kanye remains the V1 owner for generation.
- Tony is standardized as a single development owner with mode profiles: `tony-kimi` for exploration, `tony` for plan/review, and `tony-dev` for execution. Current prod-ready blocker: `tony.codebase-exploration` must align protocol YAML, registry, runner, and handoff inputs around explicit `target_repo` and `task_request`.
- `Jackette`, `Jhin`, and `Walter` remain later/draft.
- Per-agent `ROLE_PERMISSIONS` files do not exist except for Jack.
- Skills are installed everywhere and must be governed by the central allowlist matrix until runtime enforcement exists.

## Toolbox Change Governance

Jack may maintain toolbox governance when the requested change is explicit and bounded.
The procedure is:

- [TOOLBOX_CHANGE_PROCEDURE.md](/Users/moufdi/openclaw/docs/ops/agent-governance/TOOLBOX_CHANGE_PROCEDURE.md)

The working list for agent/toolbox consolidation is:

- [AGENT_TOOLBOX_CONSOLIDATION.md](/Users/moufdi/openclaw/docs/ops/agent-governance/AGENT_TOOLBOX_CONSOLIDATION.md)

The input/output and post-deployment test contract is:

- [WORKFLOW_IO_TEST_CONTRACTS.md](/Users/moufdi/openclaw/docs/ops/agent-governance/WORKFLOW_IO_TEST_CONTRACTS.md)

The execution plan and runner mapping are:

- [WORKFLOW_POST_DEPLOY_TEST_PLAN.md](/Users/moufdi/openclaw/docs/ops/agent-governance/WORKFLOW_POST_DEPLOY_TEST_PLAN.md)
- [workflow-runner-input-map.yaml](/Users/moufdi/openclaw/docs/ops/agent-governance/workflow-runner-input-map.yaml)
- [workflow-test-fixtures.yaml](/Users/moufdi/openclaw/docs/ops/agent-governance/workflow-test-fixtures.yaml)

Default rule:

- add capabilities to the owning agent only
- keep write actions approval-gated unless a validated route explicitly allows autonomous E2E
- use direct tool access for one-off owned work
- promote repeated direct tool patterns into protocol candidates

## Proof Targets

Discussion work:

- final confirmation with actions taken and any blocker
- stable links or paths if artifacts were created

Protocol work:

- route package proof
- structured JSON or manifest when the route defines it
- report bundle when expected, commonly HTML/PDF/JSON
- replay/validation evidence when a route claims prod maturity

External mutation:

- pre-mutation resolved target
- explicit approval
- post-mutation readback or platform confirmation
- MM/run event when mission-bound

Dev work:

- code delta or explicit no-change verdict
- targeted tests/build/lint when available
- git/PR only when requested

## Anti-Patterns

- asking an unrelated agent to use a toolbox outside its role
- treating installed skills as permission
- treating a channel transcript as business truth
- starting with browser or terminal on backend-owned facts
- marking `done` from runtime completion alone
- silently upgrading direct one-off tool use into production protocol execution
- blocking a whole brand because one surface is missing
