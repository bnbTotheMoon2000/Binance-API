from binance.um_futures import UMFutures
import websocket
import json 

api_key = ""
secret = ""
# input limit price 
limit_price = ""
# input symbol 
symbol = ""
# input leverage 
leverage = ""

leverage = int(leverage)
limit_price = float(limit_price)
um_stream =f'wss://fstream.binance.com/ws/{symbol.lower()}@markPrice'
ws = websocket.create_connection(um_stream)

mark_price = ws.recv()
mark_price = json.loads(mark_price)
mark_price = float(mark_price['p'])

client = UMFutures(key=api_key,secret=secret,base_url ="https://testnet.binancefuture.com" )
available = round(float(client.account()['availableBalance']),2)

print("current ETHUSDT mark price: ",mark_price)
print("avaiable margin: ",available)

print("the given limit price: ",)
leverage = int("20")
print("leverage on ETHUSDT: ",leverage)

if mark_price > limit_price:
    sell_max_open = round((available*leverage) / (mark_price+abs(mark_price-limit_price)*leverage),3)
    buy_max_open = round((available*leverage) / limit_price,3)
    
    print("max_sell:",sell_max_open)
    print("max_buy:",buy_max_open)

elif mark_price < limit_price:
    
    sell_max_open = round((available*leverage) / limit_price,3)
    buy_max_open = round((available*leverage) / (limit_price+abs(mark_price-limit_price)*leverage),3)
    print("max_sell:",sell_max_open)
    print("max_buy:",buy_max_open)
