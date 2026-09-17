#!/usr/bin/env python3
from ib_insync import IB, Stock, Option
import math
import sys

HOST = '127.0.0.1'
PORT = 7496
CLIENT_ID = 9876
TICKER = sys.argv[1].upper() if len(sys.argv) > 1 else 'ALV'
EXP = sys.argv[2] if len(sys.argv) > 2 else '20260918'
STRIKE = float(sys.argv[3]) if len(sys.argv) > 3 else 120.0


def clean(v):
    if v is None:
        return None
    try:
        return None if isinstance(v, float) and math.isnan(v) else v
    except (TypeError, ValueError):
        return None


def show(label, t):
    g = getattr(t, 'modelGreeks', None)
    print(label, {
        'last': clean(getattr(t, 'last', None)),
        'bid': clean(getattr(t, 'bid', None)),
        'ask': clean(getattr(t, 'ask', None)),
        'delta': clean(getattr(t, 'delta', None)) if hasattr(t, 'delta') else None,
        'model_delta': clean(getattr(g, 'delta', None)) if g else None,
        'gamma': clean(getattr(t, 'gamma', None)) if hasattr(t, 'gamma') else None,
        'model_gamma': clean(getattr(g, 'gamma', None)) if g else None,
        'theta': clean(getattr(t, 'theta', None)) if hasattr(t, 'theta') else None,
        'model_theta': clean(getattr(g, 'theta', None)) if g else None,
        'vega': clean(getattr(t, 'vega', None)) if hasattr(t, 'vega') else None,
        'model_vega': clean(getattr(g, 'vega', None)) if g else None,
        'volume': clean(getattr(t, 'volume', None)),
        'openInterest': clean(getattr(t, 'openInterest', None)),
        'historicalVol': clean(getattr(t, 'historicalVol', None)),
        'impliedVol': clean(getattr(t, 'impliedVol', None)),
    })

ib = IB()
try:
    ib.connect(HOST, PORT, clientId=CLIENT_ID, timeout=10)
    for typ in (1, 3):
        ib.reqMarketDataType(typ)
        print('MARKET_DATA_TYPE', typ)
        stock = Stock(TICKER, 'SMART', 'USD')
        ib.qualifyContracts(stock)
        st = ib.reqMktData(stock, snapshot=True)
        ib.sleep(3)
        show('STOCK', st)
        opt = Option(TICKER, EXP, STRIKE, 'P', 'SMART', multiplier='100', currency='USD')
        q = ib.qualifyContracts(opt)
        if not q:
            print('NO_QUALIFIED_OPTION')
            continue
        c = q[0]
        print('OPTION', c)
        dt = ib.reqMktData(c, '', snapshot=True, regulatorySnapshot=False)
        gt = ib.reqMktData(c, '100,101,104,106', snapshot=False, regulatorySnapshot=False)
        ib.sleep(10)
        show('DEFAULT', dt)
        show('GENERIC', gt)
        ib.cancelMktData(c)
finally:
    ib.disconnect()
