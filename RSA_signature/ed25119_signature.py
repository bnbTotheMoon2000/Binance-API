import base64
import requests
import time
from urllib.parse import urlencode
from cryptography.hazmat.primitives.serialization import load_pem_private_key

""" 
Start to send a request 
"""

api_key = ""
private_key_path = "api_secret.pem"
headers = {"Content-Type": "application/json;charset=utf-8", "X-MBX-APIKEY": api_key}

# Reading private key 
with open(private_key_path,'rb') as file:
    private_key = load_pem_private_key(data=file.read(),password=None)

# Signature function
def signature(obj):
    return base64.b64encode(private_key.sign(obj.encode('ASCII'))).decode('utf-8')

# Timestamp
def get_timestamp():
    return int(time.time()*1000)

def um_account_info(**kwargs):
    if kwargs ==None:
        params = {'timestamp':get_timestamp()}
    else:
        params = kwargs
        params['timestamp'] = get_timestamp()
    sign = signature(urlencode(params))
    params['signature'] = sign
    response = requests.get(
    f'https://fapi.binance.com/fapi/v2/account?{urlencode(params)}',
    headers=headers
    )
    print(response.request.url)
    return response.json()

def um_new_order(**kwargs):
    params = kwargs
    params['timestamp'] = get_timestamp()
    sign = signature(urlencode(params))
    params['signature'] = sign
    response = requests.post(
        f"https://fapi.binance.com/fapi/v1/order?{urlencode(params)}",
        headers = headers
    )
    print(response.request.url)
    return response.json()

um_new_order(symbol='XRPUSDT',side='BUY',type='LIMIT',price=0.3,quantity=100,timeInForce='GTC')

