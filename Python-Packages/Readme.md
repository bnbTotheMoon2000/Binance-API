### The files under Python-Packages integrate Binance API into Python functions. You could send API requests by calling the relevant functions. Here below provides 
examples on how to use this package. 

1. Download all the py files and save in the same folder.
2. main.py provides functions to generate signature, timestamp, processing readable time, and sending requests.
3. Examples to use.

// parameter testnet is to define the created object envronment is production or testnet. Which is a mandatory parameter. 
// testnet=True, the base url is https://testnet.binance.vision, and websocket url is wss://testnet.binance.vision/ws

// request_url = True, the response will return the full request URL. 
// show_headers = True, the response will include response header. 

1) Create an object 
from Spot import Spot_trading
api_key = ""
api_secret = ""
spot = Spot_trading(api_key=api_key,api_secret=api_secret,testnet=True,request_url = True, show_headers=True)
print(spot.account_information(recvWindow=5000))

![image](https://github.com/bnbTotheMoon2000/Binance-API/assets/121224650/99442d3d-e3b8-4774-938b-99a5dd276309)

2) startTime and endTime 
endpoints can be input startTime and endTime. You need to insert readable time by the format of %Y-%m-%d %H:%M:%S 

![image](https://github.com/bnbTotheMoon2000/Binance-API/assets/121224650/97c5a9fa-61ae-493d-8c5e-c763bee097ae)

3) websocket

You could call websocket_market function to subscribe streams. 

![image](https://github.com/bnbTotheMoon2000/Binance-API/assets/121224650/105909a1-87b6-4ce2-9a77-62070fe962da)

Book multiple streams 
streams='bnbusdt@kline_1m/btcusdt@kline_1m'

![image](https://github.com/bnbTotheMoon2000/Binance-API/assets/121224650/04fa7ebc-19fc-48ba-8f9e-c0be061d5c6b)

4) Websocket API

![image](https://github.com/bnbTotheMoon2000/Binance-API/assets/121224650/5b727dc9-87ab-4493-a0d9-5e1a64d814ae)






