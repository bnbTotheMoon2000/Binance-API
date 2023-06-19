import requests
import numpy as np
import pandas as pd 

# define a RSI function
def rsi(series, period):
    delta = series.diff().dropna()
    u = delta * 0
    d = u.copy()
    u[delta > 0] = delta[delta > 0]
    d[delta < 0] = -delta[delta < 0]
    u[u.index[period-1]] = np.mean(u[:period]) 
    u = u.drop(u.index[:(period-1)])
    d[d.index[period-1]] = np.mean(d[:period]) 
    d = d.drop(d.index[:(period-1)])
    rs = u.ewm(com=period-1, min_periods=0, adjust=False, ignore_na=False).mean() / \
         d.ewm(com=period-1, min_periods=0, adjust=False, ignore_na=False).mean()
    return 100 - 100 / (1 + rs)
  
# Send a request 
symbol = "XRPBUSD"
interval = "1m"

url = f"https://fapi.binance.com/fapi/v1/klines?symbol={symbol}&interval={interval}"
response = requests.request("GET", url)
results = response.json()

df = pd.DataFrame(results,columns=range(0,12)).iloc[:,[0,4,5]]
df.columns = ['time','close','volume']
df['time'] = pd.to_datetime(df['time'],unit='ms')
df.set_index(df['time'],inplace=True)
df['close'] = df['close'].astype('float')
df.drop(columns=['time'],inplace=True)

df['RSI'] = rsi(df['close'], 14)
df = df.round(4)
print(df)
