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
    
    
    def ping(self):
        '''
        GET /fapi/v1/ping
        Test connectivity to the Rest API.
        https://binance-docs.github.io/apidocs/futures/en/#test-connectivity
        '''
        endpoint = "/fapi/v1/ping"
        test_ping = self.send_public_request('GET',endpoint)
        return test_ping
    
    def check_server_time(self):
        '''
        GET /fapi/v1/time
        Test connectivity to the Rest API and get the current server time.
        https://binance-docs.github.io/apidocs/futures/en/#check-server-time
        '''
        endpoint = "/fapi/v1/time"
        server_time = self.send_public_request("GET",endpoint)
        return server_time

    def exchangeInfo(self):
        '''
        GET /fapi/v1/exchangeInfo
        Current exchange trading rules and symbol information
        https://binance-docs.github.io/apidocs/futures/en/#exchange-information 
        '''
        endpoint = "/fapi/v1/exchangeInfo"
        exchangeInfo = self.send_public_request("GET",endpoint)
        return exchangeInfo

    def orderBook(self,symbol,limit=None):
        '''
        GET /fapi/v1/depth
        order book data
        https://binance-docs.github.io/apidocs/futures/en/#order-book
        '''
        endpoint = "/fapi/v1/depth"
        params = {
            "symbol": symbol,
            "limit": limit
        }
        orderBook = self.send_public_request("GET",endpoint,params)
        return orderBook
    
    def recent_trades_list(self,symbol,limit=None):
        '''
        GET /fapi/v1/trades
        Get recent market trades
        https://binance-docs.github.io/apidocs/futures/en/#recent-trades-list
        '''
        endpoint = "/fapi/v1/trades"
        params = {
            "symbol":symbol,
            "limit":limit
        }
        result = self.send_public_request("GET",endpoint,params)
        return result
    
    def old_trades_lookup(self,symbol,limit=None,fromId=None):
        '''
        GET /fapi/v1/historicalTrades
        Get older market historical trades.
        https://binance-docs.github.io/apidocs/futures/en/#old-trades-lookup-market_data

        '''
        endpoint = "/fapi/v1/historicalTrades"
        params = {
           "symbol": symbol,
           "limit": limit,
           "fromId": fromId 
        }
        result = self.send_public_request("GET",endpoint,params)
        return result

    def aggregate_trades_list(self,symbol,fromId=None,startTime=None,endTime=None,limit=None):
        '''
        GET /fapi/v1/aggTrades
        Get compressed, aggregate market trades. Market trades that fill in 100ms with 
        the same price and the same taking side will have the quantity aggregated.
        https://binance-docs.github.io/apidocs/futures/en/#compressed-aggregate-trades-list
        '''
        endpoint = "/fapi/v1/aggTrades"
        params = {
            "symbol":symbol,
            "fromId":fromId,
            "startTime": self.time_ts(startTime),
            "endTime": self.time_ts(endTime),
            "limit": limit
        }
        result = self.send_public_request("GET",endpoint,params)
        return result

    def Klines(self,symbol,interval,startTime=None,endTime=None,limit=None):
        '''
        GET /fapi/v1/klines
        Kline/candlestick bars for a symbol. Klines are uniquely identified by their open time.
        https://binance-docs.github.io/apidocs/futures/en/#compressed-aggregate-trades-list
        '''

        endpoint = "/fapi/v1/klines"
        params = {
            "symbol":symbol,
            "interval":interval,
            "startTime": self.time_ts(startTime),
            "endTime": self.time_ts(endTime),
            "limit":limit
        }
        result = self.send_public_request("GET",endpoint,params)
        return result
    
    def continuous_contract_kline(self,pair,contractType,interval,startTime=None,endTime=None,limit=None):
        '''
        GET /fapi/v1/continuousKlines
        Kline/candlestick bars for a specific contract type.

        Klines are uniquely identified by their open time.      
        https://binance-docs.github.io/apidocs/futures/en/#continuous-contract-kline-candlestick-data
        '''
        endpoint = "/fapi/v1/continuousKlines"
        params = {
            "pair":pair,
            "contractType":contractType,
            "interval": interval,
            "startTime": self.time_ts(startTime),
            "endTime":self.time_ts(endTime),
            "limit":limit
        }
        result = self.send_public_request("GET",endpoint,params)
        return result

    def index_price_kline(self,pair,interval,startTime=None,endTime=None,limit=None):
        '''
        GET /fapi/v1/indexPriceKlines

        Kline/candlestick bars for the index price of a pair.

        Klines are uniquely identified by their open time.

        https://binance-docs.github.io/apidocs/futures/en/#index-price-kline-candlestick-data
        '''

        endpoint = "/fapi/v1/indexPriceKlines"
        params={
            "pair":pair,
            "interval": interval,
            "startTime" : self.time_ts(startTime),
            "endTime" : self.time_ts(endTime),
            "limit" : limit
        }
        result = self.send_public_request("GET",endpoint,params)
        return result


    def mark_price_kline(self,symbol,interval,startTime=None,endTime=None,limit=None):
        '''
        GET /fapi/v1/markPriceKlines

        Kline/candlestick bars for the mark price of a symbol.

        Klines are uniquely identified by their open time.

        https://binance-docs.github.io/apidocs/futures/en/#index-price-kline-candlestick-data
        '''

        endpoint = "/fapi/v1/markPriceKlines"
        params={
            "symbol":symbol,
            "interval": interval,
            "startTime" : self.time_ts(startTime),
            "endTime" : self.time_ts(endTime),
            "limit" : limit
        }
        result = self.send_public_request("GET",endpoint,params)
        return result
    
    def mark_price(self,symbol=None):
        '''
        GET /fapi/v1/premiumIndex
        Mark Price and Funding Rate

        https://binance-docs.github.io/apidocs/futures/en/#mark-price
        '''
        endpoint = "/fapi/v1/premiumIndex"
        params = {
            "symbol": symbol
        }
        result = self.send_public_request("GET",endpoint,params)
        return result

    def get_funding_rate_history(self,symbol=None,startTime=None,endTime=None,limit=None):
        '''
        GET /fapi/v1/fundingRate

        https://binance-docs.github.io/apidocs/futures/en/#get-funding-rate-history

        If startTime and endTime are not sent, the most recent limit datas are returned.
        If the number of data between startTime and endTime is larger than limit, return as startTime + limit.
        In ascending order.

        '''

        endpoint = "/fapi/v1/fundingRate"
        params = {
            "symbol": symbol,
            "startTime": self.time_ts(startTime),
            "endTime": self.time_ts(endTime),
            "limit": limit
        }
        result = self.send_public_request("GET",endpoint,params)
        return result

    def ticker_price_change_statistics_24hr(self,symbol=None):
        '''
        GET /fapi/v1/ticker/24hr

        24 hour rolling window price change statistics.
        Careful when accessing this with no symbol.

        https://binance-docs.github.io/apidocs/futures/en/#24hr-ticker-price-change-statistics
        '''

        endpoint = "/fapi/v1/ticker/24hr"

        params = {
            "symbol" : symbol
        }
        result = self.send_public_request("GET",endpoint,params)
        return result
    
    def symbol_price_ticker(self,symbol=None):
        '''
        GET /fapi/v1/ticker/price

        Latest price for a symbol or symbols.

        https://binance-docs.github.io/apidocs/futures/en/#symbol-price-ticker
        '''
        endpoint = "/fapi/v1/ticker/price"
        params = {
            "symbol": symbol
        }
        result = self.send_public_request("GET",endpoint,params)
        return result
    
    def symbol_order_book_ticker(self,symbol=None):
        '''
        GET /fapi/v1/ticker/bookTicker
        Best price/qty on the order book for a symbol or symbols.

        https://binance-docs.github.io/apidocs/futures/en/#symbol-order-book-ticker

        '''

        endpoint = "/fapi/v1/ticker/bookTicker"

        params = {
            "symbol": symbol
        }
        result = self.send_public_request("GET",endpoint,params)
        return result

    def open_interest(self,symbol):
        '''
        GET /fapi/v1/openInterest
        Get present open interest of a specific symbol.

        https://binance-docs.github.io/apidocs/futures/en/#open-interest

        '''
        endpoint = "/fapi/v1/openInterest"
        params = {
            "symbol": symbol
        }

        result = self.send_public_request("GET",endpoint,params)
        return result
    
    def open_interest_statistics(self,symbol,period,limit=None,startTime=None,endTime=None):
        '''
        GET /futures/data/openInterestHist

        https://binance-docs.github.io/apidocs/futures/en/#open-interest-statistics

        If startTime and endTime are not sent, the most recent data is returned.
        Only the data of the latest 30 days is available.

        '''

        endpoint = "/futures/data/openInterestHist"
        params = {
            "symbol": symbol,
            "period": period,
            "limit": limit,
            "startTime": self.time_ts(startTime),
            "endTime": self.time_ts(endTime)
        }
        result = self.send_public_request("GET",endpoint,params)
        return result


    def top_trader_long_short_ratio_accounts(self,symbol,period,limit=None,startTime=None,endTime=None):
        '''
        GET /futures/data/topLongShortAccountRatio
        https://binance-docs.github.io/apidocs/futures/en/#top-trader-long-short-ratio-accounts

        If startTime and endTime are not sent, the most recent data is returned.
        Only the data of the latest 30 days is available.

        '''

        endpoint = "/futures/data/topLongShortAccountRatio"
        params = {
            "symbol":symbol,
            "period": period,
            "limit": limit,
            "startTime": self.time_ts(startTime),
            "endTime": self.time_ts(endTime)
        }
        result = self.send_public_request("GET",endpoint,params)
        return result


    def top_trader_long_short_ratio_positions(self,symbol,period,limit=None,startTime=None,endTime=None):
        '''
        GET /futures/data/topLongShortPositionRatio

        https://binance-docs.github.io/apidocs/futures/en/#top-trader-long-short-ratio-positions

        If startTime and endTime are not sent, the most recent data is returned.
        Only the data of the latest 30 days is available.

        '''

        endpoint = "/futures/data/topLongShortPositionRatio"
        params = {
            "symbol":symbol,
            "period": period,
            "limit": limit,
            "startTime": self.time_ts(startTime),
            "endTime": self.time_ts(endTime)
        }
        result = self.send_public_request("GET",endpoint,params)
        return result



    def long_short_ratio(self,symbol,period,limit=None,startTime=None,endTime=None):
        '''
        GET /futures/data/globalLongShortAccountRatio
        https://binance-docs.github.io/apidocs/futures/en/#long-short-ratio

        If startTime and endTime are not sent, the most recent data is returned.
        Only the data of the latest 30 days is available.       

        '''
        endpoint = "/futures/data/globalLongShortAccountRatio"
        params = {
            "symbol":symbol,
            "period": period,
            "limit": limit,
            "startTime": self.time_ts(startTime),
            "endTime": self.time_ts(endTime)
        }
        result = self.send_public_request("GET",endpoint,params)
        return result



    def taker_buy_sell_volume(self,symbol,period,limit=None,startTime=None,endTime=None):
        '''
        GET /futures/data/takerlongshortRatio
        https://binance-docs.github.io/apidocs/futures/en/#taker-buy-sell-volume
        If startTime and endTime are not sent, the most recent data is returned.
        Only the data of the latest 30 days is available.
        '''

        endpoint = "/futures/data/takerlongshortRatio"
        params = {
            "symbol":symbol,
            "period": period,
            "limit": limit,
            "startTime": self.time_ts(startTime),
            "endTime": self.time_ts(endTime)
        }
        result = self.send_public_request("GET",endpoint,params)
        return result

    

    def historical_BLVT_NAV_Kline(self,symbol,interval,startTime=None,endTime=None,limit=None):
        '''
        GET /fapi/v1/lvtKlines
        The BLVT NAV system is based on Binance Futures, so the endpoint is based on fapi

        https://binance-docs.github.io/apidocs/futures/en/#historical-blvt-nav-kline-candlestick
        '''
        endpoint = "/fapi/v1/lvtKlines"
        params = {
            "symbol":symbol,
            "interval": interval,
            "startTime": self.time_ts(startTime),
            "endTime": self.time_ts(endTime),
            "limit": limit
        }
        result = self.send_public_request("GET",endpoint,params)
        return result


    def composite_index_symbol_information(self,symbol=None):
        '''
        GET /fapi/v1/indexInfo

        https://binance-docs.github.io/apidocs/futures/en/#composite-index-symbol-information

        Only for composite index symbols
        '''
        endpoint = "/fapi/v1/indexInfo"

        params = {
            "symbol": symbol

        }
        result = self.send_public_request("GET",endpoint,params)
        return result
    
    def multi_assets_mode_asset_index(self,symbol=None):
        '''
        GET /fapi/v1/assetIndex
        asset index for Multi-Assets mode

        https://binance-docs.github.io/apidocs/futures/en/#multi-assets-mode-asset-index

        '''

        endpoint = "/fapi/v1/assetIndex"

        params = {
            "symbol": symbol
        }
        result = self.send_public_request("GET",endpoint,params)
        return result


    def um_change_position_mode(self,dualSidePosition,recvWindow=None):
        '''
        POST /fapi/v1/positionSide/dual (HMAC SHA256)

        Change user's position mode (Hedge Mode or One-way Mode ) on EVERY symbol

        https://binance-docs.github.io/apidocs/futures/en/#change-position-mode-trade
        '''

        endpoint = "/fapi/v1/positionSide/dual"
        params = {
            "dualSidePosition": dualSidePosition,
            "recvWindow": recvWindow
        }

        result = self.send_signed_request_variableParams("POST",endpoint,params)
        return result


    def um_get_current_position_mode(self,recvWindow=None):
        '''
        GET /fapi/v1/positionSide/dual (HMAC SHA256)
        Get user's position mode (Hedge Mode or One-way Mode ) on EVERY symbol
        https://binance-docs.github.io/apidocs/futures/en/#get-current-position-mode-user_data
        '''
        endpoint = "/fapi/v1/positionSide/dual"
        params = {
            
            "recvWindow": recvWindow
        }

        result = self.send_signed_request_variableParams("GET",endpoint,params)
        return result

    def um_change_multi_assets_mode(self,multiAssetsMargin,recvWindow=None):
        '''
        POST /fapi/v1/multiAssetsMargin (HMAC SHA256)

        Change user's Multi-Assets mode (Multi-Assets Mode or Single-Asset Mode) on Every symbol

        https://binance-docs.github.io/apidocs/futures/en/#change-multi-assets-mode-trade
        '''
        endpoint = "/fapi/v1/multiAssetsMargin"

        params = {
            "multiAssetsMargin": multiAssetsMargin,
            "recvWindow": recvWindow
        }

        result = self.send_signed_request_variableParams("POST",endpoint,params)
        return result


    def um_get_current_multi_assets_mode(self,recvWindow=None):
        '''
        GET /fapi/v1/multiAssetsMargin (HMAC SHA256)

        Get user's Multi-Assets mode (Multi-Assets Mode or Single-Asset Mode) on Every symbol

        https://binance-docs.github.io/apidocs/futures/en/#get-current-multi-assets-mode-user_data
        '''

        endpoint = "/fapi/v1/multiAssetsMargin"
        params = {
            "recvWindow": recvWindow,
        }

        result = self.send_signed_request_variableParams("GET",endpoint,params)
        return result

    def um_new_order(self,symbol,side,type,quantity,price=None,positionSide=None,
                     timeInForce=None,reduceOnly=None,newClientOrderId=None,stopPrice=None,
                     closePosition=None,activitionPrice=None,callbackRate=None,workingType=None,
                     priceProtect=None,newOrderRespType=None,recvWindow=None):

        '''
        POST /fapi/v1/order (HMAC SHA256)

        Send in a new order.

        https://binance-docs.github.io/apidocs/futures/en/#new-order-trade
        '''
        endpoint = "/fapi/v1/order"

        params = {
            "symbol":symbol,
            "side":side,
            "type":type,
            "quantity":quantity,
            "price":price,
            "positionSide":positionSide,
            "timeInForce":timeInForce,
            "reduceOnly":reduceOnly,
            "newClientOrderId":newClientOrderId,
            "stopPrice": stopPrice,
            "closePosition":closePosition,
            "activitionPrice":activitionPrice,
            "callbackRate": callbackRate,
            "workingType": workingType,
            "priceProtect":priceProtect,
            "newOrderRespType":newOrderRespType,
            "recvWindow":recvWindow
        }

        result = self.send_signed_request_variableParams("POST",endpoint,params)
        return result



    def um_modify_order(self,orderId,symbol,side,quantity,price,origClientOrderId=None,recvWindow=None):
        '''
        PUT /fapi/v1/order (HMAC SHA256)

        Order modify function, currently only LIMIT order modification is supported, modified orders will be reordered in the match queue

        https://binance-docs.github.io/apidocs/futures/en/#modify-order-trade
        '''
        endpoint = "/fapi/v1/order"

        params = {
            "orderId":orderId,
            "symbol": symbol,
            "side":side,
            "quantity": quantity,
            "price": price,
            "origClientOrderId": origClientOrderId,
            "recvWindow": recvWindow
        }
        result = self.send_signed_request_variableParams("PUT",endpoint,params)
        return result



    def um_place_multiple_orders(self,batchOrders,recvWindow=None):
        '''
        POST /fapi/v1/batchOrders (HMAC SHA256)

        https://binance-docs.github.io/apidocs/futures/en/#modify-order-trade

        Where batchOrders is the list of order parameters in JSON

        Example: /fapi/v1/batchOrders?batchOrders=[{"type":"LIMIT","timeInForce":"GTC",
        "symbol":"BTCUSDT","side":"BUY","price":"10001","quantity":"0.001"}]
        '''
        endpoint = "/fapi/v1/batchOrders"

        params = {
            "batchOrders": batchOrders,
            "recvWindow": recvWindow
        }

        result = self.send_signed_request_variableParams("POST",endpoint,params)
        return result



    def um_modify_multiple_orders(self,batchOrders,recvWindow=None):
        '''
        PUT /fapi/v1/batchOrders (HMAC SHA256)

        https://binance-docs.github.io/apidocs/futures/en/#modify-multiple-orders-trade

        Where batchOrders is the list of order parameters in JSON

        '''

        endpoint = "/fapi/v1/batchOrders"

        params = {
            "batchOrders": batchOrders,
            "recvWindow": recvWindow
        }

        result = self.send_signed_request_variableParams("PUT",endpoint,params)
        return result


    def um_get_order_modify_history(self,symbol,orderId=None,origClientOrderId=None, startTime=None,endTime=None,limit=None,recvWindow=None):
        '''
        GET /fapi/v1/orderAmendment (HMAC SHA256)

        Get order modification history

        https://binance-docs.github.io/apidocs/futures/en/#modify-multiple-orders-trade


        Either orderId or origClientOrderId must be sent, and the orderId will prevail if both are sent.
        '''
        endpoint = "/fapi/v1/orderAmendment"

        params = {
            "symbol": symbol,
            "orderId": orderId,
            "origClientOrderId": origClientOrderId,
            "startTime": self.time_ts(startTime),
            "endTime": self.time_ts(endTime),
            "limit": limit,
            "recvWindow":recvWindow
        }


        result = self.send_signed_request_variableParams("GET",endpoint,params)
        return result


    def um_query_order(self,symbol,orderId=None,origClientOrderId=None,recvWindow=None):
        '''
        GET /fapi/v1/order (HMAC SHA256)

        Check an order's status.

        https://binance-docs.github.io/apidocs/futures/en/#query-order-user_data
        '''

        endpoint = "/fapi/v1/order"
        params = {
            "symbol": symbol,
            "orderId": orderId,
            "origClientOrderId": origClientOrderId,
            "recvWindow": recvWindow
        }
        result = self.send_signed_request_variableParams("GET",endpoint,params)
        return result

    def um_cancel_order(self,symbol,orderId=None,origClientOrderId=None,recvWindow=None):
        '''
        DELETE /fapi/v1/order (HMAC SHA256)

        Cancel an active order.

        https://binance-docs.github.io/apidocs/futures/en/#cancel-order-trade
        '''
        endpoint = "/fapi/v1/order"
        params = {
            "symbol": symbol,
            "orderId": orderId,
            "origClientOrderId": origClientOrderId,
            "recvWindow": recvWindow
        }
        result = self.send_signed_request_variableParams("DELETE",endpoint,params)
        return result

    
    def um_cancel_all_open_orders(self, symbol,recvWindow=None):
        '''
        DELETE /fapi/v1/allOpenOrders (HMAC SHA256)

        https://binance-docs.github.io/apidocs/futures/en/#cancel-all-open-orders-trade
        '''
        endpoint = "/fapi/v1/allOpenOrders"
        params = {
            "symbol": symbol,
            "recvWindow": recvWindow

        }

        result = self.send_signed_request_variableParams("DELETE",endpoint,params)
        return result


    def um_cancel_multiple_orders(self, symbol, orderIdList=None,origClientOrderIdList=None,recvWindow=None):
        '''
        DELETE /fapi/v1/batchOrders (HMAC SHA256)

        https://binance-docs.github.io/apidocs/futures/en/#cancel-multiple-orders-trade

        Either orderIdList or origClientOrderIdList must be sent.
        '''

        endpoint = "/fapi/v1/batchOrders"
        params = {
            "symbol": symbol,
            "orderIdList": orderIdList,
            "origClientOrderIdList": origClientOrderIdList,
            "recvWindow": recvWindow

        }

        result = self.send_signed_request_variableParams("DELETE",endpoint,params)
        return result

    def um_auto_cancel_all_open_orders(self,symbol,countdownTime,recvWindow=None):
        '''
        POST /fapi/v1/countdownCancelAll (HMAC SHA256)

        Cancel all open orders of the specified symbol at the end of the specified countdown.

        https://binance-docs.github.io/apidocs/futures/en/#auto-cancel-all-open-orders-trade
        '''

        endpoint = "/fapi/v1/countdownCancelAll"
        params = {
            "symbol": symbol,
            "countdownTime": countdownTime,
            "recvWindow": recvWindow
        }
        result = self.send_signed_request_variableParams("POST",endpoint,params)
        return result



    def um_query_current_open_order(self,symbol,orderId=None,origClientOrderId=None,recvWindow=None):
        '''
        GET /fapi/v1/openOrder (HMAC SHA256)

        https://binance-docs.github.io/apidocs/futures/en/#query-current-open-order-user_data

        EitherorderId or origClientOrderId must be sent
        If the queried order has been filled or cancelled, the error message "Order does not exist" will be returned.
        '''

        endpoint = "/fapi/v1/openOrder"

        params = {
            "symbol": symbol,
            "orderId": orderId,
            "origClientOrderId": origClientOrderId,
            "recvWindow":recvWindow
        }
        result = self.send_signed_request_variableParams("GET",endpoint,params)
        return result

    def um_current_all_open_orders(self,symbol=None,recvWindow=None):
        '''
        GET /fapi/v1/openOrders (HMAC SHA256)

        Get all open orders on a symbol. Careful when accessing this with no symbol.

        https://binance-docs.github.io/apidocs/futures/en/#current-all-open-orders-user_data
        '''
        endpoint = "/fapi/v1/openOrders"
        params = {
            "symbol": symbol,
            "recvWindow": recvWindow
        }
        result = self.send_signed_request_variableParams("GET",endpoint,params)
        return result



    def um_all_orders(self,symbol,orderId=None,startTime=None,endTime=None,limit=None,recvWindow=None):
        '''
        GET /fapi/v1/allOrders (HMAC SHA256)

        Get all account orders; active, canceled, or filled.

        These orders will not be found:
            order status is CANCELED or EXPIRED, AND
            order has NO filled trade, AND
            created time + 3 days < current time

        https://binance-docs.github.io/apidocs/futures/en/#all-orders-user_data
        '''

        endpoint = "/fapi/v1/allOrders"
        params = {
            "symbol": symbol,
            "orderId": orderId,
            "startTime": self.time_ts(startTime),
            "endTime": self.time_ts(endTime),
            "limit": limit,
            "recvWindow": recvWindow
        }

        result = self.send_signed_request_variableParams("GET",endpoint,params)
        return result


    def um_futures_account_balance(self,recvWindow=None):
        '''
        GET /fapi/v2/balance (HMAC SHA256)

        https://binance-docs.github.io/apidocs/futures/en/#futures-account-balance-v2-user_data
        '''

        endpoint = "/fapi/v2/balance"
        params = {
            "recvWindow": recvWindow
        }

        result = self.send_signed_request_variableParams("GET",endpoint,params)
        return result
    
    def um_account_information(self,recvWindow=None):
        '''
        GET /fapi/v2/account (HMAC SHA256)

        Get current account information. User in single-asset/ multi-assets mode will see different value, see comments in response section for detail.   Weight: 5

        https://binance-docs.github.io/apidocs/futures/en/#account-information-v2-user_data
        '''
        endpoint = "/fapi/v2/account"
        params = {
            "recvWindow": recvWindow
        }
        result = self.send_signed_request_variableParams("GET",endpoint,params)
        return result

    def um_change_initial_leverage(self,symbol,leverage,recvWindow=None):
        '''
        POST /fapi/v1/leverage (HMAC SHA256)

        Change user's initial leverage of specific symbol market.

        https://binance-docs.github.io/apidocs/futures/en/#change-initial-leverage-trade
        '''

        endpoint = "/fapi/v1/leverage"
        params = {
            "symbol": symbol,
            "leverage": leverage,
            "recvWindow": recvWindow
        }
        result = self.send_signed_request_variableParams("POST",endpoint,params)
        return result

    def um_change_margin_type(self,symbol,marginType,recvWindow=None):
        '''
        POST /fapi/v1/marginType (HMAC SHA256)

        https://binance-docs.github.io/apidocs/futures/en/#change-margin-type-trade
        '''

        endpoint = "/fapi/v1/marginType"
        params = {
            "symbol": symbol,
            "marginType": marginType,
            "recvWindow": recvWindow
        }
        result = self.send_signed_request_variableParams("POST",endpoint,params)
        return result


    def um_modify_isolated_position_margin(self,symbol,amount,type,positionSide=None,recvWindow=None):
        '''
        POST /fapi/v1/positionMargin (HMAC SHA256)

        https://binance-docs.github.io/apidocs/futures/en/#modify-isolated-position-margin-trade
        
        Only for isolated symbol
        '''
        endpoint = "/fapi/v1/positionMargin"
        params = {
            "symbol": symbol,
            "amount": amount,
            "type": type,
            "positionSide": positionSide,
            "recvWindow": recvWindow
        }
        result = self.send_signed_request_variableParams("POST",endpoint,params)
        return result


    def um_get_positin_margin_chagne_history(self,symbol,type=None,startTime=None,endTime=None,limit=None,recvWindow=None):
        '''
        GET /fapi/v1/positionMargin/history (HMAC SHA256)

        https://binance-docs.github.io/apidocs/futures/en/#get-position-margin-change-history-trade
        '''
        
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


    def um_position_information(self,symbol=None,recvWindow=None):
        '''
        GET /fapi/v2/positionRisk (HMAC SHA256)

        Get current position information.

        https://binance-docs.github.io/apidocs/futures/en/#position-information-v2-user_data
        
        '''

        endpoint = "/fapi/v2/positionRisk"
        params = {
            "symbol": symbol,
            "recvWindow": recvWindow
        }
        result = self.send_signed_request_variableParams("GET",endpoint,params)
        return result

    def um_account_trade_list(self,symbol=None,orderId=None,startTime=None,endTime=None,fromId=None,limit=None,recvWindow=None):
        '''
        GET /fapi/v1/userTrades (HMAC SHA256)

        Get trades for a specific account and symbol.

        https://binance-docs.github.io/apidocs/futures/en/#account-trade-list-user_data
        '''

        endpoint = "/fapi/v1/userTrades"
        params = {
            "symbol": symbol,
            "orderId": orderId,
            "startTime": self.time_ts(startTime),
            "endTime":self.time_ts(endTime),
            "fromId":fromId,
            "limit":limit,
            "recvWindow": recvWindow
        }
        result = self.send_signed_request_variableParams("GET",endpoint,params)
        return result



    def um_get_income_history(self,symbol=None,incomeType=None,startTime=None,endTime=None,limit=None,recvWindow=None):
        '''
        GET /fapi/v1/income (HMAC SHA256)

        https://binance-docs.github.io/apidocs/futures/en/#get-income-history-user_data
        '''

        endpoint = "/fapi/v1/income"
        params = {
            "symbol": symbol,
            "incomeType": incomeType,
            "startTime": self.time_ts(startTime),
            "endTime":self.time_ts(endTime),
            "limit":limit,
            "recvWindow": recvWindow
        }
        result = self.send_signed_request_variableParams("GET",endpoint,params)
        return result

    def um_notional_and_leverage_brackets(self,symbol=None,recvWindow=None):
        '''
        GET /fapi/v1/leverageBracket

        https://binance-docs.github.io/apidocs/futures/en/#notional-and-leverage-brackets-user_data
        '''

        endpoint = "/fapi/v1/leverageBracket"
        params = {
            "symbol": symbol,
            "recvWindow": recvWindow
        }
        result = self.send_signed_request_variableParams("GET",endpoint,params)
        return result


    def um_position_ADL_quantile_estimation(self,symbol=None,recvWindow=None):
        '''
        GET /fapi/v1/adlQuantile

        https://binance-docs.github.io/apidocs/futures/en/#position-adl-quantile-estimation-user_data

        Values update every 30s.

        Values 0, 1, 2, 3, 4 shows the queue position and possibility of ADL from low to high.

        For positions of the symbol are in One-way Mode or isolated margined in Hedge Mode, "LONG", "SHORT", and "BOTH" will be returned to show the positions' adl quantiles of different position sides.

        If the positions of the symbol are crossed margined in Hedge Mode:

            "HEDGE" as a sign will be returned instead of "BOTH";
            A same value caculated on unrealized pnls on long and short sides' positions will be shown for "LONG" and "SHORT" when there are positions in both of long and short sides.
        '''

        endpoint = "/fapi/v1/adlQuantile"
        params = {
            "symbol": symbol,
            "recvWindow": recvWindow
        }
        result = self.send_signed_request_variableParams("GET",endpoint,params)
        return result


    def um_user_force_orders(self,symbol=None,autoCloseType=None,startTime=None,endTime=None,limit=None,recvWindow=None):
        '''
        GET /fapi/v1/forceOrders

        https://binance-docs.github.io/apidocs/futures/en/#user-39-s-force-orders-user_data

        If "autoCloseType" is not sent, orders with both of the types will be returned
        If "startTime" is not sent, data within 7 days before "endTime" can be queried
        '''
        endpoint = "/fapi/v1/forceOrders"
        params = {
            "symbol": symbol,
            "autoCloseType": autoCloseType,
            "startTime": self.time_ts(startTime),
            "endTime": self.time_ts(endTime),
            "limit":limit,
            "recvWindow": recvWindow
        }
        result = self.send_signed_request_variableParams("GET",endpoint,params)
        return result


    def um_futures_trading_quantitative_rules_indicators(self,symbol=None,recvWindow=None):
        '''
        GET /fapi/v1/apiTradingStatus

        For more information on this, please refer to the Futures Trading Quantitative Rules
        https://binance-docs.github.io/apidocs/futures/en/#futures-trading-quantitative-rules-indicators-user_data
        '''
        endpoint = "/fapi/v1/apiTradingStatus"
        params = {
            "symbol": symbol,
            "recvWindow": recvWindow
        }
        result = self.send_signed_request_variableParams("GET",endpoint,params)
        return result

    def um_user_commission_rate(self,symbol=None,recvWindow=None):
        '''
        GET /fapi/v1/commissionRate (HMAC SHA256)

        https://binance-docs.github.io/apidocs/futures/en/#user-commission-rate-user_data
        '''
        endpoint = "/fapi/v1/apiTradingStatus"
        params = {
            "symbol": symbol,
            "recvWindow": recvWindow
        }
        result = self.send_signed_request_variableParams("GET",endpoint,params)
        return result

    def um_get_download_Id_for_futures_transaction_history(self,startTime,endTime,recvWindow=None):
        '''
        GET /fapi/v1/income/asyn (HMAC SHA256)

        https://binance-docs.github.io/apidocs/futures/en/#get-download-id-for-futures-transaction-history-user_data

        Request Limitation is 5 times per month, shared by front end download page and rest api

        '''
        endpoint = "/fapi/v1/income/asyn"
        params = {
            "startTime": self.time_ts(startTime),
            "endTime": self.time_ts(endTime),
            "recvWindow": recvWindow
        }
        result = self.send_signed_request_variableParams("GET",endpoint,params)
        return result

    def um_get_futures_transaction_history_download_link_by_Id(self,downloadId,recvWindow=None):
        '''
        GET /fapi/v1/income/asyn/id (HMAC SHA256)

        https://binance-docs.github.io/apidocs/futures/en/#get-futures-transaction-history-download-link-by-id-user_data

        Download link expiration: 24h
        '''

        endpoint = "/fapi/v1/income/asyn/id"
        params = {
            "downloadId": downloadId,
            "recvWindow": recvWindow
        }
        result = self.send_signed_request_variableParams("GET",endpoint,params)
        return result

    def um_classic_portfolio_margin_account_information(self,asset,recvWindow=None):
        '''
        GET /fapi/v1/pmAccountInfo

        Get Classic Portfolio Margin current account information.

        https://binance-docs.github.io/apidocs/futures/en/#classic-portfolio-margin-account-information-user_data
        
        maxWithdrawAmount is for asset transfer out to the spot wallet.
        '''
        endpoint = "/fapi/v1/pmAccountInfo"

        params = {
            "asset": asset,
            "recvWindow": recvWindow

        }
        result = self.send_signed_request_variableParams("GET",endpoint,params)
        return result


    '''
    Websocket Market
    '''
    def websocket_market(self,streams):
        url = self.websocket_url+streams
        ws = self.websocket_connect(url)
        return ws 
