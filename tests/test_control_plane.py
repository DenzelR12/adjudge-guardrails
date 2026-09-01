from datetime import datetime, timezone

from adjudge.control_plane import AuditEvent, TenantQuery, authorize_tenant_query
from adjudge.data_quality import validate_required_columns
from adjudge.lineage import LineageGraph


def test_event_hash_changes_when_chain_changes():
    one = AuditEvent("source_updated", "first", "run-1")
    two = AuditEvent("source_updated", "first", "run-1", previous_hash=one.digest())
    assert one.digest() != two.digest()


def test_required_column_contract_fails_closed():
    result = validate_required_columns([{"ad_id": "a"}], {"ad_id", "human_rating"})
    assert not result.valid


def test_tenant_query_requires_authorized_scope():
    query = TenantQuery("tenant-a", ("agreement",), datetime(2026, 1, 1, tzinfo=timezone.utc), datetime(2026, 1, 2, tzinfo=timezone.utc), "analyst")
    assert authorize_tenant_query(query, {"tenant-a"})
    assert not authorize_tenant_query(query, {"tenant-b"})


def test_lineage_reports_blast_radius():
    graph = LineageGraph()
    graph.link("source:v1", "metric:agreement")
    graph.link("metric:agreement", "dashboard:executive")
    assert graph.blast_radius("source:v1") == {"metric:agreement", "dashboard:executive"}
