# BRM Agents - Production Status

Last updated: `2026-05-05`

## Scope

This file tracks the real production state by runtime surface.

Jack / OpenClaw production target:
- AWS instance: `i-041f117445ddeafc3`
- Name: `Jack-AI-Assistant`
- Region: `eu-west-1`
- Public IP: `54.76.101.182`

Mission Manager hosted production target:
- ALB: `mission-manager-prod-alb`
- Region: `eu-west-3`
- ECS cluster: `mission-manager-prod-cluster`
- ECS service: `mission-manager-prod-backend`

Do not use local Mac behavior as evidence for production status.

## Current Executive Status

Canonical plan:

- `ORCHESTRATION_UNIFIED_PLAN.md` is now the active execution plan for subagents, protocols, workflow lifecycle, scheduler/autoloop, Hippocampus, Jack X, Mnemos, and Mission Manager visibility.

Current readiness:

- `Overall orchestration`: `~75% production-ready`
- `Hermes runtime / gateway / cron`: `usable foundation`
- `Mission Manager control plane`: `usable cockpit with canonical workflow ledger, task-centric lineage, and curator read surface`
- `Mission Manager costs`: `operator-usable for subscription-handled, out-of-subscription LLM, and external tool costs; some providers still remain unknown/credit-based`
- `Jack orchestration`: `partially usable but not production-trusted for critical autonomous work; task-centric lineage, routing summary, and protocol closure are now live, but replay/promotion and broader fallback retirement remain open`
- `Hippocampus preprocessing`: `primary interactive pre-routing packet live on Jack with deterministic fallback, canonical context_packet_ref transport, and task-bound routing summary visibility`
- `Specialist runtime`: `real bound sessions plus profile-backed direct specialist chat; first child-run lineage is live, but protocol stages/approvals/validation are still not fully unified`
- `Specialist routes`: `usable on validated route scopes with bounded context packets, dedicated tool maps, protocol indexes, and work-policy routing; still not fully route-complete`
- `Specialist route executor contract`: `first canonical registry field closed with executor.kind plus portable ~/ path resolution across local and VPS; live coverage is command-only for now`
- `Safir route-backed surface`: `first canonical mail slice now live on executor.kind=command with VPS render-only proof for safir.email-audit and safir.mail-pole-audit; email-workflow remains open`
- `Kanye creative routes`: `phase1 route-backed closeout now live on executor.kind=command with kanye.still-generate and kanye.reference-edit, plus local/VPS tests and real VPS smoke proof; tuning, MM lineage, and wider delivery/task integration remain open`
- `Toolbox standardization`: `first Shopify commerce slice is now standardized around the live shopify-stores backend; broader toolbox wave remains open but no longer depends on Shopify floor discovery`
- `Jack X memory/KG`: `usable structured pipeline plus readable Memory Wiki compiler and active Gemini semantic cache; coverage and KG quality still improving`
- `Mnemos context-check`: `usable continuity surface with proactive watch-threshold snapshots, auto-reset handoff capsules, and a cross-session journal; still not a KG writer`
- `Autoloop`: `not closed; current cron is scheduling, not protocol self-improvement`
- `Protocol improvement inbox`: `first derived task-bound inbox live; replay, promotion, and monitoring still partial`

## Shipping Matrix

| Area | Status | Notes |
| --- | --- | --- |
| Workflow ledger and task lineage | shipped | `workflow_runs` / `agent_run_events` are live and task-bound runtime truth is preserved through `mission_task_id` and `submission_scope` on governed wake routes. |
| Runtime handoff | partial | Hippocampus and specialist dispatch are both live, canonical `context_packet_ref` convergence is closed for the current slice, and `MissionTask` now exposes a task-bound routing summary; broader KG/MM-first pre-routing enrichment remains open. |
| Protocol lifecycle closure | partial | The lifecycle state machine is live in MM; reviewed promotion to `prod` and the autoloop closure remain open. |
| Autoloop improvement inbox | partial | The first task-bound improvement inbox is derived from curator recommendations, curator signals, and lifecycle state; failure classification, replay, promotion, and monitoring remain the next closure wave. |

Immediate blockers:

- `WorkflowRun` / `AgentRunEvent` now exists for Mission Manager recurring runtime reports, Jack interactive turns, and first specialist child runs, but protocol stages, approvals, validation, KG commits, and external tool costs are not all attached yet
- Jack now receives a bounded Hippocampus packet before execution, but older keyword route resolution still exists underneath and must be progressively retired
- Hermes native delegation and BRM specialist dispatch are parallel systems instead of one parent/child run model
- protocol lifecycle state machine is modeled, but reviewed promotion to `prod` and the wider autoloop closure remain partial
- older docs and snapshots still contain drift and must be treated as historical unless reconciled with `ORCHESTRATION_UNIFIED_PLAN.md`

Still explicitly true:

- business work must not bypass MM
- specialists stay bounded to their owned protocols
- `Jack X` and `Mnemos` stay outside operator mission dispatch unless a governed route explicitly says otherwise
- if a governed route does not exist, Jack must open `protocol-missing` or `capability-missing`, or enter bounded `exploratory_draft`; it must not improvise silently
- `Telegram` remains explicitly deferred post-v1

## Target Operator Workflow

The production target is:

1. `Moufdi -> Jack`
2. `Jack -> Mission Manager`
3. `Mission Manager -> specialist protocol`
4. `specialist -> reviewable artifacts + mission truth`
5. `Mission Manager -> Jack -> Moufdi`

Rules:

- business work must not bypass MM
- specialists stay bounded to their owned protocols
- `Jack X` and `Mnemos` stay outside operator mission dispatch unless a governed route explicitly says otherwise
- if a governed route does not exist, Jack must open `protocol-missing` or `capability-missing`, not improvise the work

## System Overview

Working now:

- Hermes `jack` runtime is live on the VPS and connected on WhatsApp
- direct specialist chat is now materially real on the live runtime:
  - `user + agent` session binding is isolated
  - profile-backed specialist runtimes are active behind `/specialist <agent>`
  - `/jack` returns to the bound Jack session instead of a shared mixed transcript
- the first bounded specialist work-policy floor is live:
  - `extraction`
  - `reasoning`
  - `action`
  - `follow_up`
  - `/status` now exposes the default work type plus the effective default/fallback lanes
- Mission Manager is the hosted operator plane with real mission truth and file traceability
- Mission Manager now exposes a visible `Costs` surface:
  - canonical route: `/activity`
  - visible sidebar entry: `Costs`
  - current semantics:
    - `subscription-handled`
    - `out-of-subscription llm`
    - `external tool costs`
    - `operational / synthetic excluded`
    - breakdowns by `billing_mode` and `cost_status`
  - known limit:
    - some providers remain `unknown` or `credit-based` until a defensible pricing contract is defined
- governed specialist dispatch works across the active route matrix
- active specialist routes now emit a shared runtime context packet:
  - dedicated specialist memory excerpts (`SOUL`, `MEMORY`, `USER` when present)
  - dedicated tool surface from `~/.openclaw/workspace-<agent>/TOOLS.md`
  - protocol index/package references
  - relevant shared memory hits from `~/.openclaw/memory-wiki/latest.json`
  - packet persisted as `specialist-context.json` and `specialist-context.md` inside each bundle
- `Jack X` is live on:
  - MS365 work intake (`inbox + sent`)
  - first Lark channel intake
  - first Lark table slice
  - Hermes-native WhatsApp message capture into the integrator DB
  - first durable KG extension slice for:
    - channels
    - operations
    - products
- `Jack X Memory Wiki` is live as a derived memory layer:
  - compiles Jack X channel reports plus the latest memory projection into readable pages under `~/.openclaw/memory-wiki`
  - emits reviewable candidate KG operations instead of direct destructive KG writes
  - runs through Hermes recurring jobs and is mirrored into Mission Manager recurring tasks
  - semantic layer now exists with bounded modes `deterministic`, `shadow`, `active`; production cron now runs `active` on `Gemini` with shared cache reuse and deterministic fallback for degraded cases
- `Mnemos` now covers the continuity floor needed for Jack sessions:
  - proactive watch-threshold snapshots before compaction once context pressure crosses the configured watch band
  - governed continuity capsule generation at compaction time
  - auto-reset continuity capture on session expiry so daily/idle resets do not lose live context
  - cross-session journal under `~/.openclaw/workspace-mnemos/journal/<profile>/`
  - no direct KG writes by policy; Mnemos remains continuity memory, not enterprise truth
- `Jack` now has a separate live operator email digest cron that reads the latest qualified Jack X mail artifact, including the mixed `inbox + sent` batch, without mutating Jack X memory/KG state
- the digest runtime now exposes a stable top-level `response_preview` contract so Hermes cron can auto-deliver `ok` and suppress `noop` cleanly on WhatsApp, and the review prompt now carries curated support / follow-up / finance / archive slices instead of a dry audit summary
- Hermes cron transport is now standardized enough to build on:
  - `delivery.targets`
  - multi-target WhatsApp fan-out
  - persisted delivery receipts
  - explicit target JIDs instead of fragile human aliases
- Jack runtime-state ambiguity on the VPS is now closed enough operationally:
  - live Jack and Jack-x gateways are explicitly profile-backed
  - root legacy state is archived out of the audit path
  - Jack `/status` now exposes:
    - active gateway home
    - active session store
    - active channel directory
    - WhatsApp mode
- Mission Manager now stores the first canonical workflow ledger:
  - `workflow_runs`
  - `agent_run_events`
  - `/api/workflow-runs*`
  - recurring runtime auto-mirroring from `/api/recurring-tasks/runtime`
  - task-scoped lineage keys remain machine-readable on governed wake routes:
    - `mission_task_id`
    - `submission_scope`
  - production E2E proof: forced `jack-x.db-analysis` run at `2026-04-22T23:48:26Z` created `cron:jack-x-db-analysis-evening:2026-04-22T23:48:26.000Z`
- Jack interactive turns now emit `run.started` and `run.completed` into the Mission Manager workflow ledger through Hermes hook `brm-mm-workflow-ledger`; production synthetic proof created `interactive:synthetic:synthetic-hippocampus-session:synthetic-hippocampus-validation-20260423-001`
- specialist direct chat now emits first lineage-bound child runs into Mission Manager:
  - parent interactive run remains attached
  - bounded child run carries `parent_run_id`
  - remaining gaps are on stages, approvals, validation, and broader route generalization
- Hippocampus first runtime packet is now live inside Jack gateway preprocessing:
  - source/user/channel identity
  - ordered conversation window, bounded
  - KG hits from latest Jack X memory projection
  - candidate protocol routes
  - recommended execution mode
  - guardrails
  - auxiliary LLM refiner call with short timeout and deterministic fallback
- Mission tasks now expose the first task-bound routing and protocol-improvement read surfaces:
  - `submission_scope`
  - `execution_lineage`
  - `hippocampus_summary`
  - `protocol_improvement_inbox`
  - these remain derived MM truth, not new persistence layers
- the MS365 mailbox surface is now operationally usable beyond digesting:
  - bulk search across `inbox` and `sent`
  - bounded folder/date search
  - targeted JSON extraction with optional body / headers / attachment metadata
- Kanye now has a first usable creative generation floor on the VPS:
  - `generation_policy` is active
  - exploratory still generation routes to `Nano Banana 2`
  - premium/final still generation routes to `GPT Image 2`
  - motion routes to `Higgsfield / Seedance`
  - still-image reference edits are now validated locally and on the VPS for:
    - `Nano Banana 2`
    - `GPT Image 2`
- the first toolbox-standardization slice is now closed:
  - Hermes upstream optional skill:
    - `optional-skills/productivity/shopify/SKILL.md`
  - standardized use:
    - standardized Shopify Admin/Storefront GraphQL capability
    - production commerce toolbox surface for specialist routes
  - current floor:
    - standardized around `clawd/skills/shopify-stores/scripts/shopify.py`, not a parallel runtime
    - `stores.json` is now the declared tenant/auth contract and the capability registry points to it instead of duplicating tenant lists
    - live reads validated for `maybe-paris` admin, `us-maybe-paris` admin via `client_credentials`, `maybe-paris` theme, and `blinx` admin
    - Hermes readiness now exposes all declared Shopify tenants and makes `shared_env_presence_only` explicit for auth readiness
    - the local skill doc is aligned with the command surface actually implemented in `shopify.py`
  - residuals:
    - `blinx-us` auth declared but not ready
    - `nailz` brand metadata still points to a `store_key` absent from `stores.json`

Still open:

