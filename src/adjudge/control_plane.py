from dataclasses import dataclass, field
from datetime import datetime, timezone
from hashlib import sha256
from typing import Literal
from uuid import uuid4


Severity = Literal["low", "medium", "high", "critical"]


@dataclass(frozen=True)
class AuditEvent:
    event_type: str
    summary: str
    correlation_id: str
    source_id: str | None = None
    entity_id: str | None = None
    evidence_refs: tuple[str, ...] = ()
    previous_hash: str = ""
    event_id: str = field(default_factory=lambda: str(uuid4()))
    occurred_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def digest(self) -> str:
        payload = "|".join((self.event_id, self.event_type, self.summary, self.correlation_id, self.previous_hash))
        return sha256(payload.encode()).hexdigest()


@dataclass(frozen=True)
class Hypothesis:
    statement: str
    confidence: Literal["low", "medium", "high"]
    evidence_refs: tuple[str, ...]


@dataclass(frozen=True)
class RemediationAction:
    priority: int
    action: str
    owner_role: str
    risk: Severity
    success_criteria: str
    rollback: str


@dataclass(frozen=True)
class RemediationPlan:
    incident_id: str
    problem_statement: str
    hypotheses: tuple[Hypothesis, ...]
    actions: tuple[RemediationAction, ...]
    approval_required: bool = True


@dataclass(frozen=True)
class TenantQuery:
    tenant_id: str
    metric_ids: tuple[str, ...]
    start_at: datetime
    end_at: datetime
    requested_by: str


def authorize_tenant_query(query: TenantQuery, allowed_tenants: set[str]) -> bool:
    return query.tenant_id in allowed_tenants and query.start_at < query.end_at
