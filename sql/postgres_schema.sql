CREATE TABLE IF NOT EXISTS fact_ad_review (
  ad_id TEXT PRIMARY KEY,
  customer_id TEXT NOT NULL,
  campaign_id TEXT NOT NULL,
  platform TEXT NOT NULL,
  creative_type TEXT NOT NULL,
  human_rating TEXT NOT NULL,
  llm_rating TEXT NOT NULL,
  llm_confidence DOUBLE PRECISION NOT NULL,
  disagreement_risk DOUBLE PRECISION NOT NULL,
  review_route TEXT NOT NULL,
  reviewer_override BOOLEAN NOT NULL,
  source_updated_at TIMESTAMPTZ NOT NULL
);

CREATE OR REPLACE VIEW dashboard_customer_daily AS
SELECT customer_id, DATE(source_updated_at) AS metric_date,
       COUNT(*) AS reviewed_ads,
       AVG(CASE WHEN human_rating = llm_rating THEN 1.0 ELSE 0.0 END) AS exact_agreement,
       AVG(CASE WHEN human_rating = 'bad' AND llm_rating = 'good' THEN 1.0 ELSE 0.0 END) AS false_approval_rate,
       AVG(CASE WHEN review_route = 'human_review' THEN 1.0 ELSE 0.0 END) AS human_review_rate,
       AVG(CASE WHEN reviewer_override THEN 1.0 ELSE 0.0 END) AS override_rate
FROM fact_ad_review
GROUP BY customer_id, DATE(source_updated_at);