- the distinct MM-backed `Jack mission digest` surface is not closed
- `Jack` orchestration remains frozen for critical work where trust would depend on subagent runtime truth
- Hippocampus GLM refiner is wired and called, but current z.ai calls can timeout/rate-limit; fallback routing remains deterministic and visible in `hippocampus_packet.llm`
- `Mnemos` still lacks a natural live compaction proof on a truly saturated Jack session above the real watch/compact thresholds; the runtime and reset-path continuity are now validated, but the next proof should come from a naturally loaded production session
- `Jack X` world-state coverage remains partial beyond the contracted floor:
  - more `Lark` slices still need onboarding
  - WhatsApp group traffic still needs real production volume
  - semantic merge remains candidate-only
  - per-channel worker truth is still not implemented; current floor remains source-family bounded
- KG review semantic resolution is now active, but still conservative on some human alias cases; this is a quality-tuning gap, not a runtime gap
- specialist `Lark` routes and the broader `MM + Drive + channel reply` wave are not closed yet
- specialist MM lineage is still incomplete:
  - direct specialist child runs are now real
  - profile-backed runtime is real
  - but approvals, protocol stages, validation results, KG commits, and external tool cost events are not yet all first-class MM workflow events
- `Safir` no longer lacks a route-backed floor, but still is not fully industrialized:
  - `safir.email-audit` and `safir.mail-pole-audit` are now live canonical routes with VPS render-only proof
  - `email-workflow` remains open
- `Kanye` no longer lacks a governed creative route floor:
  - `kanye.still-generate` is now live as a canonical `executor.kind=command` route
  - `kanye.reference-edit` is now live as a canonical `executor.kind=command` route
  - both routes are green on local tests, VPS route-dispatch replay, and real VPS smoke on `Nano Banana 2`
  - remaining work is the delivery/tuning wave plus MM/task lineage, not route-floor discovery
- toolbox standardization remains open:
  - the first Shopify commerce slice is now closed
  - broader capability cleanup across the rest of the stack still remains
  - the next commerce standardization work is route ownership and adjacent tools, not Shopify floor discovery
  - current explicit residuals are:
    - `blinx-us` auth not ready
    - `nailz` still points to a missing `store_key`
  - the gate is prod validation and route ownership, not just skill presence
  - explicit current commerce metadata residual:
    - `nailz` still points to a `store_key` absent from `stores.json`
- exact next-wave dependency truth is now:
  - the first two MM reflection passes are now live enough to build on:
    - `executor.kind` and `dispatch_mode` are first-class MM operator truth on the runtime-facing surfaces
    - direct specialist chat, route-backed runs, toolbox health, and Hermes cron receipts are materially projected into the cockpit
    - canonical specialist truth now surfaces across dashboard / org / member / mission views
    - the residual MM writer slice is now narrow:
      - stronger direct canonical member linkage where the registry already knows the member
      - fuller protocol/capability summary on the remaining surfaces
  - mission autonomy stays immediately after that because the current stack now has:
    - `workflow_runs`
    - `agent_run_events`
    - `recurring_tasks`
    - `recurring_task_events`
    - and now also:
      - `mission_tasks`
      - `mission_task_events`
      - derived `mission.next_check_at` on the MM backend read model
      - Hermes wake-loop ownership on top of that substrate
    - but not yet:
      - one explicit task-level split between:
        - `direct_discussion`
        - `extraction`
        - `governed_route`
      - standardized route outcomes with first-class `data_check_report`
      - curator-ready signals bound to runs / task events
  - toolbox/commerce work is no longer a floor-discovery problem:
    - the Shopify executor is standardized already
    - the remaining work is `blinx-us` auth readiness, `nailz` metadata cleanup, and route ownership on top of the existing backend
  - repo/VPS drift remains a transverse test gate:
    - some auxiliary specialist files are still not mirrored broadly enough on the VPS checkout
    - therefore every closeout slice must specify exactly which tests are replayable live and which require a wider sync first

## Capability And Deliverable Floor

Current production-shaped deliverables the system can already produce on at least one governed path:

- MM mission creation, assignment, review/blocked truth, and traceable attachments
- specialist reports in `HTML / PDF / report-data.json`
- Drive-linked deliverables pushed back into MM
- execution boards / queue seeds on selected routes
- KG candidates:
  - objects
  - relations
  - confidence hints
  - continuity capsules
- protocol bundles for `protocol-missing` and `capability-missing`

Rule:

- if a route cannot yet emit reviewable artifacts and truthful MM state together, it is not counted as production-ready

## Layered Migration Snapshot

- `Runtime / infra layer`: Hermes is now deployed on the Jack VPS under `/home/ubuntu/hermes-runtime`, with the active channel runtime bound to `HERMES_HOME=/home/ubuntu/.brm-hermes/profiles/jack`, a paired WhatsApp session at `/home/ubuntu/.brm-hermes/profiles/jack/whatsapp/session/creds.json`, and an active systemd unit `hermes-gateway-8aa553a5.service`.
- `Auth / secret layer`: VPS auth and business secrets are now seeded into the Hermes root state; `ANTHROPIC_TOKEN` and `MISSION_MANAGER_API_URL` are confirmed present, and the local Tony/Tony-dev profile auth stores were resynced to the current Codex OAuth session so governed Tony routes no longer fail on stale per-profile refresh state.
- `Docs / control-plane layer`: canonical status truth lives in `/Users/moufdi/openclaw/docs/ops` and `/Users/moufdi/hermes-runtime/docs`; the VPS copies under `/home/ubuntu/openclaw/docs/ops` and `/home/ubuntu/hermes-runtime/docs` are projected from deploy sync and must match before a wave is considered updated.
- `BRM / harness layer`: protocol ownership, route gating, and governed graph writes remain the source of truth; the first governed inbound WhatsApp message proof now exists, and the next work is to keep the same rules stable across the broader channel ecosystem.
- `Dispatch / routing layer`: supervised WhatsApp ingress is now pre-routed before runtime execution; if a governed specialist route resolves, Jack stays manager / dispatcheur and the owned specialist route runs. If a named specialist has no governed route Jack opens `jack.protocol-missing`, and if the ask is a transversal capability gap such as a store-first LP Jack opens `jack.capability-missing` with coverage matrix, proposed agent graph, and an operator decision question instead of silently falling back to `jack.supervisor.direct`. Ambiguous or underspecified asks still block.
- `Hippocampus layer`: Jack profile now builds `brm.hippocampus.packet.v1` on every Jack WhatsApp turn before prompt construction. The packet is injected into the session prompt and mirrored into the Mission Manager workflow run metadata.
- `Mission Manager layer`: hosted MM bridge, clean-slate reset, delivery gating, first handoff proofs, and the first message-created WhatsApp work path are now valid; what remains is ecosystem closeout and generalization.
- `Channel layer`: WhatsApp is now running on Hermes in production on the VPS on the `jack` profile with a first audited governed ingress proof; Telegram is explicitly out of the `v1` perimeter and stays legacy-only.
- `Coordination layer`: `Mnemos` now has a packaged Hermes continuity route (`mnemos.context-check`) with green local and VPS tests plus live VPS artifact proof on Jack sessions. The runtime now covers three moments: watch-threshold snapshot, compaction-time reinjection capsule, and auto-reset continuity handoff on session expiry. It also appends a durable continuity journal at `~/.openclaw/workspace-mnemos/journal/<profile>/YYYY-MM-DD.jsonl` with `latest-continuity.json` as the current handoff pointer. This remains a technical continuity surface, not an MM-triggered business route and not a KG writer. The only missing proof is a natural high-saturation production Jack turn above the real watch/compact thresholds. `Jhin` is next, `Kanye` now has a first governed creative route floor, and `Walter` remains draft.
- `World-state intake layer`: `Jack X` now runs under an explicit channel contract at `/Users/moufdi/hermes-runtime/contracts/jack-x-channel-registry.json`, and Hermes now writes incoming integrator traffic into the canonical VPS store `/home/ubuntu/.brm-hermes/profiles/jack/integrator_messages.db`. The live floor is now:
  - `MS365 work`: closed on incremental cursor path
  - `Lark channels`: closed on `CX_MAYBE`
  - `Lark tables`: closed on `maybe-paris`, `blinx` remains draft
  - `WhatsApp`: Hermes-native capture is now writing into the integrator DB, but the scheduled group surface remains effectively empty until real group traffic exists on the paired VPS runtime
- `Memory Wiki layer`: `Jack X` now has a readable consolidation pass at `/Users/moufdi/openclaw/scripts/jack-x-memory-wiki-compile.py`; production forced run `memwiki_20260423T164209Z_028babd0` produced `51` pages and `38` review items under `/home/ubuntu/.openclaw/memory-wiki`, with direct KG mutation disabled by policy.
- `Memory Wiki semantic layer`: `/Users/moufdi/openclaw/scripts/jack_x_semantic_memory.py` now provides the shared semantic resolver used by Memory Wiki and KG promotion review; production backfill run `memwiki_20260423T192111Z_028babd0` completed `ok` in `active` mode on the VPS with `51` fresh Gemini calls and `0` failures, and the following forced run `memwiki_20260423T192516Z_028babd0` completed `ok` with `51` cache hits and `0` fresh calls.
- `Business route layer`: no new specialist route was closed by the WhatsApp cutover itself; Rosa, Jeff, Alfred, Naya, Selena, Tony, and Cortex keep their previously validated scope.

## Current Closeout Order

1. `Workflow lineage and operator truth`
   - keep specialist child runs on the canonical `WorkflowRun` / `AgentRunEvent` path
   - close approvals, protocol stages, validation results, KG commits, and external tool cost events on the same ledger
   - MM remains the readable source of truth instead of reconstructed runtime state
2. `Mission Manager reflection residuals`
   - the first two reflection slices are now live:
     - runtime/API projection on `Capabilities`, `Live`, and workflow-facing surfaces
     - canonical specialist projection on dashboard / org / member / mission surfaces
   - remaining slice stays low-blast-radius:
     - fuller protocol/capability summary on the remaining views
     - stronger direct use of canonical member linkage where the registry already knows the member
3. `Toolbox and capability standardization`
   - standardize active tool surfaces before widening route coverage
   - adopt upstream Hermes optional skills when they are cleaner than custom local integration debt
   - first commerce floor now closed:
     - Shopify GraphQL Admin/Storefront capability from `optional-skills/productivity/shopify/SKILL.md`
     - standardized on the existing multi-store backend instead of a parallel executor
     - live contract now follows `stores.json` plus brand-pack routing and readiness checks
     - next commerce work moves to broader route ownership and adjacent tools, not Shopify floor discovery
   - exact residuals on the current commerce floor:
     - `blinx-us` auth declared but not ready
     - `nailz` still references a `store_key` absent from `stores.json`
4. `Specialist route closeout`
  - `Safir` first route-backed mail surface is now closed:
    - `safir.email-audit`
    - `safir.mail-pole-audit`
    - both validated on the VPS as render-only canonical routes
  - `Kanye` phase1 creative route floor is now closed:
    - `package_root` is live in `inventory.json`
    - canonical routes now exist:
      - `kanye.still-generate`
      - `kanye.reference-edit`
    - route packages now exist under `hermes-runtime/adapters/agents/kanye/packages`
    - local tests, VPS dispatch replay, and real VPS smokes are green
    - remaining work is tuning, delivery hardening, MM lineage, and wider motion coverage
  - route classification kept explicit as `on_demand`, `cron`, `dependent`, `internal`, `mission_required`, or `trigger_only`
5. `Mission autonomy substrate`
   - backend floor now live:
     - `mission_tasks`
     - `mission_task_events`
     - derived `mission.next_check_at`
     - nested MM API routes under `/api/missions/:id/tasks`
   - next remaining work:
     - cockpit/UI reflection
     - Hermes one-shot follow-up wake loop
   - exact current floor:
     - `workflow_runs` and `agent_run_events` exist
     - recurring wake/cron primitives exist
6. `repo/VPS truth gate`
   - local repos remain canonical code truth
   - VPS checkouts remain deploy mirrors plus live runtime state
   - every phase must declare the synced file set and exact VPS-replayable test slice
   - no phase is closed without local tests, VPS replay, live smoke when applicable, and operator confirmation over the real Jack bridge

Execution discipline for the next wave is now fixed:
- `mission autonomy truth gate` is the critical-path writer slice
- once that contract is frozen, `MM contract`, `MM review workspace`, and `Hermes outcome normalization` can run in parallel on disjoint write sets
- `Shopify residuals` and `deploy/test normalization` remain sidecar lanes, not alternate truths
- writer ownership stays single-surface to avoid conflicting truths in registries, route packages, and runtime contracts
     - mission-level task truth exists on the backend but is not fully surfaced yet
5. `Enterprise memory`
   - Jack X per-channel worker truth beyond the current source-family floor
   - Mnemos natural high-saturation compaction proof plus better operator observability
6. `Governance fallback`
   - `protocol-missing`
   - `capability-missing`
   - keep specialist execution bounded when route coverage is absent
8. `Harness+`
   - Phase 3 verification
   - iterative feedback loops tied to MM/task truth
   - final OpenClaw runtime retirement

## Parallel Execution Rule

Every remaining wave should use the same discipline:

