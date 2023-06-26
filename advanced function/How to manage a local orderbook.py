import websockets
import json
import asyncio
import nest_asyncio
import pandas as pd
import datetime
import time
import requests
import numpy as np
nest_asyncio.apply()

orderbook_ws = "wss://fstream.binance.com/ws/ethbtc@depth"
orderbook_rest = "https://fapi.binance.com/fapi/v1/depth?symbol=ETHBTC&limit=1000"

U = None
u = None
lastUpdateId = None

async def get_orderBook_WS():
    global U
    global u 
    async with websockets.connect(orderbook_ws) as websocket:
        print("WebSocket connection established")
        while True:
            futures_data = await websocket.recv()
            data = json.loads(futures_data)
            U = data.get('U')
            u = data.get('u')
            print("Start to log websocket")
            with open('OrderBook_Log.txt','a',encoding='utf-8') as f:
                f.write(json.dumps(data))
                f.write('\n')
            
                
async def get_orderBook_REST():
    global lastUpdateId 
    while True:
        response = requests.get(orderbook_rest)
        if response.status_code == 200:
            data = response.json()
            lastUpdateId = data.get('lastUpdateId')
            if isinstance(lastUpdateId,int) & isinstance(U,int) & isinstance(u,int):
                if U <= lastUpdateId and u>= lastUpdateId:
                    print("start to log!!!")
                    with open('OrderBook_Log.txt','a',encoding='utf-8') as f:
                        f.write('==='*70)
                        f.write('\n')
                        f.write(json.dumps(data))
                        f.write('\n')
                        f.write('==='*70)
                        f.write('\n')
                    break
        else:
            print("Failed to fetch order book data")
        await asyncio.sleep(1)  # wait 1 sec before sending next request. 


async def main():
    task1 = asyncio.create_task(get_orderBook_WS())
    task2 = asyncio.create_task(get_orderBook_REST())
    await asyncio.gather(task1, task2)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
