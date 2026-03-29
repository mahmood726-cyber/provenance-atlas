from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = PROJECT_ROOT / "data-source" / "portfolio-data.snapshot.json"
DATA_JSON = PROJECT_ROOT / "data.json"
DATA_JS = PROJECT_ROOT / "data.js"
PROV_GRAPH_JSON = PROJECT_ROOT / "prov-graph.json"


def slugify(value: str) -> str:
    return re.sub(r"(^-|-$)", "", re.sub(r"[^a-z0-9]+", "-", value.lower()))


def load_payload(source_path: Path) -> dict[str, object]:
    return json.loads(source_path.read_text(encoding="utf-8"))


def add_node(nodes: list[dict[str, object]], node_id: str, node_type: str, label: str, **extra: object) -> None:
    node = {"id": node_id, "provType": node_type, "label": label}
    node.update(extra)
    nodes.append(node)


def add_edge(edges: list[dict[str, object]], source: str, target: str, relation: str) -> None:
    edges.append({"source": source, "target": target, "relation": relation})


def build_graph(payload: dict[str, object]) -> dict[str, object]:
    nodes: list[dict[str, object]] = []
    edges: list[dict[str, object]] = []
    overview = payload["overview"]
    tiers = payload["tiers"]
    portfolio = payload["portfolio"]

    add_node(
        nodes,
        "entity:snapshot",
        "Entity",
        "portfolio-data.snapshot.json",
        category="source",
        path=overview["sourcePath"],
    )
    add_node(nodes, "entity:summary", "Entity", "Provenance summary", category="derived")
    add_node(nodes, "entity:dashboard", "Entity", "index.html", category="derived")
    add_node(nodes, "entity:paper", "Entity", "e156-submission/paper.json", category="derived")
    add_node(nodes, "entity:graph", "Entity", "prov-graph.json", category="derived")

    add_node(nodes, "activity:parse", "Activity", "Parse snapshot")
    add_node(nodes, "activity:summarize", "Activity", "Summarize tiers and projects")
    add_node(nodes, "activity:render", "Activity", "Render dashboard payload")
    add_node(nodes, "activity:package", "Activity", "Package E156 bundle")

    add_node(nodes, "agent:author", "Agent", "Mahmood Ahmad", role="author")
    add_node(nodes, "agent:builder", "Agent", "build_provenance_atlas.py", role="software")

    add_edge(edges, "activity:parse", "entity:snapshot", "used")
    add_edge(edges, "activity:summarize", "entity:snapshot", "used")
    add_edge(edges, "activity:render", "entity:summary", "used")
    add_edge(edges, "activity:package", "entity:summary", "used")

    add_edge(edges, "activity:summarize", "entity:summary", "generated")
    add_edge(edges, "activity:render", "entity:dashboard", "generated")
    add_edge(edges, "activity:render", "entity:graph", "generated")
    add_edge(edges, "activity:package", "entity:paper", "generated")

    add_edge(edges, "activity:parse", "agent:builder", "wasAssociatedWith")
    add_edge(edges, "activity:summarize", "agent:builder", "wasAssociatedWith")
    add_edge(edges, "activity:render", "agent:builder", "wasAssociatedWith")
    add_edge(edges, "activity:package", "agent:builder", "wasAssociatedWith")
    add_edge(edges, "activity:package", "agent:author", "wasAssociatedWith")

    for tier in tiers:
        tier_id = f"entity:tier:{tier['key']}"
        add_node(
            nodes,
            tier_id,
            "Entity",
            tier["name"],
            category="tier",
            coveragePercent=float(str(tier["opportunity"]).split("%", 1)[0]),
            projectCount=tier["count"],
            needsTriage=int(tier["statusCounts"].get("needs-triage", 0)),
        )
        add_edge(edges, "activity:summarize", tier_id, "generated")
        add_edge(edges, tier_id, "entity:snapshot", "wasDerivedFrom")

    for project in portfolio:
        project_id = f"entity:project:{slugify(project['id'] + '-' + project['name'])}"
        add_node(
            nodes,
            project_id,
            "Entity",
            project["name"],
            category="project",
            tier=project["tierShortName"],
            status=project["statusLabel"],
            statusExplicit=project["statusExplicit"],
            path=project["path"],
        )
        add_edge(edges, "activity:parse", project_id, "generated")
        add_edge(edges, project_id, "entity:snapshot", "wasDerivedFrom")
        add_edge(edges, project_id, f"entity:tier:{project['tierKey']}", "specializationOf")

    entity_count = sum(1 for node in nodes if node["provType"] == "Entity")
    activity_count = sum(1 for node in nodes if node["provType"] == "Activity")
    agent_count = sum(1 for node in nodes if node["provType"] == "Agent")
    unresolved_count = sum(1 for project in portfolio if not project["statusExplicit"])

    return {
        "project": "ProvenanceAtlas",
        "generatedAt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "prefix": {"prov": "http://www.w3.org/ns/prov#"},
        "summary": {
            "nodeCount": len(nodes),
            "edgeCount": len(edges),
            "entityCount": entity_count,
            "activityCount": activity_count,
            "agentCount": agent_count,
            "trackedProjects": overview["trackedProjects"],
            "explicitStatusCount": overview["statusLabeled"],
            "explicitCoveragePercent": overview["explicitCoveragePercent"],
            "needsTriage": unresolved_count,
        },
        "nodes": nodes,
        "edges": edges,
    }


