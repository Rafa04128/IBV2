import MetaTrader5 as mt5
import pytz
from datetime import datetime

# Connect to the MetaTrader 5 terminal
print("MetaTrader5 package author: ",mt5.__author__)
print("MetaTrader5 package version: ",mt5.__version__)

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

# set time zone to UTC
timezone = pytz.timezone("Etc/UTC")
utc_from = datetime(2020, 1, 10, tzinfo=timezone)
# create 'datetime' object in UTC time zone to avoi

# Define the trade parameters
symbol = "BTCUSD"
lot_size = 0.1
stop_loss_pips = 200
take_profit_pips = 200

# Define the EMA parameters
ema_period = 10
ema_applied_price = 6

# Request the OHLCV data
rates = mt5.copy_rates_from(symbol, mt5.TIMEFRAME_M1, 0, ema_period + 1)

# Check if the rates are retrieved successfully
if rates is None or len(rates) == 0:
    print("Failed to retrieve rates for the specified symbol and timeframe.")
    mt5.shutdown()
    exit(1)

# Request the EMA values
ema = sum(rates[i][4] for i in range(ema_period + 1)) / (ema_period + 1)

# Get the latest price
latest_price = mt5.symbol_info_tick(symbol).ask

# Check if the latest price is above the EMA
if latest_price > ema[-1]:
    # Calculate the stop loss and take profit levels
    stop_loss = latest_price - (stop_loss_pips * mt5.symbol_info(symbol).point)
    take_profit = latest_price + (take_profit_pips * mt5.symbol_info(symbol).point)

    # Prepare the trade request
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot_size,
        "type": mt5.ORDER_TYPE_BUY,
        "price": latest_price,
        "sl": stop_loss,
        "tp": take_profit,
        "magic": 123456,
        "comment": "Trade opened by Python",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_FOK,
    }

    # Send the trade request
    result = mt5.order_send(request)

    # Check if the trade request was successful
    if result.retcode == mt5.TRADE_RETCODE_DONE:
        print("Trade opened successfully.")
    else:
        print("Failed to open the trade. Error:", result.comment)
else:
    print("Price is not above the EMA. No trade opened.")

# Disconnect from the MetaTrader 5 terminal
mt5.shutdown()