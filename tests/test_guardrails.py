from datetime import datetime, timedelta, timezone

from adjudge.metrics import MetricRecord, effective_status, may_state_as_current
from adjudge.routing import route_ad


def metric(computed_at, status="verified"):
    return MetricRecord(metric_id="agreement", definition_version="1.0.0", display_name="Agreement", value=0.5, unit="proportion", definition="Exact agreement.", source_id="source", source_version="v1", computed_at=computed_at, freshness_sla_hours=24, status=status, code_version="abc123", input_hash="sha256:abc")


def test_expired_metric_fails_closed():
    now = datetime.now(timezone.utc)
    record = metric(now - timedelta(hours=25))
    assert effective_status(record, now) == "stale"
    assert not may_state_as_current(record, now)


def test_unverifiable_metric_cannot_be_current():
    now = datetime.now(timezone.utc)
    record = metric(now, "unverifiable")
    assert not may_state_as_current(record, now)


def test_unverified_metric_requires_human_review():
    decision = route_ad("good", 0.99, 0.01, "stale")
    assert decision.route == "human_review"


def test_high_disagreement_risk_requires_human_review():
    decision = route_ad("good", 0.99, 0.70, "verified")
    assert decision.route == "human_review"


def test_low_risk_good_ad_can_be_approved():
    decision = route_ad("good", 0.90, 0.10, "verified")
    assert decision.route == "auto_approve"
