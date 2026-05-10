#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import unicodedata
from collections import defaultdict
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from typing import Any

from jack_x_reporting import (
    aggregate_channel_reports,
    ensure_dir,
    read_json,
    unique_strings,
    write_json,
)
from jack_x_semantic_memory import (
    build_page_semantic_packet,
    build_page_system_prompt,
    configured_semantic_provider,
    default_semantic_cache_file,
    flush_semantic_cache,
    load_semantic_cache,
    configured_semantic_mode,
    merge_page_semantics,
    normalize_identity_label,
    resolve_semantic_payload,
    safe_slug,
    semantic_cache_stable_id,
    semantic_cache_stats,
)


HOME = Path.home()
DEFAULT_RUNTIME_ROOT = HOME / ".openclaw" / "workspace-jack-x" / "runtime"
DEFAULT_OUTPUT_ROOT = HOME / ".openclaw" / "memory-wiki"
DEFAULT_MEMORY_PROJECTION_GLOB = HOME / ".openclaw" / "workspace-jack-x" / "logs" / "cron" / "db-analysis" / "*" / "memory-projection.json"

PAGE_SCHEMA_ID = "brm.memory-wiki.page.v1"
RUN_SCHEMA_ID = "brm.memory-wiki.compile-run.v1"

ENTITY_PAGE_DIR = {
    "person": "people",
    "project": "projects",
    "brand": "projects",
    "company": "companies",
    "business_event": "operations",
    "channel": "channels",
    "operation": "operations",
    "issue": "operations",
    "task": "operations",
    "decision": "operations",
    "ecosystem": "ecosystem",
}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def normalize_label(value: str | None) -> str:
    return normalize_identity_label(value)


def slugify(value: str | None) -> str:
    return safe_slug(value)


def short_text(value: Any, limit: int = 320) -> str:
    text = " ".join(str(value or "").split())
    if len(text) <= limit:
        return text
    return text[: max(0, limit - 1)].rstrip() + "..."


def read_channel_reports(report_root: Path) -> list[dict[str, Any]]:
    reports: list[dict[str, Any]] = []
    if not report_root.exists():
        return reports
    for path in sorted(report_root.glob("*.json")):
        try:
            payload = read_json(path)
        except Exception:
            continue
        if not isinstance(payload, dict):
            continue
        payload.setdefault("paths", {})
        if isinstance(payload["paths"], dict):
            payload["paths"].setdefault("channel_report", str(path))
        reports.append(payload)
    return reports


def latest_memory_projection_path() -> Path | None:
    paths = [path for path in HOME.glob(str(DEFAULT_MEMORY_PROJECTION_GLOB).replace(str(HOME) + "/", "")) if path.exists()]
    if not paths:
        return None
    return max(paths, key=lambda path: path.stat().st_mtime)


def load_memory_projection(path: Path | None) -> dict[str, Any]:
    selected = path or latest_memory_projection_path()
    if not selected or not selected.exists():
        return {"identity_map": {"people": []}, "entity_index": {}}
    try:
        return read_json(selected)
    except Exception:
        return {"identity_map": {"people": []}, "entity_index": {}}


def projection_entities(projection: dict[str, Any]) -> list[dict[str, Any]]:
    entities: list[dict[str, Any]] = []
    seen: set[str] = set()
    for entity_type, rows in (projection.get("entity_index") or {}).items():
        if not isinstance(rows, list):
            continue
        for row in rows:
            if not isinstance(row, dict):
                continue
            entity = dict(row)
            entity.setdefault("entity_type", str(entity.get("entityType") or entity_type).lower())
            entity_id = str(entity.get("entity_id") or entity.get("id") or entity.get("name") or "")
            if not entity_id or entity_id in seen:
                continue
            seen.add(entity_id)
            entities.append(entity)
    for person in (projection.get("identity_map") or {}).get("people") or []:
        if not isinstance(person, dict):
            continue
        entity = dict(person)
        entity.setdefault("entity_type", "person")
        entity.setdefault("entityType", "person")
        entity_id = str(entity.get("entity_id") or entity.get("id") or entity.get("name") or "")
        if not entity_id or entity_id in seen:
            continue
        seen.add(entity_id)
        entities.append(entity)
    return entities


