from main import Client 
import requests

class Spot_trading(Client):
    def __init__(self,api_key,api_secret,testnet=bool,show_headers=False,request_url=False):
        super().__init__(self,api_key,api_secret,show_headers=False,request_url=False)
        self.api_key = api_key
        self.api_secret = api_secret
        self.show_headers = show_headers
        self.request_url = request_url

        if testnet:
            self.base_url = "https://testnet.binance.vision"
            self.websocket_url = "wss://testnet.binance.vision/ws"
        else:
            self.base_url = 'https://api.binance.com'
            self.websocket_url = "wss://stream.binance.com:9443/ws"

    '''
    Query IP
    '''
    def query_ip(self):
        '''
        query IP address , url : https://checkip.amazonaws.com/
        '''
        ip_query = 'https://checkip.amazonaws.com/'
        result = requests.get(ip_query).text
        return result 
    
    '''
    Wallet Endpoints
    '''
    def system_status(self):
        '''
        Fetch system status 
        0: normal;
        1: system maintenance
        '''
        endpoint = "/sapi/v1/system/status"
        system_status = self.send_public_request("GET",endpoint)
        return system_status
    
    def all_coins_information(self,recvWindow=None):
        '''
        Get information of coins (available for deposit and withdraw) for user. 
        https://binance-docs.github.io/apidocs/spot/en/#all-coins-39-information-user_data
        '''
        endpoint = "/sapi/v1/capital/config/getall"
        params = {
            'recvWindow':recvWindow
        }
        all_coins_information = self.send_signed_request_variableParams("GET",endpoint,params)
        return all_coins_information
    
    def user_asset(self,asset=None,needBtcValuation=None,recvWindow=None):
        endpoint = '/sapi/v3/asset/getUserAsset'
        params = {
            "asset":asset,
            "needBtcValuation":needBtcValuation,
            "recvWindow":recvWindow
        }
        user_asset = self.send_signed_request_variableParams("POST",endpoint,params)
        return user_asset
    
    def account_information(self,recvWindow=None):
        endpoint = "/api/v3/account"
        params = {
            'recvWindow':recvWindow
        }
        account_information = self.send_signed_request_variableParams("GET",endpoint,params)
        return account_information
    
    '''
    Websocket Market
    '''
    def websocket_market(self,streams):
        url = self.websocket_url + '/'+streams
        ws = self.websocket_connect(url)
        return ws 
