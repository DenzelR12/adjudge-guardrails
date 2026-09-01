from dataclasses import dataclass


@dataclass(frozen=True)
class CostRecord:
    run_id: str
    tenant_id: str | None
    component: str
    amount_usd: float
    unit: str


def total_cost(records: list[CostRecord]) -> float:
    return round(sum(record.amount_usd for record in records), 6)
