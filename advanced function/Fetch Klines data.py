import requests
import datetime as dt 
import time 
import pandas as pd   
import pytz

#Fetch Kline data for UM Futures Markets 

def time_ts(time_obj):   # 2023-06-14 00:00:00
    if time_obj == None:
        return None 
    else:
        obj = dt.datetime.strptime(time_obj,"%Y-%m-%d %H:%M:%S")
        obj = obj.replace(tzinfo=pytz.utc)
        timestamp = str(int(obj.timestamp()*1000))
        return timestamp

def KlineDownload(type,symbol,interval,startTime,endTime=None):
    if endTime == None:
        startTime = time_ts(startTime)
        endTime = int(time.time()*1000)
    else:
        startTime = time_ts(startTime)
        endTime = time_ts(endTime)

    df = pd.DataFrame()

    while True:
        if type=="um_futures":
            url = f"https://fapi.binance.com/fapi/v1/klines?symbol={symbol}&interval={interval}&startTime={startTime}&limit=1500"
        elif type=='spot':
            url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&startTime={startTime}&limit=1000"
        elif type =='cm_futures':
            url = f"https://dapi.binance.com/dapi/v1/klines?symbol={symbol}&interval={interval}&startTime={startTime}&limit=1500"
        result = requests.get(url)
        time.sleep(1)
        print(result.url)
        temp = pd.DataFrame(result.json(),columns=['open_time','open','high','low','close','volume','close_time','quote_asset_volume','number_of_trades',
                                        "taker_buy_base_asset_volume",'taker_buy_quote_asset_volume','ignore'])
        df  = pd.concat(objs=[df,temp],ignore_index=True)
        
        df[['open_time','close_time']] = df[['open_time','close_time']].astype(int)
        startTime = df.iloc[-1,6]+1
        if int(time.time()*1000) - df.iloc[-1,6] <0:
            df.insert(0,column='open_Time',value=pd.to_datetime(df['open_time'],unit='ms'))
            df.insert(8,column='close_Time',value=pd.to_datetime(df['close_time'],unit='ms'))
            break
        df.to_excel(f"{symbol}_{interval}_kline.xlsx")
    return df 

# Example:
KlineDownload(type='cm_futures',symbol='XRPUSD_PERP',interval='30m',startTime='2023-06-14 00:00:00')

