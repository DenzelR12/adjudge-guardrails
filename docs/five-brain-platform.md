# Six-Brain Platform and Control Plane

## Intelligence layers

1. Knowledge: grounded policy and documentation retrieval.
2. Metric evidence: current, provenance-verified measurements.
3. Operations forensics: ordered event timeline, blast radius, and evidence-ranked hypotheses.
4. Remediation planner: human-approved plans with risk, owner, rollback, and success criteria.
5. Customer analytics: tenant-scoped, governed analytics search, dashboards, and reports.
6. Advertiser and campaign intelligence: tenant- and advertiser-scoped account baselines, campaign objectives, category norms, and separately validated performance context for grounded review routing.

## Sixth-brain boundary

The Advertiser and Campaign Intelligence Brain gives reviewers bounded account context; it does not convert creative-quality labels into causal business-outcome claims. It is subject to the platform's strictest tenant and advertiser authorization scope. Context is checked against the same `verified`, `stale`, and `unverifiable` evidence contract used by the Metric Evidence Brain. See [Advertiser and Campaign Intelligence Brain](advertiser-campaign-intelligence-brain.md).

## Control-plane services

Data contracts, data quality, identity/access, audit lineage, experimentation, and FinOps are deterministic services that constrain all brains. They are not autonomous decision makers.

## Authority rule

Brains may retrieve, assess, route, and recommend. Production changes, data exports, source-contract changes, policy changes, and customer-impacting actions require explicit human approval and an audit event.
