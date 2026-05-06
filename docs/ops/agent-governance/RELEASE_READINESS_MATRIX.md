# Release Readiness Matrix

Last updated: `2026-05-06`

This is the global readiness rollup for governed V1 BRM/Hermes agents.

It does not replace the route, toolbox, environment, fixture, or IO matrices. It only answers: which agents can be tested now, which are partial, which are blocked, and what must happen next.

No deploy, restart, gateway work, runtime wiring, Mission Manager mutation, or external platform mutation is authorized by this document.

## Summary

Not all agents are production-ready as complete agent surfaces.

All V1 agents remain `beta` at global governance level because route-level readiness, fixture coverage, native `brand_scope`, and proof consistency are not uniform yet.

Several individual routes are production-usable on bounded scopes:

- Rosa report/strategy routes
- Jeff profile/performance routes
- Naya stock/sourcing routes, with fixture blockers still open
- Selena PayPal/Zendesk read/audit routes
- Alfred visibility audit
- Cortex ads observation

## Global Gates

| Gate | Status | Meaning |
| --- | --- | --- |
| `brand_scope` on brand-linked deliverables | partial | contract is now required, but representative proof bundles are legacy and need sidecar/native emission |
| reviewed fixtures | partial | strong coverage exists, but Naya sourcing input, Naya stock SKU/snapshot, Safir email brief, and Jack fresh proof remain open |
| native route proof | partial | many routes have historical/golden proof; several beta/package routes need fresh post-deploy or fixture smoke proof |
| external mutations | blocked by default | outbound messages, refunds, disputes, CRM/storefront/campaign mutations, supplier sends, publication, Drive upload require approval |
| runtime/deploy/MM | out of scope | owned by the integrator lane |

## Agent Readiness

| Agent | Prep state | What can run next | Main blocker |
| --- | --- | --- | --- |
| Jack | partial | beta fixture checks for protocol/capability/draft routes | no fresh post-deploy proof in audited paths; Higgsfield supervision remains draft |
| Jack-X | partial | frozen fixture suite for package-backed memory routes | package-only coverage and no KG commit path |
| Mnemos | ready for beta fixture | context-check fixture replay | package-only route, not a full shipped surface |
| Rosa | ready for prod route smoke | offer, performance audit, competitive watch with upload off | native `brand_scope` missing in legacy manifests |
| Jeff | ready/partial | analyse-profil and performance-report smoke; candidate-intake normalization | outreach/collab routes approval-gated and planned |
| Naya | blocked/partial | sourcing/stock once inputs are isolated | reviewed sourcing input and stock SKU/snapshot still partial |
| Selena | ready with caveats | PayPal/Zendesk reviewed exports and bounded live reads | native `brand_scope` missing; live reads must stay tiny/no mutation |
| Alfred | blocked/partial | visibility-audit is prod; strategy-plan after brand/store normalization | Phase 2 strict store mismatch, now modeled as `brand_scope` separation |
| Cortex | ready for read/dry-run | ads observation and dry-run campaign handoff | campaign publication and feedback loop remain draft/approval-gated |
| Tony | ready for beta fixture | exploration, development-plan, development on fixture repo | fixture is minimal; deploy/restart out of scope |
| Kanye | ready for beta local generation | Higgsfield still/product photoshoot validation with manifests | polling recovery, marketplace cards, Soul ID approval/consent |
| Safir | blocked/partial | email audit beta if fixture exists; workflow dry-run after brief | email-workflow business fixture missing |

## Prepared Now

- Global machine rollup: `release-readiness-matrix.yaml`
- Legacy brand proof sidecar mapping: `brand-scope-sidecars.yaml`
- Brand scope contract is mandatory for all brand-linked deliverables.

## Next Parallel Batches

| Batch | Agents | Target | Blockers |
| --- | --- | --- | --- |
| Business prod smoke | Rosa, Jeff, Selena | upload-off fixture/live-read reports with sidecar `brand_scope` | none beyond live-read limits and approval gates |
| Supply chain unblock | Naya | isolate sourcing input and known SKU/snapshot | needs reviewed input selection |
| SEO/AEO unblock | Alfred, Tony | normalize `brand_scope` vs runner store key, then rerun Phase 2 | runner/manifest contract fix |
| Technical fixture smoke | Jack, Jack-X, Mnemos, Tony | fixture-only beta validation | no KG/MM/runtime mutation |
| Creative beta QA | Kanye, Cortex | continue product/ads media validation | publication blocked; marketplace/Soul ID gates |
| Email workflow prep | Safir, Kanye, Rosa | create Safir email brief fixture and render-only workflow | business brief missing |

