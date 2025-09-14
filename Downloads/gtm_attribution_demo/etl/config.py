from pathlib import Path
DB_URL = f"sqlite:///{(Path(__file__).resolve().parents[1] / 'warehouse' / 'gtm.db')}"
DATA_DIR = Path(__file__).resolve().parents[1] / 'data'
RAW_DIR = DATA_DIR / 'raw'
REF_DIR = DATA_DIR / 'reference'
LEADS_CSV = RAW_DIR / 'leads.csv'
TOUCHES_CSV = RAW_DIR / 'touches.csv'
OPPS_CSV = RAW_DIR / 'opportunities.csv'
PRODUCT_EVENTS_CSV = RAW_DIR / 'product_events.csv'
SPEND_CSV = REF_DIR / 'spend_by_campaign.csv'
U_SHAPED_SPLIT = (0.4, 0.2, 0.4)
TIME_DECAY_HALFLIFE_DAYS = 7
LOOKBACK_DAYS = 60
