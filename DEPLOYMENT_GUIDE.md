# Credora Finance — Streamlit Cloud Deployment Bundle

This folder is prepared for deploying the interactive dashboard using Streamlit Community Cloud. The included SQLite database is a local, portable database bundled with the app; this is not a hosted PostgreSQL/database-server deployment.

## Included files
- `dashboard_app.py` — interactive Streamlit dashboard
- `credora_finance.db` — sanitized SQLite copy used by the dashboard (direct identifiers such as names, date of birth, email and phone are removed from the customers table)
- `scored_applications.csv` — scored application results used by dashboard filters
- `requirements.txt` — dashboard dependencies
- `.streamlit/config.toml` — basic Streamlit configuration

## Deploy on Streamlit Community Cloud
1. Download and extract this ZIP.
2. Sign in to GitHub and create a new repository (private is recommended).
3. Upload all files and the `.streamlit` folder from this extracted folder to the repository root. Ensure `dashboard_app.py`, `credora_finance.db`, `scored_applications.csv`, and `requirements.txt` are at the repository root.
4. Open https://share.streamlit.io/ and sign in with GitHub.
5. Choose **Create app**, select your repository, branch, and `dashboard_app.py` as the main file.
6. Click **Deploy** and wait for the build to finish. Open the generated app URL and test the filters, charts, watchlist, and CSV download.

## Before sharing
- Keep the repository private unless you have approval to publish the dataset.
- The dashboard contains model-estimated risk scores. Do not use it to make real lending decisions without validation, fairness review, security review, and business approval.
- This package does not create a public app automatically because GitHub/Streamlit account access and authorization must be completed by the account owner. A successful online deployment is only confirmed after Streamlit Cloud builds and the live URL is tested.
