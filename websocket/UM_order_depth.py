import pandas as pd 
import websocket 
import json

symbol = "BTCUSDT"
ws_order_book =f'wss://fstream.binance.com/stream?streams={symbol.lower()}@depth'

temp_list = []
def on_message(ws,message):
    json_msg = json.loads(message)
    temp_list.append(json_msg['data'])
       
def on_close(ws):
    print('connection end')
    
ws = websocket.WebSocketApp(ws_order_book,on_message=on_message,on_close=on_close)
ws.run_forever()

data = pd.DataFrame(temp_list)
data = data.explode(['b'],ignore_index=True)
data = data.explode(['a'],ignore_index=True)
data['bid_price']=data.b.apply(lambda x:x[0]).astype('float')
data['bid_qty'] = data.b.apply(lambda x:x[1]).astype('float')
data['ask_price']=data.a.apply(lambda x:x[0]).astype('float')
data['ask_qty']=data.a.apply(lambda x:x[1]).astype('float')
data.drop(columns=['b','a'],inplace=True)
data['E'] = pd.to_datetime(data['E'],unit='ms')
data['T'] = pd.to_datetime(data['T'],unit='ms')
print(data)
