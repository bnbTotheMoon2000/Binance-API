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



    '''
    BEGINNING OF MARKET DATA ENDPOINT FUNCTIONS
    '''




    def test_connectivity(self):
        '''
        If response is {} then connectivity is established
        If not, check connectivity
        '''
        endpoint = "/fapi/v1/ping"
        test_connectivity = self.send_public_request("GET", endpoint)
        return test_connectivity

    def check_server_time(self):
        '''
        If response is {"serverTime": 1687173078706} then connection is working
        If not, check error response
        '''
        endpoint = "/fapi/v1/time"
        check_server_time = self.send_public_request("GET", endpoint)
        return check_server_time

    def futures_exchange_information(self):
        '''
        Gets exchange info for futures. Includes but not limited to:
        -  exchangeFilters
        -  rateLimits
        -  assets
        -  symbols:
            * filters
            * orderType
            * timeInForce
        '''
        endpoint = "/fapi/v1/exchangeInfo"
        futures_exchange_information = self.send_public_request("GET", endpoint)
        return futures_exchange_information

    def order_book(self, symbol, limit=None):
        '''
        Define Symbol to get bid and asks for that symbol.
        Weight is adjusted by limit
        Default limit is 500; Valid limits:[5, 10, 20, 50, 100, 500, 1000]
        '''
        endpoint = "/fapi/v1/depth"
        params = {
            'symbol': symbol,
            'limit': limit
        }
        order_book = self.send_public_request("GET", endpoint, params)
        return order_book

    def recent_trades_list(self,symbol,limit=None):
        '''
        Get recent market trades

        Market trades means trades filled in the order book.
        Only market trades will be returned, which means the insurance fund trades
        and ADL trades won't be returned.
        Default limit is 500; max 1000.
        '''
        endpoint = "/fapi/v1/trades"
        params = {
            'symbol': symbol,
            'limit': limit
        }
        recent_trades_list = self.send_public_request("GET", endpoint, params)
        return recent_trades_list

    def old_trades_lookup(self,symbol,limit=None,fromId=None):
        '''
        Get older market historical trades.

        Market trades means trades filled in the order book.
        Only market trades will be returned, which means the insurance fund trades
        and ADL trades won't be returned.
        Default limit is 500; max 1000.
        fromId: TradeId to fetch from. Default gets most recent trades.
        '''
        endpoint = "/fapi/v1/historicalTrades"
        params = {
            'symbol': symbol,
            'limit': limit,
            'fromId': fromId
        }
        old_trades_lookup = self.send_public_request("GET", endpoint, params)
        return old_trades_lookup

    def compressed_aggregate_trades_list(self,symbol,fromId=None,startTime=None,endTime=None,limit=None):
        '''
        Get compressed, aggregate market trades.
        Market trades that fill in 100ms with the same price and
        the same taking side will have the quantity aggregated.

        Parameters and rules:
        https://binance-docs.github.io/apidocs/futures/en/#compressed-aggregate-trades-list
        '''
        endpoint = "/fapi/v1/aggTrades"
        params = {
            "symbol":symbol,
            'fromId':fromId,
            "startTime":self.time_ts(startTime),
            'endTime':self.time_ts(endTime),
            'limit':limit
        }
        compressed_aggregate_trades_list = self.send_public_request('GET',endpoint,params)
        return compressed_aggregate_trades_list

    '''
    Kline/Candlestick chart intervals:
    https://binance-docs.github.io/apidocs/futures/en/#public-endpoints-info

    m -> minutes; h -> hours; d -> days; w -> weeks; M -> months:

        * 1m
        * 3m
        * 5m
        * 15m
        * 30m
        * 1h
        * 2h
        * 4h
        * 6h
        * 8h
        * 12h
        * 1d
        * 3d
        * 1w
        * 1M
    '''

    def kline_candlestick_data(self,symbol,interval,startTime=None,endTime=None,limit=None):
        '''
        Kline/candlestick bars for a symbol. (OHLC)
        Klines are uniquely identified by their open time.

        Weight: based on parameter LIMIT. Min: 1, Max: 10; (https://binance-docs.github.io/apidocs/futures/en/#kline-candlestick-data)
        If startTime and endTime are not sent, the most recent klines are returned.
        '''
        endpoint = "/fapi/v1/klines"
        params = {
            "symbol":symbol,
            'interval':interval,
            "startTime":self.time_ts(startTime),
            'endTime':self.time_ts(endTime),
            'limit':limit
        }
        kline_candlestick_data = self.send_public_request('GET',endpoint,params)
        return kline_candlestick_data

    def continuous_contract_kline_candlestick_data(self,pair,contractType,interval,startTime=None,endTime=None,limit=None):
        '''
        Kline/candlestick bars for a specific contract type. (OHLC)
        Klines are uniquely identified by their open time.

        Weight: based on parameter LIMIT. Min: 1, Max: 10; (https://binance-docs.github.io/apidocs/futures/en/#continuous-contract-kline-candlestick-data)
        If startTime and endTime are not sent, the most recent klines are returned.
        Contract type:
        * Perpetual
        * CURRENT_QUARTER
        * NEXT_QUARTER
        '''
        endpoint = "/fapi/v1/continuousKlines"
        params = {
            "pair":pair,
            "contractType":contractType,
            'interval':interval,
            "startTime":self.time_ts(startTime),
            'endTime':self.time_ts(endTime),
            'limit':limit
        }
        continuous_contract_kline_candlestick_data = self.send_public_request('GET',endpoint,params)
        return continuous_contract_kline_candlestick_data

    def index_price_kline_candlestick_data(self,pair,interval,startTime=None,endTime=None,limit=None):
        '''
        Kline/candlestick bars for the index price of a pair. (OHLC)
        Klines are uniquely identified by their open time.

        Weight: based on parameter LIMIT. Min: 1, Max: 10; (https://binance-docs.github.io/apidocs/futures/en/#index-price-kline-candlestick-data)
        If startTime and endTime are not sent, the most recent klines are returned.
        '''
        endpoint = "/fapi/v1/indexPriceKlines"
        params = {
            "pair":pair,
            'interval':interval,
            "startTime":self.time_ts(startTime),
            'endTime':self.time_ts(endTime),
            'limit':limit
        }
        index_price_kline_candlestick_data = self.send_public_request('GET',endpoint,params)
        return index_price_kline_candlestick_data

    def mark_price_kline_candlestick_data(self,symbol,interval,startTime=None,endTime=None,limit=None):
        '''
        Kline/candlestick bars for the mark price of a symbol. (OHLC)
        Klines are uniquely identified by their open time.

        Weight: based on parameter LIMIT. Min: 1, Max: 10; (https://binance-docs.github.io/apidocs/futures/en/#mark-price-kline-candlestick-data)
        If startTime and endTime are not sent, the most recent klines are returned.
        '''
        endpoint = "/fapi/v1/markPriceKlines"
        params = {
            "symbol":symbol,
            'interval':interval,
            "startTime":self.time_ts(startTime),
            'endTime':self.time_ts(endTime),
            'limit':limit
        }
        mark_price_kline_candlestick_data = self.send_public_request('GET',endpoint,params)
        return mark_price_kline_candlestick_data

    def mark_price(self, symbol):
        '''
        Mark Price and Funding Rate
        '''
        endpoint = "/fapi/v1/premiumIndex"
        params = {
            'symbol': symbol,
        }
        mark_price = self.send_public_request("GET", endpoint, params)
        return mark_price

    def get_funding_rate_history(self,symbol=None,startTime=None,endTime=None,limit=None):
        '''
        If startTime and endTime are not sent, the most recent limit datas are returned.
        If the number of data between startTime and endTime is larger than limit, return as startTime + limit.
        In ascending order.
        Limit Default 100; max 1000.
        '''
        endpoint = "/fapi/v1/fundingRate"
        params = {
            "symbol":symbol,
            "startTime":self.time_ts(startTime),
            'endTime':self.time_ts(endTime),
            'limit':limit
        }
        get_funding_rate_history = self.send_public_request('GET',endpoint,params)
        return get_funding_rate_history

    def twenty_four_hour_ticker_price_change_statistics(self,symbol=None):
        '''
        24 hour rolling window price change statistics.
        Careful when accessing this with no symbol.

        Weight:
        1 for a single symbol;
        40 when the symbol parameter is omitted

        If the symbol is not sent, tickers for all symbols will be returned in an array.
        '''
        endpoint = "/fapi/v1/ticker/24hr"
        params = {
            "symbol":symbol
        }
        twenty_four_hour_ticker_price_change_statistics = self.send_public_request('GET',endpoint,params)
        return twenty_four_hour_ticker_price_change_statistics

    def symbol_price_ticker(self,symbol=None):
        '''
        Latest price for a symbol or symbols.

        Weight:
        1 for a single symbol;
        2 when the symbol parameter is omitted

        If the symbol is not sent, tickers for all symbols will be returned in an array.
        '''
        endpoint = "/fapi/v1/ticker/price"
        params = {
            "symbol":symbol
        }
        symbol_price_ticker = self.send_public_request('GET',endpoint,params)
        return symbol_price_ticker

    def symbol_order_book_ticker(self,symbol=None):
        '''
        Best price/qty on the order book for a symbol or symbols.

        Weight:
        2 for a single symbol;
        5 when the symbol parameter is omitted

        If the symbol is not sent, bookTickers for all symbols will be returned in an array.
        The field X-MBX-USED-WEIGHT-1M in response header is not accurate from this endpoint, please ignore.
        '''
        endpoint = "/fapi/v1/ticker/bookTicker"
        params = {
            "symbol":symbol
        }
        symbol_order_book_ticker = self.send_public_request('GET',endpoint,params)
        return symbol_order_book_ticker

    def open_interest(self,symbol):
        '''
        Get present open interest of a specific symbol.
        '''
        endpoint = "/fapi/v1/openInterest"
        params = {
            "symbol":symbol
        }
        open_interest = self.send_public_request('GET',endpoint,params)
        return open_interest

    def open_interest_statistics(self,symbol,period,limit=None,startTime=None,endTime=None):
        '''
        If startTime and endTime are not sent, the most recent data is returned.
        period: "5m","15m","30m","1h","2h","4h","6h","12h","1d"
        limit: default 30, max 500
        Only the data of the latest 30 days is available.
        '''
        endpoint = "/futures/data/openInterestHist"
        params = {
            "symbol":symbol,
            "period":period,
            'limit':limit,
            "startTime":self.time_ts(startTime),
            'endTime':self.time_ts(endTime),
        }
        open_interest_statistics = self.send_public_request('GET',endpoint,params)
        return open_interest_statistics

    def top_trader_long_short_ratio_account(self,symbol,period,limit=None,startTime=None,endTime=None):
        '''
        If startTime and endTime are not sent, the most recent data is returned.
        period: "5m","15m","30m","1h","2h","4h","6h","12h","1d"
        limit: default 30, max 500
        Only the data of the latest 30 days is available.
        '''
        endpoint = "/futures/data/topLongShortAccountRatio"
        params = {
            "symbol":symbol,
            "period":period,
            'limit':limit,
            "startTime":self.time_ts(startTime),
            'endTime':self.time_ts(endTime),
        }
        top_trader_long_short_ratio_account = self.send_public_request('GET',endpoint,params)
        return top_trader_long_short_ratio_account

    def top_trader_long_short_ratio_position(self,symbol,period,limit=None,startTime=None,endTime=None):
        '''
        If startTime and endTime are not sent, the most recent data is returned.
        period: "5m","15m","30m","1h","2h","4h","6h","12h","1d"
        limit: default 30, max 500
        Only the data of the latest 30 days is available.
        '''
        endpoint = "/futures/data/topLongShortPositionRatio"
        params = {
            "symbol":symbol,
            "period":period,
            'limit':limit,
            "startTime":self.time_ts(startTime),
            'endTime':self.time_ts(endTime),
        }
        top_trader_long_short_ratio_position = self.send_public_request('GET',endpoint,params)
        return top_trader_long_short_ratio_position

    def long_short_ratio(self,symbol,period,limit=None,startTime=None,endTime=None):
        '''
        (GLOBAL L/S RATIO)
        If startTime and endTime are not sent, the most recent data is returned.
        period: "5m","15m","30m","1h","2h","4h","6h","12h","1d"
        limit: default 30, max 500
        Only the data of the latest 30 days is available.
        '''
        endpoint = "/futures/data/globalLongShortAccountRatio"
        params = {
            "symbol":symbol,
            "period":period,
            'limit':limit,
            "startTime":self.time_ts(startTime),
            'endTime':self.time_ts(endTime),
        }
        long_short_ratio = self.send_public_request('GET',endpoint,params)
        return long_short_ratio

    def taker_buy_sell_volume(self,symbol,period,limit=None,startTime=None,endTime=None):
        '''
        If startTime and endTime are not sent, the most recent data is returned.
        period: "5m","15m","30m","1h","2h","4h","6h","12h","1d"
        limit: default 30, max 500
        Only the data of the latest 30 days is available.
        '''
        endpoint = "/futures/data/takerlongshortRatio"
        params = {
            "symbol":symbol,
            "period":period,
            'limit':limit,
            "startTime":self.time_ts(startTime),
            'endTime':self.time_ts(endTime),
        }
        taker_buy_sell_volume = self.send_public_request('GET',endpoint,params)
        return taker_buy_sell_volume

    def historical_BLVT_NAV_kline_candlestick(self,symbol,interval,limit=None,startTime=None,endTime=None):
        '''
        The BLVT NAV system is based on Binance Futures, so the endpoint is based on fapi
        symbol: token name, e.g. "BTCDOWN", "BTCUP"
        limit: default 500, max 1000
        '''
        endpoint = "/fapi/v1/lvtKlines"
        params = {
            "symbol":symbol,
            "interval":interval,
            'limit':limit,
            "startTime":self.time_ts(startTime),
            'endTime':self.time_ts(endTime),
        }
        historical_BLVT_NAV_kline_candlestick = self.send_public_request('GET',endpoint,params)
        return historical_BLVT_NAV_kline_candlestick

    def composite_index_symbol_information(self,symbol=None):
        '''
        Only for composite index symbols
        '''
        endpoint = "/fapi/v1/indexInfo"
        params = {
            "symbol":symbol
        }
        composite_index_symbol_information = self.send_public_request('GET',endpoint,params)
        return composite_index_symbol_information

    def multi_assets_mode_asset_index(self,symbol=None):
        '''
        Asset index for Multi-Assets mode
        Weight: 1 for a single symbol; 10 when the symbol parameter is omitted
        '''
        endpoint = "/fapi/v1/assetIndex"
        params = {
            "symbol":symbol
        }
        multi_assets_mode_asset_index = self.send_public_request('GET',endpoint,params)
        return multi_assets_mode_asset_index




    '''
    END OF MARKET DATA ENDPOINT FUNCTIONS
    '''



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



