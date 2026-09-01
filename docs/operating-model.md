# Operating Model

## Ownership

- **Source owner:** provides data contract, access approval, and change notice.
- **Data steward:** owns quality checks, classification, retention, and source freshness.
- **Metric owner:** approves definition, denominator, SLA, and acceptable tolerance.
- **Model owner:** owns model/prompt versions and offline evaluation.
- **Policy owner:** approves routing thresholds and escalation behavior.
- **Reviewer lead:** owns reviewer guidance, adjudication quality, and override feedback.

## Operational lifecycle

1. Register source contract and metric definition.
2. Ingest immutable source snapshot; validate against contract.
3. Recompute metrics and record provenance.
4. Verify freshness and computation tolerance.
5. Index approved context and serve cited answers.
6. Apply routing policy and record the decision event.
7. Monitor review overrides, false approvals, coverage, latency, and freshness compliance.
8. Re-evaluate policies on a scheduled cadence or after material drift.

## Incident handling

A failed source check, schema change, or anomalous metric triggers a fail-closed status. The system preserves prior evidence for audit, suppresses affected current claims, opens an investigation, and requires explicit approval before a revised source contract or metric definition returns to verified service.
