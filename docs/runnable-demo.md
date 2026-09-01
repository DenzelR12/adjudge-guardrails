# Runnable Demo

This demo uses only synthetic local records. It demonstrates tenant-scoped UX, dashboard trust status, and report provenance; it does not represent customer data or verified production results.

```bash
python -m pip install -e ".[dev]"
pip install streamlit fastapi uvicorn
streamlit run dashboard/streamlit_app.py
```

Every displayed metric must include status, source, metric-definition version, and generation/verification time. `UNVERIFIABLE` is the correct initial state until a source contract, snapshot, calculation, and verification run are connected.
