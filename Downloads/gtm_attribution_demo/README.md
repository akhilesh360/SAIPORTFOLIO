# B2B SaaS GTM Performance Attribution Analysis (Portfolio Demo)

End-to-end project mirroring a **Customer Data Analyst** workflow:
- Unify **Salesforce + HubSpot + Product** data
- Multi-touch attribution (First/Last/Linear/U-Shaped/Time-Decay)
- Pipeline velocity, stage conversion, SLA follow-up impact
- 1-page **Streamlit** dashboard for execs

## Quick Start
```
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m etl.run_pipeline
streamlit run dashboard/app.py
```

---

## 🌐 Live Demo (Add your link)
Once you deploy, paste your public URL here so recruiters can click and explore:
**Live Demo:** https://your-streamlit-demo-url (replace me)

### One-click Hosting Options

**A) Streamlit Community Cloud (recommended)**
1. Push this repo to GitHub.
2. Go to https://share.streamlit.io/ → “New app” → choose your repo.
3. Set **Main file path** to `app.py`.
4. (Optional) Set environment variable `DEMO_MODE=1` for faster demo loads.
5. Deploy — you’ll get a public URL like `https://your-app.streamlit.app`.

**B) Hugging Face Spaces**
1. Create a new Space → choose **Streamlit** template.
2. Upload the repo (or connect GitHub).
3. Ensure `app.py` is at repo root (already done).
4. Set `DEMO_MODE=1` in Space variables for speed (optional).
5. Deploy — you’ll get a public URL like `https://huggingface.co/spaces/<you>/<space>`.

> Tip: For a real-warehouse variant, switch to Snowflake and place creds in `.streamlit/secrets.toml` (see `secrets.template.toml`).

---

## 🧭 Coherent Narrative (use in your README & interviews)
- **Problem:** Marketing & sales leaders don’t know which channels/campaigns truly drive revenue.
- **Approach:** Unified Salesforce/HubSpot/Product into one schema → built multi-touch attribution models → surfaced KPIs in a 1‑page exec dashboard.
- **What’s unique:** Compare **First/Last/Linear/U‑Shaped/Time‑Decay** models and show how **SLA follow-up time** affects win rates and pipeline velocity.
- **Outcome:** Clear recommendations on **budget reallocation** (channels & campaigns), grounded in influenced revenue and time-to-close.

---

## ⚙️ Demo Modes
- **Full Mode (default):** 5k leads / 120k touches / 1.8k opps / 80k product events.
- **Demo Mode (hosted):** set `DEMO_MODE=1` to auto-scale to ~1k leads for snappier page loads.
  - Manual overrides: `N_LEADS, N_TOUCHES, N_OPPS, N_EVENTS, DAYS` as env vars.


---

## ⚡ Real-Time Demo Mode
This app supports a **live simulation** to impress reviewers:

- Click **“Simulate new data”** in the sidebar to append fresh touches/opportunities and **auto-recompute attribution**.
- Use the **Budget Shift Simulator** to model an illustrative reallocation (e.g., +10% to Paid Search with 1.2× ROI uplift) and see projected revenue changes.
- For hosted demos, set env var `DEMO_MODE=1` to keep dataset fast for viewers.



---

## 📈 Looker Artifacts
- `looker/gtm.model.lkml`, `looker/*.view.lkml`, `looker/dashboards/exec_1pager.dashboard.lkml` 
- Plug into your Looker **connection** and these views map to the same warehouse tables (SQLite locally; Snowflake in prod).
- Include `assets/exec_1pager.png` as a README hero/screenshot.

## 🔁 Stage-to-Stage Conversion (Funnel)
- Added `data/raw/stage_history.csv` (generated) → loaded into `stage_history` table.
- View `v_stage_conversion_full` computes conversion rates for **Prospecting→Qualification→Proposal→Negotiation→Closed Won**.

---

## 🧩 Looker Hookup — Advanced (Optional but impressive)
1. **Warehouse**: Point Looker to your Snowflake/warehouse with the same tables (`opportunities`, `touch_attribution`, `stage_history`, `product_events`, `leads`, `touches`). Use `models/snowflake/ddl.sql` to create them.
2. **Project**: Add `looker/*.lkml` into a Looker project (Git-backed). In `looker/gtm.model.lkml`, set `connection: 'YOUR_CONNECTION'`.
3. **Explores**:
   - `opportunities` ← joined to `touch_attribution` and `stage_history`
   - `leads` ← joined to `product_events`
4. **Dashboard**: Use `looker/dashboards/exec_1pager.dashboard.lkml` as a starting point or build tiles from the explores.
5. **Tip**: Keep the Streamlit demo as a public link in your README for instant viewing; mention Looker artifacts as “enterprise-ready.”

### Snapshot for README
After you run the pipeline locally, create a static PNG for quick viewing:
```bash
python -m etl.run_pipeline
python scripts/snapshot_exec_page.py
# Adds assets/exec_snapshot.png — embed it in README
```

---

## 🧼 Reset Button + Markov Attribution
- **Reset demo data**: Use the sidebar **“Reset demo data”** to rebuild the DB and recompute attribution from scratch.
- **Markov model**: See `notebooks/markov_attribution.ipynb` for a **first‑order Markov** attribution with **removal effect**.
