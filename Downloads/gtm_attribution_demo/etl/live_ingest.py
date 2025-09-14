import sqlite3, random, time
from pathlib import Path
from datetime import datetime, timedelta

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / 'warehouse' / 'gtm.db'

CHANNELS = ['paid_search','paid_social','email','content','events','partners','direct','organic']
CAMPAIGNS = {
    'paid_search': ['PS_Brand','PS_Competitor','PS_Generic'],
    'paid_social': ['FB_Gated_ebook','LI_Thought_Leadership','TW_Product_Announcement'],
    'email': ['Email_Nurture_Q3','Email_Reengagement'],
    'content': ['Blog_Series_GTM','Case_Study_ABM'],
    'events': ['Webinar_Platform_Tour','Virtual_Roundtable'],
    'partners': ['Partner_Integration_Launch','MDF_Campaign_1'],
    'direct': ['Direct_None'],
    'organic': ['Organic_None']
}

def _ensure_meta(con):
    con.execute(\"\"\"CREATE TABLE IF NOT EXISTS _meta(
        key TEXT PRIMARY KEY, val TEXT
    )\"\"\")
    for k in ['next_touch_id','next_opp_id']:
        cur = con.execute(\"SELECT val FROM _meta WHERE key=?\", (k,))
        row = cur.fetchone()
        if not row:
            # seed from existing max IDs
            if k == 'next_touch_id':
                cur2 = con.execute(\"SELECT COALESCE(MAX(CAST(substr(touch_id,2) AS INTEGER)),0) FROM touches\")
                start = (cur2.fetchone()[0] or 0) + 1
            else:
                cur2 = con.execute(\"SELECT COALESCE(MAX(CAST(substr(opp_id,2) AS INTEGER)),0) FROM opportunities\")
                start = (cur2.fetchone()[0] or 0) + 1
            con.execute(\"INSERT OR REPLACE INTO _meta(key,val) VALUES(?,?)\", (k, str(start)))
    con.commit()

def _next(con, key, pad):
    cur = con.execute(\"SELECT val FROM _meta WHERE key=?\", (key,))
    n = int(cur.fetchone()[0])
    con.execute(\"UPDATE _meta SET val=? WHERE key=?\", (str(n+1), key))
    con.commit()
    prefix = 'T' if key=='next_touch_id' else 'O'
    return f\"{prefix}{n:0{pad}d}\"

def simulate_batch(n_touches=500, n_opps=20, won_rate=0.4):
    con = sqlite3.connect(DB.as_posix())
    _ensure_meta(con)
    now = datetime.utcnow()
    # infer a valid lead_id range
    cur = con.execute(\"SELECT MIN(lead_id), MAX(lead_id) FROM leads\"); mn, mx = cur.fetchone()
    if not mn:
        return 0,0
    def rand_lead():
        # assumes IDs like L000123
        lo = int(mn[1:]); hi = int(mx[1:])
        i = random.randint(lo, hi)
        return f\"L{i:06d}\"
    # touches
    for _ in range(n_touches):
        lid = rand_lead()
        ch = random.choice(CHANNELS); camp = random.choice(CAMPAIGNS[ch])
        tid = _next(con, 'next_touch_id', pad=7)
        ts = (now - timedelta(minutes=random.randint(0, 240))).strftime('%Y-%m-%d %H:%M:%S')
        con.execute(\"INSERT OR REPLACE INTO touches(touch_id,lead_id,touch_type,channel,campaign,ts) VALUES (?,?,?,?,?,?)\",
                    (tid, lid, random.choice(['ad_click','email_open','site_session','demo_request']), ch, camp, ts))
    # opps
    for _ in range(n_opps):
        lid = rand_lead()
        is_won = 1 if random.random() < won_rate else 0
        oid = _next(con, 'next_opp_id', pad=6)
        created = (now - timedelta(days=random.randint(2, 20))).strftime('%Y-%m-%d %H:%M:%S')
        closed = now.strftime('%Y-%m-%d %H:%M:%S')
        amt = random.choice([6000,9000,12000,18000,25000,40000]) * random.uniform(0.8,1.25)
        con.execute(\"\"\"INSERT OR REPLACE INTO opportunities(opp_id,account_id,lead_id,amount,stage,created_at,closed_at,is_closed_won,owner_id)
                       VALUES (?,?,?,?,?,?,?,?,?)\"\"\",
                    (oid, f\"ACCT{random.randint(1,99999):05d}\", lid, f\"{amt:.2f}\", 'Closed Won' if is_won else 'Closed Lost',
                     created, closed, is_won, f\"USR{random.randint(1,40):03d}\"))
    con.commit()
    con.close()
    return n_touches, n_opps
