import MetaTrader5 as mt5
from datetime import datetime

# Connect to the MetaTrader 5 server

if not mt5.initialize(login=68119146, password="21126ac8", server="RoboForex-Pro"):
    print("initialize() failed, error code =",mt5.last_error())
    quit()
authorized=mt5.login(68119146, password="21126ac8", server="RoboForex-Pro")

if authorized:
    print(mt5.account_info())
    print("Show account_info()._asdict():")
    account_info_dict = mt5.account_info()._asdict()
    for prop in account_info_dict:
        print("  {}={}".format(prop, account_info_dict[prop]))
else:
    print("failed to connect at account #{}, error code: {}".format(account, mt5.last_error()))

# Specify the symbol, timeframe, and the time range
symbol = "BTCUSD"
timeframe = mt5.TIMEFRAME_M1
from_date = datetime(2022, 1, 1)
to_date = datetime(2022, 12, 20)

# Convert the date objects to MetaTrader 5 timestamps
from_timestamp = from_date.timestamp()
to_timestamp = to_date.timestamp()

# Request the OHLCV data
rates = mt5.copy_rates_from(symbol, timeframe, from_timestamp, to_timestamp)

for rate in rates:
    print(rate)


# Disconnect from the MetaTrader 5 server
mt5.shutdown()