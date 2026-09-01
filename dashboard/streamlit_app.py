from datetime import date
import streamlit as st
from adjudge.dashboard_service import report_metadata, status_banner

st.set_page_config(page_title="AdJudge Guardrails", layout="wide")
st.title("AdJudge Guardrails")
st.caption("Human-calibrated multimodal evaluation and review routing")
tenant = st.sidebar.selectbox("Customer", ["tenant_acme", "tenant_northstar"])
dates = st.sidebar.date_input("Date range", (date(2026, 9, 1), date(2026, 9, 1)))
st.sidebar.multiselect("Platform", ["facebook", "instagram"], default=["facebook", "instagram"])
st.sidebar.multiselect("Creative type", ["image", "video"], default=["image", "video"])
status = status_banner("unverifiable", "local_postgres_demo", "1.0.0")
st.warning(f"STATUS: {status['status']} — demo data is not a verified live source.")
a, b, c = st.columns(3)
a.metric("Exact agreement", "—")
b.metric("False approval rate", "—")
c.metric("Human review queue", "—")
st.subheader("Incident and remediation console")
st.info("Connect the event ledger and verified registry to inspect evidence-linked incidents.")
st.subheader("Report provenance")
st.json(report_metadata(tenant, str(dates[0]), str(dates[-1]), "unverifiable"))