1. read-only audit wave in parallel
   - one subagent or parallel audit lane per axis
   - no concurrent mutation on the same registry/protocol surface
2. single-owner implementation wave
   - one writing owner per canonical file surface
3. regression wave
   - local targeted tests
   - VPS targeted tests
   - live smoke when the surface is runtime-bearing

Current support-lane truth:

- local worktrees remain canonical
- VPS checkouts are deploy mirrors only
- VPS repo state is still noisy enough that broad replay should not be trusted without a targeted sync

## Current Validation Checks

The minimum verification pass that keeps this status truthful today is:

```bash
ssh -i /Users/moufdi/.ssh/jack-ai-assistant-key.pem ubuntu@54.76.101.182 \
  'systemctl is-active hermes-gateway-8aa553a5.service'

ssh -i /Users/moufdi/.ssh/jack-ai-assistant-key.pem ubuntu@54.76.101.182 \
  'systemctl is-active hermes-gateway-10adb74d.service'

ssh -i /Users/moufdi/.ssh/jack-ai-assistant-key.pem ubuntu@54.76.101.182 \
  'curl -fsS http://127.0.0.1:3000/health'

ssh -i /Users/moufdi/.ssh/jack-ai-assistant-key.pem ubuntu@54.76.101.182 \
  'test -f /home/ubuntu/.brm-hermes/profiles/jack/whatsapp/session/creds.json'

ssh -i /Users/moufdi/.ssh/jack-ai-assistant-key.pem ubuntu@54.76.101.182 \
  'grep -E "^(ANTHROPIC_TOKEN|MISSION_MANAGER_API_URL)=" /home/ubuntu/.brm-hermes/.env | cut -d= -f1 | sort'

curl -fsS https://api.mission-manager.brmagency.co/api/health

curl -fsS https://api.mission-manager.brmagency.co/api/workflow-runs?agent_id=jack-x\&protocol_id=jack-x.db-analysis\&limit=3

ssh -i /Users/moufdi/.ssh/jack-ai-assistant-key.pem ubuntu@54.76.101.182 \
  'cd /home/ubuntu/hermes-runtime/hermes-agent && ./venv/bin/python -m pytest tests/gateway/test_brm_supervision.py -q'

ssh -i /Users/moufdi/.ssh/jack-ai-assistant-key.pem ubuntu@54.76.101.182 \
  "cd /home/ubuntu/openclaw && \
   node --import tsx /home/ubuntu/openclaw/scripts/brm-specialist-dispatch.ts \
     --mode run \
     --route rosa.audit-performance-marketing \
     --inputs '{\"store\":\"blinx\",\"period_days\":1,\"end_date\":\"2026-04-06\"}' >/dev/null"

python3 /Users/moufdi/openclaw/scripts/mnemos-context-check.py \
  --profile jack \
  --session-id 20260409_001136_a5af1cf8 \
  --context-window-tokens 1000000

ssh -i /Users/moufdi/.ssh/jack-ai-assistant-key.pem ubuntu@54.76.101.182 \
  'grep -n "jack-x" /etc/cron.d/agent-mission-loop'

ssh -i /Users/moufdi/.ssh/jack-ai-assistant-key.pem ubuntu@54.76.101.182 \
  'HERMES_HOME=/home/ubuntu/.brm-hermes/profiles/jack /home/ubuntu/hermes-runtime/hermes-agent/venv/bin/hermes cron list --all'

ssh -i /Users/moufdi/.ssh/jack-ai-assistant-key.pem ubuntu@54.76.101.182 \
  'HERMES_HOME=/home/ubuntu/.brm-hermes/profiles/jack-x /home/ubuntu/hermes-runtime/hermes-agent/venv/bin/hermes cron list --all'

ssh -i /Users/moufdi/.ssh/jack-ai-assistant-key.pem ubuntu@54.76.101.182 \
  'python3 - <<PY
import json
from pathlib import Path
latest = json.loads(Path("/home/ubuntu/.openclaw/memory-wiki/latest.json").read_text())
print(json.dumps({
  "run_id": latest.get("run_id"),
  "page_count": latest.get("page_count"),
  "review_items": len(latest.get("review_items") or []),
  "kg_operations": len(latest.get("kg_operations") or []),
  "llm_enabled": latest.get("llm_enabled"),
}, indent=2))
PY'

ssh -i /Users/moufdi/.ssh/jack-ai-assistant-key.pem ubuntu@54.76.101.182 \
  'HERMES_HOME=/home/ubuntu/.brm-hermes/profiles/mnemos /home/ubuntu/hermes-runtime/hermes-agent/venv/bin/hermes cron list --all'
```

The documentation projection pass that must stay aligned after each deploy is:

```bash
LC_ALL=C shasum -a 256 \
  ~/openclaw/docs/ops/MASTERPLAN.md \
  ~/openclaw/docs/ops/STATUS.md \
  ~/openclaw/docs/ops/HERMES_BRM_VALIDATION_BACKLOG.md \
  ~/hermes-runtime/docs/integrations/status-matrix.md \
  ~/hermes-runtime/docs/integrations/agent-map.md \
  ~/hermes-runtime/docs/agent-channel-rollout.md

ssh -i /Users/moufdi/.ssh/jack-ai-assistant-key.pem ubuntu@54.76.101.182 \
  'LC_ALL=C shasum -a 256 \
    /home/ubuntu/openclaw/docs/ops/MASTERPLAN.md \
    /home/ubuntu/openclaw/docs/ops/STATUS.md \
    /home/ubuntu/openclaw/docs/ops/HERMES_BRM_VALIDATION_BACKLOG.md \
    /home/ubuntu/hermes-runtime/docs/integrations/status-matrix.md \
    /home/ubuntu/hermes-runtime/docs/integrations/agent-map.md \
    /home/ubuntu/hermes-runtime/docs/agent-channel-rollout.md'
```

## Current Integration Truth

- `Anthropic`, `OpenAI Codex`, `Kimi`, and `Z.AI / GLM` are now centrally resolved for the active local Hermes runtime.
- `Gemini` is centrally resolved and now materially validated on the closed `Cortex ads-observation` Phase 1 route.
- `Mission Manager API` is usable and validated as a hosted operator surface; the Hermes runtime bridge into MM now exists and is live on the first supervised path, but the full ecosystem closeout is still partial.
- `BigBlue`, `Google Search Console`, `DataForSEO`, `Hiboo ads / creatives`, `Zendesk live`, and `PayPal live` currently have a closed or bounded live validation floor on Hermes+BRM.
- `Hiboo core` is live enough for current `Naya` telemetry and `Jeff` script-first work, while the broader Hiboo ads/creatives family is only closed on the current Rosa/Cortex routes and remains partial outside those packaged surfaces.
- `Shopify`, `Klaviyo`, `Lark`, `Google Ads`, `GA4`, `Meta Ads`, `Apify`, `Recharge`, `Cloudflare`, and `GoDaddy` are now centrally wired but remain only partially validated on Hermes.
- `Lark` remains explicitly in-scope for `v1`; it is not deferred with `Telegram`.
- `Jack X` now uses a governed channel contract instead of scanning every provider alias opportunistically:
  - `/Users/moufdi/hermes-runtime/contracts/jack-x-channel-registry.json`
  - current production-default slices:
    - `mail.ms365.work`
    - `lark.messages.cx-maybe`
    - `lark.tables.operations-marketing.maybe-paris`
    - `whatsapp.groups.jack-runtime`
  - non-production slices stay explicit:
    - `lark.tables.operations-marketing.blinx` -> `draft`
    - `whatsapp.dm.operator` -> `draft`
- `Zendesk live` is now `usable`: the canonical skill, Selena live runner, package, and dispatch route are wired; the live fetch is validated on the governed bounded path using `skip-comments`, and frozen replay on the live export is stable.
- `PayPal live` is now `usable`: the canonical skill, Selena live runner, package, and dispatch route are wired; live auth, live fetch, and frozen replay on the live export are validated.
- Selena live cutover on `2026-04-05`:
  - canonical `Zendesk` and `PayPal` credentials were seeded into `brm-api-keys`
  - Hermes business sync now resolves both integrations from the canonical store
  - `zendesk.py whoami` and `paypal.py auth-check` are green with the synced Hermes env
  - `selena.paypal-dispute.phase1-live` now passes live fetch and frozen-live replay validation
  - `selena.zendesk-feedback-live` now passes live fetch and frozen-live replay validation on the governed bounded path `skip-comments`
  - review roots:
    - `/Users/moufdi/hermes-runtime/reviews/2026-04-05T-selena-live-cutover`
    - `/Users/moufdi/hermes-runtime/reviews/2026-04-05T-selena-live-frozen-validation`
- `Selena` is therefore closed for V1 on `artifact-fed` routes plus bounded live PayPal and bounded live Zendesk routes.
- WhatsApp VPS cutover on `2026-04-05` / `2026-04-06`:
  - Hermes workspace was deployed to `/home/ubuntu/hermes-runtime`
  - active runtime home is `/home/ubuntu/.brm-hermes/profiles/jack`
  - paired session now exists at `/home/ubuntu/.brm-hermes/profiles/jack/whatsapp/session/creds.json`
  - generated system service is:
    - `hermes-gateway-8aa553a5.service`
  - production health checks are green:
    - `systemctl is-active hermes-gateway-8aa553a5.service` -> `active`
    - `systemctl is-enabled hermes-gateway-8aa553a5.service` -> `enabled`
    - `curl http://127.0.0.1:3000/health` -> `{"status":"connected", ...}`
  - current VPS-seeded profile homes include:
    - `jack`
    - `jack-x`
    - `mnemos`
    - `rosa`
    - `jeff`
    - `alfred`
    - `naya`
    - `selena`
    - `tony`
    - `tony-dev`
    - `tony-kimi`
    - `cortex`
  - governed ingress truth now enforced on the VPS:
    - explicit specialist asks on WhatsApp are pre-routed before agent execution
    - resolved governed routes dispatch the owned specialist route
    - unresolved specialist asks block instead of silently falling back to `Jack direct`
  - legacy OpenClaw channel runtime on the same VPS is now disabled:
    - `jack-ai-assistant.service` -> `inactive`, `disabled`
    - `openclaw-gateway.service` -> `inactive`
  - first audited governed ingress proof is now closed:
    - allowed-user inbound message created the mission path
    - transcript / observation / MM reflection were linked on the same route
    - specialist dispatch stayed governed on `Rosa`
    - deliverables landed on Drive and were attached back into MM
    - mission/file traceability was tightened with explicit creation metadata plus `mission_id` and `run_id`
  - hosted MM board was then reset back to `0 mission` after validation so the operator surface is clean again
- `Telegram` remains a legacy OpenClaw channel surface, but it is now explicitly deferred from the `v1` closeout perimeter.
- `Mnemos` now has a first truthful Hermes route locally:
  - canonical runner:
    - `/Users/moufdi/openclaw/scripts/mnemos-context-check.py`
  - package:
    - `/Users/moufdi/hermes-runtime/adapters/agents/mnemos/packages/mnemos.context-check.protocol.yaml`
  - first smoke result on a real Jack session:
    - `/Users/moufdi/.openclaw/workspace-mnemos/reports/context-check/jack/20260406t222326z/context-check.result.json`
  - current verdict:
    - packaged and smoke-green locally and on the VPS, but not yet replay-validated
    - trigger-only, not invokable by Mission Manager
- `Google Drive` remains approval-gated by design and still belongs to the later `MM + Drive + channels` wave.
- `MS365 work` is now `usable` on Hermes+BRM:
  - canonical skill path:
    - `/Users/moufdi/clawd/skills/ms365-mail/scripts/ms365_mail.py`
  - live auth check and bounded inbox fetch are green
  - `jack-x-email-intake-pass0.py` now produces an incremental live artifact from the work inbox
    - fetch is paginated from the committed cursor
    - inbox order is ascending from the last processed timestamp
    - first bootstrap starts from a recent horizon if no cursor exists yet
  - `jack-x-email-intake-memory-update.py` now turns that artifact into:
    - local memory files
    - a shared-graph candidate
    - candidate object and relation extraction for review
    - candidate KG matches with confidence, without auto-merging them into shared graph
  - the candidate was committed through:
    - `/Users/moufdi/openclaw/scripts/brm-shared-graph.py`
    - actor: `jack-x`
  - strict graph validation after commit remains:
    - `0 errors`
    - `0 warnings`
  - review root:
    - `/Users/moufdi/hermes-runtime/reviews/2026-04-05T21-36-jack-x-ms365-memory-proof`
