# Platform Governance Standard

Last updated: `2026-05-07`

Scope: operational governance for external platforms, internal control surfaces, model providers, channels, and delivery surfaces used by BRM/Hermes agents.

This is not runtime wiring. It does not authorize gateway edits, Mission Manager implementation, deploy, restart, systemd work, credential changes, or external mutations.

## Why This Exists

Agents need reusable platform knowledge without turning every installed skill into permission.

The platform layer answers:

- what platform or surface exists
- which agent owns it
- which agents may read it
- which agents may write or mutate it
- whether it is brand-scoped, account-scoped, channel-scoped, repo-scoped, or global
- which approval gates apply
- which proof is required
- when direct tool use is acceptable
- when a route/protocol is mandatory

## Source Hierarchy

Use this order when platform information conflicts:

1. Live route/package contract
2. Platform registry in `platform-registry.yaml`
3. Brand pack and brand registry
4. Agent toolbox/environment/protocol matrices
5. Governance docs and status notes
6. Historical summaries

If a platform is missing from the registry, the agent must classify it as `unclear` and open a platform addition request before relying on it for production work.

## Platform Vs Skill Vs Protocol

Keep these concepts separate:

| Layer | Meaning | Example |
| --- | --- | --- |
| Platform | External/internal system or surface | Shopify, Klaviyo, PayPal, KG, Mission Manager |
| Skill/toolbox | How an agent operates a platform | Shopify product read helper, Higgsfield CLI skill |
| Protocol/route | Repeatable business workflow | `naya.stock-check`, `selena.paypal-dispute.phase1-live` |
| Permission | Whether an agent may use a skill/toolbox on a platform | Selena can read PayPal; refunds stay approval-gated |
| Proof | Artifact proving what happened | report bundle, manifest, readback JSON, validation summary |

Installed skills are not permissions.

## Global Platform Rules

Jack:

- has transversal read/supervision access to every governed platform registry entry
- may inspect evidence, route ownership, allowed toolboxes, gaps, and protocol candidates
- may coordinate specialist handoffs
- may perform direct bounded execution only when governed and requested
- does not get blanket mutation rights

Specialists:

- own execution inside their domain
- should not use unrelated platforms for convenience
- should convert repeated direct tool use into protocol candidates

Writes:

- must name the target platform, tenant/account/store/channel, route, delta, and proof
- must pass global approval gates when customer-visible, financial, paid, supplier-facing, external-send, publication, or ambiguous
- must be backed by pre/post readback when the platform supports it

Reads:

- may be direct only when the agent owns the surface, the target is unambiguous, and the read is logged in the final summary or artifact
- repeated reads with the same input/output shape should become a script or protocol candidate

## Platform Status

Use only:

- `draft`: documented idea or partial surface, not production reliable
- `beta`: usable for bounded supervised work with proof and known caveats
- `prod`: production-usable inside the named route/scope
- `partial`: centrally wired or observed, but not closed enough for broad use
- `legacy`: known old surface; do not expand without explicit decision
- `deferred`: intentionally out of V1
- `unclear`: evidence is insufficient

## Exhaustive Current Platform Inventory

This inventory comes from the route registry, protocol packages, governance docs, status notes, and brand packs.

### Commerce, Storefront, Subscription

| Platform | Status | Owners | Scope | Current use | Write policy |
| --- | --- | --- | --- | --- | --- |
| Shopify | `partial` with first commerce slice closed | Rosa, Naya, Tony for code/theme implementation | brand/store/tenant | products, orders, inventory, theme, storefront verification, analytics hints | publication/storefront/product/theme mutation requires route and approval |
| Recharge | `partial` | Naya/Rosa depending task; Jack supervises | brand/account, currently Botanic evidence | subscription checks in brand pack | subscription/payment mutation requires explicit approval |

### CRM, Email, Mailbox

| Platform | Status | Owners | Scope | Current use | Write policy |
| --- | --- | --- | --- | --- | --- |
| Klaviyo | `partial` | Safir for email/CRM; Rosa for marketing reads | brand/account | flow checks, email audit/design, CRM context | send, flow activation, segment mutation, CRM mutation require approval |
| MS365 mail | `beta`/usable for bounded intake | Jack-X for memory intake; Safir for mail/email context | mailbox/account | inbox + sent intake, digest, email audit context | outbound email send requires approval |

### Support, Payment, Customer Risk

| Platform | Status | Owners | Scope | Current use | Write policy |
| --- | --- | --- | --- | --- | --- |
| Zendesk | `prod` for bounded read/audit routes | Selena | brand/account/ticket | ticket fetch, reviewed export, feedback review | reply, tag/status/customer-visible update requires approval |
| PayPal | `prod` for bounded read/audit routes | Selena | brand/account/dispute | dispute fetch, reviewed export, dispute audit | dispute message, refund, payment, billing mutation requires approval |

