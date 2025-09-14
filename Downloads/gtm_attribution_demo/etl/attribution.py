import pandas as pd, numpy as np
from sqlalchemy import create_engine
from .config import DB_URL, LOOKBACK_DAYS, U_SHAPED_SPLIT, TIME_DECAY_HALFLIFE_DAYS

def _get():
    eng = create_engine(DB_URL, future=True)
    leads = pd.read_sql('select * from leads', eng, parse_dates=['created_at'])
    touches = pd.read_sql('select * from touches', eng, parse_dates=['ts'])
    opps = pd.read_sql('select * from opportunities where is_closed_won=1', eng, parse_dates=['created_at','closed_at'])
    return leads, touches, opps, eng

def _touches_for(opprow, touches):
    lb = opprow['closed_at'] - pd.Timedelta(days=LOOKBACK_DAYS)
    t = touches[(touches.lead_id==opprow.lead_id) & (touches.ts<=opprow.closed_at) & (touches.ts>=lb)].sort_values('ts')
    return t

def _linear(n): return np.ones(n)/max(n,1)
def _first(n): w=np.zeros(n); w[0]=1 if n>0 else 0; return w
def _last(n): w=np.zeros(n); w[-1]=1 if n>0 else 0; return w
def _u(n, a=0.4, m=0.2, b=0.4):
    if n==0: return np.array([])
    if n==1: return np.array([1.0])
    if n==2: return np.array([0.5,0.5])
    w=np.zeros(n); w[0]=a; w[-1]=b; w[1:-1]=m/(n-2); return w
def _decay(ts_list, conv_ts, hl=7):
    if not ts_list: return np.array([])
    ages=[(conv_ts - t).total_seconds()/86400 for t in ts_list]
    arr=np.array([0.5**(age/hl) for age in ages], float)
    s=arr.sum(); return arr/s if s>0 else np.zeros_like(arr)

def materialize():
    leads, touches, opps, eng = _get()
    rows=[]
    for _, o in opps.iterrows():
        seq=_touches_for(o, touches)
        if seq.empty: continue
        n=len(seq)
        ts=seq['ts'].dt.to_pydatetime().tolist()
        amt=float(o['amount'])
        models={
            'linear': _linear(n),
            'first_touch': _first(n),
            'last_touch': _last(n),
            'u_shaped': _u(n, *U_SHAPED_SPLIT),
            'time_decay': _decay(ts, o['closed_at'].to_pydatetime(), TIME_DECAY_HALFLIFE_DAYS)
        }
        for mname, w in models.items():
            for (ch,camp,_t), ww in zip(seq[['channel','campaign','ts']].values.tolist(), w):
                if ww>0:
                    rows.append({'opp_id':o['opp_id'],'model':mname,'channel':ch,'campaign':camp,'credit':float(ww),'amount':float(amt*ww)})
    if not rows: return
    df=pd.DataFrame(rows)
    with eng.begin() as c:
        c.exec_driver_sql('DELETE FROM touch_attribution')
        df.to_sql('touch_attribution', c, if_exists='append', index=False)
