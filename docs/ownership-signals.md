# Ownership Signals: From Gates to Consequences

## Purpose

AdJudge Guardrails was built around enforcement: verification contracts, freshness gates, and fail-closed policy. Enforcement answers "may this ship?" It cannot answer the question leadership actually asks: "who owns this outcome, and is it healthy?"

This memo defines the ownership-signal layer: the mechanisms that make autonomy and accountability visible to engineering managers, industry managers, and client partners — the audiences responsible for overall performance.

## The motivation constraint

Tooling cannot manufacture motivation. An engineer who does not care about the outcome experiences a failing check as friction, not feedback. The design response is not more gates; it is making the job unambiguous and neglect attributable:

- Define done as "the outcome stayed healthy," not "the technical solution shipped."
- Make every override attributed and time-boxed, so autonomy leaves a paper trail.
- Publish the state of ownership on a predictable cadence, so consequences arrive as visibility before they arrive as escalation.

## Audiences and the questions they own

| Audience | Question | Signal |
|---|---|---|
| Business engineer | What must pass before this judgment ships? | Verification contract and guardrails (existing) |
| Engineering manager | Who owns this outcome, and is autonomy being used or avoided? | Decision-health digest, waiver register, autonomy metrics |
| Client partner / industry lead | Can I trust what is live, and is the work protecting the business metric? | Verified-freshness status with a named owner, shown next to the metric it protects |

## Signals

### Attributed waivers with expiry

Autonomy includes the right to override a check. Every override is recorded as a waiver with a named owner, an approver, a reason, a scope, and an expiry date. An expired waiver is treated as no waiver and is flagged in the digest. This converts quiet workarounds into explicit, time-bound decisions.

### Decision-health digest

A periodic, read-only report per domain: what is verified, what is stale, what is unverifiable, who the named owner is, and which waivers are open or expiring. It gives a manager a non-nagging way to see neglect while it is still cheap to fix. Specification: [Insight Layer](insight-layer.md).

### Autonomy metrics

Four measures make the autonomy goal itself observable over a quarter:

- Self-serve vs. escalate rate: how often teams resolve verification failures without escalation.
- Time-to-refresh: how long stale metrics remain stale.
- Exception half-life: how long waivers live before resolution or renewal.
- Verified-ownership coverage: percentage of published artifacts with a current, named owner.

A baseline, a trend, and a review cadence turn "more ownership" from a slogan into a measurable quarter.

## Definition of done

The mindset shift — from finishing the technical solution to owning the outcome — happens through the definition of done, not through exhortation. When guardrail status and the business metric it protects appear on the same surface with a named owner, shipping the solution is no longer sufficient; the outcome has to stay healthy.

## Non-goals

- Not a punishment dashboard. Signals exist to make ownership discussable, not to rank people.
- No new factual claims. The sample registry remains deliberately `unverifiable`; ownership signals report the state of the system, not real advertising performance.
- No weakening of existing controls. Waivers never bypass verification; they document an accepted, expiring exception.