- `Jack` email digest is now a separate cron-backed operator surface, distinct from Jack X memorization:
  - canonical cycle runner:
    - `/Users/moufdi/hermes-runtime/scripts/jack_email_digest_cycle.py`
  - canonical digest runner:
    - `/Users/moufdi/openclaw/scripts/jack-email-digest-review.py`
  - canonical Hermes recurring manifest:
    - `/Users/moufdi/hermes-runtime/contracts/hermes-recurring-jobs.v1.json`
  - runtime truth:
    - runs explicitly on `zai/glm-5.1`
    - reads the latest qualified Jack X mail artifact plus the current memory compact candidate
    - does not mutate Jack X memory, KG, or Mission Manager
    - keeps its own digest state to avoid redigesting the same artifact indefinitely
- `Lark` channel intake is now `usable` on Hermes+BRM on the first truthful Jack X path:
  - canonical skill path:
    - `/Users/moufdi/clawd/skills/lark-api/scripts/lark.py`
  - live auth, chat metadata fetch, and bounded message fetch are green
  - `jack-x-lark-message-intake-pass0.py` now produces an incremental live artifact from configured `Lark` channels
    - fetch is paginated from a committed per-chat cursor
    - channel order is ascending from the last processed create-time
    - first bootstrap starts from a recent horizon if no cursor exists yet
  - `jack-x-lark-message-memory-update.py` now turns that artifact into:
    - local memory files
    - a shared-graph candidate
    - candidate object and relation extraction for review
    - candidate KG matches with confidence, without auto-merging them into shared graph
  - the candidate was committed through:
    - `/Users/moufdi/openclaw/scripts/brm-shared-graph.py`
    - actor: `jack-x`
  - strict graph validation after commit remains:
    - `0 errors`
    - `0 warnings`
- `Lark` tables intake is now `usable` on Hermes+BRM on the first governed production slice:
  - canonical pass0 path:
    - `/Users/moufdi/openclaw/scripts/jack-x-lark-table-intake-pass0.py`
  - canonical cycle:
    - `/Users/moufdi/hermes-runtime/scripts/jack_x_lark_table_cycle.py`
  - current contracted production slice:
    - `maybe-paris`
  - current draft slice:
    - `blinx`
- `WhatsApp` Jack X intake is now `usable` on the first bounded remote-snapshot path:
  - canonical pass0 path:
    - `/Users/moufdi/openclaw/scripts/jack-x-whatsapp-intake-pass0.py`
  - canonical cycle:
    - `/Users/moufdi/hermes-runtime/scripts/jack_x_whatsapp_cycle.py`
  - canonical Hermes recurring manifest:
    - `/Users/moufdi/hermes-runtime/contracts/hermes-recurring-jobs.v1.json`
  - source transport:
    - snapshot `whatsapp/archive/messages.jsonl`
    - snapshot `sessions/sessions.json`
    - snapshot `state.db`
    - from `jack-vps`
  - current truth:
    - DM validation path green
    - bridge runtime now records append-only raw WhatsApp messages independently from session exposure
    - Jack X reads the raw archive first and only falls back to `sessions/state.db` for compatibility
    - group-only scheduled path still needs real live group traffic on the VPS runtime to enrich the archive beyond the current DM floor
    - known historical WhatsApp groups have been reconciled into the Jack X channel registry as named `draft` channels, pending live re-observation on the Hermes VPS runtime
- Jack X / digest recurring cutover on `2026-04-11`:
  - canonical recurring manifest:
    - `/Users/moufdi/hermes-runtime/contracts/hermes-recurring-jobs.v1.json`
  - canonical syncer:
    - `/Users/moufdi/hermes-runtime/scripts/sync-hermes-recurring-jobs.py`
  - canonical profile gateway installer:
    - `/Users/moufdi/hermes-runtime/scripts/install-hermes-profile-gateway.sh`
  - canonical cycle runner:
    - `/Users/moufdi/hermes-runtime/scripts/jack_x_email_intake_cycle.py`
  - `Jack` digest cycle runner:
    - `/Users/moufdi/hermes-runtime/scripts/jack_email_digest_cycle.py`
  - `Lark` channel cycle runner:
    - `/Users/moufdi/hermes-runtime/scripts/jack_x_lark_message_cycle.py`
  - `WhatsApp` cycle runner:
    - `/Users/moufdi/hermes-runtime/scripts/jack_x_whatsapp_cycle.py`
  - `Lark` tables cycle runner:
    - `/Users/moufdi/hermes-runtime/scripts/jack_x_lark_table_cycle.py`
  - VPS runtime truth:
    - `/home/ubuntu/.brm-hermes/profiles/jack/cron/jobs.json` now carries the `jack.email-digest` schedule set (`4` jobs)
    - `email-digest-weekend` was replayed end-to-end on `2026-04-12`; first two WhatsApp auto-deliveries exposed real contract bugs (`cwd` path drift, then `response_mode` path drift), both fixed, and the final replay landed as a success message in `/home/ubuntu/.brm-hermes/profiles/jack/whatsapp/archive/messages.jsonl`
    - `/home/ubuntu/.brm-hermes/profiles/jack-x/cron/jobs.json` now carries the current `jack-x` recurring floor from `hermes-recurring-jobs.v1`:
      - `4` `jack-x.registry-ingest` jobs
      - `4` `jack-x.db-analysis` jobs
      - `4` `jack-x.memory-wiki` jobs
    - `/etc/cron.d/agent-mission-loop` no longer owns `AGENT_ID=jack-x`; that legacy line is explicitly disabled
    - dedicated Hermes cron-only gateway now runs for `jack-x` as `hermes-gateway-10adb74d.service`
    - real VPS proof on `2026-04-11` for `jack-x-lark-table-afternoon`:
      - `pass0`: `7` operations exported on `maybe-paris`
      - `memory update`: `ok`
      - `graph commit`: `ok`
      - `graph validate`: `0 error / 0 warning`
      - `MM runtime`: `runtime.ok` written against recurring task `25`
    - one-shot natural Hermes scheduler proof on `2026-04-11 23:55` Paris:
      - temporary job `jack-x-lark-table-validation-once-20260411-2155utc` fired from Hermes cron history
      - output persisted under `/home/ubuntu/.brm-hermes/profiles/jack-x/cron/output/...`
      - cycle result: `noop` on duplicate-only batch, which is expected for a validation rerun
      - MM runtime reporting now skips `404 recurring task not found` for temporary validation jobs while staying strict for canonical recurring ids
    - final VPS confirmation on `2026-04-12` after the reporting-contract closeout:
      - all four canonical Jack X cycles now append a post-step `worldstate_consolidate` artifact under `/home/ubuntu/.openclaw/workspace-jack-x/logs/cron/`
      - `jack_x_email_intake_cycle.py` finished `ok` with `199` promotable emails, graph commit `ok`, strict validate `0 error / 0 warning`, and `worldstate_summary.status = ok`
      - `jack_x_lark_message_cycle.py` finished `ok` on the weekend slice with duplicate-only `noop`, cursor advance `advanced`, and `worldstate_summary.status = ok`
      - `jack_x_whatsapp_cycle.py` finished `ok` on the group-only weekend slice with duplicate-only `noop` and `worldstate_summary.status = ok`
      - `jack_x_lark_table_cycle.py` finished `ok` on the weekend slice with duplicate-only `noop` and `worldstate_summary.status = ok`
      - the only scheduler red observed during validation was a temporary lock collision on `jack-x-lark-table-weekend`; it was replayed cleanly through Hermes cron and the canonical scheduler state now sits at `last_status = ok`
      - latest consolidated worldstate reports from this confirmation keep `missing_durable_entity_types = []` and `missing_durable_relation_types = []`
  - `mnemos` stays explicit:
    - `trigger_only`
    - no recurring Hermes cron job until cadence/policy is intentionally defined
    - latest technical trigger proof on `2026-04-11`:
      - `mnemos-context-check.py` ran under `HERMES_HOME=/home/ubuntu/.brm-hermes/profiles/jack`
      - source session: `20260411_141721_ab2b8360`
      - verdict: `review_ready`
      - saturation band: `normal`
  - as of `2026-04-09`, the `Jack` email digest cadence is now:
    - weekdays: `10:00`, `15:00`, `19:00`
    - weekend: `10:00`
  - as of `2026-04-09`, the `Jack X` email memorization cadence is now separated and staggered ahead of digest at:
    - weekdays: `09:50`, `14:50`, `18:50`
    - weekend: `09:50`
  - as of `2026-04-08`, the `Lark` channel cadence is staggered on the same rhythm at:
    - weekdays: `10:05`, `15:05`, `19:05`
    - weekend: `10:05`
  - as of `2026-04-08`, the `WhatsApp` cadence is staggered on the same rhythm at:
    - weekdays: `10:07`, `15:07`, `19:07`
    - weekend: `10:07`
  - as of `2026-04-08`, the `Lark` tables cadence is staggered on the same rhythm at:
    - weekdays: `10:10`, `15:10`, `19:10`
    - weekend: `10:10`
  - as of `2026-04-23`, the `Jack X Memory Wiki` cadence is staggered after DB analysis at:
    - weekdays: `10:25`, `15:25`, `19:25`
    - weekend: `10:25`
  - as of `2026-04-23`, the `Jack X Memory Wiki` cron command now runs with:
    - `--semantic-mode active`
    - `--semantic-provider gemini`
    - `--semantic-cache-file ${HOME}/.openclaw/semantic-cache/jack-x-semantic-cache.json`
  - the memory-update stage now deduplicates before any durable write:
    - promoted message fingerprints are tracked in `/Users/moufdi/.openclaw/workspace-jack-x/runtime/dedup-state.json`
    - duplicate-only batches exit `noop` before graph commit
    - promoted Lark message fingerprints are tracked in `/Users/moufdi/.openclaw/workspace-jack-x/runtime/lark-message-dedup-state.json`
    - promoted WhatsApp message fingerprints are tracked in `/Users/moufdi/.openclaw/workspace-jack-x/runtime/whatsapp-dedup-state.json`
    - promoted Lark table operation fingerprints are tracked in `/Users/moufdi/.openclaw/workspace-jack-x/runtime/lark-table-dedup-state.json`
  - cursor advance now happens only after the cycle is safe to close:
    - graph commit succeeded
    - strict graph validation succeeded
    - dedup finalize succeeded, or the batch was a safe `noop`
  - manual cycle run is green end-to-end:
    - BRM gates
    - live MS365 pass0
    - local memory update
    - governed graph commit
    - strict graph validate
  - manual `Lark` cycle run is green end-to-end on `CX_MAYBE`:
    - BRM gates
    - live Lark channel pass0
    - local memory update
    - governed graph commit
    - strict graph validate
  - manual `Lark` tables cycle run is green end-to-end on the contracted `maybe-paris` slice:
    - BRM gates
    - live Lark table pass0
    - local memory update
    - governed graph commit
    - strict graph validate
  - manual `WhatsApp` cycle validation is green on the bounded DM path:
    - remote runtime snapshot
    - local pass0
    - local memory update
    - governed graph commit
    - strict graph validate
  - scheduled `WhatsApp` group path is wired but currently `noop` until the VPS runtime exposes real group sessions
  - `launchctl print` confirms the new BRM service exists in the GUI domain
  - the old service `com.openclaw.jackx.extraction` is no longer present in the GUI domain
  - review root:
    - `/Users/moufdi/hermes-runtime/reviews/2026-04-05T21-45-jack-x-cron-cutover`
- first live `Drive -> MM blocked` proof on `2026-04-05`:
  - live mission: `64 / HBRM-JEFF-DRIVE-001`
  - route: `jeff.performance-report`
  - governed dispatch produced workspace artifacts and stopped at the operator approval gate:
    - `route_status = blocked_pending_approval`
    - `route_can_finalize = false`
    - blocker code: `delivery_approval_required`
  - MM mission `64` now reflects:
    - `todo -> in_progress -> blocked`
    - artifact paths in notes/logs
    - explicit blocker and next action
  - review root:
    - `/Users/moufdi/hermes-runtime/reviews/2026-04-05T20-50-mm-drive-proof`
- second live `Drive -> MM blocked` proof on `2026-04-05`:
  - live mission: `65 / HBRM-NAYA-DRIVE-001`
  - route: `naya.product-sourcing`
  - governed dispatch produced workspace artifacts and stopped at the operator approval gate:
    - `route_status = blocked_pending_approval`
    - `route_can_finalize = false`
    - blocker code: `delivery_approval_required`
  - MM mission `65` now reflects:
    - `todo -> in_progress -> blocked`
    - artifact paths in notes/logs
    - explicit blocker and next action
  - review root:
    - `/Users/moufdi/hermes-runtime/reviews/2026-04-05T21-20-naya-drive-proof`
- third live `Drive -> MM blocked` proof on `2026-04-05`:
  - live mission: `66 / HBRM-ALFRED-DRIVE-001`
  - route: `alfred.visibility-audit`
  - governed dispatch produced workspace artifacts and stopped at the operator approval gate:
    - `route_status = blocked_pending_approval`
    - `route_can_finalize = false`
    - blocker code: `delivery_approval_required`
  - MM mission `66` now reflects:
    - `todo -> in_progress -> blocked`
    - artifact paths in notes/logs
    - explicit blocker and next action
  - `Alfred` is now present again in the hosted MM member roster as a real `ai_agent` member:
    - member id: `28`
  - review root:
    - `/Users/moufdi/hermes-runtime/reviews/2026-04-05T21-35-alfred-drive-proof`
