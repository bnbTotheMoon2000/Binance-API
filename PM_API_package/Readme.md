This is a simple package to test portfolio margin endpoints in Python. 

Example to use the package. 

from PM_api import Client
api_key = ""
api_secret = ""

client = Client(api_key,api_secret,base_url)

# to Query Margin Max Withdraw, GET /papi/v1/margin/maxWithdraw
client.query_margin_max_withdraw(asset='USDT')

Response: 
GET https://papi.binance.com/papi/v1/margin/maxWithdraw?asset=USDT&timestamp=1683566345072&signature=f88f3cabdd858985b23f3e1ff39e2f89c9a530f4218d74fbd9c5c11b5f97d4eb
{'amount': '8.8'}
