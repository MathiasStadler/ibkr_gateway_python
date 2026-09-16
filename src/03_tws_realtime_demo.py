#!/usr/bin/env python3
# TWS-Socket-Version mit reqMarketDataType(3) (realtime = Alt+Ctrl+T in TWS GUI)
from ib_insync import IB, Stock, Option
TWS_HOST = '127.0.0.1'
TWS_PORT = 7496

ib = IB()
ib.connect(TWS_HOST, TWS_PORT, clientId=99)
ib.reqMarketDataType(3)  # 3 = Realtime (entspricht Alt+Ctrl+T in TWS)
print("TWS verbunden. MarketDataType=3 (Realtime) aktiv.")
# Beispiel: SPY-Options abrufen (nur Demo - Daten kommen jetzt vollständig)
contract = Stock('SPY', 'SMART', 'USD')
ib.qualifyContracts(contract)
print(f"ConId SPY: {contract.conId}")
ib.sleep(2)
ib.disconnect()
