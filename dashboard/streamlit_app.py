from datetime import date
import streamlit as st
from adjudge.dashboard_service import report_metadata, status_banner
from adjudge.demo_data import customer_metrics
st.set_page_config(page_title='AdJudge Guardrails',layout='wide')
st.title('AdJudge Guardrails')
st.caption('Human-calibrated multimodal evaluation and review routing')
tenant=st.sidebar.selectbox('Customer',['tenant_acme','tenant_northstar'])
dates=st.sidebar.date_input('Date range',(date(2026,9,1),date(2026,9,1)))
platforms=st.sidebar.multiselect('Platform',['facebook','instagram'],default=['facebook','instagram'])
types=st.sidebar.multiselect('Creative type',['image','video'],default=['image','video'])
status=status_banner('unverifiable','synthetic_demo','1.0.0')
st.warning(f"STATUS: {status['status']} — synthetic demo metrics are not verified live-source results.")
m=customer_metrics(tenant,tuple(platforms),tuple(types))
a,b,c,d=st.columns(4)
a.metric('Reviewed ads',m['reviewed_ads'])
b.metric('Exact agreement','—' if m['exact_agreement'] is None else f"{m['exact_agreement']:.1%}")
c.metric('False approval rate','—' if m['false_approval_rate'] is None else f"{m['false_approval_rate']:.1%}")
d.metric('Human review queue',m['human_review_queue'])
st.subheader('Report provenance')
st.json(report_metadata(tenant,str(dates[0]),str(dates[-1]),'unverifiable'))
