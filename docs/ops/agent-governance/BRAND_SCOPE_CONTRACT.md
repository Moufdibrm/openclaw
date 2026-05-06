# Brand Scope Contract

Last updated: `2026-05-06`

This contract defines how governed agents should identify a brand, a subject, and the intended focus mode before reading or writing business surfaces.

It is a governance contract only. It does not modify brand packs, runtime routing, gateway code, Mission Manager, deployment scripts, or platform accounts.

## Decision

Every brand-linked request, workflow, and deliverable must carry a `brand_scope` object.

The source-of-truth brand identifier is the brand pack's existing `brand_id`, for example:

- `maybe-paris`
- `blinx`
- `botanic`
- `magic-styler`
- `nailz`

Agent/routing scripts may derive filesystem or runner-safe keys such as `maybe_paris`, but those are not the canonical brand identity. They are aliases scoped to a specific runner or storage layout.

## Mandatory Deliverable Rule

Any artifact tied to a brand must include `brand_scope` directly or reference a sidecar manifest that contains it.

This applies to:

- runner inputs
- `manifest.json`
- route-specific manifests
- `result.json`
- `report-data.json`
- `delivery.json`
- `verification_json`
- approval packets
- generated media manifests
- campaign briefs
- workboards and handoff packets
- memory candidates extracted from brand-specific sources

Minimum required shape:

```yaml
brand_scope:
  scope_id: "maybe-paris:brand_focus:cheveux-boucles"
  brand_pack_id: "maybe-paris"
  focus_mode: "brand_focus"
  subject_id: "cheveux-boucles"
  runtime_store_key: "maybe_paris"
```

Legacy artifacts should not be rewritten blindly. If a legacy bundle is already used as proof, create a sidecar governance manifest that maps the artifact to its `brand_scope` and records the mapping as partial until the route emits it natively.

## Fields

| Field | Required | Meaning |
| --- | --- | --- |
| `scope_id` | yes | Stable composite id: `<brand_pack_id>:<focus_mode>:<subject_id>` |
| `brand_pack_id` | yes for brand work | Canonical id from the brand pack `brand_id` |
| `focus_mode` | yes | `brand_focus` or `generic` |
| `subject_id` | yes | Normalized topic, product, campaign, customer segment, route, or problem |
| `runtime_store_key` | optional | Runner/store key when a route needs a different identifier |
| `platform_keys` | optional | Platform-specific ids from the brand registry or pack |
| `allowed_surfaces` | optional | Surfaces the route may read or mutate, still permission-gated |

## Focus Modes

`brand_focus` means:

- use the brand pack identity, voice, platform ids, known products, and constraints
- output is intended for that brand
- writes to brand surfaces remain approval-gated

Example:

```yaml
brand_scope:
  scope_id: "maybe-paris:brand_focus:cheveux-boucles"
  brand_pack_id: "maybe-paris"
  focus_mode: "brand_focus"
  subject_id: "cheveux-boucles"
  runtime_store_key: "maybe_paris"
```

`generic` means:

- the subject can be researched, tested, or documented without forcing brand-specific voice or claims
- the brand pack may still define the workspace, permissions, or destination context
- no brand platform mutation is implied by the generic mode

Example:

```yaml
brand_scope:
  scope_id: "maybe-paris:generic:cheveux-boucles"
  brand_pack_id: "maybe-paris"
  focus_mode: "generic"
  subject_id: "cheveux-boucles"
  runtime_store_key: "maybe_paris"
```

For cross-brand work that is truly not attached to any brand pack, use `global:generic:<subject_id>` and keep all mutable brand surfaces disabled.

For reusable work that starts from a brand context but should not be brand-specific, keep the brand pack id and set `focus_mode=generic`. This allows the system to know where the request came from while avoiding accidental brand claims or platform writes.

## Store Key Rule

Do not compare raw `brand_pack_id` and `runtime_store_key` as if they were the same field.

Correct:

```yaml
brand_pack_id: "maybe-paris"
runtime_store_key: "maybe_paris"
```

Incorrect:

```yaml
brand_pack_id: "maybe_paris"
runtime_store_key: "maybe-paris"
```

If a runner currently mixes those fields, the route is partial until it either:

1. accepts a `brand_scope` object, or
2. performs deterministic alias normalization before strict validation.

## Agent Handling

| Agent | Brand scope use |
| --- | --- |
| Jack | asks for or infers `brand_scope`, then routes to the specialist |
| Jack-X | stores memory against `scope_id`, never against ambiguous display names |
| Rosa | uses `brand_focus` for offer/marketing decisions; may use `generic` for reusable market research |
| Alfred | uses `brand_focus` for SEO/AEO work on a brand; may use `generic` for topic/category research |
| Cortex | uses `brand_focus` for ads linked to a brand; `generic` only for reusable creative or strategy patterns |
| Kanye | uses `brand_focus` for brand assets; `generic` for pure style/visual exploration |
| Safir | uses `brand_focus` for brand email; `generic` for reusable email workflow tests |
| Tony | implements only after the route provides exact `brand_scope`, target surfaces, and approval gate |

## Validation

A workflow cannot be considered beta/prod-ready if:

- `brand_pack_id` is missing for brand-specific work
- `focus_mode` is missing or outside `brand_focus|generic`
- `subject_id` is missing for topic, product, campaign, or route-specific work
- a brand-linked deliverable omits `brand_scope`
- the route's manifest and result use different brand scope values
- a route compares `brand_pack_id` and `runtime_store_key` as one undifferentiated field
- mutable surfaces are implied by `generic`
