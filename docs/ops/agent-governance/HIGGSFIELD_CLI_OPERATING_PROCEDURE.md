# Higgsfield CLI Operating Procedure

Last updated: `2026-05-06`

Status: `beta`

This procedure governs the official `higgsfield-ai/skills` package installed in the Jack and Kanye Hermes profiles.
It covers profile skill usage, CLI execution, artifacts, proof, and failure recovery.

It does not authorize campaign publication, ad delivery mutation, payments, deploy, restart, gateway work, or Mission Manager implementation changes.

## Ownership

| Surface | Owner | Notes |
| --- | --- | --- |
| Higgsfield creative generation | Kanye | Preferred specialist owner. |
| Higgsfield governance updates | Jack | May maintain matrices and procedures when explicitly requested. |
| Direct governed creative execution | Jack or Kanye | Jack may execute only when explicitly asked or supervising a bounded route. |
| External publication or paid delivery | Approval-gated | Never autonomous from a skill install alone. |

## Installed Skills

Installed in:

- `/Users/moufdi/.brm-hermes/profiles/jack/skills`
- `/Users/moufdi/.brm-hermes/profiles/kanye/skills`

Skills:

| Skill | Status | Owner | Allowed use | Gate |
| --- | --- | --- | --- | --- |
| `higgsfield-generate` | beta | Kanye | Generic image/video generation through official CLI. | Live still test passed; polling recovery must be standardized before prod. |
| `higgsfield-product-photoshoot` | beta | Kanye | Product-focused visuals with backend prompt enhancement. | Product-shot validation passed; lifestyle scenes need prompt-safety review after one `nsfw` false-positive. |
| `higgsfield-marketplace-cards` | draft test pending | Kanye | Marketplace listing/cards/A+ style image sets. | Needs product/brand scoped validation before beta. |
| `higgsfield-soul-id` | draft gated | Kanye | Reusable face/identity model setup. | Requires explicit operator approval, identity consent, and paid-plan confirmation. |

## Auth And Secrets

Do not print, copy, commit, or document secret values.

Accepted local auth surfaces:

- Existing Hermes generation tool: `HF_KEY` plus `HF_API_SECRET` through the profile env loader.
- Official CLI: local `higgsfield auth login` token store.

Validation may only report:

- variable presence
- CLI authenticated yes/no
- subscription plan label
- credits present yes/no

Validation must not report:

- token values
- API key secret values
- raw auth files
- full email address if avoidable

## Standard Output Layout

Use these paths for official CLI validation and beta runs:

| Artifact | Path |
| --- | --- |
| Prompt | `/Users/moufdi/.openclaw/workspace-kanye/higgsfield-validation/<run_id>/prompt.txt` |
| Raw CLI output | `/Users/moufdi/.openclaw/workspace-kanye/higgsfield-validation/<run_id>/higgsfield-output.json` |
| Recovered job JSON | `/Users/moufdi/.openclaw/workspace-kanye/higgsfield-validation/<run_id>/higgsfield-job.json` |
| Manifest | `/Users/moufdi/.openclaw/workspace-kanye/higgsfield-validation/<run_id>/manifest.json` |
| Downloaded media | `/Users/moufdi/.brm-hermes/profiles/kanye/generated_media/higgsfield-cli-validation/<run_id>_<label>.<ext>` |

The manifest is the proof target.
The downloaded local media is the deliverable target.

## Attachment Inputs

For skills that accept reference media, use the central attachment policy:

- `docs/ops/agent-governance/SKILL_ATTACHMENT_POLICY.md`

Minimum rule:

- resolve URL or chat attachment into a local run artifact first
- record source URL, local path, SHA-256, MIME type, dimensions, and attachment role
- pass local paths to CLI flags such as `--image`
- keep generated outputs under the profile `generated_media` tree
- never treat a generated output as the original source in later runs

## Minimal Still Test

Use one low-risk still generation test when validating auth or command surface.
Keep the prompt neutral and non-customer-facing.

Example shape:

```bash
run_id="$(date -u +%Y%m%dT%H%M%SZ)"
outdir="/Users/moufdi/.openclaw/workspace-kanye/higgsfield-validation/$run_id"
mkdir -p "$outdir"

prompt="A clean square product-style validation image for BRM agent governance: a minimal desk with a notebook labeled KANYE, soft daylight, neutral background, no logos, no people, high fidelity."
printf '%s\n' "$prompt" > "$outdir/prompt.txt"

higgsfield generate create gpt_image_2 \
  --prompt "$prompt" \
  --aspect_ratio 1:1 \
  --resolution 1k \
  --quality low \
  --wait \
  --json > "$outdir/higgsfield-output.json"
```

