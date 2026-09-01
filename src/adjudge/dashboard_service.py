from datetime import datetime, timezone


def status_banner(status: str, source: str, definition_version: str) -> dict:
    if status not in {"verified", "stale", "unverifiable"}:
        raise ValueError("invalid status")
    return {"status": status.upper(), "source": source, "definition_version": definition_version, "generated_at": datetime.now(timezone.utc).isoformat()}


def report_metadata(tenant_id: str, start_at: str, end_at: str, status: str) -> dict:
    return {"tenant_id": tenant_id, "date_range": {"start": start_at, "end": end_at}, "source": "local_postgres_demo", "metric_definition_version": "1.0.0", "status": status.upper(), "generated_at": datetime.now(timezone.utc).isoformat()}
