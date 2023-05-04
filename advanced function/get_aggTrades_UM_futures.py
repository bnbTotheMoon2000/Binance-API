import requests
import pandas as pd 
import warnings
import time
import json 
from datetime import datetime 
import pytz
warnings.filterwarnings("ignore", category=Warning)

start_time = input("Please input start_time (xxxx-xx-xx xx:xx:xx): ")
end_time = input("Please input end_time (xxxx-xx-xx xx:xx:xx): ")
symbol = input("Please input a symbol: ")

t1 = datetime.strptime(start_time,"%Y-%m-%d %H:%M:%S")
t2 = datetime.strptime(end_time,"%Y-%m-%d %H:%M:%S")

tz = pytz.timezone('UTC')
t1_utc = tz.localize(t1).astimezone(pytz.utc)
t2_utc = tz.localize(t2).astimezone(pytz.utc)

start_ts =int(datetime.timestamp(t1_utc))*1000
end_ts=int(datetime.timestamp(t2_utc))*1000


trades_url = f"https://fapi.binance.com/fapi/v1/aggTrades"
df = pd.DataFrame()

while True:
    trades = []
    params = {'symbol':symbol,
              'startTime':start_ts,
              'limit':1000}
    
    response = requests.get(trades_url,params=params)
    time.sleep(1)
    print(response.url)
    data = json.loads(response.text)
    df = df.append(pd.DataFrame(data),ignore_index=True)
    trades.extend(data)
    
    start_ts =int(trades[-1]['T'])    
    if trades[-1]['T'] > end_ts:
        break

df.columns = ['agg_trade_id','price','quantity','1st_trade_id','last_trade_id','timestamp','maker_buyer']
df['time'] = pd.to_datetime(df['timestamp'], unit='ms')
df.index  = df['time']
print(df)
