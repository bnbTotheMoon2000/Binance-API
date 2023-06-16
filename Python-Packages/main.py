import hmac
import time
import hashlib
import requests
from urllib.parse import urlencode
import websocket
import json

class Client:
    def __init__(self,api_key,api_secret,base_url,show_headers=False,request_url= False):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url
        self.show_headers = show_headers
        self.request_url = request_url

        
    def hashing(self,query_string):
        query_string = query_string
        return hmac.new(
            self.api_secret.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256
        ).hexdigest()
    
    def get_timestamp(self):
        return int(time.time()*1000)
    
    def dispatch_request(self,apply_method):
        session = requests.Session()
        session.headers.update(
            {"Content-Type": "application/json;charset=utf-8", "X-MBX-APIKEY": self.api_key}
        )
        methods = {
            "GET": session.get,
            "DELETE": session.delete,
            "PUT": session.put,
            "POST": session.post,
        }
        if apply_method == list(methods.keys())[0]:
            return methods.get('GET')
        elif apply_method == list(methods.keys())[1]:
            return methods.get('DELETE')
        elif apply_method == list(methods.keys())[2]:
            return methods.get('PUT')   
        elif apply_method == list(methods.keys())[3]:
            return methods.get('POST')   
    
    def send_signed_request_variableParams(self,apply_method,url_path,payload={}):
        query_string = urlencode({k:v for k,v in payload.items() if v is not None})
        query_string = query_string.replace("%27", "%22")
        if query_string:
            query_string = "{}&timestamp={}".format(query_string, self.get_timestamp())
        else:
            query_string = "timestamp={}".format(self.get_timestamp())

        url = (
            self.base_url +url_path+"?" + query_string + "&signature=" + self.hashing(query_string)
        )
        #print("{} {}".format(apply_method, url))
        params = {"url": url, "params": {}}
        response = self.dispatch_request(apply_method)(**params)

        try:
            results = {'status_code':response.status_code,'response': response.json()}
        except json.JSONDecodeError:
            results = response.text
            return results
        except:
            results = {'status_code':response.status_code,'response':response.text}
            return results
        
        if self.request_url==False and self.show_headers==False:
            results = {"status_code": response.status_code, "response": response.json()}

        elif self.request_url== True and self.show_headers==False:
            results = {"request_url": url, "status_code": response.status_code, "response": response.json()}
        
        elif self.show_headers==True and self.request_url== False:
            results = {"headers": response.headers, "status_code": response.status_code, "response": response.json()}

        elif self.request_url==True and self.show_headers==True:
            results = {"request_url": url, "headers": response.headers, "status_code": response.status_code, "response": response.json()}
         
        return results 
        
    
    def send_public_request(self,apply_method,url_path,payload={}):
        query_string = urlencode({k:v for k,v in payload.items() if v is not None})
        query_string = query_string.replace("%27", "%22")
        url = self.base_url + url_path
        if query_string:
            url = url + "?" + query_string
        print("{}".format(url))
        response = self.dispatch_request(apply_method)(url=url)
        return response.json()

    def websocket_connect(self,url):
        print(url)
        def on_message(ws,message):
            json_msg = json.loads(message)
            print(json_msg)
        def on_close(ws,message):
            print(message)
        ws = websocket.WebSocketApp(url,on_message=on_message,on_close=on_close)
        ws.run_forever()
