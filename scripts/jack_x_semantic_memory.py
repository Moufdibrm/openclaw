from __future__ import annotations

import json
import os
import re
import time
import unicodedata
import urllib.error
import urllib.request
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from typing import Any


SEMANTIC_MODES = {"deterministic", "shadow", "active"}
SEMANTIC_PROVIDERS = {"gemini", "glm"}
DEFAULT_BASE_URL = "https://api.z.ai/api/coding/paas/v4"
HOME = Path.home()
DEFAULT_SEMANTIC_CACHE_FILE = HOME / ".openclaw" / "semantic-cache" / "jack-x-semantic-cache.json"
SEMANTIC_CACHE_SCHEMA_ID = "brm.semantic-cache.v1"
ALLOWED_PAGE_ENTITY_TYPES = {
    "entity",
    "person",
    "project",
    "brand",
    "business_event",
    "company",
    "channel",
    "operation",
    "issue",
    "task",
    "decision",
    "product",
}
ALLOWED_REVIEW_ACTIONS = {"already_known", "promote", "review", "reject"}


def normalize_identity_label(value: str | None) -> str:
    ascii_value = unicodedata.normalize("NFKD", str(value or "")).encode("ascii", "ignore").decode("ascii")
    raw = ascii_value.strip().lower()
    return " ".join(raw.replace("-", " ").split())


def short_text(value: Any, limit: int = 320) -> str:
    text = " ".join(str(value or "").split())
    if len(text) <= limit:
        return text
    return text[: max(0, limit - 1)].rstrip() + "..."


def unique_strings(values: list[Any], *, limit: int | None = None) -> list[str]:
    seen: set[str] = set()
    rows: list[str] = []
    for value in values:
        text = str(value or "").strip()
        if not text or text in seen:
            continue
        seen.add(text)
        rows.append(text)
        if limit is not None and len(rows) >= limit:
            break
    return rows


def semantic_mode(value: str | None, *, default: str = "deterministic") -> str:
    mode = str(value or default).strip().lower()
    return mode if mode in SEMANTIC_MODES else default


def configured_semantic_mode(*, cli_mode: str | None = None, env_var: str = "LLM_WIKI_MODE") -> str:
    return semantic_mode(cli_mode or os.getenv(env_var), default="deterministic")


def semantic_provider(value: str | None, *, default: str = "gemini") -> str:
    provider = str(value or default).strip().lower()
    return provider if provider in SEMANTIC_PROVIDERS else default


