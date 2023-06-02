### This package can be used to send requests to access Binance websocket API endpoints. 

#### Usage: 

1. Initialization

from Websocket_API import Websocket_api

ws = Websocket_api(api_key,api_secret,testnet=True) # testnet=True , access to testnet url , "wss://testnet.binance.vision/ws-api/v3"

2. Calling functions to access relevant endpoints 

print(result = ws.account_order_history(symbol='BNBUSDT'))


