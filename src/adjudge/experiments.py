from dataclasses import dataclass


@dataclass(frozen=True)
class ExperimentRecord:
    experiment_id: str
    candidate_version: str
    baseline_version: str
    metric_definition_version: str
    success_criteria: str
    outcome: str = "pending"


def eligible_for_rollout(record: ExperimentRecord) -> bool:
    return record.outcome == "approved"
