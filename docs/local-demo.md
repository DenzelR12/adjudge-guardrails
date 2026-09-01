# Local Demo

The demo data is synthetic and is included only to exercise the architecture. It is not customer data and it does not represent measured Kaggle results.

1. Start Postgres: `docker compose up -d`.
2. Apply `sql/postgres_schema.sql` and load `data/demo/ad_reviews.csv` with your local Postgres client.
3. Install the package: `python -m pip install -e ".[dev]"`.
4. Run tests: `make test`.
5. Run the Streamlit interface after installing Streamlit: `streamlit run dashboard/streamlit_app.py`.

The demo illustrates tenant-scoped metrics, false-approval monitoring, and human-review routing. Production use requires database-enforced row-level security, authenticated identity, source contracts, and verified metric provenance.
