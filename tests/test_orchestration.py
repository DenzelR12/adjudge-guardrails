from datetime import datetime, timezone

from adjudge.connectors import Watermark
from adjudge.orchestration import refresh


class BrokenSource:
    source_id = "broken"

    def validate_contract(self):
        raise ValueError("schema changed")

    def read_changes(self, watermark, cutoff):
        raise AssertionError("must not read after failed validation")


def test_failed_validation_does_not_commit_watermark():
    watermark = Watermark("broken", datetime(2026, 1, 1, tzinfo=timezone.utc), "prior")
    result = refresh(BrokenSource(), watermark, datetime.now(timezone.utc), lambda rows: None, lambda *args: None)
    assert result.status == "unverifiable"
    assert result.committed_watermark is None
    assert "not advanced" in result.message
