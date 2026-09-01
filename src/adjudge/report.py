import hashlib
from datetime import datetime, timezone

from pydantic import BaseModel, model_validator

from adjudge.metrics import MetricRecord, effective_status


class WaiverRecord(BaseModel):
    waiver_id: str
    metric_id: str
    owner: str
    approver: str
    reason: str
    created_at: datetime
    expires_at: datetime
    scope: str

    @model_validator(mode="after")
    def expires_after_creation(self):
        if self.expires_at <= self.created_at:
            raise ValueError("waiver expiry must be after creation")
        return self


def _is_unowned(owner: str | None) -> bool:
    return not owner or owner.startswith("REPLACE_WITH")


def _digest(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:12]


def build_report(records: list[MetricRecord], waivers: list[WaiverRecord], registry_text: str, waivers_text: str, now: datetime | None = None) -> str:
    now = now or datetime.now(timezone.utc)
    statuses = [(record, effective_status(record, now)) for record in records]
    counts = {status: sum(1 for _, s in statuses if s == status) for status in ("verified", "stale", "unverifiable")}
    active = [waiver for waiver in waivers if waiver.expires_at > now]
    expired = [waiver for waiver in waivers if waiver.expires_at <= now]
    waived_ids = {waiver.metric_id for waiver in active}
    escalations = [
        (record, status)
        for record, status in statuses
        if status != "verified" and record.metric_id not in waived_ids and _is_unowned(record.owner)
    ]
    owned = sum(1 for record in records if not _is_unowned(record.owner))
    coverage = (100.0 * owned / len(records)) if records else 0.0

    lines = [
        "# Decision-Health Report",
        "",
        f"Registry sha256: {_digest(registry_text)} | Waivers sha256: {_digest(waivers_text)} | As of: {now.isoformat()}",
        "",
        "## Status summary",
        "",
        f"- verified: {counts['verified']}",
        f"- stale: {counts['stale']}",
        f"- unverifiable: {counts['unverifiable']}",
        "",
        "## Metrics",
        "",
        "| Metric | Owner | Status | Computed at | SLA (hours) |",
        "|---|---|---|---|---|",
    ]
    for record, status in statuses:
        owner = record.owner if not _is_unowned(record.owner) else "—"
        lines.append(f"| `{record.metric_id}` | {owner} | {status} | {record.computed_at.isoformat()} | {record.freshness_sla_hours} |")

    lines += ["", f"## Active waivers ({len(active)})", ""]
    if active:
        lines += ["| Waiver | Metric | Owner | Approver | Expires |", "|---|---|---|---|---|"]
        for waiver in active:
            lines.append(f"| `{waiver.waiver_id}` | `{waiver.metric_id}` | {waiver.owner} | {waiver.approver} | {waiver.expires_at.isoformat()} |")
    else:
        lines.append("- None")

    lines += ["", f"## Expired waivers ({len(expired)}) — flagged", ""]
    if expired:
        lines += ["| Waiver | Metric | Owner | Approver | Expired |", "|---|---|---|---|---|"]
        for waiver in expired:
            lines.append(f"| `{waiver.waiver_id}` | `{waiver.metric_id}` | {waiver.owner} | {waiver.approver} | {waiver.expires_at.isoformat()} |")
    else:
        lines.append("- None")

    lines += ["", "## Escalations", ""]
    if escalations:
        for record, status in escalations:
            lines.append(f"- `{record.metric_id}` — {status}; no active waiver; no named owner")
    else:
        lines.append("- None")

    lines += [
        "",
        "## Autonomy metrics",
        "",
        f"- Verified-ownership coverage: {coverage:.1f}% ({owned}/{len(records)} metrics with a named owner)",
        "- Self-serve vs. escalate rate: requires decision-event history (not yet instrumented)",
        "- Time-to-refresh: requires status-transition history (not yet instrumented)",
        "- Exception half-life: requires waiver-resolution history (not yet instrumented)",
        "",
    ]
    return "\n".join(lines)
