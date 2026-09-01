from adjudge.dashboard_service import report_metadata, status_banner


def test_banner_normalizes_status():
    assert status_banner("stale", "source", "1.0")["status"] == "STALE"


def test_report_keeps_tenant_scope():
    report = report_metadata("tenant_acme", "2026-09-01", "2026-09-02", "verified")
    assert report["tenant_id"] == "tenant_acme"
    assert report["status"] == "VERIFIED"
