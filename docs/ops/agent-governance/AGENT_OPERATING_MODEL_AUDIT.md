# Agent Operating Model Audit

Date: `2026-05-07`

Scope: governance synthesis of the existing BRM/Hermes agent protocols, skills, toolboxes, memory loop, and operating ideas. This document does not authorize runtime wiring, gateway edits, Mission Manager implementation, deploy, restart, or systemd work.

## What Already Exists

Current live registry:

- `25` specialist routes in `/Users/moufdi/hermes-runtime/contracts/specialist-route-registry.json`
- route owners: Jack, Tony, Selena, Kanye, Safir, Rosa, Jeff, Alfred, Naya, Cortex
- package-only or recurring protocols also exist for Jack-X, Mnemos, Jack direct MM supervision, Jack email digest, Jack-X memory/wiki, and planned feedback loops

Current protocol package pattern:

- common stage shape: `preflight -> extract/execute/decision/analysis -> verification -> delivery`
- common gates: completeness, stage order, model, timeout, context, script-first, tool allowlist, output contract, status
- common output proof: compact JSON, report bundle, verification JSON/report, delivery JSON, memory candidate, graph snapshot, code delta, or final summary
- common principle: no `done` without proof

Current governance pattern:

- skills are centralized
- an installed skill is not permission
- permission comes from agent role, toolbox matrix, route package allowlist, and approval gates
- direct tool use is allowed only when owned, bounded, logged, and low-risk
- repeated direct tool use should become a draft protocol

## Core Shared Ideas

These ideas are already reused across agents and should become shared standards.

### 1. Protocol First

Every agent should classify the route before using tools:

- environment
- brand/tenant/surface when relevant
- route or protocol
- allowed toolset
- proof target
- approval gate

If the route is missing, Jack should use `jack.protocol-missing` or `jack.capability-missing`, not improvise silently.

### 2. Script First

When a canonical script exists, the agent should use it instead of free-form terminal/browser work.

Examples:

- Selena uses PayPal/Zendesk scripts and audit runners.
- Naya uses Shopify/BigBlue/sourcing scripts.
- Alfred uses phase runners.
- Tony uses repo/test commands in the target repo, not arbitrary execution.
- Jack-X uses intake, memory review, wiki, and graph candidate scripts.

### 3. Read/Write Split

Reads can be broader when the surface is owned by the agent.
Writes must be narrower and usually approval-gated.

Global write gates:

- external message send
- customer-visible support reply
- PayPal dispute message
- refund, payment, billing, invoice, subscription, dispute, or financial mutation
- campaign publication or ad account mutation
- supplier/order/purchase mutation
- production deploy, restart, or systemd
- ambiguous target, tenant, brand, or delta

### 4. Phase Model

The ecosystem repeatedly uses three phases:

- Phase 1: observation/audit/read/report
- Phase 2: creation/plan/draft/build
- Phase 3: publication feedback loop, monitoring, iteration, task board

This should remain standard, but each agent owns different surfaces.

### 5. Proof Before Status

A completed run must leave a proof:

- report bundle
- manifest
- compact JSON
- verification JSON/report
- delivery JSON
- changed files and tests
- memory candidate/review
- graph candidate/commit proof
- explicit blocked/no-change verdict

Mission Manager is tracking, not proof by itself.

### 6. Brand Scope Standard

Brand-linked work should resolve:

- `brand_id`
- `scope_mode`: `brand_focus` or `generic`
- tenant/account/store when relevant
- missing surfaces as partial data, not total blockers

A missing Klaviyo surface for one brand should block Klaviyo work only, not unrelated Shopify, creative, support, or stock work.

### 7. Jack Is Transversal

Jack should access every toolbox surface for:

- routing
- supervision
- gap detection
- capability/protocol drafting
- light direct execution when governed
- reading evidence
- asking approvals
- coordinating handoffs

But Jack's transversal access is not blanket mutation permission.
Jack can see and coordinate all lanes, while specialist agents own the domain execution.
External writes and high-risk business mutations still require route ownership and approval.

### 8. Memory And Feedback Improve The System

Memory is not only recall. It should improve protocols.

The loop should be:

1. direct work or protocol run happens
2. artifacts/logs/proofs are captured
3. Jack-X extracts durable memory candidates
4. LLM Wiki slowly consolidates and proposes refinements
5. Jack-X reviews and commits governed KG updates
6. a curator function detects repeated patterns, gaps, duplicated knowledge, protocol failures, and tool needs
7. governance matrices and draft protocols improve

## Agent-by-Agent Synthesis

### Jack

Real idea:

- transversal operator, router, supervisor, and governed direct executor

Needs:

