from base64 import b64encode
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
import time 
import requests

# give api key
api_key = ""

# .pem path
private_key = "test_key.pem"

# open the file saved priviate key, and make a signature
def rsa_hashing(private_key, payload, passphrase=None):
    # load the key
    with open (private_key, "r") as private_key_file:
        private_key = RSA.importKey(private_key_file.read(), passphrase=passphrase)
    h = SHA256.new(payload.encode("utf-8"))
    signature = pkcs1_15.new(private_key).sign(h)
    return b64encode(signature).decode("utf-8") 

 # get timestamp
def time_stamp():
    return str(int(time.time())*1000)

# request header
headers = headers = {
  'Content-Type': 'application/json',
  'X-MBX-APIKEY': api_key
}

# query account information 
url = f"https://testnet.binance.vision/api/v3/account?timestamp={timestamp}&signature={sign}"
print(requests.get(url,headers=headers).json())
