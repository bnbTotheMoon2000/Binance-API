import websocket
import time
import hashlib
import requests
import json
import hmac

KEY = ""
SECRET =  ""
BASE_URL = 'https://testnet.binance.vision'

# get timestamp 
def get_timestamp():
    return int(time.time()*1000)

# get parameters that needs to be signed by api secret  
def hashing(query_string):
    return hmac.new(
        SECRET.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256
    ).hexdigest()
 
# sort 
temp_list = []
for k,v in parameters.items():
    temp_list.append(k+'='+v)
    temp_list = sorted(temp_list)
    param = "&".join(temp_list)
 
# make a signature and add signature on parameter 
signature = hashing(param)
parameters.update({"signature":signature})

# convert request parameters into Json format 
request = json.dumps({
  "id": "testing",
  "method": "order.place","params":parameters})

# create a websocket object and connect to testnet 
ws = websocket.WebSocket()
ws.connect('wss://testnet.binance.vision/ws-api/v3')

# send request
ws.send(request)

# get server's response
response = ws.recv()

response_data = json.loads(response)
print(request) # print request information
print(response_data) #print response data 

# close connection
ws.close() 
  