def configured_semantic_provider(*, cli_provider: str | None = None, env_var: str = "BRM_SEMANTIC_PROVIDER") -> str:
    explicit = str(cli_provider or os.getenv(env_var) or os.getenv("LLM_WIKI_PROVIDER") or "").strip()
    if explicit:
        return semantic_provider(explicit, default="gemini")
    if _env_lookup(("GEMINI_API_KEY", "GOOGLE_API_KEY")):
        return "gemini"
    if _env_lookup(("LLM_WIKI_API_KEY", "GLM_API_KEY", "ZAI_API_KEY")):
        return "glm"
    return "gemini"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def ensure_parent_dir(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def read_json_file(path: Path, default: dict[str, Any]) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return dict(default)
    return payload if isinstance(payload, dict) else dict(default)


def write_json_file(path: Path, payload: dict[str, Any]) -> None:
    ensure_parent_dir(path)
    temp_path = path.with_suffix(path.suffix + ".tmp")
    temp_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temp_path.replace(path)


def default_semantic_cache_file(path: str | Path | None = None) -> Path:
    return Path(path or DEFAULT_SEMANTIC_CACHE_FILE).expanduser().resolve()


def load_semantic_cache(path: str | Path | None = None) -> dict[str, Any]:
    cache_path = default_semantic_cache_file(path)
    payload = read_json_file(
        cache_path,
        default={
            "schema_id": SEMANTIC_CACHE_SCHEMA_ID,
            "updated_at": None,
            "entries": {},
        },
    )
    payload["schema_id"] = SEMANTIC_CACHE_SCHEMA_ID
    payload["entries"] = payload.get("entries") if isinstance(payload.get("entries"), dict) else {}
    payload["_path"] = str(cache_path)
    payload["_dirty"] = False
    return payload


def flush_semantic_cache(cache: dict[str, Any]) -> None:
    if not cache.get("_dirty"):
        return
    path = default_semantic_cache_file(cache.get("_path"))
    payload = {
        "schema_id": SEMANTIC_CACHE_SCHEMA_ID,
        "updated_at": now_iso(),
        "entries": cache.get("entries") or {},
    }
    write_json_file(path, payload)
    cache["_dirty"] = False
    cache["_path"] = str(path)


def semantic_cache_stats(cache: dict[str, Any]) -> dict[str, int]:
    entries = cache.get("entries") if isinstance(cache.get("entries"), dict) else {}
    return {"entry_count": len(entries)}


def semantic_cache_stable_id(namespace: str, key: str) -> str:
    return f"{namespace}:{safe_slug(key)}"


def semantic_input_hash(*, provider: str, model: str, system_prompt: str, payload: dict[str, Any]) -> str:
    basis = json.dumps(
        {
            "schema": "semantic-input.v2",
            "provider": provider,
            "model": model,
            "system_prompt": system_prompt,
            "payload": payload,
        },
        ensure_ascii=False,
        sort_keys=True,
    )
    return sha256(basis.encode("utf-8")).hexdigest()


def extract_json(value: str) -> dict[str, Any] | None:
    text = str(value or "").strip()
    if not text:
        return None
    try:
        payload = json.loads(text)
        return payload if isinstance(payload, dict) else None
    except Exception:
        pass
    start = text.find("{")
    end = text.rfind("}")
    if start >= 0 and end > start:
        try:
            payload = json.loads(text[start : end + 1])
            return payload if isinstance(payload, dict) else None
        except Exception:
            return None
    return None


def _env_lookup(names: tuple[str, ...], default: str = "") -> str:
    for name in names:
        value = str(os.getenv(name, "")).strip()
        if value:
            return value
    return default


def _stubbed_response() -> dict[str, Any] | None:
    inline = str(os.getenv("BRM_SEMANTIC_STUB_RESPONSE", "")).strip()
    if inline:
        return extract_json(inline)
    path_value = str(os.getenv("BRM_SEMANTIC_STUB_RESPONSE_FILE", "")).strip()
    if not path_value:
        return None
    try:
        return extract_json(open(path_value, "r", encoding="utf-8").read())
    except Exception:
        return None


def default_model_for_provider(provider: str) -> str:
    if provider == "gemini":
        return "gemini-2.5-flash"
    return "glm-4.5-flash"


def resolve_model(provider: str, model_override: str | None = None) -> str:
    explicit = str(model_override or "").strip()
    if explicit:
        return explicit
    if provider == "gemini":
        return _env_lookup(("LLM_WIKI_MODEL", "BRM_SEMANTIC_MODEL", "GEMINI_MODEL"), default=default_model_for_provider(provider))
    return _env_lookup(("LLM_WIKI_MODEL", "BRM_SEMANTIC_MODEL", "GLM_MODEL"), default=default_model_for_provider(provider))


def _call_glm_chat(
    *,
    api_key: str,
    base_url: str,
    model: str,
    system_prompt: str,
    payload: dict[str, Any],
    timeout: float,
) -> tuple[dict[str, Any] | None, dict[str, Any]]:
    request_payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": json.dumps(payload, ensure_ascii=False, sort_keys=True)},
        ],
        "temperature": 0,
        "max_tokens": 900,
    }
    request = urllib.request.Request(
        f"{base_url.rstrip('/')}/chat/completions",
        data=json.dumps(request_payload, ensure_ascii=False).encode("utf-8"),
        method="POST",
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        result = json.load(response)
    content = (((result.get("choices") or [{}])[0].get("message") or {}).get("content") or "").strip()
    return extract_json(content), {"http_provider": "glm"}


def _call_gemini_generate_content(
    *,
    api_key: str,
    model: str,
    system_prompt: str,
    payload: dict[str, Any],
    timeout: float,
) -> tuple[dict[str, Any] | None, dict[str, Any]]:
    request_payload = {
        "generationConfig": {
            "temperature": 0,
            "responseMimeType": "application/json",
        },
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "text": (
                            f"{system_prompt}\n\n"
                            "Return JSON only.\n\n"
                            f"INPUT:\n{json.dumps(payload, ensure_ascii=False, sort_keys=True)}"
                        )
                    }
                ],
            }
        ],
    }
    request = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}",
        data=json.dumps(request_payload, ensure_ascii=False).encode("utf-8"),
        method="POST",
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        result = json.load(response)
    parts = (((result.get("candidates") or [{}])[0].get("content") or {}).get("parts") or [])
    content = str(parts[0].get("text") or "").strip() if parts else ""
    return extract_json(content), {"http_provider": "gemini"}


