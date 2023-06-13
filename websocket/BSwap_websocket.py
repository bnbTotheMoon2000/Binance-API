import websocket
import time
import json
import hmac
import hashlib
import urllib.parse
import uuid 

def random_string():
    return str(uuid.uuid1())[:32]

def time_stamp():
    return str(int(time.time()*1000))

def signature(key,obj):
    sign = hmac.new(key=key.encode('utf-8'),msg=obj.encode('utf-8'),digestmod=hashlib.sha256)
    return sign.hexdigest()


#websocket.enableTrace(True)
ws1 = websocket.WebSocket()

api_key = ""
api_secret = ""
topic = "earn_swapprice_62|earn_swapprice_72"
base_url = "wss://api.binance.com"
endpoint_path = "/sapi/wss"

params = {
    "random": random_string(),
    "topic": topic,
    "recvWindow":60000,
    "timestamp":time_stamp()
}
querystring = urllib.parse.urlencode(params,safe="|")
sign = signature(api_secret,querystring)
params.update({'signature':sign})
querystring = urllib.parse.urlencode(params,safe="|")
url = urllib.parse.urljoin(base_url,endpoint_path)+"?"+querystring
print(url)

try:
    ws1.connect(url, header={"X-MBX-APIKEY": api_key, "Content-Type": "application/x-www-form-urlencoded"})
    while True:
        print(json.loads(ws1.recv()))
except Exception as e:
    print(e)
