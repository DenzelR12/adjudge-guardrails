# Threat Model

## Primary risks and controls

| Risk | Control |
|---|---|
| Prompt injection in retrieved documents | Treat retrieved content as untrusted; separate retrieval from policy evaluation and never execute document instructions |
| Stale or silently changed sources | Snapshot IDs, schema contracts, freshness SLAs, scheduled verification, fail-closed status |
| Unsupported metric claims | Structured metric registry and deterministic `may_state_as_current` gate |
| Evaluation-data poisoning | Source ownership, immutable snapshots, hashes, review sampling, and anomaly detection |
| Data leakage | Least-privilege connectors, secret manager, classification labels, redaction, retention limits, and tenant isolation |
| Model overreliance | Human-review routes for low confidence, high disagreement risk, and all unverifiable metrics |
| Audit gaps | Append-only decision events containing source, evidence, model, policy, and timestamp identifiers |

This repository is a reference implementation. A production threat assessment must be completed for each deployment, data classification, jurisdiction, model provider, and integration boundary.