def call_semantic_llm(
    *,
    mode: str,
    provider: str | None = None,
    system_prompt: str,
    payload: dict[str, Any],
    model_override: str | None = None,
    timeout: float = 6.0,
) -> tuple[dict[str, Any] | None, dict[str, Any]]:
    resolved_mode = semantic_mode(mode)
    resolved_provider = configured_semantic_provider(cli_provider=provider)
    model = resolve_model(resolved_provider, model_override=model_override)
    meta = {
        "enabled": resolved_mode != "deterministic",
        "mode": resolved_mode,
        "provider": resolved_provider,
        "called": False,
        "status": "disabled" if resolved_mode == "deterministic" else "skipped",
        "model": model,
        "duration_ms": 0,
        "fallback_used": resolved_mode != "active",
    }
    if resolved_mode == "deterministic":
        return None, meta

    stubbed = _stubbed_response()
    if stubbed is not None:
        meta.update({"called": True, "status": "stubbed"})
        return stubbed, meta

    if resolved_provider == "gemini":
        api_key = _env_lookup(("GEMINI_API_KEY", "GOOGLE_API_KEY"))
    else:
        api_key = _env_lookup(("LLM_WIKI_API_KEY", "GLM_API_KEY", "ZAI_API_KEY"))
    if not api_key:
        meta["status"] = "missing_api_key"
        return None, meta

    started = time.time()
    try:
        meta["called"] = True
        if resolved_provider == "gemini":
            parsed, provider_meta = _call_gemini_generate_content(
                api_key=api_key,
                model=model,
                system_prompt=system_prompt,
                payload=payload,
                timeout=timeout,
            )
        else:
            parsed, provider_meta = _call_glm_chat(
                api_key=api_key,
                base_url=_env_lookup(("LLM_WIKI_BASE_URL", "GLM_BASE_URL"), default=DEFAULT_BASE_URL),
                model=model,
                system_prompt=system_prompt,
                payload=payload,
                timeout=timeout,
            )
        meta.update(provider_meta)
        meta["status"] = "ok" if parsed else "empty"
        return parsed, meta
    except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError) as exc:
        meta["status"] = "failed"
        meta["error"] = short_text(exc, 220)
        return None, meta
    finally:
        meta["duration_ms"] = int((time.time() - started) * 1000)


