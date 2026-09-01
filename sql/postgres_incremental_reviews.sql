SELECT ad_id, human_rating, llm_rating, llm_confidence, llm_rationale,
       source_updated_at, source_version
FROM ad_quality_reviews
WHERE source_updated_at > %(watermark)s
  AND source_updated_at <= %(cutoff)s
ORDER BY source_updated_at ASC, ad_id ASC;
