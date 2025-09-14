from pathlib import Path
import csv, random
from datetime import datetime, timedelta
import os

N_LEADS = int(os.environ.get('N_LEADS', 5000))
N_TOUCHES = int(os.environ.get('N_TOUCHES', 120000))
N_OPPS = int(os.environ.get('N_OPPS', 1800))
N_EVENTS = int(os.environ.get('N_EVENTS', 80000))
START = datetime(2025,7,1)
DAYS = int(os.environ.get('DAYS', 60))
RANDOM_SEED = 13

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

random.seed(RANDOM_SEED)
base = Path(__file__).resolve().parents[1]
raw = base / 'data' / 'raw'
raw.mkdir(parents=True, exist_ok=True)

def ts(day):
    d = START + timedelta(days=day)
    hour = random.choices(range(24), weights=[1,1,1,1,1,1,2,3,5,6,5,3,2,2,2,2,3,5,7,6,3,2,1,1])[0]
    return d.replace(hour=hour, minute=random.randint(0,59), second=random.randint(0,59))

# Leads
with (raw/'leads.csv').open('w', newline='') as f:
    w = csv.writer(f); w.writerow(['lead_id','email','created_at','source_channel','campaign','owner_id','first_response_minutes'])
    for i in range(1, N_LEADS+1):
        created = ts(random.randint(0, DAYS-1))
        ch = random.choices(CHANNELS, weights=[14,12,10,6,5,4,9,15])[0]
        camp = random.choice(CAMPAIGNS[ch]); owner = f"USR{random.randint(1,40):03d}"
        base_resp = {'paid_search':90,'paid_social':120,'email':240,'content':360,'events':180,'partners':200,'direct':300,'organic':360}[ch]
        first_resp = max(5, base_resp + random.randint(-45,120))
        w.writerow([f"L{i:06d}", f"user{i}@example.com", created.strftime('%Y-%m-%d %H:%M:%S'), ch, camp, owner, first_resp])

# Touches
with (raw/'touches.csv').open('w', newline='') as f:
    w = csv.writer(f); w.writerow(['touch_id','lead_id','touch_type','channel','campaign','ts'])
    for i in range(1, N_TOUCHES+1):
        lid = f"L{random.randint(1,N_LEADS):06d}"
        day = random.randint(0, DAYS-1)
        ch = random.choices(CHANNELS, weights=[16,12,14,8,6,5,10,18])[0]
        camp = random.choice(CAMPAIGNS[ch])
        ttype = random.choices(['ad_view','ad_click','email_open','email_click','site_session','demo_request'], weights=[10,12,8,7,20,5])[0]
        w.writerow([f"T{i:07d}", lid, ttype, ch, camp, ts(day).strftime('%Y-%m-%d %H:%M:%S')])

# Opportunities
with (raw/'opportunities.csv').open('w', newline='') as f:
    w = csv.writer(f); w.writerow(['opp_id','account_id','lead_id','amount','stage','created_at','closed_at','is_closed_won','owner_id'])
    for i in range(1, N_OPPS+1):
        lid = f"L{random.randint(1,N_LEADS):06d}"
        created_day = random.randint(5, DAYS-10)
        created = ts(created_day); cycle = random.randint(5,25); closed = ts(created_day+cycle)
        is_won = random.random() < 0.42; stage = 'Closed Won' if is_won else 'Closed Lost'
        amount = random.choice([6000,9000,12000,18000,25000,40000]) * random.uniform(0.8,1.25)
        w.writerow([f"O{i:06d}", f"ACCT{random.randint(1,4000):05d}", lid, f"{amount:.2f}", stage, created.strftime('%Y-%m-%d %H:%M:%S'), closed.strftime('%Y-%m-%d %H:%M:%S'), int(is_won), f"USR{random.randint(1,40):03d}"])

# Product events
with (raw/'product_events.csv').open('w', newline='') as f:
    w = csv.writer(f); w.writerow(['event_id','lead_id','event_type','ts'])
    for i in range(1, N_EVENTS+1):
        lid = f"L{random.randint(1,N_LEADS):06d}"; day = random.randint(0, DAYS-1)
        etype = random.choices(['signup','activation','feature_use'], weights=[10,6,20])[0]
        w.writerow([f"E{i:07d}", lid, etype, ts(day).strftime('%Y-%m-%d %H:%M:%S')])

print('Synthetic data generated.')

# Optional demo downsizing for hosted environments
if os.environ.get('DEMO_MODE', '0') == '1':
    N_LEADS = min(N_LEADS, 1000)
    N_TOUCHES = min(N_TOUCHES, 20000)
    N_OPPS = min(N_OPPS, 400)
    N_EVENTS = min(N_EVENTS, 15000)
