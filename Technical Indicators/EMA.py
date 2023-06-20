import requests
import numpy as np
import pytz
from datetime import datetime
import pandas as pd

def calculate_ema(data, length):
    alpha = 2 / (length + 1)
    ema = np.zeros(len(data))
    ema[0] = data[0]

    for i in range(1, len(data)):
        ema[i] = alpha * data[i] + (1 - alpha) * ema[i - 1]
    return ema

def time_ts(given_time):
    time_obj = datetime.strptime(given_time,"%Y-%m-%d %H:%M:%S")
    time_obj = time_obj.replace(pytz.utc)
    timestamp = int(time_obj.timestamp()*1000)
    return timestamp

symbol = 'BTCUSDT'
startTime = '2023-06-01 00:00:00'
interval = '1h'
url = "https://fapi.binance.com/fapi/v1/klines"
params = {
    'symbol':symbol,
    'interval':interval,
    'startTime':startTime
}
resp = requests.get(url,params=params)
data = resp.json()
price = pd.DataFrame(data)
price = price.iloc[:,:6]
price.columns = ['openTime','open','high','low','close','volume']
price[['open','high','low','close','volume']]  = price[['open','high','low','close','volume']].astype('float')
close_list = price.close.to_list()
close_list = calculate_ema(close_list,12)
price['openTime'] = pd.to_datetime(price['openTime'],unit='ms')
price['ema_12'] = close_list
price['ema_12'] = price['ema_12'].apply(round,ndigits=2)
print(price)


