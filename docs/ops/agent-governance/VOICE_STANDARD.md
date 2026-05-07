# Voice Standard

Date: `2026-05-07`

This is the BRM/Hermes voice standard for governed agents.

## Decision

Input voice:

- provider: `openai`
- model: `whisper-1`
- scope: every profile that accepts voice/audio input
- rule: no local faster-whisper fallback for governed BRM agent profiles unless explicitly approved as an offline contingency

Output voice:

- target provider: `higgsfield`
- model family: voice clone / agent voice identity
- scope: one distinct voice identity per governed agent
- status: `planned_gated`, not runtime-active until Higgsfield voice generation is validated end-to-end

## Why

The input side needs one reliable standard. `whisper-1` through OpenAI avoids the previous bug class where `whisper-1` was interpreted as a local faster-whisper model name.

The output side should differentiate agents. Higgsfield voice clones can give each agent a recognizable identity, but the runtime currently exposes non-Higgsfield TTS providers on the standard TTS path. Therefore Higgsfield voice output is the target standard and must be validated before switching live reply audio.

## Input Contract

Every profile with voice enabled must have:

```yaml
stt:
  enabled: true
  provider: openai
  model: whisper-1
```

Validation:

- YAML parses
- every `stt.enabled: true` profile has `provider: openai`
- every governed voice input uses `model: whisper-1`
- OpenAI key presence may be checked, but secrets must never be printed

## Output Contract

Voice output is not a generic TTS setting. It is an agent identity surface.

Each agent voice must have:

- `agent_id`
- `voice_provider: higgsfield`
- `voice_profile_id` or `pending_clone`
- source/consent record when a real human voice is involved
- short test phrase
- generated test clip
- manifest with prompt/text, provider job id, local artifact path, and QA verdict

External audio sending remains approval-gated.

## Agent Voice Slots

| Agent | Voice status | Target provider | Notes |
| --- | --- | --- | --- |
| Jack | pending clone | Higgsfield | operator-facing control-plane voice |
| Jack-X | pending clone | Higgsfield | memory/intake voice, should be distinct from Jack |
| Mnemos | pending clone | Higgsfield | concise continuity voice |
| Rosa | pending clone | Higgsfield | marketing strategist voice |
| Jeff | pending clone | Higgsfield | creator/influence voice |
| Naya | pending clone | Higgsfield | supply/ops voice |
| Selena | pending clone | Higgsfield | support-risk voice |
| Alfred | pending clone | Higgsfield | SEO/AEO analyst voice |
| Cortex | pending clone | Higgsfield | paid-media analyst voice |
| Tony | pending clone | Higgsfield | developer voice |
| Kanye | pending clone | Higgsfield | creative generation voice |
| Safir | pending clone | Higgsfield | email/CRM voice |

Later profiles:

- `jackette`, `jhin`, `walter`: no V1 voice identity until promoted, but their STT config should still follow OpenAI `whisper-1` if voice is enabled.

## Current Runtime Gap

Jack currently has a legacy TTS config using ElevenLabs. This is not the target standard.

Do not promote ElevenLabs as the BRM voice identity path. Keep it as legacy until a Higgsfield voice output path is implemented and validated, or until Moufdi explicitly asks for a temporary fallback.

## Promotion Gates

Higgsfield output voice becomes `beta` only after:

1. CLI/API capability for audio/voice generation is confirmed.
2. One non-sensitive agent test voice is generated.
3. The generated clip is saved locally with a manifest.
4. The voice identity is mapped in `voice-standard.yaml`.
5. External sending is still blocked behind approval.

It becomes `prod` only after:

1. each V1 agent has an approved voice identity
2. reply audio can be generated through a repeatable route/tool
3. failures return text fallback cleanly
4. no provider secrets or voice source material leak into logs
