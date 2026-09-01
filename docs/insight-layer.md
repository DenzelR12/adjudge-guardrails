# Insight Layer: `make report` Specification

## Goal

A read-only report command that composes the existing verification (`make verify`) and freshness (`make freshness`) outputs into a one-page ownership and decision-health digest for engineering managers and client partners.

The report changes who the system speaks to, not what it enforces. Guardrails keep deciding what may ship; the report shows who is accountable for what shipped.

## Inputs

- Metric registry (existing): metric definitions, sources, freshness SLAs, statuses.
- Verification results: the deterministic output of the verification policy.
- Freshness results: SLA evaluation per metric.
- Waiver registry (new, configuration-only): recorded exceptions to verification or freshness requirements.

## Output

A Markdown digest written to stdout, with an optional file output. Sections:

1. Status summary: counts of `verified`, `stale`, and `unverifiable` metrics.
2. Domain table: metric, named owner, status, last verified at, SLA, age.
3. Open waivers: owner, approver, reason, scope, expiry, with expired waivers flagged.
4. Escalations: stale or unverifiable metrics with no active waiver and no named owner.

## Waiver registry contract

Each waiver record carries:

| Field | Meaning |
|---|---|
| `id` | Stable waiver identifier |
| `metric` | The metric or artifact covered |
| `owner` | Person accountable for resolution |
| `approver` | Person who accepted the exception |
| `reason` | Why the exception exists |
| `created_at` | When the waiver was recorded |
| `expires_at` | When the waiver lapses |
| `scope` | The decisions the waiver covers |

Rules:

- An expired waiver is treated as no waiver and is flagged in the report.
- A waiver never converts an `unverifiable` metric into a publishable one; it documents an accepted exception to escalation timing.
- The waiver registry is configuration. A malformed registry fails closed: the report refuses to run rather than silently dropping waivers.

## Autonomy metrics

The report computes four trend measures per domain:

- Self-serve vs. escalate rate: verification failures resolved without escalation, divided by total failures.
- Time-to-refresh: median time a metric spends in `stale` before returning to `verified`.
- Exception half-life: median age of waivers at resolution or renewal.
- Verified-ownership coverage: share of published metrics with a current named owner.

## Design constraints

- Read-only: the report never mutates the registry, waivers, or verification state.
- Deterministic: identical inputs produce an identical digest.
- No new runtime dependencies: the report composes existing command outputs and a declarative waiver file.
- Audited: generating a report emits an audit event with the input versions used.

## Acceptance tests

- An expired waiver is flagged and excluded from active-waiver counts.
- A metric with no owner cannot be counted toward verified-ownership coverage.
- A malformed waiver registry aborts the report with a non-zero exit and no output mutation.
- The digest lists every `stale` and `unverifiable` metric exactly once.
- Running the report twice on unchanged inputs produces byte-identical output.

## Rollout

Implemented: `make report` composes the metric registry and waiver file into the digest above, and the acceptance tests run in the standard suite (`tests/test_report.py`). Verified-ownership coverage is computed today; the three history-dependent autonomy metrics report as not yet instrumented until decision-event history exists.
