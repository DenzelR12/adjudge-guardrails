# Advertiser and Campaign Intelligence Brain

## Purpose

The Advertiser and Campaign Intelligence Brain is the sixth intelligence layer in AdJudge Guardrails. It provides tenant-scoped context that lets the platform distinguish a creative judgment made against a global rubric from a judgment grounded in the advertiser's own history, campaign objective, and category conventions.

It does not turn creative-quality labels into performance claims. The current scoring system remains an audit of human-versus-LLM creative-quality judgments. Performance-aware signals are a separate roadmap capability and must be independently validated before they can influence a production decision.

## Why a sixth brain

The first five brains answer whether a judgment is rubric-consistent, policy-compliant, measurable, explainable, and remediable. They cannot answer whether a score is unusual or actionable for the specific advertiser and campaign being reviewed.

A global rubric can flatten meaningful context:

- Awareness, conversion, retention, and lead-generation campaigns optimize for different creative behavior.
- A category convention can look weak under a generic quality rubric while remaining normal for that vertical.
- An absolute score cannot tell a reviewer whether a creative has materially changed from an advertiser's historical baseline.

This brain supplies context for review routing and analyst interpretation. It never overrides a deterministic policy, an authorization decision, or a verified metric.

## Scoped data contract

| Domain | Allowed examples | Not allowed |
|---|---|---|
| Advertiser baseline | Historical creative-quality distributions, rubric-versioned scores, known disagreement clusters | Cross-tenant advertiser history |
| Campaign context | Declared objective, lifecycle phase, creative format, approved category | Inferred sensitive attributes |
| Category norms | Versioned, aggregate category benchmarks and documented conventions | Unverifiable claims about category outcomes |
| Performance linkage | Separately validated, provenance-verified aggregate signals when available | Causal performance claims from creative labels alone |

Every record must carry `tenant_id`, `advertiser_id`, source version, metric definition version, `measured_at`, and freshness status.

## Access and isolation

- The brain has the strictest authorization boundary in the platform.
- Retrieval is filtered by live tenant and advertiser authorization before content enters the retrieval window.
- Tenant filtering is enforced at both the policy layer and database/query layer.
- A caller evaluating advertiser A cannot retrieve advertiser B's context, even if both have semantically similar content.
- Permission revocation is fail-closed: if authorization or tenant resolution cannot be verified, the brain returns no context and records an audit event.

## Freshness and verification

Campaign state and account baselines can drift. Before advertiser context is supplied to a reviewer or model, the metric evidence controls determine whether each source is `verified`, `stale`, or `unverifiable`.

| Status | Brain behavior |
|---|---|
| `verified` | Context may be used with source and metric provenance |
| `stale` | Context is labeled stale and may not be presented as current |
| `unverifiable` | Context is withheld from factual claims and escalated for review |

## Output contract

The brain returns a bounded context packet, not an autonomous decision:

```json
{
  "tenant_id": "tenant_123",
  "advertiser_id": "advertiser_456",
  "campaign_id": "campaign_789",
  "authorization": "verified",
  "context_status": "verified",
  "campaign_objective": "lead_generation",
  "baseline_reference": "versioned metric reference",
  "provenance": ["source_version", "metric_definition", "measured_at"],
  "limitations": ["creative quality does not establish business outcome"]
}
```

The review router can use the packet to prioritize human attention, explain a score relative to the permitted account baseline, and flag a material context gap. Any customer-impacting action remains subject to explicit human approval and an audit event.

## Acceptance tests

- Cross-advertiser retrieval is denied and logged.
- A revoked principal loses access without waiting for index refresh.
- Stale or unverifiable context cannot support a current factual statement.
- The context packet includes provenance, freshness status, and the creative-quality limitation.
- Campaign context cannot override policy, authorization, or human-approval controls.
