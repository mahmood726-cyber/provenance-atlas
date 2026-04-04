M. Mahmood

ProvenanceAtlas: Static Lineage Graphing for the C Drive Evidence Portfolio

Can a portfolio inventory also show how its evidence was transformed, not just what projects it contains? We reused the bundled ResearchConstellation snapshot containing 134 indexed projects across 12 tiers and converted it into a PROV-style entity-activity-agent graph. ProvenanceAtlas v0.1 emits project entities, tier entities, summary outputs, and explicit build activities so lineage remains inspectable in a static repository for downstream review. The generated graph contained 157 nodes and 439 edges, while explicit lifecycle coverage remained 38.1 percent (51 of 134 projects), leaving 83 unresolved records inside the lineage. The strongest provenance pressure came from tiers 10 and 12, which alone contributed 57 unresolved projects and concentrated most broken downstream status chains. This reframes the portfolio gap as a provenance problem: without frozen lifecycle labels, later packaging, dashboards, and exchange layers inherit ambiguity by design. The atlas clarifies derivation paths, but it does not inspect live filesystem events, Git history, or authorship beyond the bundled snapshot.

Outside Notes

Type: methods
Primary estimand: explicit lifecycle coverage in the provenance graph
Certainty: moderate
Validation: DRAFT
