from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract

import threading
import time

class IBapi(EWrapper, EClient):
	def __init__(self):
		EClient.__init__(self, self)
	def historicalData(self, reqId, bar):
		print(f'Time: {bar.date} Close: {bar.close}')
		
def run_loop():
	app.run()

app = IBapi()
app.connect('127.0.0.1', 7497, 1)

#Start the socket in a thread
api_thread = threading.Thread(target=run_loop, daemon=True)
api_thread.start()

time.sleep(1) #Sleep interval to allow time for connection to server

#Create contract object
eurusd_contract = Contract()
eurusd_contract.symbol = 'VIX'
eurusd_contract.secType = 'IND'
eurusd_contract.exchange = 'CBOE'
eurusd_contract.currency = 'USD'

#Request historical candles
# app.reqHistoricalData(1, eurusd_contract, '', '2 D', '1 hour', 'BID', 0, 2, False, [])
app.reqHistoricalData(1, eurusd_contract, '', '1 D', '1 day', 'TRADES', 0, 2, False, [])
# data = app.reqHistoricalData(
#     eurusd_contract,                  # VIX index contract object
#     endDateTime='',             # Empty string means "latest data available"
#     durationStr='1 D',          # Duration of the historical data (1 day)
#     barSizeSetting='1 day',     # Bar size of the historical data (1 day)
#     whatToShow='TRADES',        # Data type to request (trade data)
#     useRTH=True,                # Use regular trading hours data only
#     formatDate=1                # Format date as UNIX timestamp
# )

time.sleep(5) #sleep to allow enough time for data to be returned
app.disconnect()