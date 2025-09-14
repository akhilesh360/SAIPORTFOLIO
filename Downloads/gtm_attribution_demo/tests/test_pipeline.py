from pathlib import Path
import subprocess, sys, sqlite3

def test_pipeline():
    root = Path(__file__).resolve().parents[1]
    subprocess.check_call([sys.executable, '-m', 'etl.run_pipeline'], cwd=root.as_posix())
    db = root/'warehouse'/'gtm.db'
    assert db.exists()
    con = sqlite3.connect(db.as_posix())
    cur = con.execute("SELECT name FROM sqlite_master WHERE type='table'")
    names = {r[0] for r in cur.fetchall()}
    assert {'leads','touches','opportunities','product_events','touch_attribution'} <= names
