import websocket
import time
import json
import hmac
import hashlib
import urllib.parse

#websocket.enableTrace(True)
ws1 = websocket.WebSocket()

api_key = ""
secret_key = ""

base_url = "wss://api.binance.com"
endpoint_path = "/sapi/wss"

timestamp = round(time.time()*1000)
params = {
    "random": "56724ac693184379ae23ffe5e910063c",
    "topic": "earn_swapprice_62",
    "recvWindow":60000,
    "timestamp":timestamp
}
querystring = urllib.parse.urlencode(params,safe="|")

signature = hmac.new(secret_key.encode('utf-8'),msg = querystring.encode('utf-8'), digestmod = hashlib.sha256).hexdigest()
url = base_url + endpoint_path + "?" + querystring + "&signature=" + signature.upper()

print(url)
try:
    ws1.connect(url, header={"X-MBX-APIKEY": api_key, "Content-Type": "application/x-www-form-urlencoded"})
    while True:
        print(json.loads(ws1.recv()))
except Exception as e:
    print(e)
