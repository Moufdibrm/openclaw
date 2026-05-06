# Ads Media Orchestration Plan

Last updated: `2026-05-06`

This plan defines the governed Cortex + Kanye release slice for ads strategy, asset generation, media QA, and campaign dry-run handoff.

It does not authorize live campaign publication, ad spend mutation, paid delivery mutation, external upload, deploy, restart, gateway work, or Mission Manager mutation.

## Production Target

The target is:

- `prod` for read-only ads observation.
- `beta` for Cortex creative brief extraction and Cortex to Kanye asset requests.
- `beta` for Kanye local media generation with manifests and attachment provenance.
- `beta` for Cortex media QA and campaign plan dry-run.
- `approval_gated` for publication, campaign mutation, budget/spend, paid delivery, and public asset distribution.

## Agent Roles

| Agent | Role in this slice | Allowed contribution | Blocked or gated |
|---|---|---|---|
| Jack | Router, approval boundary, governance proof reviewer | Validate route, approval gates, render final decision packet | No hidden publication, spend, deploy, gateway, or MM mutation |
| Cortex | Ads owner | Ads observation, creative brief, media QA, campaign plan dry-run, feedback input | No live campaign mutation, no ad publication, no budget/spend change without approval |
| Kanye | Creative media owner | Generate/edit local image/video assets, product photoshoot, manifests, attachment provenance | No public publication, no paid delivery mutation, no identity/private media use without approval |
| Rosa | Offer and marketing context | Offer mechanics, product positioning, brand constraints, performance context | No direct Higgsfield generation, no campaign mutation |
| Naya | Stock and operational feasibility | Stock/product availability warnings for promoted products | No supplier/order/payment mutation |
| Alfred | Landing and SEO context | Landing page/visibility dependency checks when a campaign needs landing support | No site/theme/publication mutation without route and approval |
| Safir | CRM/email reuse downstream | Convert approved ad assets into email workflow drafts later | No external email send or CRM mutation without approval |
| Tony | Script/dev hardening when delegated | Harden wrappers or test harnesses only when explicitly asked | No deploy/restart/release control in this governance lane |
| Jack-X | Memory and protocol learning | Capture repeated direct patterns as future protocol candidates | No external replies or business mutation |
| Mnemos | Continuity | Keep long-run continuity and context pressure artifacts | No business execution |

## Orchestrated Slices

### T0: Fixture And Evidence Base

Purpose:

- lock the safe inputs and golden outputs already available

Status:

- `available`

Key evidence:

- Cortex ads observation report-data:
  `/Users/moufdi/.openclaw/workspace-cortex/deliverables/maybe-paris/cortex-ads-observation/2026/2026-04-15__ads-observation-maybe-paris__mm-174__run-20260415t162850z/ads-observation.report-data.json`
- Cortex campaign creative briefs:
  `/Users/moufdi/.openclaw/workspace-cortex/reports/campaign-management/2026-04-03T21-04-02Z-maybe-paris/creative-briefs.json`
- Kanye Monoi product source:
  `/Users/moufdi/.openclaw/workspace-kanye/higgsfield-product-photoshoot-validation/20260505T222952Z/monoi_love_detoure.png`

### T1: Cortex Ads Observation

Owner:

- Cortex

Purpose:

- read paid media data and render the campaign state without mutation

Status:

- `prod`

Outputs:

- HTML/PDF report
- report-data JSON
- result JSON
- manifest

Gates:

- upload disabled unless approved
- no campaign mutation

### T2: Cortex Creative Brief Extraction

Owner:

- Cortex

Purpose:

- turn observation and campaign plan data into clear creative asset requests

Status:

- `beta_candidate`

Outputs:

- `creative-briefs.json`
- normalized asset request packet
- constraints for Kanye

Required refinement:

- normalize brief fields for Kanye: `brand`, `campaign_objective`, `offer`, `product_focus`, `audience`, `formats`, `source_assets`, `claims_allowed`, `claims_forbidden`, `proof_target`.

### T3: Cortex To Kanye Asset Request

Owner:

- Cortex creates request
- Kanye accepts and executes
- Jack verifies gates

Purpose:

- make the handoff explicit enough that Kanye does not infer campaign strategy

Status:

- `draft_to_beta`

Required input:

- `asset_request_id`
- `brand`
- `campaign_objective`
- `product_or_offer`
- `target_audience`
- `asset_formats`
- `source_assets`
- `brand_constraints`
- `approval_gates`

