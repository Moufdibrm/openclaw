# Higgsfield Validation Report

Last updated: `2026-05-06`

Scope: official `higgsfield-ai/skills` package installed for Jack and Kanye.

## Current Result

Status: `beta`

The official Higgsfield CLI is installed and authenticated locally.
The existing Hermes HF API pair is configured through the profile env loader.
A bounded still-image generation test passed and produced a local deliverable plus manifest.
A bounded product photoshoot test also passed using the Monoi Love cutout as a local attachment.
Additional Monoi Love QA variants produced non-white hero, conceptual, and recovered lifestyle media.
The local Kanye product-photoshoot helper was validated end-to-end and wrote a manifest plus downloaded media.

No runtime deploy, service restart, gateway edit, Mission Manager edit, or reserved Jack file edit was performed.

## Validation Evidence

| Evidence | Path |
| --- | --- |
| Manifest | `/Users/moufdi/.openclaw/workspace-kanye/higgsfield-validation/20260505T214148Z/manifest.json` |
| Prompt | `/Users/moufdi/.openclaw/workspace-kanye/higgsfield-validation/20260505T214148Z/prompt.txt` |
| Job JSON | `/Users/moufdi/.openclaw/workspace-kanye/higgsfield-validation/20260505T214148Z/higgsfield-job.json` |
| Local media | `/Users/moufdi/.brm-hermes/profiles/kanye/generated_media/higgsfield-cli-validation/20260505T214148Z_higgsfield_cli_gpt_image_2.png` |
| Product photoshoot manifest | `/Users/moufdi/.openclaw/workspace-kanye/higgsfield-product-photoshoot-validation/20260505T222952Z/manifest.json` |
| Product source attachment | `/Users/moufdi/.openclaw/workspace-kanye/higgsfield-product-photoshoot-validation/20260505T222952Z/monoi_love_detoure.png` |
| Product generated media | `/Users/moufdi/.brm-hermes/profiles/kanye/generated_media/higgsfield-product-photoshoot-validation/20260505T222952Z_monoi_love_product_shot.png` |
| Product photoshoot QA manifest | `/Users/moufdi/.openclaw/workspace-kanye/higgsfield-product-photoshoot-qa/20260505T230630Z/manifest.json` |
| Product QA hero media | `/Users/moufdi/.brm-hermes/profiles/kanye/generated_media/higgsfield-product-photoshoot-qa/20260505T230630Z_monoi_love_hero_safe.png` |
| Product QA conceptual media | `/Users/moufdi/.brm-hermes/profiles/kanye/generated_media/higgsfield-product-photoshoot-qa/20260505T230630Z_monoi_love_conceptual_safe.png` |
| Product QA lifestyle media | `/Users/moufdi/.brm-hermes/profiles/kanye/generated_media/higgsfield-product-photoshoot-qa/20260505T230630Z_monoi_love_lifestyle_safe.png` |
| Product helper validation manifest | `/Users/moufdi/.openclaw/workspace-kanye/higgsfield-product-photoshoot-runs/20260505T232850Z/manifest.json` |
| Product helper validation media | `/Users/moufdi/.brm-hermes/profiles/kanye/generated_media/higgsfield-product-photoshoot-runs/20260505T232850Z_monoi_love_helper_validation_product_shot_1.png` |

Observed manifest fields:

- agent: `kanye`
- skill package: `higgsfield-ai/skills`
- skill: `higgsfield-generate`
- route: `official_higgsfield_cli`
- provider: `higgsfield`
- model: `gpt_image_2`
- display model: `GPT Image 2`
- dimensions: `1024x1024`
- status: `passed_with_polling_502_recovered_by_get`

## Test Incident

The command path generated a successful job, but `generate create --wait` returned an HTTP `502` during polling.
Recovery through `higgsfield generate get <job_id>` succeeded and the media was downloaded.

Implication:

- the skill can be used in beta
- prod promotion must wait until polling recovery is standardized
- retries must first check whether the failed polling command actually created a completed job

## Product Photoshoot Incident

The first `lifestyle_scene` product photoshoot attempt returned `nsfw` with no URL.
A single controlled retry in `product_shot` mode used a neutral product-only prompt and succeeded.
Further QA produced `hero_banner` and `conceptual_product` normally.
A safe `lifestyle_scene` in `3:4` completed server-side, but the wrapper returned `Cannot reach`; `higgsfield generate get <job_id>` recovered the result URL and the media was downloaded.
The CLI rejected `4:5` for product photoshoot, so route docs should use the accepted CLI ratios.

Implication:

- `higgsfield-product-photoshoot` can move to beta for product-shot validation and guarded product use
- lifestyle modes are usable in beta only with prompt-safety guidance and recovery handling
- product reference images should be stored locally as governed attachments before CLI execution

## Skill Status

| Skill | Status | Evidence | Next gate |
| --- | --- | --- | --- |
| `higgsfield-generate` | beta | Live still test passed. | Standardize polling recovery and owner review. |
| `higgsfield-product-photoshoot` | beta | Product-shot, hero, conceptual, recovered lifestyle, and helper validation passed with manifests/media. | QA more variants and review owner outputs before prod. |
| `higgsfield-marketplace-cards` | draft test pending | Installed, command surface clear, not live-tested; higher compliance risk. | One brand/product marketplace validation with manifest. |
| `higgsfield-soul-id` | draft gated | Installed, not live-tested. | Explicit operator approval, identity consent, plan check. |

## Model Caveats

- `Nano Banana 2` appeared in the CLI model list as `nano_banana_flash`.
- `nano_banana_2` may correspond to a different Nano Banana tier than the skill examples imply.
- `higgsfield-soul-id` references `soul_cinema_studio`; the observed CLI model list exposed `soul_cinematic`. Verify before Soul workflows.

## Agent Boundaries

| Agent | Permission |
| --- | --- |
| Kanye | Preferred owner for Higgsfield generation and validation. |
| Jack | May supervise, update governance, and execute bounded creative work when explicitly requested. |
| Rosa | May request creative assets through handoff; should not generate directly by default. |
| Safir | May request email/image assets through handoff; should not generate directly by default. |
| Jhin | Deferred for V1 governance; potential future visual execution owner, not promoted here. |
| Cortex | May request ad creative inputs; no generation or publication rights from this validation. |
| Tony | Dev/git owner only; not a creative generation owner. |

## Remaining Gaps

- Standard CLI polling recovery is manual, not wrapped.
- `product-photoshoot` passed product-shot, hero, conceptual, and recovered lifestyle. Remaining gaps: one `nsfw` false-positive, accepted aspect ratios differ from skill docs, and wrapper recovery is manual.
- `marketplace-cards` and `soul-id` have not been live-tested.
- Jack direct Higgsfield execution is still an explicit exception because `jack.higgsfield-skill-supervision` remains draft.
- No prod route should depend on the official CLI until output proof, recovery, and retry behavior are stable.
- External publication and paid media delivery remain approval-gated.

## Recommendation

Keep `higgsfield-generate` and `higgsfield-product-photoshoot` at beta.
Promote the official Higgsfield CLI path to prod only after recovery, attachment handling, QA, and retry behavior are embedded into a route package/runbook and reviewed with multiple specialist-owned outputs.
