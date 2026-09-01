from dataclasses import dataclass
from datetime import datetime

ALLOWED_METRICS = {"reviewed_ads", "exact_agreement", "false_approval_rate"}
ALLOWED_DIMENSIONS = {"campaign_id", "platform", "creative_type", "review_route"}


@dataclass(frozen=True)
class AnalyticsRequest:
    tenant_id: str
    metrics: tuple[str, ...]
    dimensions: tuple[str, ...]
    start_at: datetime
    end_at: datetime


def validate_request(request: AnalyticsRequest) -> None:
    if not request.tenant_id:
        raise ValueError("tenant_id is required")
    if not set(request.metrics) <= ALLOWED_METRICS:
        raise ValueError("metric is not in the approved semantic catalog")
    if not set(request.dimensions) <= ALLOWED_DIMENSIONS:
        raise ValueError("dimension is not in the approved semantic catalog")
    if request.start_at >= request.end_at:
        raise ValueError("invalid time range")


def build_customer_query(request: AnalyticsRequest) -> tuple[str, dict]:
    validate_request(request)
    selections = list(request.dimensions) + list(request.metrics)
    sql = "SELECT " + ", ".join(selections) + " FROM dashboard_customer_daily WHERE customer_id = %(tenant_id)s"
    return sql, {"tenant_id": request.tenant_id}
