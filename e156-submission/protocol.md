Mahmood Ahmad
Tahir Heart Institute
author@example.com

Protocol: ProvenanceAtlas - Static Portfolio Lineage Audit

This protocol describes a snapshot-first provenance audit using the bundled `data-source/portfolio-data.snapshot.json` copied from `ResearchConstellation`. Eligible records are all 134 indexed project rows across the 12 portfolio tiers preserved in that snapshot. The primary estimand is explicit lifecycle coverage in the provenance graph, defined as the proportion of project entities that retain an explicit lifecycle label instead of remaining unresolved. Secondary outputs will count graph nodes, edges, entity types, unresolved records by tier, and the concentration of lineage pressure across the portfolio. The build process will emit `prov-graph.json`, `data.json`, `data.js`, and a static dashboard that exposes entity-activity-agent structure without requiring a database or graph server. Activities will represent parsing, summarization, rendering, and paper packaging so downstream reviewers can trace how derived outputs were assembled from the bundled source. Anticipated limitations include no live filesystem provenance, no Git commit ingestion, no event timestamps beyond the build run, and persistent dependence on upstream status normalization.

Outside Notes

Type: protocol
Primary estimand: explicit lifecycle coverage in the provenance graph
App: ProvenanceAtlas v0.1
Code: repository root, scripts/build_provenance_atlas.py, prov-graph.json, and data-source/portfolio-data.snapshot.json
Date: 2026-03-29
Validation: DRAFT

References

1. PROV-Overview: An Overview of the PROV Family of Documents. W3C Recommendation; 2013.
2. Moreau L, Groth P, Hartig O, et al. The rationale of PROV. J Web Semantics. 2015;35:235-257.
3. Sandve GK, Nekrutenko A, Taylor J, Hovig E. Ten simple rules for reproducible computational research. PLoS Comput Biol. 2013;9:e1003285.

AI Disclosure

This protocol was drafted from versioned local artifacts and deterministic build logic. AI was used as a drafting and implementation assistant under author supervision, with the author retaining responsibility for scope, methods, and reporting choices.