def resolve_semantic_payload(
    *,
    mode: str,
    provider: str | None,
    system_prompt: str,
    payload: dict[str, Any],
    cache: dict[str, Any] | None,
    stable_id: str,
    timeout: float,
    model_override: str | None = None,
) -> tuple[dict[str, Any] | None, dict[str, Any]]:
    resolved_mode = semantic_mode(mode)
    resolved_provider = configured_semantic_provider(cli_provider=provider)
    model = resolve_model(resolved_provider, model_override=model_override)
    meta = {
        "enabled": resolved_mode != "deterministic",
        "mode": resolved_mode,
        "provider": resolved_provider,
        "called": False,
        "status": "disabled" if resolved_mode == "deterministic" else "skipped",
        "model": model,
        "duration_ms": 0,
        "fallback_used": resolved_mode != "active",
        "cache_status": "disabled" if resolved_mode == "deterministic" else "miss",
        "stable_id": stable_id,
    }
    if resolved_mode == "deterministic":
        return None, meta

    entries = cache.get("entries") if isinstance((cache or {}).get("entries"), dict) else {}
    entry = entries.get(stable_id) if isinstance(entries, dict) else None
    input_hash = semantic_input_hash(provider=resolved_provider, model=model, system_prompt=system_prompt, payload=payload)
    meta["input_hash"] = input_hash
    if entry and entry.get("input_hash") == input_hash and isinstance(entry.get("payload"), dict):
        meta["status"] = "cache_hit"
        meta["cache_status"] = "exact"
        meta["fallback_used"] = False
        return dict(entry["payload"]), meta

    stale_payload = dict(entry["payload"]) if entry and isinstance(entry.get("payload"), dict) else None
    fresh_payload, call_meta = call_semantic_llm(
        mode=resolved_mode,
        provider=resolved_provider,
        system_prompt=system_prompt,
        payload=payload,
        model_override=model_override,
        timeout=timeout,
    )
    meta.update(call_meta)
    meta["input_hash"] = input_hash
    if fresh_payload:
        meta["cache_status"] = "refresh" if stale_payload else "write"
        if cache is not None:
            cache.setdefault("entries", {})
            cache["entries"][stable_id] = {
                "input_hash": input_hash,
                "payload": fresh_payload,
                "provider": resolved_provider,
                "model": model,
                "updated_at": now_iso(),
            }
            cache["_dirty"] = True
        return fresh_payload, meta

    if stale_payload and resolved_mode == "active":
        meta["status"] = "stale_hit"
        meta["cache_status"] = "stale"
        meta["fallback_used"] = True
        return stale_payload, meta

    return None, meta


def merge_page_semantics(
    *,
    seed: dict[str, Any],
    deterministic: dict[str, Any],
    semantic_payload: dict[str, Any] | None,
    mode: str,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any] | None]:
    merged_seed = dict(seed)
    merged_content = dict(deterministic)
    if not semantic_payload:
        return merged_seed, merged_content, None

    canonical_label = str(semantic_payload.get("canonical_label") or "").strip()
    semantic_aliases = unique_strings(list(seed.get("aliases") or []) + list(semantic_payload.get("aliases") or []), limit=16)
    semantic_entity_type = str(semantic_payload.get("entity_type") or "").strip().lower()
    semantic_confidence = semantic_payload.get("confidence")
    semantic_notes = {
        "canonical_label": canonical_label or None,
        "decision": str(semantic_payload.get("decision") or "").strip().lower() or None,
        "reasoning_summary": short_text(semantic_payload.get("reasoning_summary") or "", 240) or None,
    }

    if semantic_aliases:
        merged_seed["aliases"] = semantic_aliases
    if semantic_entity_type in ALLOWED_PAGE_ENTITY_TYPES and not merged_seed.get("kg_entity_ids"):
        merged_seed["entity_type"] = semantic_entity_type
    if isinstance(semantic_confidence, (int, float)):
        confidence = float(semantic_confidence)
        merged_seed["confidence"] = round(min(max(confidence, 0.0), 1.0), 2)
    if canonical_label:
        merged_seed["semantic_canonical_label"] = canonical_label

    if semantic_mode(mode) == "active":
        if canonical_label and not merged_seed.get("kg_entity_ids"):
            merged_seed["label"] = canonical_label
        if semantic_payload.get("summary"):
            merged_content["summary"] = short_text(semantic_payload["summary"], 520)
        for key in ["facts", "relationships", "recent_signals", "open_questions"]:
            rows = [short_text(item, 260) for item in (semantic_payload.get(key) or []) if str(item).strip()]
            if rows:
                merged_content[key] = unique_strings(rows, limit=10)

    return merged_seed, merged_content, semantic_notes