- access to all skill/toolbox families for reading, routing, and supervision
- ability to call specialist routes
- ability to create protocol/capability gap artifacts
- access to KG/MM/brand packs/route registries
- direct execution only when route-governed or explicitly requested

Specific overlay:

- `protocol-missing`
- `capability-missing`
- `draft-protocol-runtime`
- direct MM supervision and email digest package paths
- Higgsfield direct use remains explicit exception; Kanye is preferred creative owner

Open gaps:

- Jack profile-level docs are stronger than most agents, but Jack needs the final cross-agent operating model linked into his startup/governance path without touching reserved files until explicitly allowed.

### Jack-X

Real idea:

- long-term memory and multi-channel extraction
- not a final decision maker

Needs:

- MS365, Lark, WhatsApp snapshot, MM agent session reads
- graph candidate generation
- promotion review
- durable KG write after gates
- Memory Wiki refinement review
- future-time correction feedback loop

Specific overlay:

- candidate extraction, confidence, provenance, dedup, promotion review, KG validation
- LLM Wiki is advisory, not writer

Open gaps:

- live review gate must prevent unapproved full-candidate KG apply
- LLM Wiki `kg_operations` need a repeatable bridge into Jack-X review
- feedback loop is rehearsed but not live route yet

### Mnemos

Real idea:

- continuity and compaction, not enterprise memory ownership

Needs:

- local session/context artifacts
- context pressure metering
- reinjection capsules
- handoff summaries

Specific overlay:

- no external read/write
- no durable KG ownership
- no business execution

Open gaps:

- should stay narrow; risk is scope creep into Jack-X memory.

### Rosa

Real idea:

- marketing strategist: offers, performance, market intelligence

Needs:

- Shopify/Klaviyo/Hiboo/Lark/GA4/GSC/DataForSEO reads
- report generation
- creative asset requests via Kanye/Jack
- campaign/storefront/CRM mutation only with route+approval

Specific overlay:

- offer strategy
- performance marketing audit
- competitive watch
- market graph refresh
- campaign planning and feedback loop concepts from historical protocols

Open gaps:

- stronger handoff format to Kanye/Cortex for creative and ads decisions
- clearer mutation path when marketing recommendations become campaign/storefront/CRM actions

### Jeff

Real idea:

- influence operations: creators, outreach, collaboration ops

Needs:

- Hiboo creator/profile reads
- inbox signal inputs
- candidate registry
- report bundles
- outreach and collaboration mutation gates

Specific overlay:

- profile analysis
- performance reporting
- candidate intake
- planned outreach pipeline and collaboration management

Open gaps:

- standardized outreach draft proof before contact
- collaboration mutation protocol remains planned/approval-gated

### Naya

Real idea:

- stock, sourcing, supply chain feasibility

Needs:

- Shopify reads
- BigBlue reads
- stock telemetry
- sourcing sheets
- local report artifacts
- supplier/order/purchase mutation gates

Specific overlay:

- stock check
- product sourcing
- campaign stock support
- supplier communication draft path

Open gaps:

- supplier question packs and supplier communication protocol remain draft
- campaign support should become a repeatable route linked to Rosa/Cortex planning

### Selena

Real idea:

- support risk, PayPal disputes, Zendesk feedback

Needs:

- PayPal read/fetch
- Zendesk read/fetch
- reviewed export analysis
- strict proof before any customer-visible action

Specific overlay:

- PayPal phase1 audit/live
- Zendesk feedback review/live
- no direct support mutation by default

Open gaps:

- approval checklist for replies, dispute messages, refunds, and customer-visible updates
- phase 2/3 support action routes remain gated

### Alfred

Real idea:

- SEO/AEO visibility and strategy artifacts

Needs:

- GSC/DataForSEO/GA4/site-audit reads
- report bundle generation
- strategy-plan and deployment-feedback input artifacts
- Drive delivery approval gate

Specific overlay:

- deterministic phases: visibility audit -> strategy plan -> deployment feedback loop
- bundle-first reports and workboard artifacts

Open gaps:

- phase 2/3 are supervised/beta but not all registry-live
- no site/theme mutation without explicit route

### Cortex

Real idea:

- paid media observation, campaign handoff, feedback loop

Needs:

- Hiboo/Meta/Google Ads reads
- creative observation
- creative handoff to Kanye
- task board and campaign feedback artifacts
- campaign mutation/ad publication approval gates

Specific overlay:

- ads observation
- campaign management
- alerts
- task management
- weekly report
- feedback loop

Open gaps:

- phase 2/3 are planned/draft in governance
- needs explicit integration with Kanye for assets and Rosa for offer/landing decisions

### Tony

Real idea:

- development owner: code, repos, tests, Git, implementation

