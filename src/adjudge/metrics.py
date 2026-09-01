from datetime import datetime, timedelta, timezone
from typing import Literal

from pydantic import BaseModel, Field, model_validator

MetricStatus = Literal["verified", "stale", "unverifiable"]


class MetricRecord(BaseModel):
    metric_id: str
    definition_version: str
    display_name: str
    value: float
    unit: str
    definition: str
    source_id: str
    source_version: str
    computed_at: datetime
    freshness_sla_hours: int = Field(gt=0)
    status: MetricStatus
    owner: str | None = None
    code_version: str
    input_hash: str

    @model_validator(mode="after")
    def verified_requires_complete_provenance(self):
        required = (self.source_version, self.code_version, self.input_hash)
        if self.status == "verified" and any(not item or item.startswith("REPLACE_WITH") for item in required):
            raise ValueError("verified metrics require non-placeholder provenance")
        return self


def effective_status(record: MetricRecord, now: datetime | None = None) -> MetricStatus:
    now = now or datetime.now(timezone.utc)
    age = now - record.computed_at.astimezone(timezone.utc)
    return "stale" if age > timedelta(hours=record.freshness_sla_hours) else record.status


def may_state_as_current(record: MetricRecord, now: datetime | None = None) -> bool:
    return effective_status(record, now) == "verified"
