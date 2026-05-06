# Alfred SEO/AEO Orchestration Plan

Last updated: `2026-05-06`

This plan governs Alfred's visibility, SEO strategy, AEO/GEO readiness, and post-implementation feedback loop. It is a governance and test artifact only: no site/theme mutation, Drive upload, publication, deployment, gateway change, or Mission Manager mutation is authorized here.

## Current State

Alfred has one production-ready route and two downstream beta routes:

| Route | Status | Current proof | Gate |
| --- | --- | --- | --- |
| `alfred.visibility-audit` | prod | Reviewed HTML/PDF/JSON bundle exists for Maybe Paris | can run/render without external mutation |
| `alfred.strategy-plan` | beta / blocked locally | Runner exists, strict Phase 1 input gates exist | blocked by store identifier mismatch between Phase 1 manifest/result and report data |
| `alfred.deployment-feedback-loop` | beta / blocked | Runner exists and requires Phase 2 manifest, board seed, events, and handoff | blocked until Phase 2 produces valid artifacts |

Known Phase 1 source bundle:

| Artifact | Path | SHA-256 |
| --- | --- | --- |
| reviewed report data | `/Users/moufdi/.openclaw/workspace-alfred/reports/maybe_paris/2026-03-22-visibility-audit/visibility-audit.report-data.reviewed.json` | `b73d7cbfc1f6cf8d0100b61355fa2ac003eb091d0c0a269e247324933507a4f4` |
| strategy input | `/Users/moufdi/.openclaw/workspace-alfred/reports/maybe_paris/2026-03-22-visibility-audit/strategy-plan.input.json` | `0a402c46ec1d46b775d39c0455f0d2e2a33e303db5b116e9ce40395630f9d733` |
| visibility manifest | `/Users/moufdi/.openclaw/workspace-alfred/reports/maybe_paris/2026-03-22-visibility-audit/visibility-audit.manifest.json` | `892500cffad7fe496c52e4ecb2b2606925c696114cb93a64aae1d90feadca43b` |

## Agent Roles

| Agent | Role in Alfred lane | May do | Must not do |
| --- | --- | --- | --- |
| Alfred | owner for visibility audit, SEO/AEO strategy, measurement loop | read GSC/DataForSEO/GA4/site artifacts, render reports, build SEO/AEO workboard | mutate Shopify/theme/site, publish pages, upload Drive without approval |
| Tony | implementation owner for code, theme, repository, git | implement approved site/theme/schema/robots/llms changes | deploy/restart unless explicitly delegated outside this lane |
| Rosa | marketing/offer context | provide offer priorities, brand and campaign context | publish marketing changes without approval |
| Cortex | ads dependency | consume landing/SEO readiness before paid-media pushes | mutate Alfred SEO artifacts |
| Kanye | asset dependency | provide media only when landing/content needs visual assets | publish media or alter site |
| Jack | supervisor/approval router | approve or route validated actions | bypass approval gates |

## Tool Policy

Alfred's minimal toolbox:

| Toolbox | Mode | Notes |
| --- | --- | --- |
| `gsc-read` | read | Search Console reads and reviewed exports only |
| `dataforseo-read` | read | SERP/keyword/backlink observations |
| `ga4-read` | read | analytics context where wired |
| `site-audit-read` | read | rendered page checks, robots/sitemap/schema reads |
| `canonical-alfred-runners` | local write | write only report artifacts under Alfred workspace |
| `seo-strategy-reporting` | local write | strategy HTML/PDF/JSON, workboard seed, feedback inputs |

Approval-gated or forbidden without explicit approval:

| Surface | Policy |
| --- | --- |
| Shopify pages/products/blog/theme | approval required, Tony implementation owner |
| `robots.txt`, `llms.txt`, schema JSON-LD | approval required, Tony implementation owner |
| Drive upload/delivery | approval required |
| PR/outreach/external publication | approval required |
| paid traffic/campaign changes | outside Alfred, Cortex-owned and approval-gated |

## Workflow Inputs And Outputs

### `alfred.visibility-audit`

Inputs:

- `store`
- `domain`
- `date` or reviewed report-data path
- `skip_drive=true` by default in governance tests

Outputs:

- `visibility-audit.html`
- `visibility-audit.pdf`
- `visibility-audit.report-data.json`
- `strategy-plan.input.json`
- `visibility-audit.manifest.json`
- `visibility-audit.result.json`

Proof expected:

- manifest contains report and strategy-input hashes
- result status is `render_only_ok`, `rendered`, or approval-blocked if Drive was attempted
- no site or Drive mutation unless approved

