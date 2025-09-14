from sqlalchemy import create_engine
from .config import DB_URL
import subprocess, sys
from pathlib import Path
from .load_to_warehouse import build
from .attribution import materialize

def ensure_data():
    root = Path(__file__).resolve().parents[1]
    paths = [root/'data'/'raw'/p for p in ['leads.csv','touches.csv','opportunities.csv','product_events.csv']]
    if not all(p.exists() for p in paths):
        subprocess.check_call([sys.executable, 'etl/generate_synth.py'], cwd=root.as_posix())
        subprocess.check_call([sys.executable, 'etl/generate_stage_history.py'], cwd=root.as_posix())

def main():
    ensure_data()
    eng = create_engine(DB_URL, future=True)
    build(eng)
    materialize()
    print('Pipeline complete.')

if __name__ == '__main__':
    main()
