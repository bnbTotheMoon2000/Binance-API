import websocket
import time
import hashlib
from urllib.parse import urlencode
import json
import hmac
import uuid 

class Websocket_api():
    '''
    Initialization and basic functions
    '''

    def __init__(self,api_key,api_secret,testnet=bool):
        self.api_key = api_key
        self.api_secret = api_secret
        if testnet:
            self.base_url = "wss://testnet.binance.vision/ws-api/v3"
        else:
            self.base_url = "wss://ws-api.binance.com:443/ws-api/v3"
    
    def get_timestamp(self):
        return int(time.time()*1000)
    
    def hashing(self,query_string,api_secret):
        return hmac.new(
        api_secret.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256
    ).hexdigest()

    def websocket_request(self,method,payload={}):
        parameters = {
        "apiKey":self.api_key,
        "timestamp":str(self.get_timestamp())
        }
        parameters.update(payload)
        temp_list = []
        for k,v in parameters.items():
            temp_list.append(k+'='+v)
        temp_list = sorted(temp_list)
        param = "&".join(temp_list)
        sign = self.hashing(param,self.api_secret)
        signature = {'signature':sign}
        parameters.update(signature)
        request = json.dumps(
        {
            'id':str(uuid.uuid4()),
            'method':method,
            'params':parameters})
        ws = websocket.WebSocket()
        ws.connect(self.base_url)
        ws.send(request)
        print(request)
        response = ws.recv()
        response_data = json.loads(response)
        ws.close()
        return response_data

    def websocket_public(self,method,payload={}):
        request = json.dumps({
            'id':str(uuid.uuid4()),
            'method':method,
            'params':payload
            })
        ws = websocket.WebSocket()
        ws.connect(self.base_url)
        ws.send(request)
        print(request)
        response = ws.recv()
        response_data = json.loads(response)
        ws.close()
        print(response_data)
    

    def payload_process(self,payload):
        payload = {k:v for k,v in payload.items() if v is not None}
        return payload

    '''
    Account Requests
    '''

    def account_information(self,recvWindow=None):
        payload = {'recvWindow':recvWindow}
        payload= self.payload_process(payload)
        method = "account.status"
        account_information = self.websocket_request(method=method,payload=payload)
        return account_information
    
    def account_order_rate_limits(self,recvWindow=None):
        payload = {'recvWindow':recvWindow}
        payload= self.payload_process(payload)
        method = "account.rateLimits.orders"
        account_order_rate_limits = self.websocket_request(method=method,payload=payload)
        return account_order_rate_limits
    
    def account_order_history(self,symbol,orderId=None,startTime=None,endTime=None,
                              limit=None,recvWindow=None):
        payload = {'symbol':symbol,
                   'orderId':orderId,
                   'startTime':startTime,
                   'endTime':endTime,
                   'limit':limit,
                   'recvWindow':recvWindow
                   }
        payload= self.payload_process(payload)
        method = "allOrders"
        account_order_history = self.websocket_request(method=method,payload=payload)
        return account_order_history
    
    def account_oco_history(self,fromId=None,startTime=None,endTime=None,limit=None,recvWindow=None):
        """
        Query information about your OCOs, filtered by time range
        """

        payload = {
            "fromId":fromId,
            "startTime":startTime,
            "endTime":endTime,
            "limit":limit,
            "recvWindow":recvWindow}
        payload= self.payload_process(payload)
        method = "allOrderLists"
        account_oco_history = self.websocket_request(method=method,payload=payload)
        return account_oco_history
    
    def account_trade_history(self,symbol,orderId=None,startTime=None,endTime=None,fromId=None,limit=None,recvWindow=None):
        '''
        Query information about all your trades, filtered by time range.
        '''
        payload = {
            'symbol':symbol,
            "orderId":orderId,
            "startTime":startTime,
            "endTime":endTime,
            'fromId':fromId,
            "limit":limit,
            "recvWindow":recvWindow}
        payload= self.payload_process(payload)
        method = "myTrades"
        account_trade_history = self.websocket_request(method=method,payload=payload)
        return account_trade_history
    
    def account_prevented_matches(self,symbol,preventedMatchId=None,orderId=None,fromPreventedMatchId=None,limit=None,recvWindow=None):
        """
        Displays the list of orders that were expired because of STP trigger.

        Combinations supported:
        symbol + preventedMatchId
        symbol + orderId
        symbol + orderId + fromPreventedMatchId (limit will default to 500)
        symbol + orderId + fromPreventedMatchId + limit
        """
        payload = {
            'symbol':symbol,
            "preventedMatchId":preventedMatchId,
            "orderId":orderId,
            "fromPreventedMatchId":fromPreventedMatchId,
            "limit":limit,
            "recvWindow":recvWindow}
        
        payload= self.payload_process(payload)
        method = "myPreventedMatches"
        account_prevented_matches = self.websocket_request(method=method,payload=payload)
        return account_prevented_matches
    

    
    '''
    Trading Requests
    '''
    def new_order(self,symbol,side,type,timeInForce=None,quantity=None,quoteOrderQty=None,price=None,
                       newClientOrderId=None,strategyId=None,strategyType=None,stopPrice=None,trailingDelta=None,
                       icebergQty=None,newOrderRespType=None,selfTradePreventionMode=None,recvWindow=None):
        
        method = "order.place"
        payload = {
            "symbol":symbol,
            "side":side,
            'type':type,
            'timeInForce':timeInForce,
            'quantity':quantity,
            'quoteOrderQty':quoteOrderQty,
            'price':price,
            'newClientOrderId':newClientOrderId,
            "strategyId":strategyId,
            "strategyType":strategyType,
            "stopPrice":stopPrice,
            "trailingDelta":trailingDelta,
            "icebergQty":icebergQty,
            "newOrderRespType":newOrderRespType,
            "selfTradePreventionMode":selfTradePreventionMode,
            "recvWindow":recvWindow
        }
        payload = self.payload_process(payload)
        new_order = self.websocket_request(method=method,payload=payload)
        return new_order
    
    def test_new_order(self,symbol,side,type,timeInForce=None,quantity=None,quoteOrderQty=None,price=None,
                       newClientOrderId=None,strategyId=None,strategyType=None,stopPrice=None,trailingDelta=None,
                       icebergQty=None,newOrderRespType=None,selfTradePreventionMode=None,recvWindow=None):
        
        method = "order.test"
        payload = {
            "symbol":symbol,
            "side":side,
            'type':type,
            'timeInForce':timeInForce,
            'quantity':str(quantity),
            'quoteOrderQty':quoteOrderQty,
            'price':str(price),
            'newClientOrderId':newClientOrderId,
            "strategyId":strategyId,
            "strategyType":strategyType,
            "stopPrice":str(stopPrice),
            "trailingDelta":trailingDelta,
            "icebergQty":str(icebergQty),
            "newOrderRespType":newOrderRespType,
            "selfTradePreventionMode":selfTradePreventionMode,
            "recvWindow":str(recvWindow)
        }
        payload = self.payload_process(payload)
        test_new_order = self.websocket_request(method=method,payload=payload)
        return test_new_order
    
    def query_order(self,symbol,orderId=None,origClientOrderId=None,recvWindow=None):
        method = "order.status"
        payload = {
            'symbol':symbol,
            'orderId':orderId,
            'origClientOrderId':origClientOrderId,
            'recvWindow':recvWindow
        }
        payload = self.payload_process(payload)
        query_order = self.websocket_request(method=method,payload=payload)
        return query_order
    
    def cancel_order(self,symbol,orderId=None,origClientOrderId=None,newClientOrderId=None,cancelRestrictions=None,recvWindow=None):
        '''
        Cancel an active order

        Either orderId or origClientOrderId must be sent 

        cancelRestrictions:

        ONLY_NEW: Cancel will succeed if the order status is NEW. 
        ONLY_PARTIALLY_FILLED: Cancel will succed if order status is PARTIALLY_FILLED.
        '''
        method = "order.cancel"
        payload = {
            "symbol": symbol,
            "orderId": orderId,
            "origClientOrderId": origClientOrderId,
            "newClientOrderId": newClientOrderId,
            "cancelRestrictions": cancelRestrictions,
            "recvWindow": recvWindow
        }
        payload = self.payload_process(payload)
        cancel_order = self.websocket_request(method=method,payload=payload)
        return cancel_order

    def cancel_and_replace_order(self,symbol,cancelReplaceMode,side,type,cancelOrderId=None,cancelOrigClientOrderId=None,cancelNewClientOrderId=None,
                                 timeInForce=None,price=None,quantity=None,quoteOrderQty=None,newClientOrderId=None,newOrderRespType=None,stopPrice=None,
                                 trailingDelta=None,icebergQty=None,strategyId=None,strategyType=None,selfTradePreventionMode=None,cancelRestrictions=None,recvWindow=None):
        
        '''
        Cancel an existing order and immediately place a new order instead of the canceled one.
        https://binance-docs.github.io/apidocs/websocket_api/en/#cancel-order-trade
        '''
        metnod = "order.cancelReplace"
        pass
    
    
    def cancel_open_orders(self,symbol,recvWindow=None):
        method = "openOrders.cancelAll"
        payload = {
            'symbol':symbol,
            'recvWindow':recvWindow
        }
        payload = self.payload_process(payload)
        cancel_open_orders = self.websocket_request(method=method,payload=payload)
        return cancel_open_orders
    
    def place_new_oco(self,symbol,side,price,quantity,listClientOrderId=None,limitClientOrderId=None,limitIcebergQty=None,limitStrategyId=None,
                      limitStrategyType=None,stopPrice=None,trailingDelta=None,stopClientOrderId=None,stopLimitPrice=None,stopLimitTimeInForce=None,
                      stopIcebergQty=None,stopStrategyId=None,stopStrategyType=None,newOrderRespType=None,selfTradePreventionMode=None,recvWindow=None):
        
        """
        Either stopPrice or trailingDelta, or both must be specified
        """

        method = "orderList.place"
        payload = {
            "symbol":symbol,
            "side":side,
            "price":price,
            "quantity":quantity,
            "listClientOrderId":listClientOrderId,
            "limitClientOrderId":limitClientOrderId,
            "limitIcebergQty":limitIcebergQty,
            "limitStrategyId":limitStrategyId,
            "limitStrategyType":limitStrategyType,
            "stopPrice":stopPrice,
            "trailingDelta":trailingDelta,
            "stopClientOrderId":stopClientOrderId,
            "stopLimitPrice":stopLimitPrice,
            "stopLimitTimeInForce":stopLimitTimeInForce,
            "stopIcebergQty":stopIcebergQty,
            "stopStrategyId":stopStrategyId,
            "stopStrategyType":stopStrategyType,
            "newOrderRespType":newOrderRespType,
            "selfTradePreventionMode":selfTradePreventionMode,
            "recvWindow":recvWindow

        }
        payload = self.payload_process(payload)
        place_new_oco = self.websocket_request(method=method,payload=payload)
        return place_new_oco
    
    def current_open_orders(self,symbol=None,recvWindow=None):
        '''
        Query open orders
        '''
        method = "openOrders.status"
        payload = {
            "symbol":symbol,
            "recvWindow":recvWindow
        }
        payload = self.payload_process(payload)
        current_open_orders = self.websocket_request(method=method,payload=payload)
        return current_open_orders
        pass
    
    """
    Market data requests
    """
    def klines(self,symbol,interval,startTime=None,endTime=None,limit=500):
        method = "klines"
        payload = {
            'symbol':symbol,
            'interval':interval,
            'startTime':startTime,
            "endTime":endTime,
            "limit":limit
        }
        payload = self.payload_process(payload)
        klines = self.websocket_public(method=method,payload=payload)
        return klines
    
    def order_book(self,symbol,limit=None):
        method = "depth"
        payload = {
            'symbol':symbol,
            'limit':limit
        }
        payload = self.payload_process(payload)
        order_book = self.websocket_public(method=method,payload=payload)
        return order_book
    
    def recent_trades(self,symbol,limit=None):
        method = "depth"
        payload = {
            'symbol':symbol,
            'limit':limit
        }
        payload = self.payload_process(payload)
        recent_trades = self.websocket_public(method=method,payload=payload)
        return recent_trades
    
    def historical_trades(self,symbol,fromId=None,limit=None):
        '''
        If fromId is not specified, the most recent trades are returned.
        '''
        method = 'trades.historical'
        payload = {'symbol':symbol,'fromId':fromId,'limit':limit}
        payload = self.payload_process(payload)
        historical_trades = self.websocket_public(method=method,payload=payload)
        return historical_trades
    
    def aggregate_trades(self,symbol,fromId=None,starTime=None,endTime=None,limit=None):
        '''
        If fromId is specified, return aggtrades with aggregate trade ID >= fromId.
        Use fromId and limit to page through all aggtrades.
        If startTime and/or endTime are specified, aggtrades are filtered by execution time (T).
        fromId cannot be used together with startTime and endTime.
        If no condition is specified, the most recent aggregate trades are returned.
        '''
        method = "trades.aggregate"
        payload = {
            'symbol':symbol,
            'fromId':fromId,
            'starTime':starTime,
            'endTime':endTime,
            'limit':limit
        }
        payload = self.payload_process(payload)
        aggregate_trades =  self.websocket_public(method=method,payload=payload)
        return aggregate_trades
    
    def current_average_price(self,symbol):
        '''
        get current average price for a symbol
        '''
        method = 'avgPrice'
        payload = {
            'symbol':symbol
        }
        payload = self.payload_process(payload)
        current_average_price = self.websocket_public(method=method,payload=payload)
        return current_average_price
    
    def ticker_price_change_statistics_24hr(self,symbol=None,symbols=None,type=None):
        method = "ticker.24hr"
        payload = {
            'symbol':symbol,
            'symbols':symbols,
            'type':type
        }
        payload = self.payload_process(payload)
        ticker_price_change_statistics_24hr = self.websocket_public(method=method,payload=payload)
        return ticker_price_change_statistics_24hr
    
    def ticker_price_change_statistics_rolling_window(self,symbol=None,symbols=None,type=None,windowSize=None):
        method = "ticker"
        payload = {
            'symbol':symbol,
            'symbols':symbols,
            'type':type,
            'windowSize':windowSize
        }
        payload = self.payload_process(payload)
        ticker_price_change_statistics_rolling_window = self.websocket_public(method=method,payload=payload)
        return ticker_price_change_statistics_rolling_window
    
    def symbol_price_ticker(self,symbol=None,symbols=None):
        method='ticker.price'
        payload = {
            'symbol':symbol,
            'symbols':symbols
        }
        payload = self.payload_process(payload)
        symbol_price_ticker = self.websocket_public(method=method,payload=payload)
        return symbol_price_ticker
    
    def symbol_order_book_ticker(self,symbol=None,symbols=None):
        method='ticker.book'
        payload = {
            'symbol':symbol,
            'symbols':symbols
        }
        payload = self.payload_process(payload)
        symbol_order_book_ticker = self.websocket_public(method=method,payload=payload)
        return symbol_order_book_ticker
    
