# Root Streamlit entry to make hosting dead-simple.
# This just executes the real dashboard code at dashboard/app.py.

import runpy, os, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# Ensure pipeline has run at least once (builds DB)
try:
    subprocess.check_call([sys.executable, '-m', 'etl.run_pipeline'], cwd=ROOT.as_posix())
except Exception as e:
    # It's okay if it runs again; Streamlit reruns on edits anyway.
    pass

# Execute the dashboard
runpy.run_path((ROOT / 'dashboard' / 'app.py').as_posix())