- Mission Manager bridge live proof on `2026-04-05`:
  - bridge client: `/Users/moufdi/openclaw/src/bridges/mission-manager-client.ts`
  - bridge logic: `/Users/moufdi/openclaw/src/bridges/brm-mm-bridge.ts`
  - bridge CLI: `/Users/moufdi/openclaw/scripts/brm-mm-bridge.ts`
  - targeted tests are now `26/26` green across:
    - `brm-mm-bridge.test.ts`
    - `brm-specialist-dispatch.test.ts`
    - `brm-protocol-enforcement.test.ts`
  - live MM mission `332 / HBRM-CORTEX-001` was pushed through:
    - `todo -> in_progress -> review -> done`
  - review root:
    - `/Users/moufdi/hermes-runtime/reviews/2026-04-05T20-10-mm-bridge-cortex`
  - hosted clean-slate reset on `2026-04-05`:
    - canonical reset script now exists at `/Users/moufdi/Desktop/ClaudeCode/mission-manager-git/scripts/reset-missions-hosted.mjs`
    - the correct production reset path is now explicit:
      - reset local `missions.json`
      - upload empty `db/missions.json` to `s3://mission-manager-frontend-314146310107`
      - force ECS deployment on `mission-manager-prod-backend`
      - wait for `services-stable`
      - verify hosted API `missions=0`
    - live result:
      - hosted API before reset: `177` missions
      - hosted API after reset: `0` missions
      - ECS service returned to `steady state`
    - review root:
      - `/Users/moufdi/hermes-runtime/reviews/2026-04-05T20-35-mm-hosted-reset`
- Jack -> MM -> specialist handoff proof on `2026-04-05`:
  - live mission: `331 / HBRM-JEFF-001`
  - route: `jeff.analyse-profil`
  - dispatch plan carried the MM mission id and kept route-owned runtime knobs:
    - model: `anthropic/claude-opus-4.6`
    - gate timeout: `30s`
    - runtime timeout: `1500s`
  - live dispatch finished `exit_code=0`
  - MM mission `331` now reflects:
    - `todo -> in_progress -> review`
  - review root:
    - `/Users/moufdi/hermes-runtime/reviews/2026-04-05T20-20-mm-handoff-jeff`
  - explicit limit:
    - this is a real handoff proof, not yet the final end-to-end ecosystem with messenger ingress
- Jack -> MM -> specialist route-matrix replay on `2026-04-07`:
  - canonical replay harness:
    - `/Users/moufdi/openclaw/scripts/jack-supervised-route-handoff.py`
  - full governed matrix review root:
    - `/Users/moufdi/hermes-runtime/reviews/jack-handoff-sweep-2026-04-07T00-16-00Z`
  - `mission_only` guard remains correct:
    - `rosa.market-graph-refresh`
    - `jeff.candidate-intake`
  - governed handoff reached `todo -> in_progress -> review` on:
    - `rosa.offer-strategy.direct`
    - `rosa.audit-performance-marketing`
    - `rosa.veille-concurrentielle`
    - `jeff.analyse-profil`
    - `jeff.performance-report`
    - `alfred.visibility-audit`
    - `naya.stock-check`
    - `naya.campaign-support`
    - `naya.product-sourcing`
    - `selena.paypal-dispute.phase1-audit`
    - `selena.paypal-dispute.phase1-live`
    - `selena.zendesk-feedback-review`
    - `selena.zendesk-feedback-live`
    - `tony.codebase-exploration`
    - `cortex.ads-observation`
  - Tony closeout on `2026-04-07`:
    - per-profile Codex auth was realigned for `tony` and `tony-dev`
    - Hermes Codex streaming now reconstructs `response.output` from stream events on the current ChatGPT Codex backend
    - `tony.development-plan` moved to a canonical runner and now lands in hosted MM `review`
    - `tony.development` prompting now makes snapshot mutation explicit and the canonical route now lands in hosted MM `review`
  - operator/data fix applied during the replay:
    - hosted MM member `Alfred` recreated so `alfred.visibility-audit` can now be assigned and reviewed on the hosted board

Current decision:
- We keep working on production protocols.
- The strategic destination is now `Hermes + BRM Harness + Mission Manager + messenger ingress`, not `OpenClaw` as a runtime.
- `OpenClaw` should now be treated as a legacy runtime, script archive, and migration shim layer.
- The enforced cutover order is now:
  - integrations
  - KG and memory hydration
  - harness and protocol enforcement
  - incoming message surfaces
- We do not trust `Jack -> subagent` for critical missions until the runtime layer is fixed.
- `Mission Manager` API is usable as a supervised operator surface, but this does not imply orchestration trust.
- `Mission Manager` live data must be treated as operator visibility only, not runtime proof.
- MM hosted backend truth is `ECS/ALB eu-west-3`, not the Jack VPS.
- Runtime credential resolution is now centralized locally by design through `auth-profiles.json` plus `~/.brm-hermes/.env`, but the codebase still permits legacy inline secrets in `openclaw.json`, so hard-enforcement is not fully finished.
- Local auth migration was executed on `2026-04-01`: model-provider secrets were moved out of `openclaw.json`, the main auth store now carries `anthropic`, `google`, `kimi-coding`, and `openai-codex` profiles, and the gateway launchd plist no longer duplicates the LLM provider keys.
- Instagram graph auth is now standardized through AWS Secrets Manager -> `sync-secrets.py` -> `openclaw.json` env fallback, with conservative crawl throttling enabled.
- `candidate-intake` now auto-queues a bounded `roster-expansion` run for B+ profiles after graph sync, instead of blocking the intake response.
- `Jack X` local mission+memory validation was replayed on a frozen corpus on `2026-04-01`: `3` runs, `1` stable signature, but all runs blocked on model authentication before useful protocol execution.
- Local provider resolution re-check on `2026-04-01`: `anthropic`, `google`, and `kimi-coding` now resolve from `auth-profiles.json`; `openai-codex` still requires re-auth because the stored refresh token is invalid (`refresh_token_reused`).
- BRM Phase 0 runtime contracts are now drafted locally on `2026-04-01`: mission event, runtime observation, session envelope, artifact contract, validation report, and status gate definitions exist as the runtime-agnostic control plane contract.
- Hermes migration roots are now created locally on `2026-04-01`: workspace `/Users/moufdi/hermes-runtime` and isolated state dir `/Users/moufdi/.brm-hermes`.
- Hermes local runtime bootstrap completed on `2026-04-01`: code installed in `/Users/moufdi/hermes-runtime/hermes-agent`, compatibility link `~/.hermes -> ~/.brm-hermes` created, and native CLI `hermes` is operational.
- Hermes native OpenClaw migration was previewed on `2026-04-01`: useful for generic user-data, but insufficient for `Jack`, `Jack X`, Mission Manager governance, BRM runtime contracts, or anti-variance.
- Hermes profiles `jack` and `jack-x` now exist locally on `2026-04-01`, with BRM-specific `SOUL.md` and stable per-profile working directories.
- Hermes specialist and coordination profiles now also exist locally on `2026-04-01` (`rosa`, `naya`, `cortex`, `jhin`, `kanye`, `walter`, `tony`, `mnemos`); since then, `rosa`, `jeff`, `alfred`, `naya`, and `tony` have been materially standardized beyond scaffold state, while `jhin` is now treated as an internal visual capability under `kanye`.
- Hermes profile auth is now centralized locally through `/Users/moufdi/.brm-hermes/.env`, with profile `.env` files linked to the shared root and synced from the consolidated OpenClaw auth store where applicable.
- Hermes Anthropic auth for `jack` was corrected on `2026-04-01`: direct `ANTHROPIC_API_KEY` sync was removed, local TLS trust for the Hermes Python runtime was fixed with `SSL_CERT_FILE`, and `Claude Pro/Max` OAuth now succeeds for the `jack` profile.
- Hermes status surface still under-reports Anthropic OAuth on `2026-04-01`: `jack status` shows `Anthropic ✗ (not set)` even though `jack` executes successfully via the stored OAuth credential.
- Hermes Kimi auth for `jack-x` was corrected on `2026-04-01`: the consolidated OpenClaw `kimi-coding:default` key and shared Hermes env were updated, the `jack-x` profile stale OpenRouter base URL was removed, and `jack-x` now executes successfully on the Kimi route.
- Hermes Z.AI / GLM auth was added on `2026-04-04`: the consolidated OpenClaw auth store now carries a `zai:default` API-key profile, the shared Hermes env now syncs `GLM_API_KEY` with the coding endpoint base URL, and the global Hermes default runtime model is now `zai/glm-5` for base conversation only.
- Hermes business secret sync now has a non-interactive GCP fallback on `2026-04-05`: when the normal `gcloud` user session is stale, `/Users/moufdi/hermes-runtime/scripts/sync-business-secrets-to-hermes.py` now activates the local service account from `GOOGLE_APPLICATION_CREDENTIALS` and can successfully pull `HIBOO_SERVICE_API_KEY` into `/Users/moufdi/.brm-hermes/.env`.
- Hermes GLM smoke on `2026-04-04` is green on both paths:
  - explicit provider/model: `hermes chat --provider zai --model glm-5` -> `GLM_OK`
  - default runtime path: `hermes chat` -> `DEFAULT_GLM_OK`
- Zendesk live migration surface was added on `2026-04-05`: local skill `clawd/skills/zendesk`, live runner `selena-zendesk-feedback-live.py`, package `selena.zendesk-feedback-live`, and dispatch registry wiring now exist; replay dispatch on frozen export passes, but live Zendesk credentials are still missing.
- PayPal live migration surface was added on `2026-04-05`: local skill `clawd/skills/paypal`, live runner `selena-paypal-dispute-live.py`, package `selena.paypal-dispute.phase1-live`, and dispatch registry wiring now exist; replay dispatch on frozen export passes, but live PayPal credentials are still missing.
- Hermes business sync was hardened on `2026-04-05`: `sync-business-secrets-to-hermes.py` now records source errors instead of crashing the whole sync when `gcloud` token refresh fails.
- Selena credential centralization was hardened on `2026-04-05`:
  - `sync-business-secrets-to-hermes.py` now prefers AWS as the first source for `Zendesk` and `PayPal`
  - `rehome-business-secrets-to-aws.py` now knows how to push the `Zendesk` and `PayPal` keyset into `brm-api-keys`
- Zendesk live fetch was hardened on `2026-04-05`:
  - `/Users/moufdi/clawd/skills/zendesk/scripts/zendesk.py` now tolerates per-ticket `404 RecordNotFound` on the comments endpoint instead of aborting the whole export
- Selena Zendesk live dispatch now supports the governed bounded flag path on `2026-04-05`:
  - `skip-comments` is now route-owned in `/Users/moufdi/hermes-runtime/contracts/specialist-route-registry.json`
  - boolean bare-flag runner inputs are now supported in `/Users/moufdi/openclaw/src/bridges/brm-specialist-dispatch.ts`
  - targeted bridge/gate tests are now `20/20`
- specialist/runtime truth remains unchanged:
  - agent profiles and protocol packages still own their explicit provider/model choices
  - Jack does not gain permission to override specialist model or timeout selection
