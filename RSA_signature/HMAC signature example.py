import requests
import time
import hmac
import hashlib
from urllib.parse import urlencode

API_Key = "API key"
Secret_Key = "API secret"
base_url = "https://testnet.binance.vision"
headers = {"Content-Type": "application/json;charset=utf-8", "X-MBX-APIKEY": API_Key}

def get_sha256(Secret_Key, data):

    key = Secret_Key.encode('utf-8')  
    data = data.encode('utf-8')
    sign = hmac.new(key, data, hashlib.sha256).hexdigest()
    return sign

def get_timestamp():
    timestamp = str(int(float(time.time()) * 1000))
    return timestamp 

def spot_test_order(**args):
    params = urlencode(args)
    query_string = f"{params}&timestamp={get_timestamp()}"
    sign = get_sha256(Secret_Key, query_string)
    test_order_url = base_url+"/api/v3/order/test?"+query_string+"&signature="+sign
    resp = requests.post(test_order_url,headers=headers)
    print(resp.url)
    print(resp.json())
    
"""
Calling the function of spot_test_order, will place a test order on testnet. 

spot_test_order(symbol='BTCUSDT',side='BUY',type='MARKET',quantity=0.1)
"""
