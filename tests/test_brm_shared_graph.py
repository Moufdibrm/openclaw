from __future__ import annotations

import importlib.util
from pathlib import Path


SCRIPT_PATH = Path("/Users/moufdi/openclaw/scripts/brm-shared-graph.py")
SPEC = importlib.util.spec_from_file_location("brm_shared_graph", SCRIPT_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


def test_validate_graph_entry_accepts_new_entity_families() -> None:
    for entity_type in ("channel", "operation", "product", "application", "domain", "business_event"):
        errors, warnings = MODULE.validate_graph_entry(
            {
                "type": "entity",
                "name": f"Entity :: {entity_type}",
                "entityType": entity_type,
                "classification": "C2",
                "observations": ["ok"],
            },
            strict=True,
        )
        assert errors == []
        assert warnings == []


def test_validate_candidate_accepts_memory_curator_business_event() -> None:
    errors = MODULE.validate_candidate(
        {
            "schema_id": "brm.graph-candidate.v1",
            "candidate_id": "cand_memory_curator_test",
            "generated_at": "2026-05-10T08:00:00Z",
            "agent_id": "memory-curator",
            "protocol_id": "memory-curator.consolidation.v1",
            "summary": "Promote a curated business event split from a composite sender.",
            "entities": [
                {
                    "name": "Business event :: Patrick Philip Via Docusign",
                    "entityType": "business_event",
                    "classification": "C2",
                    "observations": ["Curated from repeated internal evidence."],
                }
            ],
            "relations": [],
        }
    )
    policy = MODULE.load_write_policy(Path("/Users/moufdi/openclaw/docs/reference/brm-harness/shared-graph-write-policy.json"))

    assert errors == []
    assert MODULE.validate_commit_actor("memory-curator", policy) == []


def test_validate_graph_entry_accepts_new_relation_families() -> None:
    for relation_type in ("mentions", "uses"):
        errors, warnings = MODULE.validate_graph_entry(
            {
                "type": "relation",
                "from": "A",
                "to": "B",
                "relationType": relation_type,
                "classification": "C2",
            },
            strict=True,
        )
        assert errors == []
        assert warnings == []


def test_validate_candidate_rejects_reported_in_provenance_relation() -> None:
    errors = MODULE.validate_candidate(
        {
            "schema_id": "brm.graph-candidate.v1",
            "candidate_id": "cand_reported_in_test",
            "generated_at": "2026-05-10T08:00:00Z",
            "agent_id": "jack-x",
            "protocol_id": "jack-x.memory-review-resolution",
            "summary": "Provenance-only relation should stay outside durable KG candidates.",
            "entities": [],
            "relations": [
                {
                    "from": "A",
                    "to": "Report",
                    "relationType": "reported_in",
                    "classification": "C2",
                }
            ],
        }
    )

    assert any("reported_in" in error for error in errors)
