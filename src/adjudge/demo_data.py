ROWS = [{"tenant_id":"tenant_acme","platform":"facebook","creative_type":"image","human":"bad","llm":"good","route":"human_review"},{"tenant_id":"tenant_acme","platform":"facebook","creative_type":"video","human":"good","llm":"good","route":"auto_approve"},{"tenant_id":"tenant_northstar","platform":"instagram","creative_type":"image","human":"fair","llm":"good","route":"human_review"},{"tenant_id":"tenant_northstar","platform":"instagram","creative_type":"video","human":"bad","llm":"bad","route":"auto_reject"}]

def customer_metrics(tenant_id, platforms=(), creative_types=()):
 rows=[r for r in ROWS if r['tenant_id']==tenant_id]
 if platforms: rows=[r for r in rows if r['platform'] in platforms]
 if creative_types: rows=[r for r in rows if r['creative_type'] in creative_types]
 n=len(rows)
 return {'reviewed_ads':n,'exact_agreement':None if not n else sum(r['human']==r['llm'] for r in rows)/n,'false_approval_rate':None if not n else sum(r['human']=='bad' and r['llm']=='good' for r in rows)/n,'human_review_queue':sum(r['route']=='human_review' for r in rows)}
