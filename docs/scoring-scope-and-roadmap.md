# Scoring Scope and Roadmap

## Purpose

AdJudge Guardrails is a governed evaluation and operating layer for AI-assisted ad creative review.

The project is designed to make creative-review signals measurable, traceable, auditable, and safe to use in operational workflows. It does not treat an LLM's confident opinion as a substitute for expert judgment, and it does not equate creative-quality labels with business outcomes.

## What the Current Dataset Supports

The initial evaluation work uses the public `AdControlCenter/ad-creative-quality-human-vs-llm` dataset.

The dataset includes human and LLM creative-quality judgments. In this context, labels such as `bad`, `fair`, and `good` are treated as source-provided creative-review judgments.

AdJudge Guardrails does not claim ownership of the source ads, source labels, or annotations. It records dataset provenance and independently recomputes metrics derived from those labels.

The initial scope includes:

- Human–LLM agreement and disagreement analysis
- LLM positivity-bias analysis, including false approvals where an expert label is negative and the LLM label is positive
- Evidence and metric provenance
- Dataset/version tracking and freshness controls
- Human-review routing for uncertain, high-risk, or conflicting assessments
- Incident investigation and approval-gated remediation workflows

## What a Creative-Quality Score Means

A creative-quality score is a judgment about the creative itself, not a guarantee of commercial performance.

A future configurable rubric may evaluate dimensions such as:

- Headline clarity and readability
- Image and headline alignment
- Message and offer consistency
- Call-to-action fit
- Visual quality and brand coherence
- Audience or category relevance
- Risk, policy, accessibility, or brand-safety signals

Each score should retain its supporting evidence, the rubric version, the model or reviewer identity, the source snapshot, and the time at which the assessment was generated.

## What AdJudge Does Not Currently Claim

The project does not currently claim that it can predict:

- Engagement, clicks, conversions, purchases, or return on ad spend
- The causal business impact of an individual creative
- That a creative resembling a historically successful ad will perform well
- A universally valid definition of `good` creative across all advertisers, verticals, audiences, markets, or campaign objectives

Creative performance depends on factors beyond the creative itself, including audience targeting, spend, placement, campaign objective, frequency, offer competitiveness, landing-page experience, brand recognition, seasonality, and measurement design.

## Future: Configurable and Vertical-Specific Rubrics

The architecture is intended to support configurable, versioned rubrics.

A general baseline rubric may be useful for broad creative review, but a high-quality assessment can differ by advertiser, industry, audience, objective, and risk context. For example, a direct-response retail creative, a financial-services creative, and a gaming creative may need different criteria and different review thresholds.

Any advertiser- or vertical-specific rubric should be explicit, versioned, documented, and independently evaluable. It should never be hidden inside an unexplained aggregate score.

## Future: Performance-Aware Signals

Performance-aware signals are a separate future capability, not an extension of a generic creative-quality label.

If legitimate, appropriately governed outcome data becomes available, the system may support separately labeled signals such as:

- `similarity_to_prior_high_performers`
- `predicted_engagement`
- `predicted_conversion`
- `predicted_purchase_intent`
- `observed_campaign_outcome`

These signals would require documented outcome definitions, appropriate access controls, exposure and spend context, training and validation splits, backtesting, calibration analysis, drift monitoring, and clear limitations.

They must remain distinct from:

- `expert_creative_quality_label`
- `llm_creative_quality_label`
- `rubric_dimension_scores`
- `risk_or_policy_flags`

The system should not collapse these different concepts into one ambiguous `ad quality` score.

## Claim-Gating Principle

AdJudge Guardrails follows a claim-gating principle:

> A capability may be described as planned only when its status is clearly marked as planned. It may be described as implemented only when the repository contains reproducible evidence, tests, documentation, and governance controls supporting that claim.

This protects users from confusing a research architecture, a quality-review system, and a validated performance-prediction system.
