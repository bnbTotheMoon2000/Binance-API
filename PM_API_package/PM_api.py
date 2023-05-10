import hmac
import time
import hashlib
import requests
from urllib.parse import urlencode
import websocket


class Client:
    def __init__(self,api_key,api_secret,base_url):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url
        
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
    
    def send_signed_request(self, apply_method,url_path, payload={}):
        
        query_string = urlencode(payload)
        # replace single quote to double quote
        query_string = query_string.replace("%27", "%22")
        if query_string:
            query_string = "{}&timestamp={}".format(query_string, self.get_timestamp())
        else:
            query_string = "timestamp={}".format(self.get_timestamp())

        url = (
            self.base_url +url_path+"?" + query_string + "&signature=" + self.hashing(query_string)
        )
        print("{} {}".format(apply_method, url))
        params = {"url": url, "params": {}}
        response = self.dispatch_request(apply_method)(**params)
        return response.json()
    
    def send_sined_request_variableParams(self,apply_method,url_path,payload={}):
        query_string = urlencode({k:v for k,v in payload.items() if v is not None})
        query_string = query_string.replace("%27", "%22")
        if query_string:
            query_string = "{}&timestamp={}".format(query_string, self.get_timestamp())
        else:
            query_string = "timestamp={}".format(self.get_timestamp())

        url = (
            self.base_url +url_path+"?" + query_string + "&signature=" + self.hashing(query_string)
        )
        print("{} {}".format(apply_method, url))
        params = {"url": url, "params": {}}
        response = self.dispatch_request(apply_method)(**params)
        return response.json()
    
    def send_public_request(self,url_path,payload={}):
        query_string = urlencode(payload, True)
        url = self.base_url + url_path
        if query_string:
            url = url + "?" + query_string
        print("{}".format(url))
        response = self.dispatch_request("GET")(url=url)
        return response.json()
    
    def account_balance(self):
        account_balance = self.send_signed_request("GET","/papi/v1/balance")
        return account_balance 
    
    def account_information(self):
        account_information = self.send_signed_request("GET","/papi/v1/account")
        return account_information 
    
    def margin_max_borrow(self,params):
        """
        pass parameter asset
        """
        margin_max_borrow = self.send_signed_request('GET',"/papi/v1/margin/maxBorrowable",params)
        return margin_max_borrow

    def query_margin_max_withdraw(self,asset=None):
        """
        pass parameter asset
        """
        endpoint = "/papi/v1/margin/maxWithdraw"
        params = {'asset':asset}
        query_margin_max_withdraw = self.send_signed_request('GET',endpoint,params)
        return query_margin_max_withdraw
    
    def query_um_position_information(self,symbol=None):
        """
        pass symbol
        """
        if symbol !=None:
            params = {'symbol':symbol}
            query_um_position_information = self.send_signed_request('GET',"/papi/v1/um/positionRisk",params)
            return query_um_position_information
        else:
            query_um_position_information = self.send_signed_request('GET',"/papi/v1/um/positionRisk")
            return query_um_position_information
        
    def query_cm_position_information(self,marginAsset=None,pair=None):
        endpoint = "/papi/v1/cm/positionRisk"
        params = {'marginAsset':marginAsset,
                  "pair":pair}
        query_cm_position_information = self.send_sined_request_variableParams('GET',endpoint,params)
        return query_cm_position_information
        
    def change_um_initial_leverage(self,symbol,leverage=int):
        params = {'symbol':symbol,
                  'leverage':leverage}
        change_um_initial_leverage = self.send_signed_request("POST",'/papi/v1/um/leverage',params)
        return change_um_initial_leverage
    
    def change_cm_initial_leverage(self,symbol,leverage=int):
        params = {'symbol':symbol,
                  'leverage':leverage}
        change_cm_initial_leverage = self.send_signed_request("POST",'/papi/v1/um/leverage',params)
        return change_cm_initial_leverage
    
    def change_um_position_mode(self,dualSidePosition):
        '''
        dualSidePosition
        true: Hedge Mode
        false: One-way Mode
        '''
        params = {'dualSidePosition':dualSidePosition}
        change_um_position_mode = self.send_signed_request("POST","/papi/v1/um/positionSide/dual",params)
        return change_um_position_mode
    
    def get_um_current_position_mode(self):
        get_um_current_position_mode = self.send_signed_request("GET",'/papi/v1/um/positionSide/dual')
        return get_um_current_position_mode
    
    def get_cm_current_position_mode(self):
        get_cm_current_position_mode = self.send_signed_request("GET",'/papi/v1/cm/positionSide/dual')
        return get_cm_current_position_mode
    
    def um_account_trade_list(self,symbol,starTime=None, endTime=None,fromId=None,limit=None):
        endpoint = "/papi/v1/um/userTrades"
        params = {
            "symbol": symbol,
            "startTime": starTime,
            "endTime": endTime,
            "fromId": fromId,
            "limit": limit,
        }
        um_account_trade_list = self.send_sined_request_variableParams("GET",endpoint,params)
        return um_account_trade_list
    
    def cm_account_trade_list(self,symbol,starTime=None, endTime=None,fromId=None,recvWindow=None,limit=None):
        endpoint = "/papi/v1/cm/userTrades"
        params = {
            "symbol": symbol,
            "startTime": starTime,
            "endTime": endTime,
            "fromId": fromId,
            "recvWindow":recvWindow,
            "limit": limit
        }
        cm_account_trade_list = self.send_sined_request_variableParams("GET",endpoint,params)
        return cm_account_trade_list
    
    def um_notional_and_leverage_brackets(self,symbol=None,recvWindow=None):
        endpoint = "/papi/v1/um/leverageBracket"
        params = {
            'symbol':symbol,
            'recvWindow':recvWindow
        }
        um_notional_and_leverage_brackets = self.send_sined_request_variableParams('GET',endpoint,params)
        return um_notional_and_leverage_brackets
    
    def cm_notional_and_leverage_brackets(self,symbol=None,recvWindow=None):
        endpoint = "/papi/v1/cm/leverageBracket"
        params = {
            'symbol':symbol,
            'recvWindow':recvWindow
        }
        cm_notional_and_leverage_brackets = self.send_sined_request_variableParams('GET',endpoint,params)
        return cm_notional_and_leverage_brackets
    
    def query_user_margin_force_orders(self,starTime=None,endTime=None,current=None,size=None,recvWindow=None):
        endpoint = "/papi/v1/margin/forceOrders"
        params = {
            'startTime':starTime,
            'endTime':endTime,
            'current':current,
            'size':size,
            "recvWindow":recvWindow
        }
        query_user_margin_force_orders = self.send_sined_request_variableParams("GET",endpoint,params)
        return query_user_margin_force_orders

    def query_user_um_force_orders(self,symbol=None,autoCloseType=None,starTime=None,endTime=None,limit=None,recvWindow=None):
        """
        autoCloseType (ENUM): LIQUIDATION / ADL,
        if starTime not sent, data within 7 days before endTime can be queried. 
        """
        endpoint = "/papi/v1/um/forceOrders"
        params = {
            "symbol":symbol,
            "autoCloseType":autoCloseType,
            'startTime':starTime,
            'endTime':endTime,
            'limit':limit,
            "recvWindow":recvWindow
        }
        query_user_um_force_orders = self.send_sined_request_variableParams("GET",endpoint,params)
        return query_user_um_force_orders
    
    def query_user_cm_force_orders(self,symbol=None,autoCloseType=None,starTime=None,endTime=None,limit=None,recvWindow=None):
        """
        autoCloseType (ENUM): LIQUIDATION / ADL,
        if starTime not sent, data within 7 days before endTime can be queried. 
        """
        endpoint = "/papi/v1/cm/forceOrders"
        params = {
            "symbol":symbol,
            "autoCloseType":autoCloseType,
            'startTime':starTime,
            'endTime':endTime,
            'limit':limit,
            "recvWindow":recvWindow
        }
        query_user_cm_force_orders = self.send_sined_request_variableParams("GET",endpoint,params)
        return query_user_cm_force_orders
    
    def PM_um_trading_quantitative_rules_indicators(self,symbol=None,recvWindow=None):
        endpoint = "/papi/v1/um/apiTradingStatus"
        params = {
            'symbol':symbol,
            "recvWindow":recvWindow
        }
        PM_um_trading_quantitative_rules_indicators = self.send_sined_request_variableParams("GET",endpoint,params)
        return PM_um_trading_quantitative_rules_indicators
    
    def get_user_commission_rate_for_um(self,symbol):
        endpoint = "/papi/v1/um/commissionRate"
        params = {'symbol':symbol}
        get_user_commission_rate_for_um = self.send_sined_request_variableParams('GET',endpoint,params)
        return get_user_commission_rate_for_um
    
    def get_user_commission_rate_for_cm(self,symbol):
        endpoint = "/papi/v1/cm/commissionRate"
        params = {'symbol':symbol}
        get_user_commission_rate_for_cm = self.send_sined_request_variableParams('GET',endpoint,params)
        return get_user_commission_rate_for_cm
    
    def query_margin_loan_record(self,asset,txId=None,starTime=None,endTime=None,current=1,size=None,archived="false",recvWindow=None):
        """
        txId: tranId in POST /papi/v1/marginLoan,
        current: querying page, start from 1, default 1,
        archived: Default: false. Set to true for archived data from 6 months ago
        https://binance-docs.github.io/apidocs/pm/en/#query-margin-loan-record-user_data
        """
        endpoint = "/papi/v1/margin/marginLoan"
        params = {
            "asset":asset,
            "txId":txId,
            "starTime":starTime,
            "endTime":endTime,
            "current":current,
            "size":size,
            "archived":archived,
            "recvWindow":recvWindow
        }
        query_margin_loan_record = self.send_sined_request_variableParams('GET',endpoint,params)
        return query_margin_loan_record
    
    def query_margin_repay_record(self,asset,txId=None,starTime=None,endTime=None,current=1,size=None,archived="false",recvWindow=None):
        """
        txId: tranId in POST /papi/v1/marginLoan,
        current: querying page, start from 1, default 1,
        archived: Default: false. Set to true for archived data from 6 months ago
        https://binance-docs.github.io/apidocs/pm/en/#query-margin-repay-record-user_data
        """
        endpoint = "/papi/v1/margin/repayLoan"
        params = {
            "asset":asset,
            "txId":txId,
            "starTime":starTime,
            "endTime":endTime,
            "current":current,
            "size":size,
            "archived":archived,
            "recvWindow":recvWindow
        }
        query_margin_repay_record = self.send_sined_request_variableParams('GET',endpoint,params)
        return query_margin_repay_record
    
    def get_margin_borrow_loan_interest_history(self,asset,txId=None,starTime=None,endTime=None,current=1,size=None,archived="false",recvWindow=None):
        """
        txId: tranId in POST /papi/v1/marginLoan,
        current: querying page, start from 1, default 1,
        archived: Default: false. Set to true for archived data from 6 months ago
        https://binance-docs.github.io/apidocs/pm/en/#get-margin-borrow-loan-interest-history-user_data
        """
        endpoint = "/papi/v1/margin/marginInterestHistory"
        params = {
            "asset":asset,
            "txId":txId,
            "starTime":starTime,
            "endTime":endTime,
            "current":current,
            "size":size,
            "archived":archived,
            "recvWindow":recvWindow
        }
        query_margin_repay_record = self.send_sined_request_variableParams('GET',endpoint,params)
        return query_margin_repay_record
    
    def query_PM_interest_history(self,asset=None,starTime=None,endTime=None,size=10,recvWindow=None):
        '''
        query user's portfolio margin interest history.
        '''
        endpoint = "/papi/v1/portfolio/interest-history"
        params = {
            'asset':asset,
            'starTime':starTime,
            'endTime':endTime,
            'size':size,
            'recvWindow':recvWindow
        }
        query_PM_interest_history = self.send_sined_request_variableParams("GET",endpoint,params)
        return query_PM_interest_history
    
    def fund_auto_collection(self,asset=None,recvWindow=None):
        """
        Fund collection for Portfolio Margin
        """
        endpoint = "/papi/v1/auto-collection"
        params = {'asset':asset,"recvWindow":recvWindow}
        fund_auto_collection  = self.send_sined_request_variableParams("POST",endpoint,params)
        return fund_auto_collection

    def bnb_transfer(self,amount,transferSide,recvWindow=None):
        """
        transferSide (ENUM): "TO_UM" or "FROM_UM"
        """
        endpoint = "/papi/v1/bnb-transfer"
        params = {
            'amount':amount,
            'transferSide':transferSide,
            "recvWindow":recvWindow
        }
        bnb_transfer = self.send_sined_request_variableParams("POST",endpoint,params)
        return bnb_transfer

    def create_listenKey(self):
        headers = {'X-MBX-APIKEY': self.api_key}
        listenKey = requests.post("https://papi.binance.com/papi/v1/listenKey",headers=headers)
        return listenKey.json()
    
    def update_listenKey(self):
        headers = {'X-MBX-APIKEY': self.api_key}
        listenKey = requests.put("https://papi.binance.com/papi/v1/listenKey",headers=headers)
        return listenKey.json()
    
    def delete_listenKey(self):
        headers = {'X-MBX-APIKEY': self.api_key}
        listenKey = requests.delete("https://papi.binance.com/papi/v1/listenKey",headers=headers)
        return listenKey.json()
    
    def user_stream(self,listenKey):
        stream_url = f"wss://fstream.binance.com/pm/stream/ws/{listenKey}"
        def on_message(ws,message):
            print(message)
        ws = websocket.WebSocketApp(stream_url,on_message=on_message)
        ws.run_forever()

