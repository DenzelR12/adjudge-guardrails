from adjudge.demo_data import customer_metrics

def test_customer_metrics_are_tenant_scoped():
 assert customer_metrics('tenant_acme')['reviewed_ads']==2
 assert customer_metrics('tenant_northstar')['reviewed_ads']==2
 assert customer_metrics('tenant_acme')['false_approval_rate']==0.5

def test_filters_can_remove_all_rows():
 assert customer_metrics('tenant_acme',('instagram',))['reviewed_ads']==0
