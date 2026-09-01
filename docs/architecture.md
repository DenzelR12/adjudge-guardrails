# Architecture

## Objective

AdJudge Guardrails is a reference architecture for AI-assisted multimodal creative review. It makes retrieval, metric freshness, verification, and routing explicit system concerns rather than implicit LLM behavior.

## Control plane and data plane

The data plane ingests source documents, datasets, model outputs, and review feedback. The control plane owns source contracts, metric definitions, freshness SLAs, routing thresholds, access policies, and audit retention. Keeping these responsibilities separate lets teams change a model or vector store without redefining what constitutes a valid metric.

```text
Sources -> adapters -> validation -> document index + metric registry
                                         |                 |
Question -> retrieval -> evidence bundle + deterministic verification
                                                    |
                                                    v
                                      routing policy -> answer / human queue / block
```

## Non-negotiable invariants

1. A generated answer may not elevate a stale or unverifiable metric into a current factual claim.
2. Metric definitions are versioned; changed filters, denominators, mappings, or computation code create a new definition version.
3. Source refresh failure preserves the last verified artifact but marks its status stale; it never silently publishes replacement data.
4. Every decision stores the source snapshot, evidence IDs, policy version, model version, timestamp, and route rationale.
5. Retrieval context is untrusted input. Source text cannot override system policy or authorize access.

## Enterprise implementation path

The local package is designed to evolve into independently deployable ingestion workers, a document/vector store, a metadata registry, a verification service, a policy decision point, and an audit sink. Production deployments should add identity-aware access control, tenant isolation, encryption, secret management, retention controls, and tamper-evident event storage.
