<!-- sentinel:skip-file — hardcoded paths are fixture/registry/audit-narrative data for this repo's research workflow, not portable application configuration. Same pattern as push_all_repos.py and E156 workbook files. -->

# ProvenanceAtlas

ProvenanceAtlas is a new project derived from the `ResearchConstellation` portfolio snapshot, but with a different aim: make the lineage of the portfolio explicit instead of only making the inventory visible.

## Why this exists

The portfolio atlas tells you what is there and which projects still need triage. It does not yet show:

- what source artifact the portfolio came from
- which transformations turned that source into derived outputs
- where unresolved status states interrupt the lineage

ProvenanceAtlas fills that gap with a static PROV-style graph.

## What it produces

- `prov-graph.json` - entity, activity, and agent nodes with typed edges
- `data.json` and `data.js` - dashboard payloads
- `index.html` - human-facing lineage dashboard
- `e156-submission/` - paper, protocol, metadata, and reader page

## Rebuild

Run:

`python C:\Users\user\ProvenanceAtlas\scripts\build_provenance_atlas.py`

For a custom source file:

`python C:\Users\user\ProvenanceAtlas\scripts\build_provenance_atlas.py --source path\to\portfolio-data.json`

## Standards basis

This project is informed by the W3C PROV family of provenance models, but implemented as a lightweight JSON graph that stays easy to serve from GitHub Pages and easy to audit in a local folder.
