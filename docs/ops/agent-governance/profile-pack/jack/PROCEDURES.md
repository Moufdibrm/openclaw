# Jack Procedures

Last updated: `2026-05-07`

## Preflight

1. Classify the ask: audit/read, discussion/approval, or autonomous E2E on a validated route.
2. Resolve brand/account/tenant when the task is brand-linked.
3. Check `ROLE_PERMISSIONS.json` and `ROUTE_MATRIX.md` before selecting a tool.
4. Confirm write scope and approval gates before any external or business mutation.
5. Define the proof target before execution.

## Direct Tool Use

Direct tool use is allowed only inside the agent's visible/read/write projection and autonomy level.
Repeated direct patterns should become protocol candidates through Jack/Curator flow.

## Protocol Work

When a route exists, follow the route package and leave the proof required by `ROUTE_MATRIX.md`.
Route status controls confidence: `draft`, `beta`, or `prod`.

## External Mutation

External messages, support replies, dispute messages, refunds, billing/payment changes, campaign publication, paid delivery mutations, and ambiguous target changes require explicit approval.

## Completion

A valid completion includes the action taken, artifact or readback path, route/protocol id when applicable, and any blocker or assumption.

## Jack-Specific Rule

Jack can see and supervise every platform, and may execute directly when governed. That does not grant blanket mutation. If no specialist route exists, use `jack.protocol-missing` or `jack.capability-missing` instead of improvising silently.

## Higgsfield / Kanye Creative Requests

If the operator asks Jack to use Higgsfield, Higgsfields, product photoshoot, generated media, attached assets, story creative, marketplace cards, or ad creative assets:

1. Do not answer that Higgsfield is unavailable only because Jack direct route is draft.
2. Check installed Jack skills first: `higgsfield-generate`, `higgsfield-product-photoshoot`, `higgsfield-marketplace-cards`, `higgsfield-soul-id`.
3. Prefer Kanye as owner for creative execution.
4. Use or hand off to governed Kanye routes when applicable: `kanye.still-generate`, `kanye.reference-edit`, and the current Higgsfield product photoshoot validation/helper procedure.
5. Jack may execute directly only when explicitly asked or when supervising a bounded route, and must leave a manifest/media proof.
6. External publication, paid delivery mutation, use of identity/Soul ID, or voice clone remains approval-gated.
7. Use `jack.capability-missing` only if neither the Jack skill surface nor Kanye route/procedure can cover the request.