def build_dashboard_data(payload: dict[str, object], graph: dict[str, object]) -> dict[str, object]:
    tiers = [
        {
            "name": tier["shortName"],
            "fullName": tier["name"],
            "count": tier["count"],
            "needsTriage": int(tier["statusCounts"].get("needs-triage", 0)),
            "coveragePercent": float(str(tier["opportunity"]).split("%", 1)[0]),
        }
        for tier in payload["tiers"]
    ]
    project_type_counts = Counter(project["type"] for project in payload["portfolio"])
    explicit_status_counts = Counter(
        project["statusLabel"] for project in payload["portfolio"] if project["statusExplicit"]
    )
    unresolved_projects = [
        {
            "name": project["name"],
            "tier": project["tierShortName"],
            "type": project["type"],
            "path": project["path"],
        }
        for project in payload["portfolio"]
        if not project["statusExplicit"]
    ]

    return {
        "project": {
            "name": "ProvenanceAtlas",
            "version": "0.1.0",
            "generatedAt": graph["generatedAt"],
            "sourcePath": payload["overview"]["sourcePath"],
            "designBasis": [
                "W3C PROV style entity-activity-agent graph",
                "Static lineage dashboard",
                "Explicit unresolved status reporting",
            ],
        },
        "metrics": graph["summary"],
        "tierCoverage": sorted(tiers, key=lambda item: (-item["needsTriage"], item["coveragePercent"], item["name"])),
        "typeBreakdown": [
            {"type": item[0], "count": item[1]}
            for item in sorted(project_type_counts.items(), key=lambda pair: (-pair[1], pair[0]))
        ],
        "explicitStatusBreakdown": [
            {"status": item[0], "count": item[1]}
            for item in sorted(explicit_status_counts.items(), key=lambda pair: (-pair[1], pair[0]))
        ],
        "unresolvedProjects": unresolved_projects[:14],
        "activityFlow": [
            {"activity": "Parse snapshot", "detail": "Converts the bundled portfolio snapshot into project entities."},
            {"activity": "Summarize tiers and projects", "detail": "Derives tier-level and summary entities from the parsed source."},
            {"activity": "Render dashboard payload", "detail": "Emits static data and graph files for browser delivery."},
            {"activity": "Package E156 bundle", "detail": "Links the generated summary into the paper-facing capsule."},
        ],
    }


def write_outputs(data: dict[str, object], graph: dict[str, object]) -> None:
    DATA_JSON.write_text(json.dumps(data, indent=2), encoding="utf-8")
    DATA_JS.write_text("window.PROVENANCE_ATLAS_DATA = " + json.dumps(data, indent=2) + ";\n", encoding="utf-8")
    PROV_GRAPH_JSON.write_text(json.dumps(graph, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build ProvenanceAtlas artifacts.")
    parser.add_argument(
        "--source",
        help="Optional path to a portfolio-data.json file. Relative paths resolve from the repository root.",
    )
    args = parser.parse_args()

    source_path = Path(args.source) if args.source else DEFAULT_SOURCE
    if not source_path.is_absolute():
        source_path = PROJECT_ROOT / source_path
    if not source_path.exists():
        raise SystemExit(f"Source data not found: {source_path}")

    payload = load_payload(source_path)
    graph = build_graph(payload)
    data = build_dashboard_data(payload, graph)
    write_outputs(data, graph)
    summary = graph["summary"]
    print(
        "Built ProvenanceAtlas "
        f"({summary['nodeCount']} nodes, "
        f"{summary['edgeCount']} edges, "
        f"{summary['explicitCoveragePercent']}% explicit lifecycle coverage)."
    )


if __name__ == "__main__":
    main()