def build_page_semantic_packet(seed: dict[str, Any], deterministic: dict[str, Any]) -> dict[str, Any]:
    return {
        "task": "resolve_enterprise_memory_page",
        "seed": seed,
        "deterministic_draft": deterministic,
        "instructions": {
            "return_json_only": True,
            "allowed_entity_types": sorted(ALLOWED_PAGE_ENTITY_TYPES),
            "constraints": [
                "Do not invent facts.",
                "Prefer canonical business labels when strongly supported.",
                "Return concise relationships and open questions only when grounded in evidence.",
            ],
        },
    }


def build_page_system_prompt() -> str:
    return (
        "You compile a BRM enterprise memory page. "
        "Return JSON only with keys: canonical_label, entity_type, aliases, confidence, "
        "summary, facts, relationships, recent_signals, open_questions, decision, reasoning_summary. "
        "Do not invent facts. Keep statements concise and evidence-bound."
    )


def merge_review_semantics(
    *,
    reviewed: dict[str, Any],
    semantic_payload: dict[str, Any] | None,
    auto_promote_types: set[str],
) -> tuple[dict[str, Any], dict[str, Any] | None]:
    merged = dict(reviewed)
    if not semantic_payload:
        return merged, None

    semantic_action = str(semantic_payload.get("action") or "").strip().lower()
    canonical_label = str(semantic_payload.get("canonical_label") or "").strip()
    semantic_reason = short_text(semantic_payload.get("reason") or semantic_payload.get("reasoning_summary") or "", 220)
    semantic_existing = semantic_payload.get("existing_match") if isinstance(semantic_payload.get("existing_match"), dict) else None
    semantic_confidence = semantic_payload.get("confidence")
    notes = {
        "action": semantic_action or None,
        "canonical_label": canonical_label or None,
        "reason": semantic_reason or None,
    }

    if canonical_label:
        merged["semantic_canonical_label"] = canonical_label
    if semantic_existing:
        merged["semantic_existing_match"] = semantic_existing

    if semantic_action == "already_known" and semantic_existing:
        merged["action"] = "already_known"
        merged["existing_match"] = {
            "name": semantic_existing.get("name"),
            "entityType": semantic_existing.get("entityType"),
            "confidence": semantic_existing.get("confidence"),
            "source": "semantic_match",
        }
        if semantic_reason:
            merged["reason"] = semantic_reason
        return merged, notes

    if semantic_action == "review" and merged.get("action") == "reject":
        merged["action"] = "review"
        if semantic_reason:
            merged["reason"] = semantic_reason
        return merged, notes

    if (
        semantic_action == "promote"
        and merged.get("action") == "review"
        and str(merged.get("object_type") or "") in auto_promote_types
        and float(merged.get("confidence") or semantic_confidence or 0) >= 0.8
    ):
        merged["action"] = "promote"
        if semantic_reason:
            merged["reason"] = semantic_reason
        return merged, notes

    return merged, notes


def build_review_semantic_packet(
    candidate: dict[str, Any],
    reviewed: dict[str, Any],
    source_family: str,
    *,
    candidate_entity_matches: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    return {
        "task": "review_kg_promotion_candidate",
        "source_family": source_family,
        "candidate": candidate,
        "deterministic_review": reviewed,
        "candidate_entity_matches": candidate_entity_matches or [],
        "instructions": {
            "return_json_only": True,
            "allowed_actions": sorted(ALLOWED_REVIEW_ACTIONS),
            "constraints": [
                "Never invent an existing KG match.",
                "Use already_known only when the candidate clearly maps to a known entity.",
                "Use candidate_entity_matches when they provide a plausible alias or identity clue.",
                "Use reject only for clear noise or non-durable signals.",
                "Be conservative with promote decisions.",
            ],
        },
    }


def build_review_system_prompt() -> str:
    return (
        "You review a BRM KG promotion candidate. "
        "Return JSON only with keys: action, canonical_label, existing_match, confidence, reason, reasoning_summary. "
        "Do not invent matches. Be conservative and prefer review when uncertain."
    )


def safe_slug(value: str | None) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", normalize_identity_label(value)).strip("-")
    return slug or "unknown"
