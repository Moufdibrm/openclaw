# Agent Governance

Last updated: `2026-05-10`

This folder is the operational governance base for BRM/Hermes agents.

It documents:

- which agents are in V1
- which agents are deferred
- which tools and skills each agent may use
- which environments are canonical
- which external surfaces are read-only, mutable, or approval-gated
- which protocols are usable, partial, or missing
- which proof each agent must leave behind

It is intentionally simple. Runtime wiring, gateway work, Mission Manager implementation, deploy, restart, and VPS release control are out of scope for this folder.

## Files

- `AGENT_GOVERNANCE_MATRIX.md`
  - human-readable matrix and current decisions
- `agent-toolbox-matrix.yaml`
  - machine-readable agent to skills/tools/permission baseline
- `agent-environment-matrix.yaml`
  - machine-readable agent to profile/workdir/surface baseline
- `agent-protocol-matrix.yaml`
  - machine-readable agent to current protocol/route baseline
- `TOOLBOX_CHANGE_PROCEDURE.md`
  - how Jack or another governed agent may add, remove, or modify toolbox access
- `AGENT_TOOLBOX_CONSOLIDATION.md`
  - working list for consolidating agent toolboxes into scripts, skills, docs, and protocols
- `agent-toolbox-consolidation.yaml`
  - lightweight machine-readable consolidation backlog; not a permission register
- `SKILL_ATTACHMENT_POLICY.md`
  - shared attachment/reference-file contract for skills and protocol manifests
- `BRAND_SCOPE_CONTRACT.md`
  - shared brand scope model for `brand_focus` vs `generic` work
- `brand-scope-contract.yaml`
  - machine-readable brand scope contract and validation rules
- `brand-scope-sidecars.yaml`
  - sidecar mapping for legacy brand-linked proof bundles that do not yet emit native `brand_scope`
- `RELEASE_READINESS_MATRIX.md`
  - global agent readiness rollup and next parallel batches
- `release-readiness-matrix.yaml`
  - machine-readable global release/prep rollup; references source matrices instead of duplicating them
- `SUPERVISED_PRODUCTION_VALIDATION_MISSION.md`
  - mission plan to validate V1 agents for supervised production start
- `supervised-production-validation-mission.yaml`
  - machine-readable mission, workstreams, gates, and per-agent targets
- `supervised-production-validation-ledger.yaml`
  - execution ledger template/status for supervised production validation
- `WORKFLOW_IO_TEST_CONTRACTS.md`
  - human-readable input/output/test contract for each governed workflow
- `workflow-io-test-matrix.yaml`
  - machine-readable workflow input/output/post-deploy test expectations
- `WORKFLOW_POST_DEPLOY_TEST_PLAN.md`
  - phased plan for testing workflows after runtime deployment is handled by the integrator lane
- `workflow-runner-input-map.yaml`
  - contract input to runtime runner argument mapping and test mode classification
- `workflow-test-fixtures.yaml`
  - fixture readiness checklist by test wave
- `PHASE0_FIXTURE_INVENTORY.md`
  - audited Phase 0 fixture inventory with real paths, statuses, and blockers
- `ADS_MEDIA_ORCHESTRATION_PLAN.md`
  - human-readable Cortex + Kanye ads/media release-candidate plan
- `ads-media-orchestration-matrix.yaml`
  - machine-readable Cortex + Kanye ads/media orchestration contract
- `ads-media-test-ledger.yaml`
  - execution ledger for the ads/media release candidate
- `ALFRED_ORCHESTRATION_PLAN.md`
  - human-readable Alfred SEO/AEO orchestration plan
- `alfred-orchestration-matrix.yaml`
  - machine-readable Alfred workflow, toolbox, approval, and test contract
- `alfred-test-ledger.yaml`
  - execution ledger for the Alfred SEO/AEO release candidate
- `HIGGSFIELD_CLI_OPERATING_PROCEDURE.md`
  - official Higgsfield CLI procedure, artifact layout, and polling recovery
- `HIGGSFIELD_VALIDATION_REPORT.md`
  - current Higgsfield beta validation evidence and remaining gates
- `MEMORY_LIFECYCLE_BACKLOG_20260508.md`
  - Jack-X, Memory Curator, LLM Wiki, KG, and MM memory lifecycle backlog/status

## Scope

V1 agents:

- `jack`
- `jack-x`
- `mnemos`
- `rosa`
- `jeff`
- `naya`
- `selena`
- `alfred`
- `cortex`
- `tony`
- `kanye`
- `safir`

Later agents:

- `jackette`
- `jhin`
- `walter`

Later agents may keep local profiles, SOUL files, and legacy protocol notes, but they are not V1 governed execution agents until a route/package/toolbox pass promotes them.

## Product Decisions

Agent status is intentionally limited to:

- `draft`
- `beta`
- `prod`

Autonomy is limited to:

- `audit_read`: read, inspect, summarize, and report.
- `discussion_approval`: discuss, plan, draft, and prepare action, but ask before the real external or business mutation.
- `autonomous_e2e_validated_route`: run end-to-end only on an already validated route, with the route's own tool allowlist and proof contract.

Approval is always required for:

- outbound messages to external parties
- customer-visible support replies or dispute messages
- refunds, payment, billing, dispute, or financial mutations
- any action where the target identity or delta is ambiguous

Jack may execute work directly when the route and tool policy allow it.
Specialists remain preferred for deep domain work because they have narrower context, specialized model policy, and trainable protocol history.

Tony owns development work. If the task is code or git, route to Tony by default.
Production deploy, service restart, gateway wiring, and Mission Manager implementation remain separate operator/integrator lanes unless explicitly delegated.

Jack X is the long-term memory agent. It may update memory/KG through governed validation paths, but durable quality cleanup and duplicate reduction need a later refinement layer.

Brand packs should be clean, standard, and easy to complete.
Missing brand surfaces do not block unrelated work on the same brand.
They only block the missing surface until completion data is supplied, discovered, or requested.

External platforms expose skills/toolboxes. Protocols are the repeatable backbone on top of those skills.
Direct tool use is allowed when the agent owns the surface and the action stays inside its autonomy level; repeated direct patterns should become Curator protocol candidates later.

## Current Interpretation

Most V1 agents are `beta` at the agent-governance level because role permissions and skill allowlists are not yet enforced per agent.
Some individual routes are already `prod` or production-usable on their bounded scope.

That distinction is deliberate:

- agent status answers "can I trust this whole agent surface?"
- route status answers "can I trust this exact route?"

## Non-Negotiables

- route before tool
- skill/toolbox before protocol
- protocol before repeatable production execution
- no fake done
- no hidden blocker
- no external mutation without the required approval
- no direct production deploy/restart/release-control work from this governance lane
- no Mission Manager code changes from this governance lane
- no runtime/gateway/deploy file edits from this governance lane