## Polling 502 Recovery

Observed behavior:

- `higgsfield generate create ... --wait --json` may return `HTTP 502` during polling.
- The job may still complete server-side.
- `higgsfield product-photoshoot create ... --json` may also return `Cannot reach <job_url>` while the underlying job is completed.

Standard recovery:

1. Run `higgsfield generate list --json`.
2. Identify the most recent job matching the expected model and timestamp.
3. Run `higgsfield generate get <job_id> --json`.
4. If `status` is `completed` and `result_url` exists, download the media.
5. Write a manifest with status `passed_with_polling_502_recovered_by_get`.
6. Do not submit a retry until recovery confirms there is no completed job.

This recovery must be wrapped or documented in the route before prod promotion.

## Product Photoshoot Caveats

Observed during Monoi Love QA:

- `product_shot`, `hero_banner`, `conceptual_product`, and recovered `lifestyle_scene` produced usable local media.
- The CLI rejected `4:5` for product photoshoot even though broader skill docs mention it.
- Use currently accepted ratios: `1:1`, `4:3`, `3:4`, `16:9`, `9:16`, `3:2`, `2:3`.
- If the product-photoshoot wrapper cannot reach a job, extract the job id and run `higgsfield generate get <job_id> --json` before retrying.
- Keep lifestyle prompts explicitly safe: no people, no skin, no body parts, no extra text, no invented claims.

Local Kanye helper:

- `/Users/moufdi/.openclaw/workspace-kanye/bin/higgsfield-product-photoshoot-run`

The helper keeps attachment provenance, downloads result media, writes `manifest.json`, and automatically attempts `generate get` recovery when a job id appears in a failed product-photoshoot response.

Helper validation evidence:

- `/Users/moufdi/.openclaw/workspace-kanye/higgsfield-product-photoshoot-runs/20260505T232850Z/manifest.json`

## Model Name Caveats

Observed CLI model names can differ from skill examples.
Before a beta/prod run, resolve the model id with:

```bash
higgsfield model list --json
higgsfield model get <job_set_type> --json
```

Known caveats from the first audit:

- `Nano Banana 2` appeared in the CLI as `nano_banana_flash`.
- `nano_banana_2` may map to a different Nano Banana tier than the skill text implies.
- `higgsfield-soul-id` references `soul_cinema_studio`, while the CLI model list exposed `soul_cinematic`; verify before using Soul workflows.

## Manifest Contract

Required fields:

```json
{
  "status": "passed_with_polling_502_recovered_by_get",
  "run_id": "YYYYMMDDTHHMMSSZ",
  "agent": "kanye",
  "skill_package": "higgsfield-ai/skills",
  "skill": "higgsfield-generate",
  "job_id": "...",
  "route": "official_higgsfield_cli",
  "provider": "higgsfield",
  "model": "...",
  "display_model": "...",
  "prompt_file": "...",
  "result_url": "...",
  "asset_path": "...",
  "job_json": "...",
  "dimensions": {
    "width": 1024,
    "height": 1024
  },
  "notes": []
}
```

## Promotion Gates

Draft to beta:

- skill installed in the owning profile
- CLI installed
- auth confirmed without secret output
- at least one bounded test manifest exists

Current beta evidence:

- `higgsfield-generate`: `/Users/moufdi/.openclaw/workspace-kanye/higgsfield-validation/20260505T214148Z/manifest.json`
- `higgsfield-product-photoshoot`: `/Users/moufdi/.openclaw/workspace-kanye/higgsfield-product-photoshoot-validation/20260505T222952Z/manifest.json`
- `higgsfield-product-photoshoot` QA variants: `/Users/moufdi/.openclaw/workspace-kanye/higgsfield-product-photoshoot-qa/20260505T230630Z/manifest.json`
- `higgsfield-product-photoshoot` helper validation: `/Users/moufdi/.openclaw/workspace-kanye/higgsfield-product-photoshoot-runs/20260505T232850Z/manifest.json`

Beta to prod:

- polling recovery standardized
- output path and manifest contract stable
- cost/error notes captured
- multiple owner-reviewed image/video outputs
- route package or runbook references the procedure
- external publication remains approval-gated

## Anti-Patterns

- treating installed skills as permission
- retrying after a polling error before checking `generate list` / `generate get`
- printing tokens or API secrets
- using Soul ID without explicit operator approval and identity consent
- publishing generated assets externally without approval
- granting Higgsfield access to non-creative agents for convenience
