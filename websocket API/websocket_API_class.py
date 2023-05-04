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
            "id": "testing",
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
      
# call request function from the class 
# for example, to place an order 

websocket = Websocket_api(api_key,secret_key,base_url)
parameters = {
    'symbol':'BNBUSDT',
    "timeInForce":'GTC',
    'type':'LIMIT',
    'newOrderRespType':'RESULT',
    'price':'200.00',
    'quantity':"1.3",
    'side':'BUY',    
}

websocket.request(method= 'order.place',payload = parameters)
