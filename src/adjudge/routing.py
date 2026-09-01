from dataclasses import dataclass
from typing import Literal

Route = Literal["auto_approve", "auto_reject", "human_review"]


@dataclass(frozen=True)
class Decision:
    route: Route
    reason: str


def route_ad(llm_rating: str, confidence: float, disagreement_risk: float, metric_status: str) -> Decision:
    if metric_status != "verified":
        return Decision("human_review", "Measured claim is stale or unverifiable")
    if disagreement_risk >= 0.65:
        return Decision("human_review", "Predicted expert/LLM disagreement risk is high")
    if confidence < 0.70:
        return Decision("human_review", "Model confidence is below policy threshold")
    if llm_rating == "bad":
        return Decision("auto_reject", "Low-risk negative assessment")
    if llm_rating == "good":
        return Decision("auto_approve", "Low-risk positive assessment")
    return Decision("human_review", "Borderline or unspecified case")
