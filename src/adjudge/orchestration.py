from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4

from adjudge.connectors import IncrementalSource, Watermark


@dataclass(frozen=True)
class RefreshResult:
    run_id: str
    status: str
    rows_read: int
    committed_watermark: datetime | None
    message: str


def refresh(source: IncrementalSource, watermark: Watermark, cutoff: datetime, validate_rows, publish) -> RefreshResult:
    run_id = str(uuid4())
    try:
        source.validate_contract()
        read = source.read_changes(watermark, cutoff)
        validate_rows(read.rows)
        publish(read.rows, read.source_version, read.cutoff, run_id)
        return RefreshResult(run_id, "verified", len(read.rows), read.cutoff, "Published and committed")
    except Exception as error:
        return RefreshResult(run_id, "unverifiable", 0, None, f"Watermark not advanced: {error}")
