import websocket
import json

symbol = "BTCUSDT"
socket = f'wss://stream.binance.com:9443/ws/{symbol.lower()}@depth'

def on_message(ws,message):
    json_msg = json.loads(message)
    print(json_msg)
    
def on_close(ws):
    print('connection end')

def on_error(ws,message):
    print(message)

def on_open(ws):
    print("start websocket")

ws = websocket.WebSocketApp(socket,on_message=on_message,on_close=on_close,on_error=on_error,on_open=on_open)
ws.run_forever()
