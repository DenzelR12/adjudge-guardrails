# AdJudge Guardrails

An enterprise reference implementation for auditing, governing, and operationalizing AI-assisted creative-quality review. AdJudge measures human–LLM disagreement, detects systematic positivity bias, enforces evidence and freshness controls, routes high-risk judgments to humans, and supports tenant-safe analytics, incident forensics, and remediation planning.

## Problem

A fluent multimodal LLM rating or rationale is not evidence that its judgment matches expert creative review. AdJudge turns public human-versus-LLM evaluation data into a governed system: it independently computes metrics from versioned snapshots, blocks stale or unverifiable claims, and routes risky decisions to human reviewers.

## Evaluation data and attribution

The initial benchmark uses a public dataset released by AdControlCenter and distributed via Hugging Face.

The publisher describes 500 real Facebook ads from 253 advertisers, with human-expert and Claude Sonnet 4.6 creative-quality judgments and model rationales. The source provides derived features, labels, and public Meta Ad Library identifiers (`ad_archive_id`); this repository does not redistribute original creative assets.

AdJudge does not claim ownership of the source ads or annotations. Its contribution is the independent evaluation, provenance, governance, review-routing, analytics, forensics, and remediation architecture around the public source.

## Source-reported finding

AdControlCenter reports 26.8% human–LLM agreement on image-quality ratings; the LLM rated 71.8% of ads good, while human experts rated 20.0% good. AdJudge treats those as source-reported benchmark statements, not live project metrics. Any AdJudge metric must be independently recomputed from a versioned snapshot and pass the verification policy before it may be stated as current.

## Scoring scope

AdJudge Guardrails currently focuses on auditing and operationalizing human-versus-LLM **creative-quality judgments**. It does not claim that a `good`, `fair`, or `bad` creative label predicts engagement, purchases, or other business outcomes.

The roadmap supports configurable and vertical-specific creative rubrics, as well as separately validated performance-aware signals when legitimate outcome data and appropriate validation are available.

See [Scoring Scope and Roadmap](docs/scoring-scope-and-roadmap.md) for the definitions, limitations, and claim-gating rules.

## System capabilities

- Knowledge Brain: grounded policy and documentation retrieval.
- Metric Evidence Brain: source-versioned, freshness-controlled measurements.
- Operations Forensics Brain: event timelines, lineage, blast radius, and evidence-ranked hypotheses.
- Remediation Planner Brain: human-approved plans with risk, rollback, ownership, and measurable success criteria.
- Customer Analytics Brain: tenant-scoped semantic analytics, dashboards, and reports.

## Verification contract

| Status | Meaning | Answer policy |
|---|---|---|
| `verified` | Source, definition, and recomputation checks pass within SLA | May state the metric with provenance |
| `stale` | Previous result exceeds its freshness SLA | Label it stale; do not imply currency |
| `unverifiable` | Source, schema, definition, or recomputation cannot be validated | Block it from current factual claims |

## Enterprise principles

- Retrieval does not override deterministic policy or authorization.
- Metrics are governed data products with versioned definitions, sources, inputs, code, freshness SLAs, and audit history.
- Data-contract failures do not silently publish replacement results.
- Customer analytics must enforce tenant scope at the policy and database layers.
- Root-cause outputs are hypotheses with cited evidence, not unsupported causal conclusions.
- Production changes, exports, policy changes, and customer-impacting actions require human approval.

See architecture, metric governance, five-brain platform, customer data governance, and operations runbook.

## Quick start

```bash
python -m pip install -e ".[dev]"
make test
make freshness
make verify
```

The sample registry is deliberately unverifiable. It is a template, not a measured result.

## License

MIT.
