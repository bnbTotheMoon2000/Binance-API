from main import Client 
import datetime as dt 
import requests 

class UM_futures(Client):
    def __init__(self,api_key,api_secret,testnet=bool,show_headers=False,request_url=False):
        super().__init__(self,api_key,api_secret,show_headers=False,request_url=False)
        self.api_key = api_key
        self.api_secret = api_secret
        self.show_headers = show_headers
        self.request_url = request_url

        if testnet != True:
            self.base_url = "https://fapi.binance.com"
            self.websocket_url = "wss://fstream.binance.com/ws/"
        else:
            self.base_url = 'https://testnet.binancefuture.com'
            self.websocket_url = "wss://stream.binancefuture.com/ws/"

    def time_ts(self,time_obj):
        if time_obj is None:
            return None
        
        strptime = dt.datetime.strptime(time_obj,"%Y-%m-%d %H:%M:%S")
        ts = str(int(dt.datetime.timestamp(strptime)*1000))
        return ts 
    
    def get_positin_margin_chagne_history(self,symbol,type=None,startTime=None,endTime=None,limit=None,recvWindow=None):
        endpoint = "/fapi/v1/positionMargin/history"
        params = {
            "symbol":symbol,
            'type':type,
            "startTime":self.time_ts(startTime),
            'endTime':self.time_ts(endTime),
            'limit':limit,
            'recvWindow':recvWindow
        }
        get_positin_margin_chagne_history = self.send_signed_request_variableParams('GET',endpoint,params)
        return get_positin_margin_chagne_history

    
    '''
    Websocket Market
    '''
    def websocket_market(self,streams):
        url = self.websocket_url+streams
        ws = self.websocket_connect(url)
        return ws 