Needs:

- target repo resolution
- repo filesystem, terminal, package manager, tests/build/lint
- Git/GitHub when requested
- mode separation: explore, plan, execute, review

Specific overlay:

- `tony-kimi` exploration sidecar
- `tony` planning/review
- `tony-dev` execution
- no deploy/restart/release control unless explicitly delegated

Open gaps:

- `tony.codebase-exploration` input contract drift
- wrapper test harness requires import path fix
- runtime path normalization for review artifacts

### Kanye

Real idea:

- creative generation and reference edits

Needs:

- image/video generation providers
- official Higgsfield CLI skills
- attachment/reference media policy
- local generated media artifacts
- publication/delivery gates

Specific overlay:

- still generation
- reference edit
- Higgsfield generate/product-photoshoot/marketplace-cards/soul-id
- product photoshoot proof and polling recovery

Open gaps:

- standardize Higgsfield polling/recovery wrapper
- more QA variants before prod
- voice output via Higgsfield is planned/gated, not validated

### Safir

Real idea:

- email and CRM audit, workflow design, drafting

Needs:

- MS365/Klaviyo reads
- email template analysis
- renderable email draft pipeline
- creative handoff to Kanye
- approval before send or CRM mutation

Specific overlay:

- email audit
- mail pole audit
- email workflow draft path

Open gaps:

- email workflow needs reopened with modern design/image model floor
- send/live CRM mutation remains approval-gated

## What Should Be Standard And Shared

These should be common across all V1 agents:

- `ROLE_PERMISSIONS.md/json`
- `ENVIRONMENT_MAP.md`
- `ROUTE_MATRIX.md`
- `PROCEDURES.md`
- detailed `SOUL.md`
- STT: OpenAI `whisper-1`
- proof vocabulary: `report_bundle`, `compact_json`, `verification_json`, `delivery_json`, `manifest`, `blocked`, `no_change`
- global approval gates
- brand scope contract
- attachment policy
- route maturity: `draft`, `beta`, `prod`
- phase model: observation, creation, feedback loop
- direct tool use to protocol candidate rule
- source hierarchy: runtime registry/protocol package > profile prompt > governance doc > summary matrix

## What Should Stay Specific

These must remain agent-specific overlays:

- domain surfaces and credentials
- canonical scripts
- route inputs
- proof format details
- approved mutation targets
- model/stage preferences where meaningful
- sidecar profiles
- report templates
- brand/business semantics

Examples:

- Selena owns support-risk, not Klaviyo email design.
- Safir owns email/CRM design, not Zendesk replies.
- Kanye owns media generation, not campaign publication.
- Cortex owns ads observation and feedback, not direct creative generation.
- Tony owns code, not production release control.
- Jack-X owns memory/KG candidate lifecycle, not operator replies.
- Mnemos owns continuity, not durable enterprise truth.

## Curator Function

The curator should start as a function/protocol layer, not necessarily a new runtime agent.

Purpose:

- read protocol run artifacts, logs, missions, direct tool traces, Memory Wiki proposals, and feedback reports
- detect repeated direct tool use
- detect protocol failures, duplicate knowledge, stale assumptions, missing tools, and poor proof
- propose draft protocol updates or toolbox consolidation tasks
- feed Jack/Jack-X governance without executing business mutations

Inputs:

- route manifests and verification reports
- Mission Manager status patterns
- Jack-X memory reviews
- LLM Wiki `kg_operations`
- direct tool summaries
- agent final summaries and blockers

Outputs:

- `protocol_candidate`
- `toolbox_gap`
- `skill_doc_update`
- `memory_refinement_candidate`
- `route_quality_issue`
- `agent_scope_conflict`
- `approval_gate_gap`

Rules:

- curator does not mutate external systems
- curator does not write durable KG directly
- curator does not widen permissions
- curator can propose changes to governance matrices and protocol drafts
- Jack/operator approve governance changes
- Jack-X handles memory/KG promotions

## Next Implementation Order

1. Create or align profile-level `ROLE_PERMISSIONS`, `ENVIRONMENT_MAP`, `ROUTE_MATRIX`, and `PROCEDURES` for remaining V1 agents.
2. Add a shared agent procedure template to avoid each profile inventing its own structure.
3. Add curator feedback-loop draft registry and proof contract.
4. Standardize read/write toolboxes by platform: Shopify, Klaviyo, Zendesk, PayPal, BigBlue, paid media, Git/GitHub, Higgsfield, MS365/Lark.
5. Test conversation -> action for each agent:
   - read-only request
   - discussion/approval request
   - validated route request
   - external mutation request
   - out-of-scope request
6. Promote only after artifacts and proof pass.
