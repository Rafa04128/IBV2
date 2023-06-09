import MetaTrader5 as mt5
from datetime import datetime
import pandas as pd 
import pytz
# Connect to the MetaTrader 5 server

print("MetaTrader5 package author: ",mt5.__author__)
print("MetaTrader5 package version: ",mt5.__version__)

pd.set_option('display.max_columns', 500) # number of columns to be displayed
pd.set_option('display.width', 1500)      # max table width to display

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

symbols=mt5.symbols_get()
print('Symbols: ', len(symbols))
count=0

# display the first five ones
for s in symbols:
    count+=1
    print("{}. {}".format(count,s.name))
    if count==118: break
print()

ru_symbols=mt5.symbols_get("*TC*")
print('len(*TC*): ', len(ru_symbols))
for s in ru_symbols:
    print(s.name)
print()

selected=mt5.symbol_select("GBPUSD",True)
if not selected:
    print("Failed to select GBPUSD")
    mt5.shutdown()
    quit()

 # set time zone to UTC
timezone = pytz.timezone("Etc/UTC")

# create 'datetime' objects in UTC time zone to avoid the implementation of a local time zone offset
utc_from = datetime(2020, 1, 10, tzinfo=timezone)
utc_to = datetime(2020, 1, 11, tzinfo=timezone)

# request AUDUSD ticks within 11.01.2020 - 11.01.2020
ticks = mt5.copy_ticks_range("CADCHF", utc_from, utc_to, mt5.COPY_TICKS_ALL)
print("Ticks received:",len(ticks))


mt5.shutdown()

# display data on each tick on a new line
print("Display obtained ticks 'as is'")
count = 0
for tick in ticks:
    count+=1
    print(tick)
    if count >= 10:
        break

ticks_frame = pd.DataFrame(ticks)
# convert time in seconds into the datetime format
ticks_frame['time']=pd.to_datetime(ticks_frame['time'], unit='s')

# display data
print("\nDisplay dataframe with ticks")
print(ticks_frame.head(10)) 
