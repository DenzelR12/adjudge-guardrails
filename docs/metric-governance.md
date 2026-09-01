# Metric Governance Standard

## Required provenance

A metric is a governed data product, not a number in a report. It requires: stable ID, definition and definition version, value/unit, source/version, computation time, freshness SLA, code version, input hash, and status.

## Status and response policy

| Status | Interpretation | Permitted behavior |
|---|---|---|
| `verified` | Required provenance exists and deterministic verification is within SLA | State as current and attach provenance |
| `stale` | A prior calculation exists but exceeds its freshness SLA | Label as stale; do not imply currency |
| `unverifiable` | Source, schema, definition, or recomputation fails | Block it from current metric claims |

## Release gate

A metric-bearing report must fail release when required source fields are unavailable, schema validation fails, a snapshot cannot be identified, computation fails, or recomputed output differs from the stored value beyond approved tolerance. Definition changes require review and a new metric version; historical records remain immutable.