- Jeff `analyse-profil` was connected on Hermes on `2026-04-03`: the pass0 and report scripts are now locally portable, the first Hermes package exists, a real live run on `romi_allata` completed successfully, and the delivery path stops at the expected BRM Drive approval gate instead of bypassing operator control.
- Jeff `performance-report` was packaged on Hermes on `2026-04-03`: the route now has its own BRM package, launch/stage gates pass locally, a real live local replay succeeds, and upload delivery stops at the expected BRM approval gate.
- Jeff `candidate-intake` was made portable and packaged on Hermes on `2026-04-03`: the runtime no longer depends on VPS-only workspace paths, the core local intake run succeeds, the graph helper now writes to the local graph workspace, and full exact-following graph completion remains under live observation instead of being falsely claimed.
- Jack-safe specialist dispatch is now real on Hermes on `2026-04-03`:
  - implementation: `/Users/moufdi/openclaw/scripts/brm-specialist-dispatch.ts`
  - registry: `/Users/moufdi/hermes-runtime/contracts/specialist-route-registry.json`
  - targeted tests: `/Users/moufdi/openclaw/src/bridges/brm-specialist-dispatch.test.ts`
  - result: `19/19` targeted bridge + gate tests are green when combined with the BRM protocol gate suite
  - enforced rule: Jack may choose the route id and mission context, but not the model or timeout
  - current dispatch truth:
    - `rosa.offer-strategy.direct` -> `spawn_profile`
    - `jeff.analyse-profil` -> `run_canonical`
    - `jeff.performance-report` -> `run_canonical`
    - `jeff.candidate-intake` -> `mission_only`
    - `alfred.visibility-audit` -> `run_canonical` on reviewed report-data only
    - `naya.stock-check` -> `run_canonical`
    - `naya.campaign-support` -> `run_canonical`
    - `naya.product-sourcing` -> `run_canonical`
    - `selena.paypal-dispute.phase1-audit` -> `run_canonical`
    - `selena.zendesk-feedback-review` -> `run_canonical`
  - observed live closeout:
    - `rosa.offer-strategy.direct` specialist dispatch -> `ROSA_DISPATCH_OK`
    - `rosa.audit-performance-marketing` live specialist dispatch -> `review_ready`
    - `jeff.analyse-profil` specialist dispatch -> `ok`
    - `jeff.performance-report` specialist dispatch -> `ok`
    - `alfred.visibility-audit` reviewed-bundle specialist dispatch -> `ok`
    - `naya.stock-check` reviewed-snapshot specialist dispatch -> `ok`
    - `naya.campaign-support` reviewed-snapshot specialist dispatch -> `ok`
    - `naya.product-sourcing` reviewed-sheet specialist dispatch -> `ok`
    - `selena.paypal-dispute.phase1-audit` specialist dispatch -> `ok`
    - `selena.zendesk-feedback-review` specialist dispatch -> `ok`
    - `selena.paypal-dispute.phase1-live` replay-export specialist dispatch -> `ok`
    - `selena.zendesk-feedback-live` replay-export specialist dispatch -> `ok`
  - explicit limits:
    - `jeff.candidate-intake` stays `mission_only` until the exact-following graph branch has a full observed Hermes closeout
    - `alfred.visibility-audit` composite live refresh path was observed as variable and is intentionally not the Jack-safe route
    - `naya.stock-check` validated Jack-safe path still exists on reviewed stock snapshots; the live path is now also validated on a bounded telemetry pilot
    - `selena` is validated on canonical artifact-fed routes only; PayPal phase 2/3 and live Zendesk connectivity remain out of scope
- Alfred runtime portability on Hermes was hardened on `2026-04-02`: local path resolution is now explicit, the first `visibility-audit` BRM package exists, and launch gates pass locally without VPS path assumptions.
- Alfred connectivity on Hermes was closed on `2026-04-03`: live Search Console queries now succeed locally, the canonical Phase 1 bundle `maybe_paris/2026-03-22` was replayed locally, DataForSEO now resolves through the Hermes business sync and AWS secret path, and `visibility-audit` runs locally to `render_only_ok`.
- Alfred delivery on Hermes now reaches the expected operator gate on `2026-04-03`: `visibility-audit` with Drive enabled ends in `blocked_pending_approval`, which confirms the runtime path is live and the only remaining stop is the BRM write-approval gate by design.
- Alfred deterministic dispatch was closed on Hermes on `2026-04-03`: the reviewed-bundle render path passed `3 runs / 0 variance` with stable signature `f7efb4d415f231905a5e8b15404ce5d133de2ef57eea42b404c9043e1ef337de`, while the composite live refresh path was explicitly observed to drift and was therefore split out of the Jack-safe route.
- Naya first-wave Hermes validation was closed on `2026-04-03`:
  - `naya.stock-check` is now protocol-validated on strict supervised runs `1/2/3` with stable signature `0fe8977fd8427c79b1f5b124c6630732cfd7d653122876235ae5152eb489f5c4`
  - `naya.campaign-support` is now protocol-validated on strict supervised runs `1/2/3` with stable signature `7170674ada12d4a2925d03dc5d88ea741f7359bb2041fca7c096420fc6a16478`
  - `naya.product-sourcing` is now protocol-validated on strict supervised runs `1/2/3` with stable signature `13506a272c0455c990f2a37f066171db06c2c695617cf3b1017bf66145e10a71`
  - `Jack`-safe dispatch truth on Hermes:
    - `naya.stock-check` -> `run_canonical`
    - `naya.campaign-support` -> `run_canonical`
    - `naya.product-sourcing` -> `run_canonical`
  - enforced rule: Jack may choose the route id and mission context, but not the model or timeout
  - explicit limit:
    - BigBlue inventory/product/order reads are restored, and `naya-stock-telemetry-pass0.py` now materializes a bounded `56-day` telemetry artifact from BigBlue plus Hiboo purchase-order signal
    - standalone pass0 replay on `2026-04-03` completed in `2m34s`, non-truncated, on `17723` filtered orders across `36` pages
    - live `naya.stock-check` dispatch was replayed on `2026-04-03` with `3 runs / 0 variance`, stable signature `5e4411ed66b5ae9eb0a09c92c7369ac3fc961a6618c2f12e0a8068182f52c6c1`
    - live `naya.campaign-support` now supports the same bounded live pass0 evidence model; BRM dispatch loads `~/.brm-hermes/.env` before gate and runner execution
    - live campaign-support frozen-artifact replay on `2026-04-04` passed `3 runs / 0 variance`, stable signature `4390873454ab9008eb125071d931729c4389feb87e34f4a886547bc6ffb6a736`
    - current live pilot verdict for `Pulse My Hair`: `4572u`, `26.1/j`, `175.2j`, `🟡 SURVEILLER`
    - current live campaign-support verdict for `flash-sale-pulse`: `GO`, `170.2j` coverage after campaign
    - `naya-kimi` remains a future extraction sidecar only and is not part of the validated closeout
- Tony first-wave Hermes validation was closed on `2026-04-03`:
  - `tony.codebase-exploration` is now protocol-validated on strict supervised runs `1/2/3` with stable signature `b53c1d197feb25305f1f6e08de0ea27d0136d852387f0b418aad869bfaed4126`
  - `tony.development-plan` is now protocol-validated on strict supervised runs `1/2/3` with stable signature `aecdf5967f24d3573a7b8c4339ea1a4cedd21a1628463a486e18feb45cd2dfc2`
  - `tony.development` is now protocol-validated on strict supervised runs `1/2/3` with stable signature `a3c705c0d04103fe54ebb2a15fbc95be5854a2c1c2e05460ac97afc7d6ab5f4f`
  - `Jack`-safe dispatch truth on Hermes:
    - `tony.codebase-exploration` -> `spawn_profile` on `tony-kimi`
    - `tony.development-plan` -> `spawn_profile` on `tony`
    - `tony.development` -> `run_canonical` on `tony-dev`
  - enforced rule: Jack may choose the route id and mission context, but not the model or timeout
  - execution route truth:
    - canonical runner: `/Users/moufdi/openclaw/scripts/tony-development-route.py`
    - frozen validation fixture: `/Users/moufdi/hermes-runtime/fixtures/tony-dev-fixture-template`
    - route-owned execution timeout: `900s`
    - route-owned validation timeout: `300s`
  - explicit limits:
    - this closes the canonical fixture route, not every arbitrary codebase mutation pattern
    - `tony.development-plan` launch is still gate-owned: a prompt alone is rejected, and the route becomes dispatchable only when the required `exploration_artifact` compact JSON is supplied alongside the prompt
- Cortex `ads-observation` is now closed for V1 on `2026-04-05`:
  - canonical runner: `/Users/moufdi/openclaw/scripts/cortex-ads-observation.py`
  - replay validator: `/Users/moufdi/openclaw/scripts/cortex_runtime_validate.py`
  - frozen replay validation root: `/Users/moufdi/hermes-runtime/reviews/cortex-ads-observation-validation-2026-04-05`
  - live dispatch closeout root: `/Users/moufdi/hermes-runtime/reviews/2026-04-05T18-20-cortex-phase1-closeout`
  - stable signature: `5ec4e6874824f07a09f2346e99e94dbe56ffad40d6f8a087b419aa80bd388bc7`
  - BRM live dispatch route: `cortex.ads-observation` -> `run_canonical`
  - explicit limit: only Phase 1 is runnable; later phases remain `design-drafted`
- Hermes first real smoke tests on `2026-04-01` are now split correctly:
  - `jack` is `smoke-validated` on Hermes via `Claude Pro/Max` OAuth with output `JACK_OK`
  - `jack-x` is `smoke-validated` on Hermes via `kimi-coding` with outputs `JACKX_OK` and `JACKX_ALIAS_OK`
  - conclusion: wave 1 and wave 2 are now open for protocol validation on frozen corpora
- Hermes protocol-validation waves were initialized on `2026-04-01`:
  - `jack` review root: `/Users/moufdi/hermes-runtime/reviews/2026-04-01T21-04-59.382Z-wave-1-jack-protocol-validation`
  - `jack-x` review root: `/Users/moufdi/hermes-runtime/reviews/2026-04-01T21-04-59.382Z-wave-2-jack-x-protocol-validation`
  - protocol matrices and frozen corpus packages now define the first validation batches explicitly
- First protocol-validation dry runs were executed on `2026-04-01`:
  - `jack` and `jack-x` both returned substantively correct dry-run decisions
  - both still drift on the strict machine output contract (markdown fences and loose field normalization)
  - interpretation: migration is started, but protocol validation is still `in_progress`, not `validated`
- Strict protocol-validation runner is now in place on `2026-04-02`: `/Users/moufdi/hermes-runtime/scripts/run-protocol-validation.mjs` with machine contracts for `jack` and `jack-x`.
- Hermes Batch 1 protocol validation is now real on `2026-04-02`:
  - `jack` Batch 1 passed on strict runs `2/3/4` with stable signature `3a6a7af4088bcc16b05630024c7d4b4411715c8f408785c807be78579762a2d0`
  - `jack-x` Batch 1 passed on strict runs `3/4/5` with stable signature `78899406e6657621b68249c56ba45841540d6d26f285931a04afd7efb2e41734`
  - interpretation: runtime smoke plus first protocol batch are now validated for both agents, but later protocol batches and channel migration remain open
- Hermes Batch 2 protocol validation is now real on `2026-04-02`:
  - `jack` Batch 2 passed on strict runs `1/2/3` with stable signature `0e47aa43c29ffeeccce88db3329c6ec6fee7ac25a361be37512f9a6f3cd93d75`
  - `jack-x` Batch 2 passed on strict runs `1/2/3` with stable signature `bd19030426794e3879eee4704753aee99e4407f19d016a30710ebb7d95c1c2e3`
  - interpretation: both agents now have runtime smoke plus Batch 1 and Batch 2 validated on Hermes; Batch 3, specialist migrations, and channel migration remain open
- Hermes Batch 3 protocol validation is now real on `2026-04-02`:
  - `jack` Batch 3 passed on strict runs `1/2/3` with stable signature `34aef74ed51d65b73ec04c013b83166c7fe813a1f177f5a1afe3141ea5c87af1`
  - `jack-x` Batch 3 passed on strict runs `1/2/3` with stable signature `e38b233418d007f48c482cee0dd4f6faf0e3b3c59a8b3c29a1fd344094bd8ccc`
  - interpretation: Jack and Jack X now cover runtime smoke plus the direct operational protocol surface on Hermes; remaining gaps are Jack governance meta-protocols, the Hermes -> MM bridge implementation, specialist migrations, and channel migration
- Hermes local runtime recheck was replayed on `2026-04-02` after model-policy enforcement:
  - `jack` Batch 3 recheck passed again on strict runs `1/2/3` with the same stable signature `34aef74ed51d65b73ec04c013b83166c7fe813a1f177f5a1afe3141ea5c87af1`
  - `jack-x` Batch 3 recheck passed again on strict runs `1/2/3` with the same stable signature `e38b233418d007f48c482cee0dd4f6faf0e3b3c59a8b3c29a1fd344094bd8ccc`
  - interpretation: `jack` and `jack-x` can be treated as `OK on local Hermes supervised runtime`
  - explicit limit: this is not a claim that the memory graph is cleanly typed/enforced or that MM bridge / production channels are fully ready
- Hermes BRM runtime gates now exist locally on `2026-04-02`:
  - implementation: `/Users/moufdi/openclaw/src/bridges/brm-protocol-enforcement.ts`
  - CLI preflight: `/Users/moufdi/openclaw/scripts/brm-protocol-gate-check.ts`
  - scope: protocol package loading, non-runnable rejection, launch gates, and stage/status/output gates
  - local test result: `7/7` targeted tests passed
  - live wrapper now exists at `/Users/moufdi/hermes-runtime/scripts/brm-hermes-run.sh`
  - `jack` and `jack-x` local wrappers are now wired through this path when BRM protocol flags are present
  - supervised wrapper tests passed locally on `2026-04-02`:
    - `jack` unsupervised runtime output: `JACK_WRAPPER_OK`
    - `jack` supervised runtime output: `JACK_SUPERVISED_OK`
    - `jack-x` supervised runtime output: `JACKX_SUPERVISED_OK`
    - rejection path verified before execution on model/timeout drift
  - interactive shell variance on `jack` was removed on `2026-04-02`: `~/.zshrc` no longer aliases `jack` to the legacy OpenClaw manager; that legacy path is now explicit as `jack_openclaw`
  - important limit: this is not yet runtime-wide for every Hermes profile
  - attempted repo typecheck still fails on pre-existing unrelated errors in `src/cron/isolated-agent/run.ts` and `src/hooks/bundled/telegram-mirror/handler.ts`
