import requests 
import time
import uuid 
import hmac
import hashlib 
import json

api_key = ""
api_secret = ""


# BinancePay_Nonce must be 32 digits, A random string with 32 bytes, e.g. random ascii decimal within a-z and A-Z and loop 32 times to form a random string
def random_string():
    random = str(uuid.uuid4()).replace("-","")
    return random[:32]

def hashing(to_hashing:str):
    return (
        hmac.new(api_secret.encode("utf-8"), to_hashing.encode("utf-8"), hashlib.sha512)
        .hexdigest()
        .upper()
    )


def send_signed_request(method,url_path, payload={}):
        """
        url_path: endpoint path, eg: /binancepay/openapi/balance
        payload: parameter in dict, eg: {"wallet":'FUNDING_WALLET',"currency":"BUSD"}
        """
        session = requests.Session()
        http_method = {
            "GET": session.get,
            "DELETE": session.delete,
            "PUT": session.put,
            "POST": session.post,
        }
        method = http_method.get(method)
        base_url = "https://bpay.binanceapi.com:443"
        
        timestamp = int(time.time())*1000
        nonce = random_string()
        payload_to_sign = (
            str(timestamp) + "\n" + nonce + "\n" + json.dumps(payload) + "\n"
        )
        signature = hashing(payload_to_sign)
        session.headers={   "Content-Type": "application/json;charset=utf-8",
                "BinancePay-Timestamp": str(timestamp),
                "BinancePay-Nonce": nonce,
                "BinancePay-Certificate-SN": api_key,
                "BinancePay-Signature": signature,
            }
        
        url = base_url + url_path
        params = {"url": url, "data": json.dumps(payload)}
        response = method(**params)
        print(response)
        try:
            data = response.json()
        except ValueError:
            data = response.text

        return data

path = "/binancepay/openapi/balance"
params = {
    "wallet":'FUNDING_WALLET',
    "currency":"BUSD"
}

print(send_signed_request("POST",url_path=path,payload=params))
