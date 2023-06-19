from UM_Futures import UM_futures
import json

um = UM_futures(
    api_key="",
    api_secret="",
    testnet=True,
    show_headers=False)



# IF YOU ARE USING VSCODE, UNCOMMENT THE CODE YOU WANT TO TEST WITH CTRL + /
# (MAC/LINUX USE: CMD + /)




'''
BEGINNING OF FUTURES MARKET DATA ENDPOINTS
'''




# POSITION MARGIN CHANGE HISTORY
# data = um.get_positin_margin_chagne_history(symbol="BTCUSDT")
# print(json.dumps(data, indent=4))

# TEST CONNECTIVITY
# con = um.test_connectivity()
# print(json.dumps(con, indent=4))

# CHECK SERVER TIME
# sTime = um.check_server_time()
# print(json.dumps(sTime, indent=4))

# EXCHANGE INFORMATION
# exchangeInfo = um.futures_exchange_information()
# print(json.dumps(exchangeInfo, indent=4))

# ORDER BOOK
# #book = um.order_book(symbol='BTCUSDT')
# book = um.order_book(symbol='BTCUSDT', limit=10)
# print(json.dumps(book, indent=4))

# RECENT TRADES LIST
# rTrades = um.recent_trades_list(symbol='BTCUSDT', limit=10)
# print(json.dumps(rTrades, indent=4))

#  OLD TRADES LOOKUP (MARKET_DATA)
# oTrades = um.old_trades_lookup(symbol='BTCUSDT', limit=10)
# print(json.dumps(oTrades, indent=4))

# COMPRESSED/AGGREGATE TRADES LIST
# aggTrades = um.compressed_aggregate_trades_list(symbol='BTCUSDT', limit=10)
# print(json.dumps(aggTrades, indent=4))

# KLINE/CANDLESTICK DATA
# kLine = um.kline_candlestick_data(symbol='BTCUSDT', interval='1m', limit=10)
# print(json.dumps(kLine, indent=4))

# CONTINUOUS CONTRACT KLINE/CANDLESTICK DATA
# contKLine = um.continuous_contract_kline_candlestick_data(pair='BTCUSDT',contractType='PERPETUAL' ,interval='1h', limit=10)
# print(json.dumps(contKLine, indent=4))

# INDEX PRICE KLINE/CANDLESTICK DATA
# indexKLINE = um.index_price_kline_candlestick_data(pair='BTCUSDT' ,interval='1d', limit=10)
# print(json.dumps(indexKLINE, indent=4))

# MARK PRICE KLINE/CANDLESTICK DATA
# markKLine = um.mark_price_kline_candlestick_data(symbol='BTCUSDT' ,interval='1w', limit=10)
# print(json.dumps(markKLine, indent=4))

# MARK PRICE
# mPrice = um.mark_price(symbol='BTCUSDT')
# print(json.dumps(mPrice, indent=4))

# GET FUNDING RATE HISTORY
# fundRate = um.get_funding_rate_history()
# print(json.dumps(fundRate, indent=4))

# 24HR TICKER PRICE CHANGE STATISTICS
# twoFourTicker = um.twenty_four_hour_ticker_price_change_statistics()
# print(json.dumps(twoFourTicker, indent=4))

# SYMBOL PRICE TICKER
# symTicker = um.symbol_price_ticker()
# print(json.dumps(symTicker, indent=4))

# SYMBOL ORDER BOOK TICKER
# symOrderBook = um.symbol_order_book_ticker()
# print(json.dumps(symOrderBook, indent=4))

# OPEN INTEREST
# opInter = um.open_interest(symbol='BTCUSDT')
# print(json.dumps(opInter, indent=4))

# OPEN INTEREST STATISTICS
## NOT AVAILABLE FOR TESTNET
# opIntStats = um.open_interest_statistics(symbol='BTCUSDT', period='5m')
# print(json.dumps(opIntStats, indent=4))

# TOP TRADER LONG/SHORT RATIO (ACCOUNTS)
## NOT AVAILABLE FOR TESTNET
# topTradeAcc = um.top_trader_long_short_ratio_account(symbol='BTCUSDT', period='1h')
# print(json.dumps(topTradeAcc, indent=4))

# TOP TRADER LONG/SHORT RATIO (POSITIONS)
## NOT AVAILABLE FOR TESTNET
# topTradePos = um.top_trader_long_short_ratio_position(symbol='BTCUSDT', period='1d')
# print(json.dumps(topTradePos, indent=4))

# LONG/SHORT RATIO (GLOBAL)
## NOT AVAILABLE FOR TESTNET
# globLongShort = um.long_short_ratio(symbol='BTCUSDT', period='1d')
# print(json.dumps(globLongShort, indent=4))

# TAKER BUY/SELL VOLUME
## NOT AVAILABLE FOR TESTNET
# takerVolume = um.taker_buy_sell_volume(symbol='BTCUSDT', period='1d')
# print(json.dumps(takerVolume, indent=4))

# HISTORICAL BLVT NAV KLINE/CANDLESTICK
## NOT AVAILABLE FOR TESTNET
# histBLVT = um.historical_BLVT_NAV_kline_candlestick(symbol='BTCDOWN', interval='1d')
# print(json.dumps(histBLVT, indent=4))

# COMPOSITE INDEX SYMBOL INFORMATION
# compIndex = um.composite_index_symbol_information()
# print(json.dumps(compIndex, indent=4))

# MULTI-ASSETS MODE ASSET INDEX
# multiAssetIndex = um.multi_assets_mode_asset_index()
# print(json.dumps(multiAssetIndex, indent=4))




'''
END OF FUTURES MARKET DATA ENDPOINTS
'''