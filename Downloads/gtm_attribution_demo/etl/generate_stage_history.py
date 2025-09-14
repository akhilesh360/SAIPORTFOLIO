import pandas as pd
from pathlib import Path
from datetime import timedelta

ROOT = Path(__file__).resolve().parents[1]
raw = ROOT / 'data' / 'raw'

def generate():
    opps = pd.read_csv(raw/'opportunities.csv', parse_dates=['created_at','closed_at'])
    rows = []
    stage_order = ['Prospecting','Qualification','Proposal','Negotiation','Closed Won','Closed Lost']
    for _, o in opps.iterrows():
        # Build a path ending at Closed Won or Closed Lost
        if o['stage'] == 'Closed Won':
            path = ['Prospecting','Qualification','Proposal','Negotiation','Closed Won']
        else:
            # some lost earlier; randomly pick a cut stage
            # (deterministic-ish using amount)
            cut_idx = int((hash(o['opp_id']) % 3) + 2)  # 2..4
            path = stage_order[:cut_idx] + ['Closed Lost']
        # Distribute timestamps between created_at and closed_at
        start = o['created_at']
        end = o['closed_at']
        if pd.isna(end):
            end = start + timedelta(days=14)
        total = len(path)
        for i, st in enumerate(path):
            ts = start + (end - start) * (i / max(total-1,1))
            rows.append({'opp_id': o['opp_id'], 'stage': st, 'ts': ts})
    df = pd.DataFrame(rows)
    df.to_csv(raw/'stage_history.csv', index=False)

if __name__ == '__main__':
    generate()