### Supply Chain, Product Ops

| Platform | Status | Owners | Scope | Current use | Write policy |
| --- | --- | --- | --- | --- | --- |
| BigBlue | `beta`/bounded live validation floor | Naya | brand/logistics account | inventory, product, order, telemetry reads | order, shipment, fulfillment mutation requires approval |
| Hiboo core | `beta` | Naya, Jeff, Rosa | account/store/brand | product, production, governance, creator/profile signals | data mutation/collaboration change requires approval |
| Sourcing sheets | `draft`/artifact-fed | Naya | sheet/file/brand | reviewed sourcing inputs and supplier question packs | supplier message/order/purchase mutation requires approval |

### Paid Media, Ads, Creative Performance

| Platform | Status | Owners | Scope | Current use | Write policy |
| --- | --- | --- | --- | --- | --- |
| Meta Ads | `partial` | Cortex | brand/ad account | ad account mapping, paid media observation | campaign/ad publication or budget mutation requires approval |
| Google Ads | `partial` | Cortex | brand/ad account | paid media observation and account mapping | campaign/ad publication or budget mutation requires approval |
| Hiboo ads/creatives | `beta` on current routes, partial outside them | Cortex, Rosa, Kanye handoff | brand/account | ads observation, creative performance, media handoff | campaign mutation/publication requires approval |

### Analytics, Search, Visibility

| Platform | Status | Owners | Scope | Current use | Write policy |
| --- | --- | --- | --- | --- | --- |
| GA4 | `partial` | Rosa, Alfred | brand/property | analytics context and performance reporting | analytics config mutation requires approval |
| Google Search Console | `prod` for current Alfred read route | Alfred, Rosa read support | domain/property | search visibility and SEO/AEO audit | property/site mutation is not an Alfred default right |
| DataForSEO | `prod`/bounded validation floor | Alfred, Rosa | query/domain/brand | SERP, keyword, visibility data | read-only unless a new write-capable product is explicitly added |
| Public site rendering/browser verification | `beta` | Alfred, Tony, Jack | URL/domain/repo | rendered evidence, storefront/site QA | no site mutation; code/theme changes go through Tony/approved route |

### Creator, Social, Web Data

| Platform | Status | Owners | Scope | Current use | Write policy |
| --- | --- | --- | --- | --- | --- |
| Instagram public/profile signals | `beta` through governed creator workflows | Jeff | handle/profile/brand | creator profile analysis and candidate intake | contact/send/collab mutation requires approval |
| Instagram Graph auth | `partial` | Jeff/Cortex depending surface | app/account | standardized auth mention exists; operational scope remains bounded | account or publishing mutation requires approval |
| Apify | `partial`/centrally wired | Jeff | actor/task/dataset | creator/social/web extraction support | actor writes or account-costly runs require route proof |

### Channels, Collaboration, Delivery

| Platform | Status | Owners | Scope | Current use | Write policy |
| --- | --- | --- | --- | --- | --- |
| WhatsApp | `beta`/prod operator path for Jack, partial group volume | Jack for operator channel; Jack-X for bounded intake | profile/channel/session | operator ingress, specialist routing, memory snapshot | outbound message/fan-out requires approval unless existing governed operator reply path allows it |
| Lark messages | `beta`/usable first slices | Jack-X, Rosa/Safir/Naya read depending route | chat/channel/brand | channel intake, team discussion, email/ops context | posting or table mutation requires approval unless route explicitly allows |
| Lark tables | `beta` for Maybe slice, draft elsewhere | Jack-X, Rosa/Safir/Naya depending table | table/app/brand | operations calendar, structured intake | table write/update requires approval or owned route |
| Google Drive | `partial`, approval-gated by design | Jeff, Alfred, Cortex, Jack supervision | folder/file/delivery target | report delivery attempts and approval-blocked proof | upload/share/delivery requires approval |
| Telegram | `deferred`/legacy | none in V1 | channel | legacy OpenClaw channel only | no V1 use |

### Creative, Media, Voice

