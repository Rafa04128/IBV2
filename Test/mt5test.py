import MetaTrader5 as mt5
import time

mt5.initialize(
    path="C:\\Users\\R. García\\Downloads\\mt5setup.exe",
    login=68119146,  # Replace with your login ID
    password="21126ac8",
    server="RoboForex-Pro"
)

if not mt5.terminal_info().connected:
    print("Failed to connect to the MetaTrader 5 server.")
    mt5.shutdown()
    exit()
time.sleep(1)
symbol = "BTCUSD"  # Replace with the desired symbol
tick = mt5.symbol_info_tick(symbol)
if tick is None:
    print("Failed to retrieve tick data for symbol:", symbol)
else:
    print("Symbol:", symbol)
    print("Bid:", tick.bid)
    print("Ask:", tick.ask)
    print("Time:", tick.time)

mt5.shutdown()