Output:

- accepted request packet or rejected request with missing fields

### T4: Kanye Asset Generation

Owner:

- Kanye

Purpose:

- produce local generated media with source provenance and manifest

Status:

- `beta`

Current usable lanes:

- `higgsfield-generate`
- `higgsfield-product-photoshoot`
- `still-generate`
- `reference-edit`

Still gated or draft:

- `higgsfield-marketplace-cards`
- `higgsfield-soul-id`

Required proof:

- source attachment metadata
- prompt or bounded generation request
- tool output
- downloaded media path
- manifest
- no secret values
- no publication

### T5: Cortex Media QA

Owner:

- Cortex

Purpose:

- decide which generated assets fit ad strategy and which should be rejected or iterated

Status:

- `draft_to_beta`

Inputs:

- Kanye media manifest
- generated media paths
- Cortex creative brief
- brand constraints

Outputs:

- asset QA verdict
- recommended use by funnel stage
- reject reasons
- next variation request

Gates:

- QA can approve for internal campaign draft only
- public publication remains approval-gated

### T6: Campaign Plan Dry-Run

Owner:

- Cortex

Purpose:

- generate the campaign plan using approved local assets, without live platform mutation

Status:

- `draft`

Outputs:

- campaign-management report
- ads task board
- creative briefs
- audience test plan
- budget shift plan
- publication feedback input

Gates:

- budget/spend mutation blocked
- campaign/ad publication blocked
- platform write blocked

### T7: Approval Packet

Owner:

- Jack, with Cortex and Kanye evidence

Purpose:

- give Moufdi a clean decision packet before any live mutation

Status:

- `required_before_live`

Packet fields:

- campaign objective
- proposed assets
- media manifests
- QA verdict
- budget/spend delta
- platform targets
- expected mutation
- rollback/readback plan
- explicit approval request

### T8: Live Publication And Spend Mutation

Owner:

- outside this governance lane unless explicitly delegated

Status:

- `blocked_until_approval`

Required before any run:

- explicit Moufdi approval
- resolved platform target
- resolved campaign/ad IDs or creation spec
- post-mutation readback plan

### T9: Feedback Loop

Owner:

- Cortex

Purpose:

- analyze post-publication metrics and produce the next cycle input

Status:

- `future_after_live_publication`

Input:

- post-publication metrics
- approved media manifest
- campaign readback

Output:

- feedback report
- next-cycle creative and budget recommendations

## Parallel Launch Plan

Lane A: Cortex strategy and QA

- extract usable creative briefs from existing campaign-management fixture
- define normalized asset request packet
- prepare media QA rubric

Lane B: Kanye asset generation

- keep Monoi Love product photoshoot assets as current beta evidence
- test marketplace cards next, with no publication
- document failed or caveated model behavior instead of hiding it

Lane C: Governance and approval

- keep publication/spend gates explicit
- record all proof paths in the ads-media ledger
- prepare approval packet template

Lane D: Dependent agents

- Rosa supplies offer context when campaign objective is ambiguous
- Naya supplies stock feasibility when a product is promoted
- Alfred supplies landing dependency checks
- Safir consumes approved assets later for email workflow
- Tony hardens wrappers only when delegated

## Production-Ready Definition

This slice is production-ready when:

1. Cortex can produce or replay ads observation with no mutation.
2. Cortex can produce a normalized creative asset request.
3. Kanye can produce media from the request with manifest and attachment provenance.
4. Cortex can QA the media and return campaign fit/reject/iterate decisions.
5. Cortex can produce a campaign dry-run packet with publication blocked.
6. Jack can assemble an approval packet that clearly names live mutation targets.
7. All YAML parses, local paths exist, and no secrets are recorded.

Until T7 is approved, the production claim is:

`prod for read/draft/local asset generation; blocked for publication and spend`.

## RC1 Result

Run:

- `/Users/moufdi/.openclaw/workspace-cortex/ads-media-orchestration/20260506T012139Z/manifest.json`

Produced:

- Cortex to Kanye asset request
- Cortex media QA report
- Cortex campaign dry-run
- Jack approval packet draft
- Kanye marketplace-cards enhance-only validation

Current result:

- `passed_dry_run_no_mutation`
- publication/spend remains blocked
- marketplace-cards is partially validated only, because no marketplace media was generated
- human visual approval remains required before any live ad upload
