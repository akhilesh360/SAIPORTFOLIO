import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / 'warehouse' / 'gtm.db'

st.set_page_config(page_title='GTM Attribution — Exec 1-Pager', layout='wide')
st.title('🧭 GTM Performance Attribution — Exec 1-Pager')
st.caption('Unify CRM + Marketing + Product → Attribution & KPIs')
st.sidebar.header('⚡ Live Demo Controls')
st.sidebar.divider()
if st.sidebar.button('Reset demo data'):
    try:
        # Wipe DB and rebuild from raw synthetic data
        if DB.exists():
            DB.unlink()
        import subprocess, sys
        subprocess.check_call([sys.executable, '-m', 'etl.run_pipeline'], cwd=ROOT.as_posix())
        st.success('Demo data reset and recomputed. Refresh the page.')
        st.stop()
    except Exception as e:
        st.error(f'Failed to reset: {e}')
        st.stop()

simulate = st.sidebar.button('Simulate new data (touches & opps)')
boost = st.sidebar.slider('Budget Shift: move % to target channel (toy model)', 0, 20, 10)
uplift = st.sidebar.slider('Expected ROI uplift on target (x)', 1.0, 2.0, 1.2, 0.05)
target_channel = st.sidebar.selectbox('Target channel', ['paid_search','paid_social','email','content','events','partners','direct','organic'])
if simulate:
    try:
        from etl.live_ingest import simulate_batch
        n_t, n_o = simulate_batch()
        # Recompute attribution after new data
        import subprocess, sys
        subprocess.check_call([sys.executable, '-m', 'etl.run_pipeline'], cwd=ROOT.as_posix())
        st.success(f'Inserted {n_t} touches and {n_o} opps; recomputed attribution.')
    except Exception as e:
        st.error(f'Live simulate failed: {e}')
        st.stop()


if not DB.exists():
    st.warning('Database not found. Run: `python -m etl.run_pipeline`')
    st.stop()

con = sqlite3.connect(DB.as_posix())

with open(ROOT/'models'/'sqlite'/'kpis.sql') as f:
    con.executescript(f.read())

models = pd.read_sql_query('SELECT DISTINCT model FROM touch_attribution', con)
if models.empty:
    st.warning('No attribution data. Run: `python -m etl.run_pipeline`')
    st.stop()

m = st.radio('Attribution Model', models['model'].tolist(), horizontal=True)

col1, col2, col3 = st.columns(3)
velocity = pd.read_sql_query('SELECT * FROM v_velocity', con)
attrib_channel = pd.read_sql_query(f"SELECT channel, attributed_revenue FROM v_attrib_by_channel WHERE model='{m}' ORDER BY attributed_revenue DESC", con)
total_attr = attrib_channel['attributed_revenue'].sum()

with col1:
    st.metric('Avg Days to Close (Won)', f"{velocity['avg_days_to_close'].iloc[0]:.1f}")
won_count = pd.read_sql_query('SELECT COUNT(*) AS won FROM opportunities WHERE is_closed_won=1', con)['won'].iloc[0]
with col2:
    st.metric('Closed Won Deals', int(won_count))
with col3:
    st.metric('Attributed Revenue', f"${total_attr:,.0f}")

st.subheader('Attributed Revenue by Channel')
st.markdown('**Budget Shift Simulator (illustrative):** Move budget to a target channel and assume ROI uplift to see projected attributed revenue.')
base_channel_df = attrib_channel.copy()
proj_df = base_channel_df.copy()
if not base_channel_df.empty:
    total = float(base_channel_df['attributed_revenue'].sum())
    if total > 0:
        # simple toy model: allocate `boost%` of total budget from other channels to target, apply `uplift` multiplier on that slice
        shift_amt = total * (boost/100.0)
        # subtract evenly from non-target channels
        mask = proj_df['channel'] != target_channel
        non_target_count = int(mask.sum())
        if non_target_count > 0:
            proj_df.loc[mask, 'attributed_revenue'] = proj_df.loc[mask, 'attributed_revenue'] - (shift_amt / non_target_count)
        # add shifted & uplifted to target
        proj_df.loc[proj_df['channel']==target_channel, 'attributed_revenue'] += shift_amt * uplift
        proj_df['attributed_revenue'] = proj_df['attributed_revenue'].clip(lower=0)
        delta = proj_df['attributed_revenue'].sum() - total
        st.caption(f'Projected delta (illustrative): {delta:,.0f}')

fig1, ax1 = plt.subplots()
ax1.bar(attrib_channel['channel'], attrib_channel['attributed_revenue'])
ax1.set_xlabel('Channel'); ax1.set_ylabel('Attributed Revenue')
plt.xticks(rotation=30, ha='right')
st.pyplot(fig1)

st.subheader('Top 10 Campaigns (Attributed Revenue)')
attrib_campaign = pd.read_sql_query(f"""SELECT campaign, attributed_revenue FROM v_attrib_by_campaign
WHERE model='{m}' ORDER BY attributed_revenue DESC LIMIT 10""", con)
st.dataframe(attrib_campaign)

st.markdown('---')
st.subheader('SLA Follow-up Impact (Lead Response Buckets)')
sla = pd.read_sql_query('SELECT * FROM v_sla_buckets', con)
fig2, ax2 = plt.subplots()
ax2.bar(sla['sla_bucket'], sla['leads'])
ax2.set_xlabel('First Response Time'); ax2.set_ylabel('# Leads')
st.pyplot(fig2)

st.caption('Switch models to compare First/Last/Linear/U-Shaped/Time-Decay assumptions.')


st.markdown('---')
st.subheader('Stage-to-Stage Conversion Funnel')
try:
    conv = pd.read_sql_query('SELECT * FROM v_stage_conversion_full ORDER BY path', con)
    st.dataframe(conv)
except Exception as e:
    st.info('Stage conversion view unavailable: ' + str(e))


# Funnel chart (matplotlib) for stage conversion
st.subheader('Stage Conversion — Funnel Chart')
try:
    conv = pd.read_sql_query('SELECT * FROM v_stage_conversion_full ORDER BY path', con)
    if not conv.empty:
        # Prepare funnel-like bars (horizontal)
        # We assume 'at_stage' approximates count at each from_stage; take the maximum per starting node.
        agg = conv.groupby(conv['path'].str.split('→').str[0]).agg({'at_stage':'max'}).reset_index()
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots()
        ax.barh(agg['path'], agg['at_stage'])
        ax.set_xlabel('Count at stage')
        ax.set_ylabel('Stage')
        st.pyplot(fig)
    else:
        st.info('No stage conversion data to plot.')
except Exception as e:
    st.info('Funnel chart unavailable: ' + str(e))
