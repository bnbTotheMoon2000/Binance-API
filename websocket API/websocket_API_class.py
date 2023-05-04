import websocket
import time
import hashlib
import requests
import json
import hmac
import uuid 


# define a websocket API class
class Websocket_api():
    def __init__(self,api_key,secret_key,base_url):
        self.api_key = api_key
        self.secret_key = secret_key
        self.base_url = base_url
    
    def get_timestamp(self):
        return int(time.time()*1000)
    
    def hasing(self,query_string):
        return hmac.new(
        self.secret_key.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256
    ).hexdigest()

    def request(self,method,payload={}):
        payload.update({"apiKey":self.api_key,'timestamp':str(self.get_timestamp())})
        temp_list = []
        for k,v in payload.items():
            temp_list.append(k+'='+v)
            temp_list = sorted(temp_list)
            param = "&".join(temp_list)
            signature = self.hasing(param)
        payload.update({'signature':signature})

        request = json.dumps({
            "id": str(uuid.uuid4()).replace("-","")[:8],
            "method": method,
            "params":payload})
        ws = websocket.WebSocket()
        ws.connect(self.base_url)

        # send request
        ws.send(request)
        # get server's response
        response = ws.recv()
        ws.close() 
        return response 
    
    def create_listen_key(self):
        payload = {"apiKey":self.api_key}
        request = json.dumps({
            "id":str(uuid.uuid4()).replace("-","")[:8],
            "method":"userDataStream.start",
            "params":payload
        })
        ws = websocket.WebSocket()
        ws.connect(self.base_url)
        ws.send(request)
        response = ws.recv()
        ws.close()
        return response 
      
# call request function from the class 
# for example, to place an order 

ws = Websocket_api(api_key,secret_key,base_url)
parameters = {
    'symbol':'BNBUSDT',
    "timeInForce":'GTC',
    'type':'LIMIT',
    'newOrderRespType':'RESULT',
    'price':'200.00',
    'quantity':"1.3",
    'side':'BUY'}
ws.request(method="order.place",payload=parameters)
