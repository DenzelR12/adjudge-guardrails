from dataclasses import dataclass
from datetime import datetime
from typing import Protocol


@dataclass(frozen=True)
class Watermark:
    source_id: str
    value: datetime
    run_id: str


@dataclass(frozen=True)
class SourceRead:
    rows: list[dict]
    source_version: str
    cutoff: datetime


class IncrementalSource(Protocol):
    source_id: str

    def validate_contract(self) -> None: ...
    def read_changes(self, watermark: Watermark, cutoff: datetime) -> SourceRead: ...
