# Tony Log Bug Audit

Date: `2026-05-07`

Scope: governance audit and implementation handoff only. No runtime, gateway, Mission Manager, deploy, restart, or systemd file was edited.

## Current State

Tony has three governed runtime routes:

- `tony.codebase-exploration`
  - Registry mode: `run_canonical`
  - Profile: `tony-kimi`
  - Intended model lane: Kimi coding
  - Current risk: input contract drift and possible wrong default repo
- `tony.development-plan`
  - Registry mode: `run_canonical`
  - Profile: `tony`
  - Intended model lane: OpenAI Codex GPT
  - Current risk: stale artifact paths can still block plan creation if old fixtures are reused
- `tony.development`
  - Registry mode: `run_canonical`
  - Profile: `tony-dev`
  - Intended model lane: OpenAI Codex GPT
  - Current risk: validation harness and path hygiene need cleanup before production confidence

Historical rerun evidence shows the implementation path can work:

- `tony.development-plan` rerun reached `review_ready` once the exploration artifact path was corrected to `/Users/moufdi/hermes-runtime/reviews/...`.
- `tony.development` rerun reached `ok`, `canFinalize=true`, changed only the fixture snapshot, and passed `npm test`.

## Findings

### TONY-001 - Stale `BRMXHERMES` review paths block plan/dev routes

Severity: high

Evidence:

- Failed sweep root: `/Users/moufdi/.openclaw/mm-route-sweep-tony-cortex`
- `tony.development-plan` failed at stage `analysis` with `FileNotFoundError`.
- `tony.development` failed at stage `preflight` with the same missing artifact.
- Missing path:
  - `/Users/moufdi/BRMXHERMES/hermes/runtime/reviews/2026-04-03T14-41-30Z-wave-4-tony-exploration-validation/run-1.normalized.json`
- Existing canonical path:
  - `/Users/moufdi/hermes-runtime/reviews/2026-04-03T14-41-30Z-wave-4-tony-exploration-validation/run-1.normalized.json`

Interpretation:

`/Users/moufdi/BRMXHERMES/hermes/runtime` still exists locally, but its `reviews` tree is not the canonical current review store. Any fixture, handoff, or user payload that points to `BRMXHERMES/hermes/runtime/reviews` can fail even when the real artifact exists under `/Users/moufdi/hermes-runtime/reviews`.

Required fix:

- Normalize Tony review artifact inputs through the canonical runtime resolver before route execution.
- Update sweep fixtures and Jack handoff examples to pass `/Users/moufdi/hermes-runtime/...` review artifacts.
- Fail early with a clean blocked status when an artifact is missing, not a raw Python traceback.

Expected test:

- Run `tony.development-plan` with the canonical exploration artifact path and confirm `route_status=review_ready`.
- Run `tony.development` with canonical exploration and plan artifacts on the fixture snapshot and confirm `route_status=ok`, `canFinalize=true`, and test evidence exists.
- Run one negative test with a missing artifact and confirm the route returns a clean blocked result.

### TONY-002 - `tony.codebase-exploration` input contract is inconsistent

Severity: high

Evidence:

- Protocol YAML requires:
  - `target_repo`
  - `task_request`
- Runtime registry only requires:
  - `prompt`
- Runtime runner accepts:
  - required `--prompt`
  - optional `--target-repo`
  - no `--task-request`
- The supervised handoff message for `tony.codebase-exploration` sends only a prompt asking to inspect Hermes runtime.
- The runner default target repo is `resolve_operator_root()`, which resolves to the OpenClaw/operator repo, not Hermes runtime.

Interpretation:

This route can appear successful while inspecting the wrong repo or while bypassing the protocol input contract. This is the most important Tony governance issue because it can create bad downstream plan/dev artifacts.

Required fix:

- Decide and enforce one contract:
  - recommended: require `prompt` and `target_repo` for `tony.codebase-exploration`; keep `task_request` optional or map it explicitly from `prompt`.
- Update protocol YAML, registry args, runner args, and handoff payload so they agree.
- The default should be safe for smoke tests only. Production or supervised handoff runs should pass `target_repo` explicitly.

Expected test:

- Launch `tony.codebase-exploration` on `/Users/moufdi/hermes-runtime/fixtures/tony-dev-fixture-template` and confirm the artifact reports that exact target repo.
- Launch on `/Users/moufdi/hermes-runtime` only in read-only mode and confirm inspected files are from that repo.
- Confirm route summary is structured and not a raw fenced block.

### TONY-003 - Runtime wrapper tests depend on implicit `PYTHONPATH`

Severity: medium

Evidence:

- Command:
  - `python3 -m pytest -q tests/test_tony_runtime_route_wrappers.py`
- Result:
  - `3 failed, 1 passed`
- Failure:
  - `ModuleNotFoundError: No module named 'openclaw_route_wrapper'`
- Passing command:
  - `PYTHONPATH=/Users/moufdi/hermes-runtime/scripts python3 -m pytest -q tests/test_tony_runtime_route_wrappers.py`
- Passing result:
  - `4 passed in 0.10s`

Interpretation:

The wrappers compile, but the test loader imports wrapper files by path without adding `scripts/` to `sys.path`. This makes Tony validation sensitive to the caller environment.

Required fix:

- Make the tests self-contained by inserting `/Users/moufdi/hermes-runtime/scripts` into `sys.path` before loading wrapper modules, or package the wrapper helper in an importable module.

Expected test:

- `python3 -m pytest -q tests/test_tony_runtime_route_wrappers.py` must pass without external `PYTHONPATH`.

### TONY-004 - `tony-kimi` profile has a stale terminal cwd

Severity: medium