### `alfred.strategy-plan`

Inputs:

- valid Phase 1 source bundle
- matching store identifier across `visibility-audit.report-data.json`, `strategy-plan.input.json`, `visibility-audit.result.json`, and `visibility-audit.manifest.json`
- `skip_drive=true` for beta tests

Outputs:

- `strategy-plan.html`
- `strategy-plan.pdf`
- `strategy-plan.report-data.json`
- `deployment-feedback-loop.input.json`
- `execution-board.seed.json`
- `execution-board.html`
- `execution-events.jsonl`
- `strategy-plan.manifest.json`
- `strategy-plan.result.json`

Current local test result:

- command: `python3 /Users/moufdi/openclaw/scripts/alfred-phase2.py strategy-plan --store maybe_paris --domain maybe-paris.co --date 2026-03-22 --skip-drive`
- status: `blocked_invalid_inputs`
- reason: `Phase 1 manifest store mismatch.`
- result: `/Users/moufdi/.openclaw/workspace-alfred/reports/maybe_paris/2026-03-22-strategy-plan/strategy-plan.result.json`

Interpretation:

- `maybe-paris` is the canonical `brand_pack_id` from the brand pack.
- `maybe_paris` is Alfred's runner/filesystem `runtime_store_key`.
- The block is not a missing brand. The route currently compares identifiers from different roles as one strict `store` field.

### `alfred.deployment-feedback-loop`

Inputs:

- successful Phase 2 bundle
- `deployment-feedback-loop.input.json`
- `execution-board.seed.json`
- `execution-events.jsonl`
- strategy manifest and result
- implementation/progress evidence after approved Tony/Rosa work

Outputs:

- `deployment-feedback-loop.html`
- `deployment-feedback-loop.pdf`
- `deployment-feedback-loop.report-data.json`
- activated execution board
- measurement schedule
- rank/content feedback queues
- manifest and result

Current status:

- blocked until `alfred.strategy-plan` produces a valid manifest and board seed
- live site mutation remains out of scope for this governance lane

## Orchestration Slices

| Slice | Owner | Status | Output |
| --- | --- | --- | --- |
| A0 baseline fixture and hashes | Alfred | passed | source bundle located and hashed |
| A1 Phase 1 visibility evidence | Alfred | passed | prod visibility report exists |
| A2 Phase 2 runner gate | Alfred | blocked | store mismatch proof captured |
| A3 SEO/AEO workboard design | Alfred + Rosa | ready | strategy tasks from `strategy-plan.input.json` |
| A4 implementation handoff | Tony | blocked | requires approved task list and exact target files/surfaces |
| A5 publication/delivery | Jack approval | blocked | requires approval before site/Drive/external mutation |
| A6 feedback loop | Alfred | blocked | requires successful Phase 2 plus implementation evidence |

## Current Priority Backlog

From the reviewed Maybe Paris visibility audit:

| Priority | Work | Gate |
| --- | --- | --- |
| P0 | create `Cheveux Bouclés & Boucles` cluster page | content publication approval |
| P0 | create `Masques Capillaires` cluster page | content publication approval |
| P0 | create `Lissage & Défrisage` cluster page | content publication approval |
| P0 | create `Botox Capillaire` cluster page | content publication approval |
| P0 | create `Kératine & Traitements` cluster page | content publication approval |
| P0 | create `Routine & Soins Généraux` cluster page | content publication approval |
| P0 | unblock AI crawlers in `robots.txt` | Tony + approval |
| P0 | create `llms.txt` | Tony + approval |
| P0 | add Organization schema on homepage | Tony + approval |
| P1 | fix missing H1s | Tony + approval |
| P1 | add FAQ schema and RAFT structure | Tony/Rosa + approval |

## Gaps

1. Brand scope fields are not separated yet: `maybe-paris` appears as canonical brand pack id, while `maybe_paris` appears as Alfred runner/filesystem key.
2. Phase 2 cannot be considered beta-pass locally until that mismatch is fixed by accepting `brand_scope` or deterministic alias normalization.
3. Phase 3 has no valid local input bundle yet because Phase 2 is blocked.
4. The SEO implementation owner must remain Tony for site/theme/files; Alfred only owns analysis, plan, measurement and report artifacts.
5. The Drive delivery behavior is still approval-gated and should stay disabled for governance tests.

## Next Decision

The next practical step is to normalize Alfred's route contract around `brand_scope`: canonical `brand_pack_id=maybe-paris`, runner `runtime_store_key=maybe_paris`, and explicit `focus_mode` / `subject_id`.