def build_entity_index(projection: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    index: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for entity in projection_entities(projection):
        labels = [str(entity.get("name") or "")]
        labels.extend(str(alias) for alias in (entity.get("aliases") or []) if alias)
        for label in labels:
            normalized = normalize_label(label)
            if normalized:
                index[normalized].append(entity)
    return dict(index)


def find_projection_matches(label: str, entity_index: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    normalized = normalize_label(label)
    if not normalized:
        return []
    return entity_index.get(normalized) or []


def report_source_ref(report: dict[str, Any]) -> dict[str, Any]:
    scope = report.get("scope") or {}
    return {
        "channel_id": scope.get("primary_channel_id"),
        "channel_label": scope.get("primary_label"),
        "source_family": report.get("source_family"),
        "generated_at": report.get("generated_at"),
        "report_path": (report.get("paths") or {}).get("channel_report"),
        "source_artifact": report.get("source_artifact") or (report.get("paths") or {}).get("source_artifact"),
    }


def collect_evidence_by_label(channel_reports: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    evidence: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for report in channel_reports:
        source_ref = report_source_ref(report)
        macro = report.get("macro_summary") or {}
        for bucket, entity_type in [
            ("people", "person"),
            ("organizations", "company"),
            ("projects", "project"),
            ("brands", "project"),
            ("channels", "channel"),
            ("operations", "operation"),
            ("products", "product"),
            ("issues", "issue"),
            ("tasks", "task"),
            ("decisions", "decision"),
        ]:
            for label in macro.get(bucket) or []:
                key = normalize_label(label)
                if not key:
                    continue
                evidence[key].append(
                    {
                        "label": label,
                        "entity_type": entity_type,
                        "bucket": bucket,
                        "summary": short_text(report.get("report_summary"), 240),
                        "source": source_ref,
                    }
                )
    return dict(evidence)


def infer_page_type(label: str, evidence_rows: list[dict[str, Any]], projection_matches: list[dict[str, Any]]) -> str:
    if projection_matches:
        entity_type = str(projection_matches[0].get("entity_type") or projection_matches[0].get("entityType") or "").lower()
        if entity_type:
            return entity_type
    counts: dict[str, int] = defaultdict(int)
    for row in evidence_rows:
        counts[str(row.get("entity_type") or "entity")] += 1
    if counts:
        return sorted(counts.items(), key=lambda item: item[1], reverse=True)[0][0]
    return "entity"


def build_page_seed(
    *,
    label: str,
    evidence_rows: list[dict[str, Any]],
    projection_matches: list[dict[str, Any]],
) -> dict[str, Any]:
    entity_type = infer_page_type(label, evidence_rows, projection_matches)
    matched = projection_matches[0] if projection_matches else {}
    if matched.get("name"):
        label = str(matched["name"])
    observations = [
        short_text(item, 260)
        for item in (matched.get("observations") or [])[:8]
        if str(item).strip()
    ]
    source_refs = []
    recent_signals = []
    for row in evidence_rows[:12]:
        source = row.get("source") or {}
        source_ref = {
            "channel_id": source.get("channel_id"),
            "channel_label": source.get("channel_label"),
            "source_family": source.get("source_family"),
            "generated_at": source.get("generated_at"),
            "report_path": source.get("report_path"),
        }
        if source_ref not in source_refs:
            source_refs.append(source_ref)
        if row.get("summary"):
            recent_signals.append(short_text(row["summary"], 220))
    confidence = float(matched.get("confidence") or 0.0) if matched else 0.0
    if evidence_rows:
        confidence = max(confidence, min(0.9, 0.45 + 0.1 * len(evidence_rows)))
    return {
        "label": label,
        "entity_type": entity_type,
        "kg_entity_ids": unique_strings([str(item.get("entity_id") or item.get("id") or "") for item in projection_matches if item.get("entity_id") or item.get("id")]),
        "aliases": unique_strings([str(alias) for item in projection_matches for alias in (item.get("aliases") or []) if alias])[:12],
        "observations": observations,
        "recent_signals": unique_strings(recent_signals)[:8],
        "source_refs": source_refs[:12],
        "confidence": round(min(max(confidence, 0.0), 1.0), 2),
        "identity_status": matched.get("identity_status") or matched.get("status") or ("matched" if matched else "candidate"),
    }


def deterministic_page_content(seed: dict[str, Any]) -> dict[str, Any]:
    label = str(seed.get("label") or "Unknown")
    entity_type = str(seed.get("entity_type") or "entity")
    facts = list(seed.get("observations") or [])
    if not facts and seed.get("recent_signals"):
        facts = [f"Observed in recent {entity_type} evidence: {item}" for item in seed["recent_signals"][:3]]
    if not facts:
        facts = [f"{label} is a candidate {entity_type} surfaced by Jack X reports."]
    questions = []
    if not seed.get("kg_entity_ids"):
        questions.append("Confirm whether this candidate should become a durable KG entity.")
    if entity_type == "person" and seed.get("identity_status") in {"candidate", "unreviewed", None, ""}:
        questions.append("Confirm identity, role, and relationship to BRM before durable promotion.")
    return {
        "summary": short_text(f"{label} is tracked as {entity_type}. The page is compiled from Jack X evidence and KG projection data.", 420),
        "facts": unique_strings(facts)[:8],
        "relationships": [],
        "recent_signals": list(seed.get("recent_signals") or [])[:8],
        "open_questions": questions[:6],
    }


def render_markdown_page(seed: dict[str, Any], content: dict[str, Any], *, llm_meta: dict[str, Any], semantic_notes: dict[str, Any] | None = None) -> str:
    title = str(seed.get("label") or "Unknown")
    frontmatter = {
        "schema_id": PAGE_SCHEMA_ID,
        "title": title,
        "entity_type": seed.get("entity_type"),
        "confidence": seed.get("confidence"),
        "identity_status": seed.get("identity_status"),
        "kg_entity_ids": seed.get("kg_entity_ids") or [],
        "aliases": seed.get("aliases") or [],
        "updated_at": now_iso(),
        "llm_status": llm_meta.get("status"),
        "semantic_mode": llm_meta.get("mode"),
        "semantic_canonical_label": seed.get("semantic_canonical_label"),
    }
    if semantic_notes:
        frontmatter["semantic_decision"] = semantic_notes.get("decision")
    lines = ["---"]
    for key, value in frontmatter.items():
        lines.append(f"{key}: {json.dumps(value, ensure_ascii=False)}")
    lines.extend(["---", "", f"# {title}", "", "## Current Summary", "", str(content.get("summary") or "").strip(), ""])
    for heading, key in [
        ("Known Facts", "facts"),
        ("Relationships", "relationships"),
        ("Recent Signals", "recent_signals"),
        ("Open Questions", "open_questions"),
    ]:
        lines.extend([f"## {heading}", ""])
        rows = [str(item).strip() for item in (content.get(key) or []) if str(item).strip()]
        if rows:
            for item in rows:
                lines.append(f"- {item}")
        else:
            lines.append("- None recorded.")
        lines.append("")
    lines.extend(["## Source Evidence", ""])
    refs = seed.get("source_refs") or []
    if refs:
        for ref in refs:
            label = ref.get("channel_label") or ref.get("channel_id") or ref.get("source_family") or "source"
            generated = ref.get("generated_at") or "unknown-date"
            report_path = ref.get("report_path") or "missing-report-path"
            lines.append(f"- {label} ({generated}) -> `{report_path}`")
    else:
        lines.append("- No channel report source attached.")
    lines.append("")
    return "\n".join(lines)


def page_path(output_root: Path, entity_type: str, label: str) -> Path:
    folder = ENTITY_PAGE_DIR.get(entity_type, "entities")
    return output_root / "pages" / folder / f"{slugify(label)}.md"


def kg_operation_for_page(seed: dict[str, Any], path: Path, *, semantic_notes: dict[str, Any] | None = None) -> dict[str, Any]:
    label = str(seed.get("label") or "").strip()
    entity_type = str(seed.get("entity_type") or "entity")
    confidence = float(seed.get("confidence") or 0)
    action = "link_existing" if seed.get("kg_entity_ids") else "upsert_candidate"
    status = "candidate" if action == "upsert_candidate" or confidence < 0.88 else "ready"
    if semantic_notes and semantic_notes.get("decision") in {"review", "merge_candidate"}:
        status = "candidate"
    basis = json.dumps({"label": label, "entity_type": entity_type, "path": str(path)}, sort_keys=True)
    return {
        "operation_id": f"kgop_{sha256(basis.encode('utf-8')).hexdigest()[:16]}",
        "action": action,
        "status": status,
        "entity_type": entity_type,
        "label": label,
        "confidence": round(confidence, 2),
        "kg_entity_ids": seed.get("kg_entity_ids") or [],
        "source_page": str(path),
        "source_refs": seed.get("source_refs") or [],
        "review_required": status != "ready",
        "semantic_notes": semantic_notes or None,
    }


def is_page_worthy(seed: dict[str, Any]) -> bool:
    label = str(seed.get("label") or "").strip()
    entity_type = str(seed.get("entity_type") or "entity")
    normalized = normalize_label(label)
    if not normalized or len(normalized) < 3:
        return False
    if seed.get("kg_entity_ids"):
        return True
    if normalized in {"unknown", "unknown sender", "no sender", "none", "n a"}:
        return False
    if "@_user" in label or "user_" in normalized:
        return False
    if entity_type == "person" and normalized.startswith("cli "):
        return False
    if len(label) > 110 and entity_type not in {"project", "company", "channel"}:
        return False
    if entity_type in {"person", "project", "brand", "company", "channel", "product", "operation", "decision"}:
        return True
    if entity_type in {"issue", "task"}:
        source_families = {
            str((ref or {}).get("source_family") or "")
            for ref in (seed.get("source_refs") or [])
            if isinstance(ref, dict)
        }
        return len(label) <= 90 and bool(source_families & {"lark_messages", "whatsapp", "lark_tables"})
    return False


def page_priority(seed: dict[str, Any]) -> tuple[float, str]:
    entity_type = str(seed.get("entity_type") or "entity")
    type_weight = {
        "project": 100,
        "brand": 98,
        "person": 92,
        "company": 88,
        "channel": 82,
        "operation": 70,
        "product": 68,
        "decision": 66,
        "issue": 45,
        "task": 42,
    }.get(entity_type, 20)
    kg_weight = 40 if seed.get("kg_entity_ids") else 0
    source_weight = min(20, 3 * len(seed.get("source_refs") or []))
    confidence_weight = 20 * float(seed.get("confidence") or 0)
    return (type_weight + kg_weight + source_weight + confidence_weight, str(seed.get("label") or ""))


def compile_pages(
    *,
    channel_reports: list[dict[str, Any]],
    projection: dict[str, Any],
    output_root: Path,
    max_pages: int,
    semantic_mode: str,
    semantic_provider: str,
    semantic_cache: dict[str, Any],
    llm_timeout: float,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, int]]:
    aggregated = aggregate_channel_reports(channel_reports)
    evidence = collect_evidence_by_label(aggregated.get("latest_reports") or channel_reports)
    entity_index = build_entity_index(projection)

    page_labels = set(evidence.keys())
    macro = aggregated.get("macro_summary") or {}
    for bucket in ["projects", "brands", "people", "channels", "operations", "issues", "tasks", "decisions"]:
        for label in macro.get(bucket) or []:
            key = normalize_label(label)
            if key:
                page_labels.add(key)
    for entity in projection_entities(projection):
        entity_type = str(entity.get("entity_type") or entity.get("entityType") or "").lower()
        if entity_type not in {"person", "project", "brand", "company", "channel", "application", "integration"}:
            continue
        key = normalize_label(str(entity.get("name") or ""))
        if key:
            page_labels.add(key)

    seeds: list[dict[str, Any]] = []
    for key in sorted(page_labels):
        rows = evidence.get(key) or []
        matches = find_projection_matches(key, entity_index)
        label = str((rows[0] or {}).get("label") if rows else (matches[0].get("name") if matches else key)).strip()
        seed = build_page_seed(label=label, evidence_rows=rows, projection_matches=matches)
        if is_page_worthy(seed):
            seeds.append(seed)

    seeds.sort(key=page_priority, reverse=True)

    page_rows: list[dict[str, Any]] = []
    kg_operations: list[dict[str, Any]] = []
    semantic_stats = {
        "fresh_calls": 0,
        "cache_hits": 0,
        "stale_hits": 0,
        "failures": 0,
    }
    for seed in seeds[:max_pages]:
        deterministic = deterministic_page_content(seed)
        llm_payload, llm_meta = resolve_semantic_payload(
            mode=semantic_mode,
            provider=semantic_provider,
            system_prompt=build_page_system_prompt(),
            payload=build_page_semantic_packet(seed, deterministic),
            cache=semantic_cache,
            stable_id=semantic_cache_stable_id(
                "page",
                f"{seed.get('entity_type') or 'entity'}:{seed.get('kg_entity_ids') or []}:{seed.get('label') or ''}",
            ),
            timeout=llm_timeout,
        )
        if llm_meta.get("called"):
            semantic_stats["fresh_calls"] += 1
        if llm_meta.get("status") == "cache_hit":
            semantic_stats["cache_hits"] += 1
        elif llm_meta.get("status") == "stale_hit":
            semantic_stats["stale_hits"] += 1
        elif llm_meta.get("status") == "failed":
            semantic_stats["failures"] += 1
        merged_seed, content, semantic_notes = merge_page_semantics(
            seed=seed,
            deterministic=deterministic,
            semantic_payload=llm_payload,
            mode=semantic_mode,
        )
        label = str(merged_seed.get("label") or "unknown")
        path = page_path(output_root, str(merged_seed.get("entity_type") or "entity"), label)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render_markdown_page(merged_seed, content, llm_meta=llm_meta, semantic_notes=semantic_notes), encoding="utf-8")
        operation = kg_operation_for_page(merged_seed, path, semantic_notes=semantic_notes)
        page_rows.append(
            {
                "page_id": f"{merged_seed.get('entity_type')}:{slugify(label)}",
                "title": label,
                "entity_type": merged_seed.get("entity_type"),
                "path": str(path),
                "confidence": merged_seed.get("confidence"),
                "summary": content.get("summary"),
                "aliases": merged_seed.get("aliases") or [],
                "facts": list(content.get("facts") or [])[:6],
                "relationships": list(content.get("relationships") or [])[:6],
                "recent_signals": list(content.get("recent_signals") or [])[:6],
                "open_questions": list(content.get("open_questions") or [])[:6],
                "kg_entity_ids": merged_seed.get("kg_entity_ids") or [],
                "source_refs": merged_seed.get("source_refs") or [],
                "source_families": sorted(
                    {
                        str((ref or {}).get("source_family") or "").strip()
                        for ref in (merged_seed.get("source_refs") or [])
                        if isinstance(ref, dict) and str((ref or {}).get("source_family") or "").strip()
                    }
                ),
                "source_ref_count": len(merged_seed.get("source_refs") or []),
                "llm": llm_meta,
                "semantic": semantic_notes,
                "kg_operation_id": operation["operation_id"],
            }
        )
        kg_operations.append(operation)
    return page_rows, kg_operations, semantic_stats


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile Jack X reports into a bounded enterprise memory wiki.")
    parser.add_argument("--runtime-root", default=str(DEFAULT_RUNTIME_ROOT))
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument("--memory-projection", type=Path)
    parser.add_argument("--max-pages", type=int, default=40)
    parser.add_argument("--use-llm", action="store_true")
    parser.add_argument("--semantic-mode", choices=["deterministic", "shadow", "active"])
    parser.add_argument("--semantic-provider", choices=["gemini", "glm"])
    parser.add_argument("--semantic-cache-file", type=Path, default=default_semantic_cache_file())
    parser.add_argument("--llm-timeout", type=float, default=6.0)
    args = parser.parse_args()

    runtime_root = Path(args.runtime_root).expanduser().resolve()
    output_root = ensure_dir(Path(args.output_root).expanduser().resolve())
    channel_reports = read_channel_reports(runtime_root / "channel-reports")
    projection = load_memory_projection(args.memory_projection)
    semantic_mode = configured_semantic_mode(cli_mode=args.semantic_mode)
    semantic_provider = configured_semantic_provider(cli_provider=args.semantic_provider)
    if args.use_llm and semantic_mode == "deterministic":
        semantic_mode = "active"
    semantic_cache = load_semantic_cache(args.semantic_cache_file)
    generated_at = now_iso()
    run_id = f"memwiki_{generated_at.replace(':', '').replace('-', '')}_{sha256(str(runtime_root).encode('utf-8')).hexdigest()[:8]}"

    pages, kg_operations, semantic_stats = compile_pages(
        channel_reports=channel_reports,
        projection=projection,
        output_root=output_root,
        max_pages=max(1, args.max_pages),
        semantic_mode=semantic_mode,
        semantic_provider=semantic_provider,
        semantic_cache=semantic_cache,
        llm_timeout=max(1.0, args.llm_timeout),
    )
    flush_semantic_cache(semantic_cache)
    aggregated = aggregate_channel_reports(channel_reports)
    manifest = {
        "schema_id": RUN_SCHEMA_ID,
        "run_id": run_id,
        "generated_at": generated_at,
        "agent_id": "jack-x",
        "compiler": "llm-wiki",
        "runtime_root": str(runtime_root),
        "output_root": str(output_root),
        "source_report_count": len(channel_reports),
        "selected_channel_count": len((aggregated.get("latest_reports") or [])),
        "memory_projection": str(args.memory_projection or latest_memory_projection_path() or ""),
        "llm_enabled": semantic_mode != "deterministic",
        "semantic_mode": semantic_mode,
        "semantic_provider": semantic_provider,
        "semantic_cache_file": str(default_semantic_cache_file(args.semantic_cache_file)),
        "semantic_cache_stats": semantic_cache_stats(semantic_cache),
        "semantic_run_stats": semantic_stats,
        "page_count": len(pages),
        "pages": pages,
        "kg_operations": kg_operations,
        "review_items": [item for item in kg_operations if item.get("review_required")],
        "policy": {
            "raw_db_access": "not_direct_default",
            "raw_db_rule": "LLM Wiki compiles Jack X reports and source refs; bounded DB refresh must be requested through Jack X evidence windows.",
            "kg_write_rule": "No direct KG mutation; only candidate operations or links to existing KG ids.",
        },
    }
    manifest_path = ensure_dir(output_root / "runs") / f"{run_id}.json"
    write_json(manifest_path, manifest)
    latest_path = output_root / "latest.json"
    write_json(latest_path, manifest)
    print(
        json.dumps(
            {
                "status": "ok",
                "run_id": run_id,
                "source_report_count": len(channel_reports),
                "selected_channel_count": manifest["selected_channel_count"],
                "page_count": len(pages),
                "review_count": len(manifest["review_items"]),
                "semantic_mode": semantic_mode,
                "semantic_provider": semantic_provider,
                "semantic_run_stats": semantic_stats,
                "manifest": str(manifest_path),
                "latest_manifest": str(latest_path),
                "output_root": str(output_root),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
