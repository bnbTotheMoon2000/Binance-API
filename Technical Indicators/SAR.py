import requests 
import pandas as pd 

"""
Function below built the indicator SAR values. 
"""
def calculate_sar(high, low, close,star=0.02, increment=0.02, maximum=0.2):
  """
  Paramters high, low, close need to be sent in lists.
  """
    start = 0.02
    increment = 0.02
    maximum = 0.2
    sar = [None] * len(high)
    uptrend = None
    EP = None
    SAR = None
    AF = start
    nextBarSAR = None
    
    for i in range(len(high)):
        if i > 0:
            firstTrendBar = False
            SAR = nextBarSAR
            
            if i == 1:
                prevSAR = None
                prevEP = None
                lowPrev = low[i-1]
                highPrev = high[i-1]
                closeCur = close[i]
                closePrev = close[i-1]
                
                if closeCur > closePrev:
                    uptrend = True
                    EP = high[i]
                    prevSAR = lowPrev
                    prevEP = high[i]
                else:
                    uptrend = False
                    EP = low[i]
                    prevSAR = highPrev
                    prevEP = low[i]
                
                firstTrendBar = True
                SAR = prevSAR + start * (prevEP - prevSAR)
            
            if uptrend:
                if SAR > low[i]:
                    firstTrendBar = True
                    uptrend = False
                    SAR = max(EP, high[i])
                    EP = low[i]
                    AF = start
            else:
                if SAR < high[i]:
                    firstTrendBar = True
                    uptrend = True
                    SAR = min(EP, low[i])
                    EP = high[i]
                    AF = start
            
            if not firstTrendBar:
                if uptrend:
                    if high[i] > EP:
                        EP = high[i]
                        AF = min(AF + increment, maximum)
                else:
                    if low[i] < EP:
                        EP = low[i]
                        AF = min(AF + increment, maximum)
            
            if uptrend:
                SAR = min(SAR, low[i-1])
                if i > 1:
                    SAR = min(SAR, low[i-2])
            else:
                SAR = max(SAR, high[i-1])
                if i > 1:
                    SAR = max(SAR, high[i-2])
            
            nextBarSAR = SAR + AF * (EP - SAR)
            
            if uptrend and close[i] > nextBarSAR:
                # Enter short position
                pass
            elif not uptrend and close[i] < nextBarSAR:
                # Enter long position
                pass
            
        sar[i] = SAR
    
    return sar
"""
Start to send a request 
"""
symbol = 'BNBUSDT'
interval = '30m'

url = f"https://fapi.binance.com/fapi/v1/klines?symbol={symbol}&interval={interval}"
kline = requests.get(url).json()
kline = pd.DataFrame(kline) 
kline = kline.iloc[:,:6]
kline.columns = ['time','open','high','low','close','volume']
kline['time'] = pd.to_datetime(kline['time'],unit='ms')
kline['close'] = kline['close'].astype('float')
kline['high'] = kline['high'].astype('float')
kline['low'] = kline['low'].astype('float')

kline['sar'] = calculate_sar(kline.high,kline.low,kline.close)
kline['sar'] = round(kline['sar'],5)
print(kline) 
