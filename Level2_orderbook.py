# Install the following required packages
import requests
import time
import hashlib
import hmac
from urllib.parse import urlencode


api_key = ""
secret_key = ""

class Orderbook:
    def __init__(self):
        self.S_URL_V1 = "https://api.binance.com/sapi/v1"
        self.api_key = api_key
        self.secret_key = secret_key

    def convert_time(self,ts):
        from datetime import datetime 
        time_format = datetime.utcfromtimestamp(ts/1000)
        return time_format

    def convert_ts(self,tm):
        import pytz
        from datetime import datetime
        t = datetime.strptime(tm,"%Y-%m-%d %H:%M:%S")
        tz = pytz.timezone('UTC')
        t_utc = tz.localize(t).astimezone(pytz.utc)
        ts = int(datetime.timestamp(t_utc))*1000
        return ts

    # Function to generate the signature
    def _sign(self,params={}):
        data = params.copy()
        ts = str(int(1000 * time.time()))
        data.update({"timestamp": ts})
        h = urlencode(data)
        h = h.replace("%40", "@")
        b = bytearray()
        b.extend(self.secret_key.encode())
        signature = hmac.new(b, msg=h.encode("utf-8"), digestmod=hashlib.sha256).hexdigest()
        sig = {"signature": signature}
        return data, sig


    # Function to generate the download ID
    def post(self,path, params={}):
        sign = self._sign(params)
        query = urlencode(sign[0]) + "&" + urlencode(sign[1])
        url = "%s?%s" % (path, query)
        header = {"X-MBX-APIKEY": self.api_key}
        resultPostFunction = requests.post(url, headers=header, timeout=30, verify=True)
        return resultPostFunction


    # Function to generate the download link
    def get(self,path, params):
        sign = self._sign(params)
        query = urlencode(sign[0]) + "&" + urlencode(sign[1])
        url = "%s?%s" % (path, query)
        header = {"X-MBX-APIKEY": self.api_key}
        resultGetFunction = requests.get(url, headers=header, timeout=30, verify=True)
        return resultGetFunction

    def send_request(self,symbol,startTime,endTime,dataType):
        timestamp = str(int(1000 * time.time()))
        paramsToObtainDownloadID = {
            "symbol": symbol,
            "startTime": self.convert_ts(startTime),
            "endTime": self.convert_ts(endTime),
            "dataType": dataType,
            "timestamp": timestamp,
        }

        # Calls the "post" function to obtain the download ID for the specified symbol, dataType and time range combination
        path = "%s/futuresHistDataId" % self.S_URL_V1
        resultDownloadID = self.post(path, paramsToObtainDownloadID)
        print(resultDownloadID)
        try: 
            downloadID = resultDownloadID.json()["id"]
        except KeyError as Exception:
            print(Exception)
        print(downloadID)  # prints the download ID, example: {'id': 324225}


        # Calls the "get" function to obtain the download link for the specified symbol, dataType and time range combination
        paramsToObtainDownloadLink = {"downloadId": downloadID, "timestamp": timestamp}
        pathToObtainDownloadLink = "%s/downloadLink" % self.S_URL_V1
        resultToBeDownloaded = self.get(pathToObtainDownloadLink, paramsToObtainDownloadLink)
        print(resultToBeDownloaded)
        print(resultToBeDownloaded.json()) 


orderbook = Orderbook()
orderbook.send_request(symbol='BNBUSDT',startTime='2023-07-10 00:00:00',endTime="2023-07-10 01:00:00",dataType='T_DEPTH')
