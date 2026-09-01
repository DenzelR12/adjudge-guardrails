# AdJudge Guardrails

An enterprise reference implementation for auditing, governing, and operationalizing AI-assisted creative-quality review. AdJudge measures human–LLM disagreement, detects systematic positivity bias, enforces evidence and freshness controls, routes high-risk judgments to humans, and supports tenant-safe analytics, incident forensics, remediation planning, and advertiser- and campaign-grounded review context.

## Problem

A fluent multimodal LLM rating or rationale is not evidence that its judgment matches expert creative review. AdJudge turns public human-versus-LLM evaluation data into a governed system: it independently computes metrics from versioned snapshots, blocks stale or unverifiable claims, and routes risky decisions to human reviewers.

## Who this serves

The guardrails answer an engineer's question — "may this ship?" — but the system is built for three audiences:

- Business engineers: what must pass before this judgment ships. The verification contract answers this deterministically.
- Engineering managers: who owns this outcome, and whether autonomy is being used or avoided. See [Ownership Signals](docs/ownership-signals.md).
- Client partners and industry leads: whether what is live can be trusted, and whether the technical work is protecting the business metric. Every publishable claim carries provenance, freshness status, and a named owner; see the [Insight Layer](docs/insight-layer.md) specification.

Guardrails decide what may ship; ownership signals show who is accountable for what shipped. Checks create the floor — visibility creates the consequence.

## Evaluation data and attribution

The initial benchmark uses a public dataset released by AdControlCenter and distributed via Hugging Face.

The publisher describes 500 real Facebook ads from 253 advertisers, with human-expert and Claude Sonnet 4.6 creative-quality judgments and model rationales. The source provides derived features, labels, and public Meta Ad Library identifiers (`ad_archive_id`); this repository does not redistribute original creative assets.

AdJudge does not claim ownership of the source ads or annotations. Its contribution is the independent evaluation, provenance, governance, review-routing, analytics, forensics, and remediation architecture around the public source.

## Source-reported finding

AdControlCenter reports 26.8% human–LLM agreement on image-quality ratings; the LLM rated 71.8% of ads good, while human experts rated 20.0% good. AdJudge treats those as source-reported benchmark statements, not live project metrics. Any AdJudge metric must be independently recomputed from a versioned snapshot and pass the verification policy before it may be stated as current.

## Scoring scope

AdJudge Guardrails currently focuses on auditing and operationalizing human-versus-LLM **creative-quality judgments**. It does not claim that a `good`, `fair`, or `bad` creative label predicts engagement, purchases, or other business outcomes.

The sixth brain adds advertiser- and campaign-level context so a reviewer can interpret a creative-quality judgment against a permitted account baseline, stated campaign objective, and category conventions. It does not make performance claims or override deterministic policy. The roadmap supports configurable and vertical-specific creative rubrics, plus separately validated performance-aware signals when legitimate outcome data and appropriate validation are available.

See [Scoring Scope and Roadmap](docs/scoring-scope-and-roadmap.md) and [Advertiser and Campaign Intelligence Brain](docs/advertiser-campaign-intelligence-brain.md) for definitions, limitations, and claim-gating rules.

## System capabilities

- Knowledge Brain: grounded policy and documentation retrieval.
- Metric Evidence Brain: source-versioned, freshness-controlled measurements.
- Operations Forensics Brain: event timelines, lineage, blast radius, and evidence-ranked hypotheses.
- Remediation Planner Brain: human-approved plans with risk, rollback, ownership, and measurable success criteria.
- Customer Analytics Brain: tenant-scoped semantic analytics, dashboards, and reports.
- Advertiser and Campaign Intelligence Brain: strictly tenant- and advertiser-scoped baselines, campaign objectives, category norms, and provenance-verified context for grounded review routing.

## Verification contract

| Status | Meaning | Answer policy |
|---|---|---|
| `verified` | Source, definition, and recomputation checks pass within SLA | May state the metric with provenance |
| `stale` | Previous result exceeds its freshness SLA | Label it stale; do not imply currency |
| `unverifiable` | Source, schema, definition, or recomputation cannot be validated | Block it from current factual claims |

## Enterprise principles

- Retrieval does not override deterministic policy or authorization.
- Metrics are governed data products with versioned definitions, sources, inputs, code, freshness SLAs, and audit history.
- Customer and advertiser context is security-trimmed at policy and database layers; cross-tenant or cross-advertiser retrieval fails closed.
- Data-contract failures do not silently publish replacement results.
- Root-cause outputs are hypotheses with cited evidence, not unsupported causal conclusions.
- Production changes, exports, policy changes, and customer-impacting actions require human approval.

See [architecture](docs/architecture.md), [metric governance](docs/metric-governance.md), the [six-brain platform](docs/six-brain-platform.md), [customer data governance](docs/customer-data-governance.md), and the [operations runbook](docs/runbook.md).

## Try it locally

A technical reviewer can run the local quality, freshness, and verification workflows from a clean environment:

```bash
git clone https://github.com/DenzelR12/adjudge-guardrails.git
cd adjudge-guardrails
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
make test
make freshness
make verify
```

On Windows PowerShell, activate the virtual environment with `.venv\Scripts\Activate.ps1`.

- See [Local Demo](docs/local-demo.md) for the guided walkthrough.
- See [Runnable Demo](docs/runnable-demo.md) for the end-to-end example.

### Reviewer checklist

The existing test suite covers analytics behavior, deterministic control-plane controls, dashboard-service behavior, demo-data handling, core guardrails, and orchestration. The local workflows exercise the same core claim: a metric is publishable only when its source, definition, recomputation, and freshness checks are verified.

The included sample registry is deliberately `unverifiable`. It is a demonstration of fail-closed behavior, not a measured result or a claim about current advertising performance.

## License

MIT.
