# AdJudge Guardrails

> A human-calibrated evaluation and review-routing system for multimodal ad-quality scoring. It combines a provenance-aware RAG second brain with deterministic freshness, metric-verification, and audit controls.

## Problem

Multimodal LLMs can accelerate creative review, but a fluent rating or rationale is not evidence that the judgment matches an expert reviewer. AdJudge measures human–LLM disagreement, detects high-risk false approvals, and routes uncertainty to humans instead of presenting unsupported results as current.

## What this reference architecture demonstrates

- Evidence-first RAG: answers are grounded in retrieved documents and structured provenance.
- Metric governance: every reported value has a definition, source/version, computation time, input hash, code version, freshness SLA, and status.
- Fail-closed decisioning: stale or unverifiable measured claims cannot be stated as current.
- Human-in-the-loop routing: policy sends risky or ambiguous judgments to expert review.
- Audit-ready observability: each decision retains the evidence, policy, model, and data-version identifiers that produced it.

## Architecture

```text
Sources -> contracts -> validation -> document index + metric registry
                                           |                 |
Question -> retrieval -> evidence assembly + verification -> policy gate -> cited answer / review queue
```

The RAG layer provides contextual retrieval. The verification layer independently decides whether a metric may be presented as current. Generation does not bypass that policy.

Read the [architecture](docs/architecture.md), [metric governance standard](docs/metric-governance.md), [data contracts](docs/data-contracts.md), and [operating model](docs/operating-model.md).

## Quick start

```bash
python -m pip install -e ".[dev]"
make test
make freshness
make verify
```

The included metric registry is intentionally marked `unverifiable`: it is a template, not a reported result. To publish a value as verified, supply the source snapshot/version, validate the schema, recompute using the documented definition, and record the input and code hashes.

## Dataset example

The initial adapter targets the Kaggle `adcontrolcenter/ad-creative-quality-human-vs-llm` dataset. Download it locally under the dataset terms; this repository does not redistribute source assets. The first benchmark evaluates agreement between human expert and LLM ratings. It does not claim to predict ROAS, conversions, or universal creative quality.

## Status model

| Status | Meaning | Answer policy |
|---|---|---|
| `verified` | Current source and deterministic checks pass | May state value with provenance |
| `stale` | Existing value exceeds its freshness SLA | Must label it stale |
| `unverifiable` | Missing/incompatible source or failed validation/recomputation | Must not state it as current |

## Enterprise transferability

The contracts and controls are domain-independent. Replace the ad-data adapter with product analytics, support cases, operational metrics, policy documents, or model-evaluation artifacts while preserving the same source contracts, verification release gates, access boundaries, and audit events.

## Roadmap

- [x] Typed metric provenance and freshness gate
- [x] Fail-closed verification CLI and CI workflow
- [ ] Kaggle ingestion adapter and schema contract
- [ ] Human–LLM agreement and false-approval analysis
- [ ] Agreement-risk model and review router
- [ ] Citation-first RAG retrieval service and reviewer interface
- [ ] Containerized deployment, RBAC, and telemetry adapter examples

## Security note

Never commit dataset assets, embeddings, access tokens, or production credentials. See the threat model before connecting enterprise sources.

## License

MIT.
