import json
import sys
from datetime import datetime, timedelta, timezone

from adjudge.cli import main
from adjudge.metrics import MetricRecord
from adjudge.report import WaiverRecord, build_report

NOW = datetime(2026, 9, 1, tzinfo=timezone.utc)


def metric(metric_id, status="verified", owner="metric-owner", computed_at=None):
    return MetricRecord(metric_id=metric_id, definition_version="1.0.0", display_name=metric_id, value=0.5, unit="proportion", definition="d", source_id="s", source_version="v1", computed_at=computed_at or NOW, freshness_sla_hours=24, status=status, owner=owner, code_version="abc123", input_hash="sha256:abc")


def waiver(metric_id, created_at, expires_at):
    return WaiverRecord(waiver_id=f"w-{metric_id}", metric_id=metric_id, owner="owner", approver="approver", reason="accepted risk", created_at=created_at, expires_at=expires_at, scope="demo")


def test_expired_waiver_is_flagged_and_excluded_from_active():
    record = waiver("m1", NOW - timedelta(days=40), NOW - timedelta(days=10))
    report = build_report([metric("m1")], [record], "reg", "wai", NOW)
    assert "## Active waivers (0)" in report
    assert "## Expired waivers (1) — flagged" in report
    assert "`w-m1`" in report


def test_metric_without_owner_is_excluded_from_coverage():
    report = build_report([metric("m1"), metric("m2", owner=None)], [], "reg", "wai", NOW)
    assert "Verified-ownership coverage: 50.0% (1/2 metrics with a named owner)" in report


def test_malformed_waiver_registry_fails_closed(tmp_path, capsys, monkeypatch):
    registry = tmp_path / "registry.json"
    registry.write_text(json.dumps([json.loads(metric("m1").model_dump_json())]))
    waivers = tmp_path / "waivers.json"
    waivers.write_text(json.dumps([{"waiver_id": "broken"}]))
    monkeypatch.setattr(sys, "argv", ["cli", "report", "--registry", str(registry), "--waivers", str(waivers), "--as-of", NOW.isoformat()])
    assert main() == 2
    assert capsys.readouterr().out == ""


def test_every_unhealthy_metric_is_escalated_exactly_once():
    stale_metric = metric("m-stale", computed_at=NOW - timedelta(hours=49), owner=None)
    bad_metric = metric("m-bad", status="unverifiable", owner=None)
    report = build_report([stale_metric, bad_metric], [], "reg", "wai", NOW)
    escalations = report.split("## Escalations")[1].split("## Autonomy metrics")[0]
    assert escalations.count("`m-stale`") == 1
    assert escalations.count("`m-bad`") == 1


def test_report_is_byte_identical_for_unchanged_inputs():
    args = ([metric("m1")], [waiver("m1", NOW, NOW + timedelta(days=30))], "reg", "wai", NOW)
    assert build_report(*args) == build_report(*args)
