#!/usr/bin/env python3
"""
BRM Shared Graph bridge.

Pragmatic control-plane tooling for:
- validating the shared graph
- hydrating a bounded slice into an agent brain
- seeding local Hermes memories per profile
- validating and committing reviewed graph candidates
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


HOME = Path.home()
DEFAULT_MEMORY_FILE = HOME / ".openclaw" / "knowledge-graph" / "memory.jsonl"
DEFAULT_HERMES_ROOT = HOME / ".brm-hermes" / "profiles"
DEFAULT_OPENCLAW_ROOT = HOME / ".openclaw"
DEFAULT_LEGACY_MAPPING_FILE = (
    HOME / "openclaw" / "docs" / "reference" / "brm-harness" / "shared-graph-legacy-mapping.json"
)
DEFAULT_WRITE_POLICY_FILE = (
    HOME / "openclaw" / "docs" / "reference" / "brm-harness" / "shared-graph-write-policy.json"
)
DEFAULT_CHANNEL_REGISTRY_FILE = HOME / "hermes-runtime" / "contracts" / "jack-x-channel-registry.json"

ENTITY_TYPES = {
    "agent",
    "brand",
    "business_event",
    "person",
    "company",
    "external_org",
    "team",
    "pole",
    "channel",
    "commerce_order",
    "domain",
    "operation",
    "product",
    "project",
    "mission",
    "application",
    "integration",
    "billing_record",
    "protocol_rule",
    "decision",
    "issue",
    "artifact_ref",
    "mission_ref",
    "workspace",
    "store",
    "task",
    "campaign",
}
RELATION_TYPES = {
    "assigned_to",
    "affiliated_with",
    "belongs_to",
    "depends_on",
    "governs",
    "hydrates",
    "includes",
    "informed_by",
    "member_of",
    "mentions",
    "owned_by",
    "references",
    "related_to",
    "responsible_for",
    "source_channel",
    "uses",
    "validated_as_alias_of",
    "validated_by",
    "works_on",
}
CLASSIFICATIONS = {"C1", "C2", "C3", "C4"}
PROHIBITED_CANDIDATE_ENTITY_TYPES = {"runtime_fact", "runtime_batch"}
PROHIBITED_CANDIDATE_RELATION_TYPES = {"derived_from", "reported_in"}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def is_non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and value.strip() != ""


def is_string_list(value: Any) -> bool:
    return isinstance(value, list) and all(is_non_empty_string(item) for item in value)


def load_jsonl(file_path: Path) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    if not file_path.exists():
        return entries

    with file_path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                entry = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{file_path}:{line_number}: invalid JSON: {exc}") from exc
            if not isinstance(entry, dict):
                raise ValueError(f"{file_path}:{line_number}: entry must be an object")
            entries.append(entry)
    return entries


def save_jsonl(file_path: Path, entries: list[dict[str, Any]]) -> None:
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with file_path.open("w", encoding="utf-8") as handle:
        for entry in entries:
            handle.write(json.dumps(entry, ensure_ascii=False) + "\n")


def read_json(file_path: Path) -> dict[str, Any]:
    with file_path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{file_path}: expected JSON object")
    return data


def stable_key(prefix: str, value: Any) -> str:
    digest = hashlib.sha256(str(value or "").encode("utf-8")).hexdigest()[:16]
    return f"{prefix}:{digest}"


def load_legacy_mapping(file_path: Path) -> dict[str, Any]:
    return read_json(file_path)


def load_write_policy(file_path: Path) -> dict[str, Any]:
    return read_json(file_path)


def validate_graph_entry(entry: dict[str, Any], *, strict: bool) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    entry_type = entry.get("type")

    if entry_type == "entity":
        if not is_non_empty_string(entry.get("name")):
            errors.append("entity missing non-empty name")
        if not is_non_empty_string(entry.get("entityType")):
            errors.append("entity missing entityType")
        elif entry["entityType"] not in ENTITY_TYPES:
            (errors if strict else warnings).append(f"entityType '{entry['entityType']}' not in BRM standard")
        if "classification" not in entry:
            (errors if strict else warnings).append("entity missing classification")
        elif entry["classification"] not in CLASSIFICATIONS:
            errors.append(f"entity classification '{entry['classification']}' invalid")
        if "observations" not in entry:
            errors.append("entity missing observations")
        elif not isinstance(entry["observations"], list):
            errors.append("entity observations must be a list")
        elif strict and not is_string_list(entry["observations"]):
            errors.append("entity observations must contain non-empty strings only")
        elif not strict and not all(isinstance(item, str) for item in entry["observations"]):
            warnings.append("entity observations should contain strings only")
    elif entry_type == "relation":
        if not is_non_empty_string(entry.get("from")):
            errors.append("relation missing from")
        if not is_non_empty_string(entry.get("to")):
            errors.append("relation missing to")
        if not is_non_empty_string(entry.get("relationType")):
            errors.append("relation missing relationType")
        elif entry["relationType"] not in RELATION_TYPES:
            (errors if strict else warnings).append(f"relationType '{entry['relationType']}' not in BRM standard")
        if "classification" not in entry:
            (errors if strict else warnings).append("relation missing classification")
        elif entry["classification"] not in CLASSIFICATIONS:
            errors.append(f"relation classification '{entry['classification']}' invalid")
    else:
        errors.append(f"entry type '{entry_type}' invalid")

    return errors, warnings


def local_brain_paths(agent_id: str, profile_id: str) -> dict[str, Path]:
    target_root = DEFAULT_HERMES_ROOT / profile_id / "memories"
    source_workspace = DEFAULT_OPENCLAW_ROOT / ("workspace" if agent_id == "jack" else f"workspace-{agent_id}")
    return {
        "source_memory": source_workspace / "MEMORY.md",
        "source_user": source_workspace / "USER.md",
        "target_memory": target_root / "MEMORY.md",
        "target_user": target_root / "USER.md",
    }


def build_default_memory(agent_id: str) -> str:
    title = agent_id.replace("-", " ").title()
    if agent_id == "jack":
        return "\n".join(
            [
                f"# {title} Local Brain",
                "",
                "## Current role",
                "",
                "- Jack is the BRM supervisor, not runtime proof.",
                "- Jack routes work, verifies outputs, and keeps MM status honest.",
                "- Jack must not trust child execution blindly.",
                "",
                "## Keep this small",
                "",
                "- store durable habits and operator rules only",
                "- do not duplicate shared graph facts here",
                "- do not turn this file into a transcript archive",
                "",
            ]
        ) + "\n"
    return "\n".join(
        [
            f"# {title} Local Brain",
            "",
            "## Current role",
            "",
            f"- {title} uses this file for compact profile-local memory only.",
            "- Shared company truth belongs in the BRM shared graph.",
            "- Large outputs, reports, and transcripts do not belong here.",
            "",
        ]
    ) + "\n"


def build_default_user() -> str:
    return "\n".join(
        [
            "# USER.md - About Your Human",
            "",
            "- **Name:** Moufdi",
            "- **What to call them:** Moufdi",
            "- **Timezone:** Europe/Paris",
            "- **Notes:** BRM operator; prioritize protocol clarity, auditability, and no fake done.",
            "",
        ]
    ) + "\n"


def should_use_default_user(source_user: Path) -> bool:
    if not source_user.exists():
        return True
    text = source_user.read_text(encoding="utf-8")
    placeholder_markers = [
        "- **Name:** ",
        "- **What to call them:** ",
        "- **Timezone:** ",
        "Learn about the person you're helping.",
    ]
    return all(marker in text for marker in placeholder_markers)


def command_validate(args: argparse.Namespace) -> int:
    entries = load_jsonl(Path(args.memory_file))
    errors: list[str] = []
    warnings: list[str] = []
    for index, entry in enumerate(entries, start=1):
        entry_errors, entry_warnings = validate_graph_entry(entry, strict=args.strict)
        errors.extend([f"line {index}: {message}" for message in entry_errors])
        warnings.extend([f"line {index}: {message}" for message in entry_warnings])

    report = {
        "memory_file": str(args.memory_file),
        "entry_count": len(entries),
        "error_count": len(errors),
        "warning_count": len(warnings),
        "errors": errors,
        "warnings": warnings,
        "strict": args.strict,
    }
    print(json.dumps(report, indent=2))
    return 1 if errors else 0


def entity_default_classification(
    entity_name: str,
    entity_type: str,
    mapping: dict[str, Any],
) -> str:
    name_overrides = mapping.get("entity_name_overrides", {})
    override = name_overrides.get(entity_name.lower())
    if isinstance(override, str) and override in CLASSIFICATIONS:
        return override

    default_map = mapping.get("default_classification_by_entity_type", {})
    default_value = default_map.get(entity_type)
    if isinstance(default_value, str) and default_value in CLASSIFICATIONS:
        return default_value
    return "C2"


def normalize_legacy_entries(
    entries: list[dict[str, Any]],
    mapping: dict[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    entity_type_map = mapping.get("entity_type_map", {})
    relation_type_map = mapping.get("relation_type_map", {})
    relation_default = mapping.get("relation_default_classification", "C2")

    normalized: list[dict[str, Any]] = []
    report: dict[str, Any] = {
        "entity_type_changes": {},
        "relation_type_changes": {},
        "classification_added": 0,
        "metadata_added": 0,
    }

    normalized_entities_by_name: dict[str, dict[str, Any]] = {}

    for entry in entries:
        current = dict(entry)
        if current.get("type") == "entity":
            original_type = str(current.get("entityType", ""))
            normalized_type = entity_type_map.get(original_type, original_type)
            if normalized_type != original_type:
                report["entity_type_changes"][f"{original_type}->{normalized_type}"] = (
                    report["entity_type_changes"].get(f"{original_type}->{normalized_type}", 0) + 1
                )
            current["entityType"] = normalized_type
            if current.get("classification") not in CLASSIFICATIONS:
                current["classification"] = entity_default_classification(
                    str(current.get("name", "")),
                    normalized_type,
                    mapping,
                )
                report["classification_added"] += 1
            metadata = current.get("metadata")
            if not isinstance(metadata, dict):
                metadata = {}
                report["metadata_added"] += 1
            metadata.setdefault("normalized_at", utc_now())
            if normalized_type != original_type:
                metadata.setdefault("legacy_entityType", original_type)
            current["metadata"] = metadata
            normalized_entities_by_name[str(current.get("name", "")).strip().lower()] = current
            normalized.append(current)
            continue

        if current.get("type") == "relation":
            original_type = str(current.get("relationType", ""))
            normalized_type = relation_type_map.get(original_type, original_type)
            if normalized_type != original_type:
                report["relation_type_changes"][f"{original_type}->{normalized_type}"] = (
                    report["relation_type_changes"].get(f"{original_type}->{normalized_type}", 0) + 1
                )
            current["relationType"] = normalized_type
            if current.get("classification") not in CLASSIFICATIONS:
                from_entity = normalized_entities_by_name.get(str(current.get("from", "")).strip().lower())
                to_entity = normalized_entities_by_name.get(str(current.get("to", "")).strip().lower())
                from_class = from_entity.get("classification") if isinstance(from_entity, dict) else None
                to_class = to_entity.get("classification") if isinstance(to_entity, dict) else None
                levels = {"C1": 1, "C2": 2, "C3": 3, "C4": 4}
                if from_class in levels and to_class in levels:
                    current["classification"] = from_class if levels[from_class] >= levels[to_class] else to_class
                else:
                    current["classification"] = relation_default if relation_default in CLASSIFICATIONS else "C2"
                report["classification_added"] += 1
            metadata = current.get("metadata")
            if not isinstance(metadata, dict):
                metadata = {}
                report["metadata_added"] += 1
            metadata.setdefault("normalized_at", utc_now())
            if normalized_type != original_type:
                metadata.setdefault("legacy_relationType", original_type)
            current["metadata"] = metadata
            normalized.append(current)
            continue

        normalized.append(current)

    report["entry_count"] = len(entries)
    return normalized, report


def search_entry(entry: dict[str, Any], query: str) -> bool:
    haystacks = [
        str(entry.get("name", "")),
        str(entry.get("from", "")),
        str(entry.get("to", "")),
        str(entry.get("entityType", "")),
        str(entry.get("relationType", "")),
    ]
    haystacks.extend([item for item in entry.get("observations", []) if isinstance(item, str)])
    joined = " ".join(haystacks).lower()
    return query.lower() in joined


def command_hydrate(args: argparse.Namespace) -> int:
    memory_file = Path(args.memory_file)
    entries = load_jsonl(memory_file)
    entity_names = [name.strip() for name in args.entity_name or [] if name.strip()]
    queries = [query.strip() for query in args.query or [] if query.strip()]

    matched_entities: dict[str, dict[str, Any]] = {}
    for entry in entries:
        if entry.get("type") != "entity":
            continue
        name = str(entry.get("name", "")).strip()
        if not name:
            continue
        if any(name.lower() == requested.lower() for requested in entity_names) or any(
            search_entry(entry, query) for query in queries
        ):
            matched_entities[name.lower()] = entry
            if len(matched_entities) >= args.limit:
                break

    matched_relations: list[dict[str, Any]] = []
    if matched_entities:
        selected_names = set(matched_entities.keys())
        for entry in entries:
            if entry.get("type") != "relation":
                continue
            from_name = str(entry.get("from", "")).strip().lower()
            to_name = str(entry.get("to", "")).strip().lower()
            if from_name in selected_names or to_name in selected_names:
                matched_relations.append(entry)

    brain = local_brain_paths(args.agent_id, args.profile_id)
    bundle = {
        "schema_id": "brm.brain-hydration.v1",
        "generated_at": utc_now(),
        "agent_id": args.agent_id,
        "profile_id": args.profile_id,
        "protocol_id": args.protocol_id,
        "queries": queries,
        "entity_names": entity_names,
        "local_brain": {
            "memory_path": str(brain["target_memory"]),
            "user_path": str(brain["target_user"]),
            "memory_exists": brain["target_memory"].exists(),
            "user_exists": brain["target_user"].exists(),
        },
        "shared_graph_slice": {
            "entity_count": len(matched_entities),
            "relation_count": len(matched_relations),
            "entities": list(matched_entities.values()),
            "relations": matched_relations,
        },
    }

    payload = json.dumps(bundle, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0


def command_seed_brain(args: argparse.Namespace) -> int:
    paths = local_brain_paths(args.agent_id, args.profile_id)
    target_memory = paths["target_memory"]
    target_user = paths["target_user"]
    target_memory.parent.mkdir(parents=True, exist_ok=True)

    report = {
        "agent_id": args.agent_id,
        "profile_id": args.profile_id,
        "memory_path": str(target_memory),
        "user_path": str(target_user),
        "memory_action": "skipped",
        "user_action": "skipped",
    }

    if not target_memory.exists() or args.force:
        if paths["source_memory"].exists():
            shutil.copyfile(paths["source_memory"], target_memory)
            report["memory_action"] = f"copied:{paths['source_memory']}"
        else:
            target_memory.write_text(build_default_memory(args.agent_id), encoding="utf-8")
            report["memory_action"] = "created:default"

    if not target_user.exists() or args.force:
        if paths["source_user"].exists() and not should_use_default_user(paths["source_user"]):
            shutil.copyfile(paths["source_user"], target_user)
            report["user_action"] = f"copied:{paths['source_user']}"
        else:
            target_user.write_text(build_default_user(), encoding="utf-8")
            report["user_action"] = "created:default"

    print(json.dumps(report, indent=2))
    return 0


def validate_candidate(candidate: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required_fields = [
        "schema_id",
        "candidate_id",
        "generated_at",
        "agent_id",
        "protocol_id",
        "summary",
        "entities",
        "relations",
    ]
    for field in required_fields:
        if field not in candidate:
            errors.append(f"candidate missing field '{field}'")

    if candidate.get("schema_id") != "brm.graph-candidate.v1":
        errors.append("candidate schema_id must be brm.graph-candidate.v1")

    if not isinstance(candidate.get("entities"), list):
        errors.append("candidate entities must be a list")
    else:
        for index, entity in enumerate(candidate["entities"], start=1):
            if not isinstance(entity, dict):
                errors.append(f"candidate entity {index} must be an object")
                continue
            merged = {"type": "entity", **entity}
            entry_errors, _ = validate_graph_entry(merged, strict=True)
            errors.extend([f"candidate entity {index}: {message}" for message in entry_errors])
            if entity.get("entityType") in PROHIBITED_CANDIDATE_ENTITY_TYPES:
                errors.append(
                    f"candidate entity {index}: entityType '{entity.get('entityType')}' is operational telemetry and cannot be committed to the enterprise KG"
                )
            entity_name = str(entity.get("name") or "").strip()
            if entity_name.startswith("Jack X ") and " batch " in entity_name:
                errors.append(f"candidate entity {index}: runtime batch entities belong to Jack X reports, not the enterprise KG")

    if not isinstance(candidate.get("relations"), list):
        errors.append("candidate relations must be a list")
    else:
        for index, relation in enumerate(candidate["relations"], start=1):
            if not isinstance(relation, dict):
                errors.append(f"candidate relation {index} must be an object")
                continue
            merged = {"type": "relation", **relation}
            entry_errors, _ = validate_graph_entry(merged, strict=True)
            errors.extend([f"candidate relation {index}: {message}" for message in entry_errors])
            if relation.get("relationType") in PROHIBITED_CANDIDATE_RELATION_TYPES:
                errors.append(
                    f"candidate relation {index}: relationType '{relation.get('relationType')}' belongs to the event/report layer, not the enterprise KG"
                )

    return errors


def validate_commit_actor(actor_agent_id: str | None, policy: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    allowed_commit_actors = policy.get("allowed_commit_actors", [])
    if not is_non_empty_string(actor_agent_id):
        errors.append("commit apply requires non-empty actor_agent_id")
        return errors
    if not isinstance(allowed_commit_actors, list) or not all(isinstance(item, str) for item in allowed_commit_actors):
        errors.append("write policy allowed_commit_actors must be a list of strings")
        return errors
    if actor_agent_id not in allowed_commit_actors:
        errors.append(f"actor_agent_id '{actor_agent_id}' not allowed to commit shared graph writes")
    return errors


def merge_candidate_metadata(current: dict[str, Any] | None, incoming: dict[str, Any] | None, actor_agent_id: str | None) -> dict[str, Any]:
    metadata = dict(current or {})
    if isinstance(incoming, dict):
        metadata.update(incoming)
    metadata["updated"] = utc_now()
    metadata["source"] = (incoming or {}).get("source", metadata.get("source", "graph-candidate"))
    if is_non_empty_string(actor_agent_id):
        metadata["reviewed_by"] = actor_agent_id
    elif "reviewed_by" not in metadata:
        metadata["reviewed_by"] = "unassigned"
    return metadata


def merge_entity(entries: list[dict[str, Any]], entity: dict[str, Any], actor_agent_id: str | None) -> str:
    entity_name = entity["name"].strip()
    entity_key = entity_name.lower()
    for existing in entries:
        if existing.get("type") == "entity" and str(existing.get("name", "")).strip().lower() == entity_key:
            existing_observations = [item for item in existing.get("observations", []) if isinstance(item, str)]
            incoming_observations = [item for item in entity.get("observations", []) if isinstance(item, str)]
            merged_observations = existing_observations[:]
            for observation in incoming_observations:
                if observation not in merged_observations:
                    merged_observations.append(observation)
            existing["entityType"] = entity["entityType"]
            existing["classification"] = entity["classification"]
            existing["observations"] = merged_observations
            existing["metadata"] = merge_candidate_metadata(
                existing.get("metadata") if isinstance(existing.get("metadata"), dict) else {},
                entity.get("metadata") if isinstance(entity.get("metadata"), dict) else {},
                actor_agent_id,
            )
            return "updated"

    incoming_metadata = entity.get("metadata") if isinstance(entity.get("metadata"), dict) else {}
    new_entity = {
        "type": "entity",
        "name": entity_name,
        "entityType": entity["entityType"],
        "classification": entity["classification"],
        "observations": entity["observations"],
        "metadata": merge_candidate_metadata(
            {"created": utc_now()},
            incoming_metadata,
            actor_agent_id,
        ),
    }
    entries.append(new_entity)
    return "inserted"


def merge_relation(entries: list[dict[str, Any]], relation: dict[str, Any], actor_agent_id: str | None) -> str:
    relation_key = (
        relation["from"].strip().lower(),
        relation["to"].strip().lower(),
        relation["relationType"],
    )
    for existing in entries:
        if existing.get("type") != "relation":
            continue
        existing_key = (
            str(existing.get("from", "")).strip().lower(),
            str(existing.get("to", "")).strip().lower(),
            str(existing.get("relationType", "")),
        )
        if existing_key == relation_key:
            existing["classification"] = relation["classification"]
            existing["metadata"] = merge_candidate_metadata(
                existing.get("metadata") if isinstance(existing.get("metadata"), dict) else {},
                relation.get("metadata") if isinstance(relation.get("metadata"), dict) else {},
                actor_agent_id,
            )
            return "updated"

    incoming_metadata = relation.get("metadata") if isinstance(relation.get("metadata"), dict) else {}
    new_relation = {
        "type": "relation",
        "from": relation["from"],
        "to": relation["to"],
        "relationType": relation["relationType"],
        "classification": relation["classification"],
        "metadata": merge_candidate_metadata(
            {"created": utc_now()},
            incoming_metadata,
            actor_agent_id,
        ),
    }
    entries.append(new_relation)
    return "inserted"


def command_commit_candidate(args: argparse.Namespace) -> int:
    candidate_path = Path(args.candidate)
    candidate = read_json(candidate_path)
    errors = validate_candidate(candidate)
    policy = load_write_policy(Path(args.policy_file))
    actor_agent_id = args.actor_agent_id
    if args.apply:
        errors.extend(validate_commit_actor(actor_agent_id, policy))
    if errors:
        print(json.dumps({"valid": False, "errors": errors}, indent=2))
        return 1

    memory_file = Path(args.memory_file)
    entries = load_jsonl(memory_file)
    report = {
        "valid": True,
        "apply": args.apply,
        "candidate_id": candidate["candidate_id"],
        "memory_file": str(memory_file),
        "policy_file": str(args.policy_file),
        "actor_agent_id": actor_agent_id,
        "entity_results": [],
        "relation_results": [],
    }

    for entity in candidate["entities"]:
        result = merge_entity(entries, entity, actor_agent_id)
        report["entity_results"].append({"name": entity["name"], "result": result})
    for relation in candidate["relations"]:
        result = merge_relation(entries, relation, actor_agent_id)
        report["relation_results"].append(
            {
                "from": relation["from"],
                "to": relation["to"],
                "relationType": relation["relationType"],
                "result": result,
            }
        )

    if args.apply:
        save_jsonl(memory_file, entries)

    print(json.dumps(report, indent=2))
    return 0


def kg_v2_metadata(current: dict[str, Any] | None, **extra: Any) -> dict[str, Any]:
    metadata = dict(current or {})
    metadata["kg_schema_version"] = 2
    for key, value in extra.items():
        if value is not None:
            metadata[key] = value
    return metadata


def canonical_entity(
    name: str,
    entity_type: str,
    observations: list[str],
    *,
    metadata: dict[str, Any] | None = None,
    classification: str = "C2",
) -> dict[str, Any]:
    clean_name = name.strip()
    return {
        "type": "entity",
        "name": clean_name,
        "entityType": entity_type,
        "classification": classification,
        "observations": [item for item in observations if str(item or "").strip()],
        "metadata": kg_v2_metadata(
            metadata,
            entity_id=(metadata or {}).get("entity_id") or stable_key(entity_type, clean_name.lower()),
        ),
    }


def canonical_relation(
    from_name: str,
    to_name: str,
    relation_type: str,
    *,
    metadata: dict[str, Any] | None = None,
    classification: str = "C2",
) -> dict[str, Any]:
    return {
        "type": "relation",
        "from": from_name.strip(),
        "to": to_name.strip(),
        "relationType": relation_type,
        "classification": classification,
        "metadata": kg_v2_metadata(metadata),
    }


def normalize_entry_v2(entry: dict[str, Any]) -> dict[str, Any] | None:
    entry_type = entry.get("type")
    if entry_type == "entity":
        name = str(entry.get("name") or "").strip()
        entity_type = str(entry.get("entityType") or "").strip()
        if not name or entity_type not in ENTITY_TYPES:
            return None
        observations = [str(item).strip() for item in entry.get("observations") or [] if str(item).strip()]
        metadata = entry.get("metadata") if isinstance(entry.get("metadata"), dict) else {}
        if entity_type == "person":
            aliases = metadata.get("aliases") if isinstance(metadata.get("aliases"), list) else []
            normalized_aliases = []
            for alias in [name, *aliases]:
                alias_text = str(alias or "").strip()
                if alias_text and alias_text not in normalized_aliases:
                    normalized_aliases.append(alias_text)
            metadata = {
                **metadata,
                "aliases": normalized_aliases,
                "identity_status": metadata.get("identity_status") or "unreviewed",
            }
        return canonical_entity(
            name,
            entity_type,
            observations or [f"{entity_type} carried forward during KG v2 migration."],
            metadata=metadata,
            classification=str(entry.get("classification") or "C2"),
        )
    if entry_type == "relation":
        from_name = str(entry.get("from") or "").strip()
        to_name = str(entry.get("to") or "").strip()
        relation_type = str(entry.get("relationType") or "").strip()
        if not from_name or not to_name or relation_type not in RELATION_TYPES:
            return None
        metadata = entry.get("metadata") if isinstance(entry.get("metadata"), dict) else {}
        return canonical_relation(
            from_name,
            to_name,
            relation_type,
            metadata=metadata,
            classification=str(entry.get("classification") or "C2"),
        )
    return None


def baseline_v2_entries() -> list[dict[str, Any]]:
    company = "BRM Agency"
    board = "Team :: BRM Board"
    entries = [
        canonical_entity(company, "company", ["Canonical company workspace for shared BRM operations."], metadata={"source": "kg-v2-baseline"}),
        canonical_entity(board, "team", ["Board/admin team coordinating shared BRM work."], metadata={"source": "kg-v2-baseline"}),
        canonical_entity("Pole :: Board", "pole", ["Governance and cross-company decision pole."], metadata={"source": "kg-v2-baseline"}),
        canonical_entity("Pole :: Brand/Store Operations", "pole", ["Brand, store, ecommerce, and operational execution pole."], metadata={"source": "kg-v2-baseline"}),
        canonical_entity("Pole :: Customer Experience", "pole", ["Customer, logistics, and support signal pole."], metadata={"source": "kg-v2-baseline"}),
        canonical_entity("Pole :: Growth/Marketing", "pole", ["Acquisition, email, influencer, and campaign signal pole."], metadata={"source": "kg-v2-baseline"}),
        canonical_relation(board, company, "belongs_to", metadata={"source": "kg-v2-baseline"}),
        canonical_relation("Pole :: Board", company, "belongs_to", metadata={"source": "kg-v2-baseline"}),
        canonical_relation("Pole :: Brand/Store Operations", company, "belongs_to", metadata={"source": "kg-v2-baseline"}),
        canonical_relation("Pole :: Customer Experience", company, "belongs_to", metadata={"source": "kg-v2-baseline"}),
        canonical_relation("Pole :: Growth/Marketing", company, "belongs_to", metadata={"source": "kg-v2-baseline"}),
    ]
    people = [
        ("Moufdi Biroum", ["Moufdi", "Moufdi Biroum"], "super_admin_owner"),
        ("Maé Bois", ["Maé", "Maé B", "Maé Bois"], "board_admin"),
        ("Fouad Biroum", ["Fouad", "Fouad Biroum"], "board_admin"),
        ("Najet", ["Najet", "Najet 🌹", "Najet de BRM AGENCY"], "brm_colleague"),
    ]
    for name, aliases, role in people:
        entries.append(
            canonical_entity(
                name,
                "person",
                [f"{name} is a validated BRM collaborator identity for Jack X identity resolution."],
                metadata={
                    "source": "kg-v2-baseline",
                    "aliases": aliases,
                    "identity_status": "validated",
                    "identity_confidence": 1.0,
                    "role": role,
                    "validated_by": "operator",
                },
            )
        )
        entries.append(canonical_relation(name, board, "member_of", metadata={"source": "kg-v2-baseline"}))
    return entries


def integration_name_for(channel: dict[str, Any]) -> str:
    transport = str(channel.get("transport") or "").strip().lower()
    surface = str(channel.get("surface") or "").strip().lower()
    if transport == "ms365" and surface == "mail":
        return "Integration :: Microsoft 365 Mail"
    if transport == "lark" and surface == "messages":
        return "Integration :: Lark Messages"
    if transport == "lark" and surface == "tables":
        return "Integration :: Lark Tables"
    if transport == "whatsapp":
        return "Integration :: WhatsApp"
    return f"Integration :: {transport or 'unknown'} {surface or 'surface'}".strip()


def channel_entries_from_registry(registry_file: Path) -> list[dict[str, Any]]:
    if not registry_file.exists():
        return []
    try:
        payload = read_json(registry_file)
    except Exception:
        return []
    entries: list[dict[str, Any]] = []
    seen_integrations: set[str] = set()
    for channel in payload.get("channels") or []:
        if not isinstance(channel, dict):
            continue
        channel_id = str(channel.get("channel_id") or "").strip()
        label = str(channel.get("label") or channel_id).strip()
        if not channel_id:
            continue
        channel_name = f"Channel :: {label}"
        integration_name = integration_name_for(channel)
        if integration_name not in seen_integrations:
            seen_integrations.add(integration_name)
            entries.append(
                canonical_entity(
                    integration_name,
                    "integration",
                    ["Registry-backed integration surface used by Jack X ingestion."],
                    metadata={
                        "source": "jack-x-channel-registry",
                        "transport": channel.get("transport"),
                        "surface": channel.get("surface"),
                    },
                )
            )
        entries.append(
            canonical_entity(
                channel_name,
                "channel",
                [f"Registry-backed {channel.get('transport')} {channel.get('surface')} channel: {label}."],
                metadata={
                    "source": "jack-x-channel-registry",
                    "registry_channel_id": channel_id,
                    "label": label,
                    "transport": channel.get("transport"),
                    "surface": channel.get("surface"),
                    "selectors": channel.get("selectors") if isinstance(channel.get("selectors"), dict) else {},
                    "schedule_key": channel.get("schedule_key"),
                },
            )
        )
        entries.append(canonical_relation(channel_name, integration_name, "uses", metadata={"source": "jack-x-channel-registry"}))
        entries.append(canonical_relation(channel_name, "BRM Agency", "belongs_to", metadata={"source": "jack-x-channel-registry"}))
    return entries


def migrate_entries_v2(entries: list[dict[str, Any]], registry_file: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    migrated: list[dict[str, Any]] = []
    skipped_count = 0
    for entry in entries:
        normalized = normalize_entry_v2(entry)
        if normalized is None:
            skipped_count += 1
            continue
        if normalized["type"] == "entity":
            merge_entity(migrated, normalized, "kg-v2-migration")
        else:
            merge_relation(migrated, normalized, "kg-v2-migration")

    added_entries = [*baseline_v2_entries(), *channel_entries_from_registry(registry_file)]
    for entry in added_entries:
        if entry["type"] == "entity":
            merge_entity(migrated, entry, "kg-v2-migration")
        else:
            merge_relation(migrated, entry, "kg-v2-migration")

    report = {
        "input_count": len(entries),
        "output_count": len(migrated),
        "skipped_count": skipped_count,
        "added_baseline_or_registry_count": len(added_entries),
        "entity_type_counts": {},
        "relation_type_counts": {},
    }
    for entry in migrated:
        if entry.get("type") == "entity":
            key = str(entry.get("entityType") or "<missing>")
            report["entity_type_counts"][key] = report["entity_type_counts"].get(key, 0) + 1
        elif entry.get("type") == "relation":
            key = str(entry.get("relationType") or "<missing>")
            report["relation_type_counts"][key] = report["relation_type_counts"].get(key, 0) + 1
    return migrated, report


def command_migrate_v2(args: argparse.Namespace) -> int:
    memory_file = Path(args.memory_file).expanduser()
    registry_file = Path(args.channel_registry).expanduser()
    try:
        entries = load_jsonl(memory_file)
    except ValueError as exc:
        print(
            json.dumps(
                {
                    "status": "invalid",
                    "memory_file": str(memory_file),
                    "channel_registry": str(registry_file),
                    "apply": False,
                    "read_error": str(exc),
                    "backup_path": None,
                },
                indent=2,
                ensure_ascii=False,
            )
        )
        return 1
    migrated, report = migrate_entries_v2(entries, registry_file)

    validation_errors: list[str] = []
    validation_warnings: list[str] = []
    for index, entry in enumerate(migrated, start=1):
        entry_errors, entry_warnings = validate_graph_entry(entry, strict=True)
        validation_errors.extend([f"line {index}: {message}" for message in entry_errors])
        validation_warnings.extend([f"line {index}: {message}" for message in entry_warnings])

    payload = {
        "status": "ok" if not validation_errors else "invalid",
        "memory_file": str(memory_file),
        "channel_registry": str(registry_file),
        "apply": args.apply,
        "backup_path": None,
        "report": report,
        "validation_error_count": len(validation_errors),
        "validation_warning_count": len(validation_warnings),
        "validation_errors": validation_errors,
        "validation_warnings": validation_warnings,
    }
    if args.output:
        output_path = Path(args.output).expanduser()
        save_jsonl(output_path, migrated)
        payload["output_path"] = str(output_path)
    if args.apply and not validation_errors:
        backup_path = memory_file.with_name(f"{memory_file.name}.backup.kg-v2.{datetime.now().strftime('%Y%m%d-%H%M%S')}")
        if memory_file.exists():
            shutil.copyfile(memory_file, backup_path)
        save_jsonl(memory_file, migrated)
        payload["backup_path"] = str(backup_path)

    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 1 if validation_errors else 0


def command_audit_legacy(args: argparse.Namespace) -> int:
    entries = load_jsonl(Path(args.memory_file))
    entity_type_counts: dict[str, int] = {}
    relation_type_counts: dict[str, int] = {}
    missing_classification = 0

    for entry in entries:
        if entry.get("type") == "entity":
            entity_type = str(entry.get("entityType", "<missing>"))
            entity_type_counts[entity_type] = entity_type_counts.get(entity_type, 0) + 1
            if entry.get("classification") not in CLASSIFICATIONS:
                missing_classification += 1
        elif entry.get("type") == "relation":
            relation_type = str(entry.get("relationType", "<missing>"))
            relation_type_counts[relation_type] = relation_type_counts.get(relation_type, 0) + 1
            if entry.get("classification") not in CLASSIFICATIONS:
                missing_classification += 1

    report = {
        "memory_file": str(args.memory_file),
        "entry_count": len(entries),
        "entity_type_counts": entity_type_counts,
        "relation_type_counts": relation_type_counts,
        "missing_classification": missing_classification,
        "mapping_file": str(args.mapping_file),
    }
    print(json.dumps(report, indent=2))
    return 0


def command_normalize_legacy(args: argparse.Namespace) -> int:
    memory_file = Path(args.memory_file)
    mapping = load_legacy_mapping(Path(args.mapping_file))
    entries = load_jsonl(memory_file)
    normalized, report = normalize_legacy_entries(entries, mapping)

    validation_errors: list[str] = []
    validation_warnings: list[str] = []
    for index, entry in enumerate(normalized, start=1):
        entry_errors, entry_warnings = validate_graph_entry(entry, strict=True)
        validation_errors.extend([f"line {index}: {message}" for message in entry_errors])
        validation_warnings.extend([f"line {index}: {message}" for message in entry_warnings])

    payload = {
        "memory_file": str(memory_file),
        "mapping_file": str(args.mapping_file),
        "apply": args.apply,
        "backup_path": None,
        "report": report,
        "validation_error_count": len(validation_errors),
        "validation_warning_count": len(validation_warnings),
        "validation_errors": validation_errors,
        "validation_warnings": validation_warnings,
    }

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        save_jsonl(output_path, normalized)
        payload["output_path"] = str(output_path)

    if args.apply:
        backup_path = memory_file.with_name(f"{memory_file.name}.backup.{datetime.now().strftime('%Y%m%d-%H%M%S')}")
        shutil.copyfile(memory_file, backup_path)
        save_jsonl(memory_file, normalized)
        payload["backup_path"] = str(backup_path)

    print(json.dumps(payload, indent=2))
    return 1 if validation_errors else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="BRM shared graph bridge")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser("validate", help="Validate the shared graph")
    validate_parser.add_argument("--memory-file", default=str(DEFAULT_MEMORY_FILE))
    validate_parser.add_argument("--strict", action="store_true")

    audit_parser = subparsers.add_parser("audit-legacy", help="Audit legacy graph types and missing classifications")
    audit_parser.add_argument("--memory-file", default=str(DEFAULT_MEMORY_FILE))
    audit_parser.add_argument("--mapping-file", default=str(DEFAULT_LEGACY_MAPPING_FILE))

    hydrate_parser = subparsers.add_parser("hydrate", help="Build a bounded hydration bundle")
    hydrate_parser.add_argument("--memory-file", default=str(DEFAULT_MEMORY_FILE))
    hydrate_parser.add_argument("--agent-id", required=True)
    hydrate_parser.add_argument("--profile-id", required=True)
    hydrate_parser.add_argument("--protocol-id", required=True)
    hydrate_parser.add_argument("--entity-name", action="append")
    hydrate_parser.add_argument("--query", action="append")
    hydrate_parser.add_argument("--limit", type=int, default=12)
    hydrate_parser.add_argument("--output")

    seed_parser = subparsers.add_parser("seed-brain", help="Seed local Hermes memories for a profile")
    seed_parser.add_argument("--agent-id", required=True)
    seed_parser.add_argument("--profile-id", required=True)
    seed_parser.add_argument("--force", action="store_true")

    commit_parser = subparsers.add_parser("commit-candidate", help="Validate and optionally merge a graph candidate")
    commit_parser.add_argument("--candidate", required=True)
    commit_parser.add_argument("--memory-file", default=str(DEFAULT_MEMORY_FILE))
    commit_parser.add_argument("--policy-file", default=str(DEFAULT_WRITE_POLICY_FILE))
    commit_parser.add_argument("--actor-agent-id")
    commit_parser.add_argument("--apply", action="store_true")

    normalize_parser = subparsers.add_parser("normalize-legacy", help="Normalize legacy graph types and classifications")
    normalize_parser.add_argument("--memory-file", default=str(DEFAULT_MEMORY_FILE))
    normalize_parser.add_argument("--mapping-file", default=str(DEFAULT_LEGACY_MAPPING_FILE))
    normalize_parser.add_argument("--output")
    normalize_parser.add_argument("--apply", action="store_true")

    migrate_v2_parser = subparsers.add_parser("migrate-v2", help="Migrate the shared graph in place to the KG v2 ontology")
    migrate_v2_parser.add_argument("--memory-file", default=str(DEFAULT_MEMORY_FILE))
    migrate_v2_parser.add_argument("--channel-registry", default=str(DEFAULT_CHANNEL_REGISTRY_FILE))
    migrate_v2_parser.add_argument("--output")
    migrate_v2_parser.add_argument("--apply", action="store_true")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "validate":
        return command_validate(args)
    if args.command == "audit-legacy":
        return command_audit_legacy(args)
    if args.command == "hydrate":
        return command_hydrate(args)
    if args.command == "seed-brain":
        return command_seed_brain(args)
    if args.command == "commit-candidate":
        return command_commit_candidate(args)
    if args.command == "normalize-legacy":
        return command_normalize_legacy(args)
    if args.command == "migrate-v2":
        return command_migrate_v2(args)

    parser.error(f"unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    sys.exit(main())
