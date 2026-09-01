# SQL Refresh and Dashboard Architecture

The dashboard exposes verified evaluation and review-routing metrics; it is not a direct view over arbitrary source rows.

## Refresh paths

- An event from a document or data update starts an idempotent refresh run.
- A scheduled reconciliation detects missed events, late warehouse loads, and schema drift.
- Only successful extraction, validation, recomputation, provenance write, and materialization advance the watermark.

## Watermark rule

Use a fixed run cutoff and query changes after the committed watermark. Failed extraction, validation, computation, or publication preserves the prior verified artifact and does not advance the watermark.

## Dashboard contract

Every metric displays value, verification status, data-as-of time, source version, definition version, freshness deadline, and run ID. The UI must visibly distinguish `verified`, `stale`, and `unverifiable` values.

Postgres and BigQuery implement the same source contract so policy and dashboard behavior remain database-independent.