| Platform | Status | Owners | Scope | Current use | Write policy |
| --- | --- | --- | --- | --- | --- |
| Higgsfield | `beta` for still/product tests; voice planned gated | Kanye owner; Jack supervision/direct exception | profile/API/job/media | still generation, reference edit, product photoshoot, marketplace cards draft, Soul ID gated, future voice identities | publication/delivery/voice clone requires approval and proof |
| Seedance | `draft`/mentioned motion route | Kanye | generation job/media | motion route concept | no prod use until validated |
| OpenAI | `beta`/central provider; `whisper-1` is voice input standard | Tony/Jack/general; Safir/Kanye where routed | model/provider/task | GPT/Codex, Whisper STT, image/design experiments | external sending remains platform-specific gate |
| Anthropic Claude | `beta`/central provider | Jack/specialists by route | model/provider/task | reasoning/control stages where allowed | no platform mutation by model choice alone |
| Google Gemini | `beta`/validated on Cortex and Memory Wiki semantic layer | Cortex, Jack-X/LLM Wiki, Safir experiments | model/provider/task | ads observation, semantic memory, email/design experiments | no platform mutation by model choice alone |
| Kimi | `beta` for extraction/cleanup | Tony sidecar and pass0 extract paths | model/provider/task | exploration/extraction only where route allows | should not own reasoning/control stages unless route changes |
| Z.AI / GLM | `beta` runtime base fallback/provider | Jack/runtime-owned | model/provider/task | base conversation/fallback and Hippocampus refiner path | runtime-owned, not governance mutation |
| ElevenLabs | `legacy` | none as target owner | voice provider | Jack legacy TTS block exists | do not promote; Higgsfield is target output voice |

### Internal Control, Memory, Governance

| Platform | Status | Owners | Scope | Current use | Write policy |
| --- | --- | --- | --- | --- | --- |
| Mission Manager | `beta`/usable operator visibility surface | Jack supervision; integrator owns implementation | mission/task/run | workflow ledger, operator status, costs, lineage, delivery gates | implementation/mutation outside governance lane; status updates only through governed runtime paths |
| Hermes runtime | `prod`/runtime-owned | integrator | profile/runtime/VPS | channel runtime, profiles, route execution | no governance edits to gateway/deploy/systemd/runtime prod |
| Specialist route registry | `prod` as route truth | Jack/governance, integrator for runtime wiring | registry route | route ownership and live route list | governance may document; runtime registry edits only if explicitly in scope and safe |
| Protocol packages | `prod`/`beta` by route | specialist owner plus Jack | package/stage/tool allowlist | route stage/tool/proof contracts | package changes need validation; runtime-owned execution remains separate |
| Brand registry and brand packs | `beta` source of brand scope | Jack/governance; brand owners by domain | brand/store/account/channel | brand IDs, account mappings, partial surfaces | additions must follow brand scope contract; no credential values |
| KG | `beta`, production not fully closed for live Jack-X commit | Jack-X owner, Jack/operator gate | durable memory graph | candidates, review, governed memory updates | durable write only after validation/review gates |
| LLM Wiki / Memory Wiki | `beta` advisory consolidation | LLM Wiki layer proposes; Jack-X reviews | pages/manifests/kg_operations | slow consolidation, aliases, relationships, review items | no direct KG mutation |
| Mnemos continuity journal | `beta` | Mnemos | local session/profile | context pressure, handoff capsules, continuity journal | local continuity artifacts only |
| Hippocampus packet | `partial`/runtime-owned | Jack/runtime | session/context | pre-routing enrichment and injected context | no governance runtime wiring |

### Development, Repo, Verification

| Platform | Status | Owners | Scope | Current use | Write policy |
| --- | --- | --- | --- | --- | --- |
| Local repositories/filesystem | `prod` for Tony/governance work | Tony for code; governance for docs | repo/path | code, docs, artifacts, tests | respect forbidden paths and user changes |
| Git/GitHub | `beta`/when requested | Tony | repo/branch/PR | commits, pushes, PRs, review/CI | push/PR only when requested; deploy/release remains separate |
| Package registries | `partial`/when needed | Tony/Kanye depending task | package ecosystem | dependency install, `npx skills add`, package manager tasks | adding executable deps requires scoped reason and verification |
| Browser/site verification | `beta` | Tony/Alfred/Jack | URL/local target | screenshots, render checks, storefront QA | no external mutation by browser action unless approved |

### Infra, Secrets, Edge, Domains

| Platform | Status | Owners | Scope | Current use | Write policy |
| --- | --- | --- | --- | --- | --- |
| AWS | `prod` for Mission Manager/secret infrastructure, runtime-owned | integrator; governance read-only when needed | account/region/service | ECS/ALB, Secrets Manager, business secret source, hosted MM | infra changes, deploy, secret writes require explicit request |
| AWS Secrets Manager | `prod` as secret source | integrator; governance metadata read only when needed | account/secret | `brm-api-keys`, key presence, business secret source | value read, value print, write, rotation require explicit request |
| Cloudflare | `partial`/centrally wired | integrator/Tony when delegated | zone/domain | edge/DNS readiness | DNS/edge mutation requires explicit approval |
| GoDaddy | `partial`/centrally wired | integrator/Tony when delegated | domain/account | registrar/domain readiness | domain/DNS mutation requires explicit approval |