Evidence:

- Current profile path:
  - `/Users/moufdi/.brm-hermes/profiles/tony-kimi/config.yaml`
- Current cwd:
  - `/Users/moufdi/BRMXHERMES/clawd/workspace/tech`
- That directory is missing locally.
- Canonical equivalent exists:
  - `/Users/moufdi/clawd/workspace/tech`

Interpretation:

Current canonical routes set `TERMINAL_CWD` and process `cwd` explicitly, so this may not affect every run. It still makes direct `tony-kimi` profile use fragile and can explain old `spawn_profile` drift.

Required fix:

- Change `tony-kimi` terminal cwd to `/Users/moufdi/clawd/workspace/tech` or `auto`, depending on the final runtime convention.

Expected test:

- Start a direct `tony-kimi` profile smoke and confirm terminal commands run in an existing directory.

### TONY-005 - Tony and Tony-dev have `whisper-1` without explicit STT provider

Severity: medium

Evidence:

- `/Users/moufdi/.brm-hermes/profiles/tony/config.yaml`
  - `stt.enabled: true`
  - `stt.model: whisper-1`
  - no `stt.provider`
- `/Users/moufdi/.brm-hermes/profiles/tony-dev/config.yaml`
  - `stt.enabled: true`
  - `stt.model: whisper-1`
  - no `stt.provider`

Interpretation:

This matches the previously observed Kanye anti-pattern: an OpenAI STT model name can be routed to local faster-whisper unless the provider is explicit. No Tony STT failure was observed in the current Tony logs, but the config is risky before voice usage.

Required fix:

- Add `stt.provider: openai` for Tony and Tony-dev, or disable STT for those profiles if voice is not part of their route surface.

Expected test:

- Run one STT smoke for Tony if voice remains enabled.
- If voice is not in scope, assert STT is disabled and documented.

### TONY-006 - GPT model lane produced empty responses in profile logs

Severity: medium

Evidence:

- `/Users/moufdi/.brm-hermes/profiles/tony/logs/errors.log`
  - `2026-04-07 03:14`
  - `response.output is empty`
  - after 3 retries, invalid API response
- `/Users/moufdi/.brm-hermes/profiles/tony-dev/logs/errors.log`
  - same failure pattern at `2026-04-07 03:13`

Interpretation:

This is not the same as the Selena Anthropic `HTTP 529` overload. It looks like an empty provider response from the OpenAI Codex GPT lane. The route policy should not depend on one model call returning valid content after only generic retries.

Required fix:

- Add route-step model policy with explicit fallback by stage:
  - exploration: Kimi lane
  - planning: GPT primary, compatible GPT fallback
  - execution: GPT primary, compatible GPT fallback
- Preserve route-level model gates so Jack cannot override the model ad hoc.

Expected test:

- Simulate or force one empty response and confirm Tony returns a governed retry/fallback or clean blocked status with no partial artifact promotion.

### TONY-007 - Old `spawn_profile` summaries are still noisy

Severity: low

Evidence:

- Old sweep `tony.codebase-exploration` used `dispatch_mode=spawn_profile`.
- Its route summary was ` ```json `.
- Current registry now says `run_canonical`.

Interpretation:

This looks mostly historical, but the old MM missions and summaries remain confusing. If any entrypoint still uses `spawn_profile`, it can produce unusable summaries.

Required fix:

- Confirm all live Tony dispatch entrypoints use the registry `run_canonical` mode.
- Close or annotate old blocked/review MM runs once the runtime lane owns cleanup.

Expected test:

- Fresh `tony.codebase-exploration` run should produce a canonical payload with `report_summary`, `paths`, and structured route status.

### TONY-008 - Model provider prefix warning is noisy

Severity: low

Evidence:

- Successful Tony development rerun raw output includes:
  - stripped provider prefix from `openai-codex/gpt-5.4`
  - using `gpt-5.4` for OpenAI Codex

Interpretation:

The warning is benign when the call succeeds, but it pollutes artifacts and can confuse route summaries.

Required fix:

- Normalize provider/model IDs before profile execution, or update profile config to the exact expected model string for the provider.

Expected test:

- Fresh Tony development artifact should not include model-normalization warnings in the business summary.

## Production-Ready Gate For Tony

Tony should not be treated as production-ready until these checks pass:

1. `tony.codebase-exploration` contract is aligned across protocol YAML, registry, runner, docs, and Jack handoff.
2. `tony.codebase-exploration` explicitly receives and proves the `target_repo`.
3. `tony.development-plan` and `tony.development` resolve canonical review artifacts through `/Users/moufdi/hermes-runtime`.
4. Wrapper tests pass without external `PYTHONPATH`.
5. Tony profile cwd and optional STT provider are cleaned.
6. Empty model output and provider overload have clear route outcomes: fallback or clean blocked status.
7. No route emits raw tracebacks or fenced JSON as the operator summary.

## Ownership

Governance lane:

- keep this audit and route contract expectations current
- update agent/tool/protocol matrices after runtime fixes land
- validate outputs and evidence

Tony/integrator runtime lane:

- patch wrapper imports or test harness
- patch Tony runner input contracts
- patch path normalization and clean blocked errors
- patch profile config if profile config edits are assigned
- run actual route smoke tests and decide deploy/restart timing

## Immediate Recommended Order

1. Fix `tony.codebase-exploration` contract drift first.
2. Fix canonical artifact path handling for plan/dev.
3. Fix the wrapper test harness so local validation is trustworthy.
4. Clean `tony-kimi` cwd and Tony STT provider.
5. Add model fallback/blocked semantics for empty output.
6. Run the three-route Tony smoke on fixture paths.