- BRM model policy is now clarified and locally enforced on `2026-04-02`:
  - `Kimi` is reserved for extraction and raw-result cleanup only
  - reasoning and protocol-control stages must use `Claude Opus`, `GPT`, or `Gemini`
  - the BRM gate module now rejects `Kimi` outside `pass0_extract`
  - the BRM gate module now rejects non-`Kimi` models inside `pass0_extract`
  - the Jack X package preflight and post-pass0 stages were realigned to this rule
- Hermes brain/shared-graph bridge now exists locally on `2026-04-02`:
  - implementation: `/Users/moufdi/openclaw/scripts/brm-shared-graph.py`
  - contracts: shared graph entry, brain hydration, graph candidate, legacy mapping, shared-graph write policy
  - `jack` and `jack-x` local Hermes brains are now seeded under `/Users/moufdi/.brm-hermes/profiles/*/memories/`
  - bounded hydration and candidate dry-run commit were validated locally
  - the historical shared graph was normalized in place on `2026-04-02` with backup `/Users/moufdi/.openclaw/knowledge-graph/memory.jsonl.backup.20260402-195943`
  - strict validation after normalization is now clean: `72` entries, `0` errors, `0` warnings
  - durable shared-graph commits are now governed locally by a BRM write policy: only `jack` and `jack-x` may commit reviewed graph writes during migration
  - write-policy preflight was replayed on a temporary store: `rosa` commit actor rejected, `jack` commit actor accepted, post-commit strict validation stayed clean
  - explicit limit: this memory layer is locally production-shaped, but not yet fully production-ready until specialist migrations and the Hermes -> MM/runtime bridge use the same governed write path
- Hermes specialist wave bootstrap advanced on `2026-04-02`:
  - `rosa`, `jeff`, `alfred`, and `cortex` now have BRM-specific Hermes profiles, local brains, shared `.env`, and local wrappers (`/Users/moufdi/.local/bin/{rosa,jeff,alfred,cortex}`)
  - direct smoke tests passed for all four profiles on local Hermes
  - `rosa` also passed a BRM-supervised smoke run on `rosa.offer-strategy.direct`
  - Anthropic OAuth on Hermes is still profile-local today; the valid `jack` auth state was propagated to these specialist profiles to avoid repeated manual login during this wave
  - explicit limit: only `rosa` currently has a real Hermes package in this wave; `jeff`, `alfred`, and `cortex` are runtime-wired but not yet protocol-validated
- Hermes Rosa Batch 1 protocol validation is now real on `2026-04-02`:
  - `rosa` passed on strict supervised runs `1/2/3` with stable signature `c04a15a613b855e29d0f8fe708af6e04a9ee78b6460c3def6dbda43d414a47c6`
  - route validated: `rosa.offer-strategy.direct` on protocol node `proposition-offres`
  - interpretation: `rosa` is now the first specialist agent that is protocol-validated on local supervised Hermes runtime
  - explicit limit: this validates the first direct decision route only, not the broader Rosa observation stack or public channels
- Rosa audit-performance-marketing runtime was materially realigned on `2026-04-05`:
  - shared missing dependencies were created locally: `/Users/moufdi/clawd/skills/report-html/scripts/generate.py`, `/Users/moufdi/clawd/skills/report-html/scripts/html_to_pdf.py`, `/Users/moufdi/clawd/skills/hiboo-common/scripts/hiboo.py`, and shared template refs under `/Users/moufdi/.openclaw/kg/protocols/shared/`
  - `rosa.audit-performance-marketing` now runs locally end-to-end on Hermes-managed credentials with live Hiboo + Klaviyo inputs and portable HTML/PDF rendering
  - strict frozen validation root: `/Users/moufdi/hermes-runtime/reviews/rosa-audit-validation-20260405`
  - normalized pass0 signature: `54994184c192c47f1ec0920fa92c52b3e221ce7593ef7fe3efc86c1ada631b66`
  - report HTML signature: `6ec3ecad96359b47f8e35dccf07e1f2fdc6a40d0da53a9e01719ab3d0b5b06b5`
  - interpretation: `rosa.audit-performance-marketing` is now locally runnable and stable
- Rosa market graph and competitive stack were closed for v1 on `2026-04-05`:
  - local reusable skill surface was created under `/Users/moufdi/clawd/skills/competitive-intelligence/`
  - `rosa.veille-concurrentielle` strict frozen validation root: `/Users/moufdi/hermes-runtime/reviews/rosa-veille-concurrentielle-validation-2026-04-05T15-25-00Z`
  - `rosa.veille-concurrentielle` stable signature: `6515ef34adb655c28a00633a2732fd0a59d76d0d41385df815094b17c9e53d7d`
  - `rosa.market-graph-refresh` now validates under the intended split contract: one live `seo.json` capture, then deterministic graph compile from the frozen artifact
  - `rosa.market-graph-refresh` strict compile validation root: `/Users/moufdi/hermes-runtime/reviews/rosa-market-graph-refresh-validation-2026-04-05T18-20-00Z`
  - `rosa.market-graph-refresh` stable signature: `454ecfde1742c2840f1714c7a32bb8081835a9ca4f6c21a4a6c2804c51183fcc`
  - canonical runners now exist for `rosa.audit-performance-marketing` and `rosa.veille-concurrentielle`
- Cross-route sweep replay on `2026-04-06` / `2026-04-07` reconfirmed the current specialist truth:
  - `rosa.audit-performance-marketing` direct dispatch rerun -> `review_ready` with fresh local HTML/PDF artifacts under `/Users/moufdi/.openclaw/workspace-rosa/data/maybe-paris/20260406T233413Z/audit-performance-marketing/`
  - `rosa.market-graph-refresh` mission boundary is enforced: direct dispatch still fails as expected with `mission_only`
  - `rosa.veille-concurrentielle` sequential rerun root `/Users/moufdi/hermes-runtime/reviews/rosa-veille-concurrentielle-validation-2026-04-06T23-38-15Z` restored `3 runs / 0 variance`, stable signature `3be99a80ae519e6185a2cc943d6be7f8e17025dd811cb22d482f37c773c4715f`
  - note: the earlier `stable_signature=false` during the same sweep was a false negative caused by running `market-graph-refresh` validation in parallel while `veille` consumes the shared `market-graph/current` snapshot
- Hermes specialist tooling audit was replayed on `2026-04-02`:
  - `rosa`: wrappers/profile/auth/package/scripts are present, but shared Hermes env still lacks Hiboo, Klaviyo, and Shopify keys for broader Rosa script-first routes
  - `jeff`: wrappers/profile/auth/scripts are present, but shared Hermes env still lacks Hiboo, Apify, and Google credentials, and `jeff-email-digest.py` still points to VPS-only helper paths
  - `alfred`: wrappers/profile/auth/scripts are present, but local `gsc.py` is missing, Google credentials are not wired into shared Hermes env, and phase scripts still embed `/home/ubuntu/...` paths
  - `cortex`: wrappers/profile/auth are present and Gemini env is available in shared Hermes env, but `cortex-phase3.py` is still missing and only Phase 1 should be treated as runnable
- Hermes business credential centralization was executed on `2026-04-02`:
  - new helper: `/Users/moufdi/hermes-runtime/scripts/sync-business-secrets-to-hermes.py`
  - `~/.brm-hermes/.env` now has a managed `BRM BUSINESS SYNC` block in addition to the LLM auth block
  - file-based Google credentials are re-exposed through `~/.brm-hermes/credentials/`
  - resolved into shared Hermes env:
    - Hiboo service key and aliases
    - Shopify `maybe-paris` / `blinx` / `botanic`
    - Klaviyo `maybe-paris` / `blinx` / `nailz`
    - Google Ads auth tuple
    - Google application credentials path
    - BigBlue, Lark, Meta Ads, Mission Manager, MS365 work auth
    - Recharge `botanic`
    - Cloudflare
    - GoDaddy
    - Apify
  - specialist impact after re-audit:
    - `rosa`: audited credential floor is now wired
    - `jeff`: audited credential floor is now wired
    - `alfred`: Google credentials now wired; helper/path parity is still the blocker
    - `cortex`: no credential regression; Gemini and Hiboo base override are present
  - explicit remaining missing source:
    - `MS365_REFRESH_TOKEN_MAE`
- canonical rehome was completed on `2026-04-02` for the business secrets initially recovered from local traces:
  - AWS Secrets Manager secret `brm-api-keys` now also contains:
    - `APIFY_API_TOKEN`
    - `KLAVIYO_API_KEY_MAYBE_PARIS`
    - `KLAVIYO_API_KEY_BLINX`
    - `KLAVIYO_API_KEY_NAILZ`
    - `SHOPIFY_TOKEN_BOTANIC`
    - `RECHARGE_API_TOKEN_BOTANIC`
    - `CLOUDFLARE_API_TOKEN`
    - `GODADDY_API_KEY`
    - `GODADDY_API_SECRET`
  - Hermes business sync recheck after rehome now reports `legacy_fallbacks: {}`

## Production Incident - Subagent Runtime

Status: `open`

Observed on VPS:
- `sessions_spawn` returns `accepted`
- the child transcript is created
- but the child session stays empty: only the `session` line exists

Confirmed examples:
- Jack -> Tony:
  - accepted spawn: `/home/ubuntu/.openclaw/agents/jack/sessions/618db425-ed3f-42ac-a8b3-61e68af6089d.jsonl:167`
  - empty Tony transcript: `/home/ubuntu/.openclaw/agents/tony/sessions/533139fa-52b8-45a5-aebe-d8e90139c86b.jsonl.deleted.2026-03-21T22-44-43.703Z`
- Jack -> Rosa:
  - accepted spawn: `/home/ubuntu/.openclaw/agents/jack/sessions/618db425-ed3f-42ac-a8b3-61e68af6089d.jsonl:201`
  - Jack observes `Lines: 1`: `/home/ubuntu/.openclaw/agents/jack/sessions/618db425-ed3f-42ac-a8b3-61e68af6089d.jsonl:206`
  - empty Rosa transcript: `/home/ubuntu/.openclaw/agents/rosa/sessions/d6f0d23f-5fbe-4a58-86a4-63f7d50a13e4.jsonl.deleted.2026-03-21T22-46-43.910Z`

Interpretation:
- this is not a `Tony missing` issue
- this is not a `Jack cannot spawn` issue
- this is a `runtime subagent launch` issue

## Protocol Status

### Jeff

| Protocol | Status | Notes |
|---|---|---|
| `analyse-profil` | `validated` | script-first, production-usable |
| `performance-report` | `validated` | production-usable |
| `collab-review` | `validated` | production-usable |
| `ajout-collaboration` | `validated` | API-backed, confirmation-gated |
| `collab-management` | `validated` | API-backed, confirmation-gated |
| `outreach-tracker` | `validated` | upsert path validated |
| `email-digest` | `validated` | inbox path good; influencer mapping still heuristic until fuller Hiboo resolution |
| `outreach-pipeline` | `validated with reserve` | prepare + test-send OK; Office365 send path OK; Sent-folder copy still open |
| `roster-expansion` | `validated` | exact-following + Hiboo hydration + report; now supports explicit seed handles for intake-triggered expansion |
| `creation-planning` | `on hold` | now auto-loads the latest roster-expansion signal and separates core budget from test budget, but still not closed as autonomous prod protocol |
| `candidate-intake` | `validated with Hermes dispatch restriction` | OpenClaw protocol remains strong, but Hermes direct Jack dispatch stays `mission_only` until exact-following graph closeout is fully observed |

Jeff now uses the same routing model as Rosa:
- `Phase 1 = observation`
- `Phase 2 = creation`
- `Phase 3 = publication + feedback loop`