## Not Currently Governed In V1

These names are either available in the wider local tool ecosystem or commonly adjacent, but current V1 governance docs do not prove active BRM platform ownership:

| Name | Current decision |
| --- | --- |
| Stripe | not evidenced as active V1 BRM platform; add through payment/billing onboarding before any use |
| Slack | no current V1 evidence |
| Notion | no current V1 evidence |
| TikTok Ads | no current V1 evidence |
| Pinterest Ads | no current V1 evidence |
| Amazon marketplace/ads | no current V1 evidence |
| Carrier APIs beyond BigBlue | no current V1 evidence |

Do not infer permission from local tools being available.

## Standard For Adding A Platform

Every new platform must be added as `draft` first.

Required steps:

1. Create a `platform_id`.
   - Format: lowercase kebab-case.
   - Examples: `shopify`, `meta-ads`, `memory-wiki`, `instagram-graph`.
2. Classify the platform.
   - Use one category: commerce, crm_email, support, payment, logistics, supply_chain, paid_media, analytics, visibility, creator_social, channel, collaboration, delivery, creative_ai, model_provider, internal_control, memory, development, infra, edge_domain, secrets.
3. Declare scope.
   - One or more of: global, brand_scoped, account_scoped, tenant_scoped, channel_scoped, repo_scoped, file_scoped, profile_scoped.
4. Declare owner agents.
   - One primary owner.
   - Optional secondary owners.
   - Jack is always `supervisor`, not automatic mutation owner.
5. Split surfaces.
   - `read_surfaces`
   - `write_surfaces`
   - `forbidden_surfaces`
   - `approval_gated_surfaces`
6. Declare brand-pack impact.
   - If brand-linked, add only metadata fields in brand packs.
   - Never store secret values in brand packs.
   - Missing brand fields are partial data, not global blockers.
7. Declare auth policy.
   - Record secret source and required env key names if needed.
   - Never write real secret values in docs, commits, logs, or manifests.
8. Declare skills/toolboxes.
   - Skill package or CLI name.
   - Install location/profile if relevant.
   - Owning agent.
   - Allowed agents.
   - Direct tool use policy.
9. Declare route/protocol policy.
   - Reads may start direct if low risk, owned, logged, and bounded.
   - Writes require an existing validated route or a draft route plus approval.
   - Repeated direct usage becomes `protocol_candidate`.
10. Declare proof targets.
   - Minimum: input summary, target account/brand, command/tool reference, artifact path, result status, no-mutation or mutation readback.
11. Update matrices.
   - `platform-registry.yaml`
   - `agent-toolbox-matrix.yaml`
   - `agent-environment-matrix.yaml`
   - `agent-protocol-matrix.yaml` when a route exists
   - brand pack fields when brand-scoped
12. Validate.
   - YAML/JSON parse OK.
   - Referenced docs/paths exist or are marked `planned`.
   - No secret values.
   - No forbidden runtime/gateway/deploy/MM file changes.
   - Read/write split is explicit.
   - Approval gates are explicit.
   - Jack access is supervisor/transversal, not blanket mutation.

## Promotion Gates

`draft -> beta` requires:

- registry entry complete
- owner agent assigned
- read/write split clear
- auth presence check done without secret leakage
- first bounded read or fixture test
- proof target documented
- direct use limitations documented

`beta -> prod` requires:

- repeated successful bounded runs
- route/protocol package exists for repeated workflow
- pre/post readback or deterministic no-mutation proof
- failure/retry behavior documented
- approval gate tested for blocked mutation where relevant
- brand scoping verified for at least one real brand when brand-linked
- curator feedback path defined for repeated deviations

## Platform Addition Request Template

```yaml
platform_id: ""
display_name: ""
category: ""
status: draft
scope_model: []
primary_owner_agent: ""
secondary_owner_agents: []
supervisor_agent: jack
brand_scoped: false
brand_pack_fields: []
read_surfaces: []
write_surfaces: []
approval_gated_surfaces: []
forbidden_surfaces: []
auth:
  required: true
  secret_source: ""
  env_keys: []
  secret_values_in_docs_allowed: false
skills_or_toolboxes: []
direct_tool_use_policy:
  read: "allowed_only_if_owned_bounded_logged"
  write: "route_or_explicit_approval_required"
protocol_policy:
  required_for_repeated_use: true
  required_for_external_mutation: true
proof_targets: []
test_plan:
  fixture_test: ""
  live_read_test: ""
  mutation_gate_test: ""
open_questions: []
```
