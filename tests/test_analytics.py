from datetime import datetime, timezone

import pytest

from adjudge.analytics import AnalyticsRequest, build_customer_query


def test_query_is_tenant_scoped_and_parameterized():
    request = AnalyticsRequest("tenant_acme", ("exact_agreement",), ("platform",), datetime(2026, 1, 1, tzinfo=timezone.utc), datetime(2026, 1, 2, tzinfo=timezone.utc))
    sql, params = build_customer_query(request)
    assert "customer_id = %(tenant_id)s" in sql
    assert params == {"tenant_id": "tenant_acme"}


def test_unapproved_metric_is_rejected():
    request = AnalyticsRequest("tenant_acme", ("drop table",), (), datetime(2026, 1, 1, tzinfo=timezone.utc), datetime(2026, 1, 2, tzinfo=timezone.utc))
    with pytest.raises(ValueError):
        build_customer_query(request)
