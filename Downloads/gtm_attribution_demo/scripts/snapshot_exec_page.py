"""Create a quick PNG snapshot for the README after running the pipeline.
Usage:
  python scripts/snapshot_exec_page.py
Requires: pandas, matplotlib; assumes warehouse/gtm.db exists.
"""
import sqlite3
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT/'warehouse'/'gtm.db'
OUT = ROOT/'assets'/'exec_snapshot.png'
OUT.parent.mkdir(exist_ok=True)

if not DB.exists():
    raise SystemExit('Run: python -m etl.run_pipeline')

con = sqlite3.connect(DB.as_posix())

attrib_channel = pd.read_sql_query("SELECT channel, SUM(amount) AS attributed_revenue FROM touch_attribution WHERE model='u_shaped' GROUP BY channel ORDER BY attributed_revenue DESC", con)
velocity = pd.read_sql_query('SELECT * FROM v_velocity', con)

fig, ax = plt.subplots(figsize=(8,4))
ax.bar(attrib_channel['channel'], attrib_channel['attributed_revenue'])
ax.set_title(f"U-Shaped Attributed Revenue by Channel — Avg Days to Close: {velocity['avg_days_to_close'].iloc[0]:.1f}")
ax.set_xlabel('Channel'); ax.set_ylabel('Attributed Revenue')
plt.xticks(rotation=30, ha='right')
fig.tight_layout()
fig.savefig(OUT, dpi=150)
print('Saved', OUT)