Hermes local recheck on `2026-04-03`:
- `jeff-analyse-profil-pass0.py --handle romi_allata --store maybe-paris` -> `ok`
- `jeff-analyse-profil-report.py` on the resulting data/analysis -> `ok`
- `jeff-analyse-profil-report.py --upload-drive` -> `blocked_pending_approval`
- the first package `/Users/moufdi/hermes-runtime/adapters/agents/jeff/packages/jeff.analyse-profil.protocol.yaml` now passes BRM launch + stage gates with its example contexts
- the package `/Users/moufdi/hermes-runtime/adapters/agents/jeff/packages/jeff.performance-report.protocol.yaml` now passes BRM launch + stage gates with its example contexts
- `jeff-candidate-intake.py run --store maybe-paris --handle romi_allata --skip-roster-expansion` -> intake core `ok`, registry sync `ok`, first graph attempt failed on a now-fixed legacy throttle path
- the package `/Users/moufdi/hermes-runtime/adapters/agents/jeff/packages/jeff.candidate-intake.protocol.yaml` now passes BRM launch + stage gates with its example contexts
- the exact-following `graphSync` recheck now enters the real backend polling window on local Hermes and no longer crashes immediately on `/home/ubuntu/...`; full completion still needs a dedicated observed replay before any validation claim
- specialist-dispatch recheck on `2026-04-03`:
  - `brm-specialist-dispatch.ts --mode run --route jeff.analyse-profil ...` -> `ok`
  - `brm-specialist-dispatch.ts --mode run --route jeff.performance-report ...` -> `ok`
  - `brm-specialist-dispatch.ts --mode run --route jeff.candidate-intake ...` was intentionally not promoted: the route was observed entering a real local graph crawl, but no nodes or edges were committed before manual stop, so it remains `mission_only`

Jeff protocol nodes by dominant phase:
- `Phase 1`
  - `analyse-profil`
  - `performance-report`
  - `collab-review`
  - `candidate-intake`
  - `roster-expansion`
  - `email-digest` as inbox observation / signal intake
- `Phase 2`
  - `outreach-pipeline`
  - `creation-planning`
  - `ajout-collaboration`
- `Phase 3`
  - `collab-management`
  - `outreach-tracker`
  - `email-digest` as reply / pipeline follow-up
  - `performance-report` and `collab-review` as post-publication feedback reads

Important rule:
- macro phases are routing views only
- protocols remain the real execution nodes
- some Jeff nodes are transverse, especially `email-digest`, `performance-report`, and `collab-review`

### Rosa

| Protocol | Status | Notes |
|---|---|---|
| `offer-strategy.direct` | `validated direct` | Hermes spawn route with `3 runs / 0 variance` |
| `audit-performance-marketing` | `validated direct` | canonical runner, live pass0, frozen artifact validation |
| `veille-concurrentielle` | `validated direct` | canonical runner, promoted market graph, frozen artifact validation |
| `market-graph-refresh` | `validated mission-oriented` | live discovery is budgeted; graph compile is validated from a frozen live `seo.json` |

### Cortex

| Protocol | Status | Notes |
|---|---|---|
| `ads-observation` | `validated direct` | canonical runner, live dispatch observed, frozen replay `3 runs / 0 variance` |
| `campaign-management` | `design drafted` | Phase 2 creation contract now defined locally and on VPS; target outputs include budget shifts, audience tests, creative briefs, task board, and publication handoff |
| `feedback-loop` | `design drafted` | Phase 3 publication and follow-up contract now defined with alerts, weekly report, task board, and next-cycle input |

### Jack

| Capability | Status | Notes |
|---|---|---|
| direct WhatsApp replies | `alive` | prod WhatsApp path responds |
| subagent orchestration | `KO for trust` | accepted spawn can still lead to empty child sessions |
| protocol supervision | `not trusted for critical missions` | until subagent runtime + final gates are repaired |
| Jack protocol docs | `placeholder-only` | current KG files are intent stubs, not executable production contracts |
| Jack X mission+memory route (local frozen corpus) | `blocked before validation` | observed on `2026-04-01`: `3` blocked local runs, stable blocker signature, model auth failure before useful protocol execution |
| Hermes `jack` smoke route | `validated locally` | observed on `2026-04-01`: `Claude Pro/Max` OAuth login succeeded and `Reply with exactly: JACK_OK` returned `JACK_OK` |
| Hermes `jack-x` smoke route | `validated locally` | observed on `2026-04-01`: refreshed `kimi-coding` env path and `Reply with exactly: JACKX_OK` / `JACKX_ALIAS_OK` both returned successfully |

### Mission Manager

| Capability | Status | Notes |
|---|---|---|
| hosted runtime truth | `identified` | public API routes through `mission-manager-prod-alb` -> ECS `mission-manager-prod-backend` in `eu-west-3`, not the Jack VPS |
| health / projects / missions API | `usable supervised` | hosted API tested on `2026-03-31` |
| mission create / update / read / delete | `validated supervised` | hosted API gates deployed and replayed with `3` stable validation runs on `2026-03-31` |
| live view | `operator-only / not runtime proof` | `/api/live/state` returned a sleeping roster with no live events on `2026-03-31` |
| mission chat surface | `operator relay only` | `thinking`, `sent`, or `relayed` are not proof of successful child execution |
| skill/script secret hygiene | `patched locally` | hardcoded API key exposure removed locally on `2026-03-31` |
| backend mutation gates | `validated on hosted API` | unknown project, missing active fields, duplicate active dedup, and invalid active update now reject on public prod API |

## Infra / Runtime Status

Repo on VPS:
- path: `/home/ubuntu/openclaw`
- branch: `main`
- HEAD: `09041ea53`
- relative to `upstream/main`: `ahead 9`, `behind 2319`

Important interpretation:
- this is a heavily customized production fork
- do **not** do a blind `git pull upstream` in production

Service:
- systemd unit: `/etc/systemd/system/jack-ai-assistant.service`
- repo working dir: `/home/ubuntu/openclaw`
- workspace: `/home/ubuntu/.openclaw`

Operator review package:

- `docs/reviews/jack-mm-operator-2026-03-31/diagnostic.md`
- `docs/reviews/jack-mm-operator-2026-03-31/backlog.md`
- `docs/reviews/jack-mm-operator-2026-03-31/test-summary.md`
- `docs/reviews/jack-mm-operator-2026-03-31/jack-protocol-inventory.md`
- `docs/reviews/jack-mm-operator-2026-03-31/runtime-incident.md`
- `docs/reviews/jack-mm-operator-2026-03-31/mm-public-gates-validation.md`
- `docs/reviews/jack-mm-operator-2026-04-01/jack-x-protocol-check.md`
- `docs/reviews/jack-mm-operator-2026-04-01/jack-x-validation-20260401-122020/observation.md`
- `docs/ops/AUTH_CONSOLIDATION.md`
- `docs/reviews/hermes-agent-fit-2026-04-01.md`
- `docs/reviews/hermes-runtime-migration-plan-2026-04-01.md`
- `docs/reviews/hermes-install-bootstrap-2026-04-01.md`
- `docs/reviews/hermes-profile-smoke-tests-2026-04-01.md`
- `docs/protocols/jack/docs/brm-runtime-contracts.md`
- `docs/reference/brm-harness/README.md`

## Operating Rules From Now On

1. Production truth lives on the real runtime surface, not on the Mac.
   - Jack truth: VPS
   - Mission Manager hosted API truth: ECS/ALB
2. No protocol is considered closed without:
   - a real production run
   - the required artifacts
   - no protocol bypass
3. `Jack -> subagent` is frozen for critical work until the runtime incident is closed.
4. Use direct agent runs for production protocol work when needed.
5. Update this file every time a protocol changes status.

## Workspace Delivery
- The canonical `local workspace -> official Drive -> MM` helper is deployed on `jack-vps`.
- Route pilots now wired to the standard publication flow:
  - `naya.product-sourcing`
  - `jeff.performance-report`
- VPS proofs on `2026-04-13`:
  - `naya.product-sourcing` dry-run -> standard bundle + `manifest.json` + `delivery.json` created under the local deliverables tree
  - `naya.product-sourcing --upload-drive` -> `blocked_pending_approval` with `delivery.json.publication_status = pending_approval`
  - `jeff.performance-report` dry-run -> standard bundle + `manifest.json` + `delivery.json` created under the local deliverables tree
- A real runtime bug was fixed during deployment:
  - `jeff-performance-report.py` could silently continue without a PDF because Chromium snap reported success without leaving a usable file
  - the renderer now verifies the output file and falls back through `wkhtmltopdf`, Chromium, then `WeasyPrint`
- Deployment truth:
  - `deploy-hermes-vps.sh` now syncs the new route files and the shared `workspace_delivery_bridge.py`
- The first MM operator snapshot layer is also deployed on `jack-vps`:
  - canonical script: `/home/ubuntu/clawd/skills/mission-manager/scripts/mm_operator_views.py`
  - outputs: `snapshot.json`, `deliverables.json|md`, `drive.json|md`, `integrations.json|md`
  - VPS proof on `2026-04-13`:
    - `--include-empty` => `58` missions, `9` drive projects, `43` integrations
    - default view => `0` deliverables currently linked in MM mission files
  - current truth:
    - the data layer is closed
    - the operator signal is real: MM still needs actual `mission files` attachment on the live route floor

## Alfred
- Phase 1 is now validated as a single macro-protocol: `visibility-audit`
- Canonical VPS entrypoint: `/home/ubuntu/openclaw/scripts/alfred-phase1.py visibility-audit`
- Validated Phase 1 outputs:
  - `visibility-audit.html`
  - `visibility-audit.pdf`
  - `visibility-audit.report-data.json`
  - `strategy-plan.input.json`
- Phase 2 is now the active workstream: `strategy-plan`
- Phase 2 V1 report now exists on the VPS via `/home/ubuntu/openclaw/scripts/alfred-phase2.py strategy-plan`
- Current Phase 2 status: `end-to-end supervised validation passed on VPS`; report, input gates, and workboard foundation are in place
- Hermes local parity was rechecked on `2026-04-03` with a real replay bundle:
  - `visibility-audit --store maybe_paris --date 2026-03-22 --skip-drive` -> `render_only_ok`
  - `visibility-audit --store maybe_paris --date 2026-03-22` -> `blocked_pending_approval`
  - interpretation: the route is locally connected end-to-end, and final delivery is stopped only by the BRM approval gate
- Strict input gates now exist for Phase 2: `visibility-audit.report-data.json`, `strategy-plan.input.json`, `visibility-audit.result.json`, and `visibility-audit.manifest.json` are all required and hash-checked
- Alfred now emits a first workboard foundation from Phase 2:
  - `execution-board.seed.json`
  - `execution-board.html`
  - `execution-events.jsonl`
- Cosmetic note: radar/spider rendering bug patched on the current V1 rerender
- Legacy Phase 1 folders are archived under `Desktop/protocol-validation-review/Alfred - Revue Protocoles - 2026-03-23/90 - Archive Legacy Phase 1`

- Phase 3 V1 now exists on the VPS via `/home/ubuntu/openclaw/scripts/alfred-phase3.py deployment-feedback-loop`
- Phase 3 currently outputs a first operating report + live execution board + content creation queue + rank tracker seed + feedback schedule
- Phase 3 status: `end-to-end supervised validation passed on VPS`; report, live board, queues, and cadence outputs are in place
- Alfred Phase 2/3 now use a canonical artifact resolver; manifests are resolved only from `reports/<store>/<date>-<protocol>/`, and a fresh supervised Phase 3 rerun confirmed no wrong-path lookup and no date guessing when date is omitted

## Safir
- Audit VPS realise le `2026-03-24`
- Catalogue present : 10 protocoles
- Index Safir en retard : plusieurs protocoles sont encore marques `legacy-markdown` alors que les `.protocol.yaml` existent
- Etat actuel : `partially standardized`
- Gaps principaux restants : `email-workflow` encore bloque, surface legacy encore heterogene sur certains docs/index, `runtime.default_enforcement: shadow` encore present hors de la premiere tranche fermee
- Ordre de standardisation retenu : `email-audit`, `email-performance`, `segment-analysis`, puis creation/production/activation
- `email-audit` : runner canonique VPS en place (`/home/ubuntu/openclaw/scripts/safir-email-audit.py`), package canonique Hermes ajoute sous `hermes-runtime/adapters/agents/safir/packages/`, route live `safir.email-audit` ajoutee au registry, et smoke VPS `render_only_ok` relance le `2026-05-02` sans mutation Lark ; le protocole reste volontairement `OPEN` au sens metier car le contexte Klaviyo live est `unavailable` et le run courant diverge encore du verdict historique Lark (`2-C` vs `2-B`)
- `mail-pole-audit` : macro-protocole Phase 1 cree sur le VPS (`/home/ubuntu/openclaw/scripts/safir-phase1.py`), iteré jusqu'au rapport V4 validé par l'utilisateur, puis validé en `zero variance supervisee` sur le VPS ; package canonique Hermes ajoute, route live `safir.mail-pole-audit` ajoutee au registry, et nouveau smoke VPS `render_only_ok` relance le `2026-05-02`
- `email-workflow` : Phase 2 reste `OPEN / BLOCKED`. Les runs VPS réels existent et les trois lanes texte (`gpt`, `opus`, `gemini`) ainsi que la chaîne image MVP ont été branchés, mais la génération d'email n'est pas jugée fonctionnelle / production-ready. Le système exploite encore mal les templates source, le renderer reconstruit trop de HTML générique, et le module image mélange encore objectif d'asset et objectif d'email. Décision utilisateur : ne pas fermer Safir Phase 2, laisser le sujet ouvert et traiter la génération d'email par un autre moyen pour l'instant.
