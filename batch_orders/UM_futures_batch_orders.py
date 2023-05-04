import json
import requests
import time
import hmac
import hashlib
from urllib.parse import quote

API_Key = ""
Secret_Key = ""

def get_sha256(Secret_Key, data):

    key = Secret_Key.encode('utf-8')  
    data = data.encode('utf-8')
    sign = hmac.new(key, data, hashlib.sha256).hexdigest()
    return sign

time_str = str(int(float(time.time()) * 1000))

orders = [{"type":"LIMIT","timeInForce":"GTC",
"symbol":"BTCUSDT","side":"BUY","price":"10001","quantity":"0.001"},
{"type":"LIMIT","timeInForce":"GTC",
"symbol":"BTCUSDT","side":"SELL","price":"60001","quantity":"0.001"}]

json_string = json.dumps(orders)
orders_encode = quote(json_string)

query_string = f"batchOrders={orders_encode}&timestamp={time_str}"

sign = get_sha256(Secret_Key, query_string)

headers = {"Content-Type": "application/json;charset=utf-8", "X-MBX-APIKEY": API_Key}
    
url = "https://testnet.binancefuture.com/fapi/v1/batchOrders"+"?"+query_string+"&signature="+sign

response = requests.post(url,headers=headers)
print(response.url)
print(response.json())
