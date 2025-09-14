import pandas as pd
from sqlalchemy import create_engine, text
from .config import DB_URL, LEADS_CSV, TOUCHES_CSV, OPPS_CSV, PRODUCT_EVENTS_CSV
from pathlib import Path

DDL = [
    """CREATE TABLE IF NOT EXISTS stage_history(opp_id TEXT, stage TEXT, ts TEXT)""",
    """CREATE TABLE IF NOT EXISTS leads(lead_id TEXT PRIMARY KEY,email TEXT,created_at TEXT,source_channel TEXT,campaign TEXT,owner_id TEXT,first_response_minutes INTEGER);""",
    """CREATE TABLE IF NOT EXISTS touches(touch_id TEXT PRIMARY KEY,lead_id TEXT,touch_type TEXT,channel TEXT,campaign TEXT,ts TEXT);""",
    """CREATE TABLE IF NOT EXISTS opportunities(opp_id TEXT PRIMARY KEY,account_id TEXT,lead_id TEXT,amount REAL,stage TEXT,created_at TEXT,closed_at TEXT,is_closed_won INTEGER,owner_id TEXT);""",
    """CREATE TABLE IF NOT EXISTS product_events(event_id TEXT PRIMARY KEY,lead_id TEXT,event_type TEXT,ts TEXT);""", 
    """CREATE TABLE IF NOT EXISTS touch_attribution(opp_id TEXT,model TEXT,channel TEXT,campaign TEXT,credit REAL,amount REAL);"""
]

def load_csv_to_table(engine, path, table):
    df = pd.read_csv(path)
    with engine.begin() as conn:
        df.to_sql(table, conn, if_exists='replace', index=False)

def build(engine):
    with engine.begin() as conn:
        for stmt in DDL: conn.execute(text(stmt))
    load_csv_to_table(engine, LEADS_CSV, 'leads')
    load_csv_to_table(engine, TOUCHES_CSV, 'touches')
    load_csv_to_table(engine, OPPS_CSV, 'opportunities')
    load_csv_to_table(engine, PRODUCT_EVENTS_CSV, 'product_events')
    # optional: stage history
    raw_stage = Path(__file__).resolve().parents[1]/'data'/'raw'/'stage_history.csv'
    if raw_stage.exists():
        load_csv_to_table(engine, raw_stage, 'stage_history')
