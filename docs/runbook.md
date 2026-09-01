# Operations Runbook

## Before connecting a source

Register the source owner, classification, retention policy, access path, expected schema, source snapshot/version method, refresh SLA, and dependent metrics. Keep credentials in a secret manager only.

## Normal run

1. Start a uniquely identified, idempotent refresh run.
2. Read changes after the committed watermark up to a fixed cutoff.
3. Validate the source contract and data-quality thresholds.
4. Recompute metrics and write provenance.
5. Atomically publish verified dashboard materialization.
6. Advance watermark and emit audit event.

## Failure

Never advance the watermark after an extraction, validation, computation, or publication error. Mark affected results stale or unverifiable, retain the last verified artifact, alert the responsible owner, and record the failure event.

## Production controls

Use least-privilege identities, network boundaries, encryption, immutable run artifacts, role-based dashboard access, structured logs, trace identifiers, alert thresholds, and recovery drills.
