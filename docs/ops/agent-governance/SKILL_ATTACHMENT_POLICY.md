# Skill Attachment Policy

Last updated: `2026-05-06`

This policy standardizes how agent skills should handle uploaded files, reference images, exported CSVs, PDFs, screenshots, and external media URLs.

It does not grant permission to use a tool.
Permission still comes from the agent toolbox matrix, route policy, and approval gates.

## Core Rule

Treat every attachment as a governed input artifact.

A skill should not rely on an implicit chat attachment or remote URL once execution starts.
Resolve the attachment into a local run folder, record provenance, then pass the local path to CLI tools whenever possible.

## Canonical Flow

1. Resolve the input source.
2. Copy or download it into the agent run folder.
3. Record provenance and metadata.
4. Pass the local file path to the skill/tool.
5. Store generated outputs separately from source attachments.
6. Write the attachment metadata into the manifest or report.

## Standard Layout

Use this shape for new skill runs:

```text
/Users/moufdi/.openclaw/workspace-<agent>/<protocol-or-skill>/<run_id>/
  attachments/
    <label>.<ext>
  attachments.json
  prompt.txt
  tool-output.json
  manifest.json
```

Generated media should stay separate:

```text
/Users/moufdi/.brm-hermes/profiles/<agent>/generated_media/<protocol-or-skill>/
```

Existing routes may keep their current layout, but new consolidations should move toward this shape.

## Attachment Metadata

Each attachment record should include:

```json
{
  "id": "product_reference_1",
  "role": "product_reference_cutout",
  "source_type": "external_url",
  "source_url": "https://...",
  "local_path": "/Users/moufdi/.openclaw/workspace-kanye/.../attachments/monoi_love_detoure.png",
  "sha256": "...",
  "mime_type": "image/png",
  "dimensions": {
    "width": 3240,
    "height": 3240
  },
  "sensitivity": "business_asset",
  "notes": []
}
```

Recommended roles:

- `product_reference_cutout`
- `product_reference_packshot`
- `style_reference`
- `brand_reference`
- `customer_export`
- `support_export`
- `campaign_snapshot`
- `email_reference`
- `identity_reference`
- `other`

## Skill Requirements

Every skill that accepts attachments should document:

- accepted file types
- maximum number of attachments
- required attachment roles
- whether remote URLs are accepted directly or must be downloaded first
- whether multiple `--image` / `--file` flags are allowed
- forbidden attachment types
- sensitivity and approval gates
- output proof contract

For CLI tools, prefer local paths over remote URLs.
Remote URLs may expire, change, leak query parameters, or produce different results later.

## Approval Gates

Explicit approval is required before using attachments that contain:

- a real person's face, likeness, identity, or private image
- customer support records
- payment, dispute, billing, invoice, or refund data
- private creator/influencer contact details
- confidential supplier or contract data

External publication or customer-visible sending remains separately approval-gated even if the attachment itself is allowed.

## Current Precedent

Kanye product photoshoot validation used:

- source URL: Shopify CDN product PNG
- local source: `/Users/moufdi/.openclaw/workspace-kanye/higgsfield-product-photoshoot-validation/20260505T222952Z/monoi_love_detoure.png`
- manifest: `/Users/moufdi/.openclaw/workspace-kanye/higgsfield-product-photoshoot-validation/20260505T222952Z/manifest.json`
- generated media: `/Users/moufdi/.brm-hermes/profiles/kanye/generated_media/higgsfield-product-photoshoot-validation/20260505T222952Z_monoi_love_product_shot.png`

This confirms the minimum attachment pattern:

- source preserved
- local copy used for CLI execution
- metadata and hashes recorded in manifest
- generated media stored outside source attachment folder
- external publication not performed

## Anti-Patterns

- passing an expiring external URL directly to a CLI when a local path works
- omitting attachment provenance from the manifest
- mixing source attachments and generated outputs in the same folder without labels
- using identity photos without explicit approval and consent
- treating a generated image as the original source in later runs
- sending or publishing generated assets externally without approval
