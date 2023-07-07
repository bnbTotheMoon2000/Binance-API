from main import Client 
import requests
import uuid
import json
import time
import websocket
import urllib.parse
import pandas as pd 
from urllib.parse import urlencode,quote,unquote
import hmac
import hashlib



class Spot_trading(Client):
    def __init__(self,api_key,api_secret,testnet=bool,show_headers=False,request_url=False):
        super().__init__(self,api_key,api_secret,show_headers=False,request_url=False)
        self.api_key = api_key
        self.api_secret = api_secret
        self.show_headers = show_headers
        self.request_url = request_url

        if testnet:
            self.base_url = "https://testnet.binance.vision"
            self.websocket_url = "wss://testnet.binance.vision/ws"
        else:

            self.base_url = 'https://api.binance.com'
            self.websocket_url = "wss://stream.binance.com:9443/stream?streams="

    

    '''
    Query IP
    '''
    def query_ip(self):
        '''
        query IP address , url : https://checkip.amazonaws.com/
        '''
        ip_query = 'https://checkip.amazonaws.com/'
        result = requests.get(ip_query).text
        return result 
    
    '''
    Wallet Endpoints
    '''
    def system_status(self):
        '''
        Fetch system status 
        0: normal;
        1: system maintenance
        '''
        endpoint = "/sapi/v1/system/status"
        system_status = self.send_public_request("GET",endpoint)
        return system_status
    
    def all_coins_information(self,recvWindow=None):
        '''
        Get information of coins (available for deposit and withdraw) for user. 
        https://binance-docs.github.io/apidocs/spot/en/#all-coins-39-information-user_data
        '''
        endpoint = "/sapi/v1/capital/config/getall"
        params = {
            'recvWindow':recvWindow
        }
        all_coins_information = self.send_signed_request_variableParams("GET",endpoint,params)
        return all_coins_information
    
    def daily_account_snapshot(self,type,startTime=None,endTime=None,limit=None,recvWindow=None):
        endpoint = "/sapi/v1/accountSnapshot"
        params = {
            'type':type,
            "startTime":startTime,
            "endTime":endTime,
            'limit':limit,
            "recvWindow":recvWindow
        }
        daily_account_snapshot = self.send_signed_request_variableParams("GET",endpoint,params)
        return daily_account_snapshot
    
    def disable_fast_withdrawal_switch(self,recvWindow=None):
        '''
        This request will disable fastwithdraw switch under your account.

        https://binance-docs.github.io/apidocs/spot/en/#disable-fast-withdraw-switch-user_data
        '''
        endpoint = "/sapi/v1/account/disableFastWithdrawSwitch"
        params = {
            'recvWindow':recvWindow
        }
        disable_fast_withdrawal_switch = self.send_signed_request_variableParams("POST",endpoint,params)
        return disable_fast_withdrawal_switch
    
    def enable_fast_withdraw_switch(self,recvWindow=None):
        '''
        This request will enable fastwithdraw switch under your account.
        https://binance-docs.github.io/apidocs/spot/en/#enable-fast-withdraw-switch-user_data
        '''
        endpoint = "/sapi/v1/account/enableFastWithdrawSwitch"
        params = {
            'recvWindow':recvWindow
        }
        enable_fast_withdraw_switch = self.send_signed_request_variableParams("POST",endpoint,params)
        return enable_fast_withdraw_switch
    
    def withdraw(self,coin,address,amount,withdrawOrderId=None,network=None,addressTag=None,transactionFeeFlag=None,
                 name=None,walletType=None,recvWindow=None):
        '''
        Submit a withdraw request.
        https://binance-docs.github.io/apidocs/spot/en/#withdraw-user_data
        '''
        endpoint = "/sapi/v1/capital/withdraw/apply"
        params = {
            "coin":coin,
            'address':address,
            'amount':amount,
            "withdrawOrderId": withdrawOrderId,
            'network':network,
            "addressTag":addressTag,
            "transactionFeeFlag":transactionFeeFlag,
            "name":name,
            'walletType':walletType,
            'recvWindow':recvWindow
        }
        withdraw = self.send_signed_request_variableParams('POST',endpoint,params)
        return withdraw
    
    def deposit_history(self,coin=None,status=None,startTime=None,endTime=None,offset=None,limit=None,recvWindow=None,txid=None):
        '''
        Fetch deposit history.
        https://binance-docs.github.io/apidocs/spot/en/#withdraw-user_data

        '''
        endpoint = '/sapi/v1/capital/deposit/hisrec'
        params = {
            'coin':coin,
            'status':status,
            'startTime':self.time_ts(startTime),
            'endTime':self.time_ts(endTime),
            'offset':offset,
            'limit':limit,
            'recvWindow':recvWindow,
            'txid':txid
        }

        deposit_history = self.send_signed_request_variableParams('GET',endpoint,params)
        return deposit_history
    
    def withdraw_history(self,coin=None,status=None,withdrawOrderId=None,
                         startTime=None,endTime=None,offset=None,limit=None,recvWindow=None):
        '''
        Fetch withdraw history.

        https://binance-docs.github.io/apidocs/spot/en/#withdraw-history-supporting-network-user_data
        '''
        endpoint = "/sapi/v1/capital/withdraw/history"
        params = {
            'coin':coin,
            'status':status,
            'startTime':self.time_ts(startTime),
            'endTime':self.time_ts(endTime),
            'offset':offset,
            'limit':limit,
            'recvWindow':recvWindow,
            'withdrawOrderId':withdrawOrderId
        }
        withdraw_history = self.send_signed_request_variableParams('GET',endpoint,params)
        return withdraw_history
    
    def deposit_address(self,coin,network=None,recvWindow=None):
        '''
        Fetch deposit address with network.
        https://binance-docs.github.io/apidocs/spot/en/#deposit-address-supporting-network-user_data

        '''
        endpoint = '/sapi/v1/capital/deposit/address'
        params = {
            'coin':coin,
            'network':network
        }
        deposit_address = self.send_signed_request_variableParams("GET",endpoint,params)
        return deposit_address
        
    def account_API_trading_status(self,recvWindow=None):
        '''
        Fetch account api trading status detail.

        https://binance-docs.github.io/apidocs/spot/en/#dustlog-user_data
        '''
        endpoint = "/sapi/v1/account/apiTradingStatus"
        params = {
            'recvWindow':recvWindow
        }
        account_API_trading_status = self.send_signed_request_variableParams("GET",endpoint,params)
        return account_API_trading_status
    
    def DustLog(self,startTime=None,endTime=None,recvWindow=None):
        '''
        Fetch BNB convert
        https://binance-docs.github.io/apidocs/spot/en/#dustlog-user_data
        '''
        endpoint = "/sapi/v1/asset/dribblet"
        params = {
            'startTime':self.time_ts(startTime),
            'endTime':self.time_ts(endTime),
            'recvWindow':recvWindow

        }
        DustLog = self.send_signed_request_variableParams("GET",endpoint,params)
        return DustLog
    
    def get_assets_that_can_be_converted_into_BNB(self,recvWindow=None):
        '''
        Fetch assets that can be converted into BNB
        https://binance-docs.github.io/apidocs/spot/en/#get-assets-that-can-be-converted-into-bnb-user_data
        '''
        endpoint = "/sapi/v1/asset/dust-btc"
        params = {
            "recvWindow":recvWindow
        }
        get_assets_that_can_be_converted_into_BNB = self.send_signed_request_variableParams("POST",endpoint,params)
        return get_assets_that_can_be_converted_into_BNB
    
    def Dust_Transfer(self,asset,recvwindow=None):
        '''
        Convert dust into BNB.
        https://binance-docs.github.io/apidocs/spot/en/#get-assets-that-can-be-converted-into-bnb-user_data
        '''
        endpoint = "/sapi/v1/asset/dust"
        params ={
            'asset':asset,
            'recvWindow':recvwindow
        }
        Dust_Transfer = self.send_signed_request_variableParams("POST",endpoint,params)
        return Dust_Transfer
    
    def asset_difvidend_record(self,asset=None,startTime=None,endTime=None,limit=None,recvWindow=None):
        '''
        Query asset dividend record.
        https://binance-docs.github.io/apidocs/spot/en/#asset-dividend-record-user_data
        '''
        endpoint = "/sapi/v1/asset/assetDividend"
        params = {
            'asset':asset,
            'startTime':self.time_ts(startTime),
            'endTime':self.time_ts(endTime),
            'limit':limit,
            'recvWindow':recvWindow
        }
        asset_difvidend_record = self.send_signed_request_variableParams("GET",endpoint,params)
        return asset_difvidend_record
    
    def asset_detail(self,asset=None,recvWindow=None):
        '''
        Fetch details of assets supported on Binance.
        https://binance-docs.github.io/apidocs/spot/en/#asset-detail-user_data

        '''
        endpoint = "/sapi/v1/asset/assetDetail"
        params = {
            'asset':asset,
            'recvWindow':recvWindow
        }
        asset_detail = self.send_signed_request_variableParams("GET",endpoint,params)
        return asset_detail
    
    def trade_fee(self,symbol=None,recvWindow=None):
        '''
        Fetch trade fee 
        https://binance-docs.github.io/apidocs/spot/en/#trade-fee-user_data
        '''
        endpoint = '/sapi/v1/asset/tradeFee'
        params = {
            'asset':symbol,
            'recvWindow':recvWindow

        }
        trade_fee = self.send_signed_request_variableParams("GET",endpoint,params)
        return trade_fee
    
    def user_universal_transfer(self,type,asset,amount,fromSymbol=None,toSymbol=None,recvWindow=None):
        '''
        Post a universal transfer (need to enable Permits Universal Transfer)
        Please check type from API documentation
        https://binance-docs.github.io/apidocs/spot/en/#user-universal-transfer-user_data
        '''
        endpoint = "/sapi/v1/asset/transfer"
        params = {
            'type':type,
            'asset':asset,
            'amount':amount,
            'fromSymbol':fromSymbol,
            'toSymbol':toSymbol,
            'recvWindow':recvWindow
        }
        user_universal_transfer = self.send_signed_request_variableParams("POST",endpoint,params)
        return user_universal_transfer
    
    def query_user_universal_transfer_history(self,type,startTime=None,endTime=None,current=None,size=None,
                                              fromSymbol=None,toSymbol=None,recvWindow=None):
        '''
        Fetch universal transfer
        https://binance-docs.github.io/apidocs/spot/en/#query-user-universal-transfer-history-user_data
        '''
        endpoint = "/sapi/v1/asset/transfer"
        params = {
            'type':type,
            'startTime':self.time_ts(startTime),
            'endTime':self.time_ts(endTime),
            'current':current,
            'size':size,
            'fromSymbol':fromSymbol,
            'toSymbol':toSymbol,
            'recvWindow':recvWindow

        }
        query_user_universal_transfer_history = self.send_signed_request_variableParams("GET",endpoint,params)
        return query_user_universal_transfer_history
    
    def funding_wallet(self,asset=None,needBtcValuation=None,recvWindow=None):
        '''
        Checking funding wallet balance.
        https://binance-docs.github.io/apidocs/spot/en/#funding-wallet-user_data

        Currently supports querying the following business assets：Binance Pay, Binance Card, Binance Gift Card, Stock Token
        '''
        endpoint = "/sapi/v1/asset/get-funding-asset"
        params = {
            'asset':asset,
            'needBtcValuation':needBtcValuation,
            "recvWindow":recvWindow
        }
        funding_wallet = self.send_signed_request_variableParams('POST',endpoint,params)
        return funding_wallet 
    
    def user_asset(self,asset=None,needBtcValuation=None,recvWindow=None):
        '''
        Get user assets, just for positive data.
        https://binance-docs.github.io/apidocs/spot/en/#funding-wallet-user_data
        '''

        endpoint = '/sapi/v3/asset/getUserAsset'
        params = {
            "asset":asset,
            "needBtcValuation":needBtcValuation,
            "recvWindow":recvWindow
        }
        user_asset = self.send_signed_request_variableParams("POST",endpoint,params)
        return user_asset
    
    def BUSD_convert(self,clientTranId,asset,amount,targetAsset,accountType=None):
        '''
        Convert transfer, convert between BUSD and stablecoins.
        https://binance-docs.github.io/apidocs/spot/en/#busd-convert-trade
        If the clientTranId has been used before, will not do the convert transfer, the original transfer will be returned.
        '''
        endpoint = "/sapi/v1/asset/convert-transfer"
        params = {
            'clientTranId':clientTranId,
            "asset":asset,
            'amount':amount,
            'targetAsset':targetAsset,
            'accountType':accountType
        }
        BUSD_convert = self.send_signed_request_variableParams("POST",endpoint,params)
        return BUSD_convert
    
    def BUSD_convert_history(self,startTime,endTime,tranId=None,clientTranId=None,asset=None,accountType=None,current=None,size=None):
        """
        Fetch BUSD conversation history
        https://binance-docs.github.io/apidocs/spot/en/#busd-convert-history-user_data
        """
        endpoint = "/sapi/v1/asset/convert-transfer/queryByPage"
        params = {
            'tranId':tranId,
            "clientTranId":clientTranId,
            "asset":asset,
            "startTime":self.time_ts(startTime),
            "endTime":self.time_ts(endTime),
            'accountType':accountType,
            'current':current,
            'size':size
        }
        BUSD_convert_history = self.send_signed_request_variableParams("GET",endpoint,params)
        return BUSD_convert_history
    
    def get_API_key_permission(self,recvWindow=None):
        '''
        Query API key permisison 
        https://binance-docs.github.io/apidocs/spot/en/#get-api-key-permission-user_data
        '''
        endpoint = "/sapi/v1/account/apiRestrictions"
        params = {
            'recvWindow':recvWindow
        }
        get_API_key_permission = self.send_signed_request_variableParams("GET",endpoint,params)
        return get_API_key_permission

    def switch_on_off_BUSD_stable_coins_conversion(self,coin,enable=bool):
        '''
        User can use it to turn on or turn off the BUSD auto-conversion from/to a specific stable coin.

        https://binance-docs.github.io/apidocs/spot/en/#query-auto-converting-stable-coins-user_data
        '''
        endpoint = "/sapi/v1/capital/contract/convertible-coins"
        params = {
            'coin':coin,
            'enable':enable
        }
        switch_on_off_BUSD_stable_coins_conversion = self.send_signed_request_variableParams('POST',endpoint,params)
        return switch_on_off_BUSD_stable_coins_conversion
    
    def one_click_arrival_deposit_apply(self,depositId=None,txId=None,subAccountId=None,subUserId=None):
        '''
        Apply deposit credit for expired address (One click arrival)
        https://binance-docs.github.io/apidocs/spot/en/#one-click-arrival-deposit-apply-for-expired-address-deposit-user_data
        '''
        endpoint = "/sapi/v1/capital/deposit/credit-apply"
        params = {
            'depositId':depositId,
            "txId":txId,
            'subAccountId':subAccountId,
            'subUserId':subUserId
        }
        one_click_arrival_deposit_apply = self.send_signed_request_variableParams("POST",endpoint,params)
        return one_click_arrival_deposit_apply
    
    """
    Sub-Account Endpoints
    """

    def enable_options_for_sub_account(self,email,recvWindow=None):
        """
        Enable Options for Sub-account (For Master Account)

        https://binance-docs.github.io/apidocs/spot/en/#enable-options-for-sub-account-for-master-account-user_data
        """
        endpoint = "/sapi/v1/sub-account/eoptions/enable"
        params = {
            "email":email,
            "recvWindow":recvWindow
        }
        enable_options_for_sub_account = self.send_signed_request_variableParams('POST',endpoint,params)
        return enable_options_for_sub_account

    def create_a_Virtual_sub_account(self,subAccountString,recvWindow=None):
        """
        (For Master Account)
        Create a virtual sub account. 
        Needs to input subAccountsString
        """
        endpoint = "/sapi/v1/sub-account/virtualSubAccount"
        params = {
            'subAccountString':subAccountString,
            "recvWindow":recvWindow
        }
        create_a_Virtual_sub_account = self.send_signed_request_variableParams('POST',endpoint,params)
        return create_a_Virtual_sub_account
    
    def query_sub_account_list(self,email=None,isFreeze=None,page=None,limit=None,recvWindow=None):
        """
        Query sub-account list 
        https://binance-docs.github.io/apidocs/spot/en/#query-sub-account-list-for-master-account
        """
        endpoint = "/sapi/v1/sub-account/list"
        params = {
            "email":email,
            "isFreeze":isFreeze,
            "page":page,
            "limit":limit,
            'recvWindow':recvWindow
        }
        query_sub_account_list = self.send_signed_request_variableParams('GET',endpoint,params)
        return query_sub_account_list
    
    def query_sub_account_spot_asset_transfer_history(self,fromEmail=None,toEmail=None,
                                                      startTime=None,endTime=None,page=None,
                                                      limit=None,recvWindow=None):
        '''
        Query sub account spot asset transfer history

        futuresType: {1:USD-Margin Futures, 2:Coin-Margin Futures}

        https://binance-docs.github.io/apidocs/spot/en/#query-sub-account-spot-asset-transfer-history-for-master-account
        '''
        endpoint = '/sapi/v1/sub-account/sub/transfer/history'
        params = {
            "fromEmail":fromEmail,
            'toEmail':toEmail,
            "startTime": self.time_ts(startTime),
            "endTime": self.time_ts(endTime),
            'page':page,
            'limit':limit,
            'recvWindow':recvWindow
        }
        query_sub_account_spot_asset_transfer_history = self.send_signed_request_variableParams("GET",endpoint,params)
        return query_sub_account_spot_asset_transfer_history

    def query_sub_account_futures_asset_transfer_history(self,email,futuresType,
                                                      startTime=None,endTime=None,page=None,
                                                      limit=None,recvWindow=None):
        '''
        Query sub account futures asset transfer history  (For Master Account)
        https://binance-docs.github.io/apidocs/spot/en/#query-sub-account-futures-asset-transfer-history-for-master-account
        '''
        endpoint = '/sapi/v1/sub-account/futures/internalTransfer'
        params = {
            'email':email,
            'futuresType':futuresType,
            "startTime": self.time_ts(startTime),
            "endTime": self.time_ts(endTime),
            'page':page,
            'limit':limit,
            'recvWindow':recvWindow
        }
        query_sub_account_futures_asset_transfer_history = self.send_signed_request_variableParams("GET",endpoint,params)
        return query_sub_account_futures_asset_transfer_history
    
    def query_sub_account_asset(self,email,recvWindow=None):
        '''
        Fetch sub-account assets
        https://binance-docs.github.io/apidocs/spot/en/#query-sub-account-assets-for-master-account
        '''
        endpoint = "/sapi/v3/sub-account/assets"
        params = {
            "email":email,
            "recvWindow":recvWindow
        }
        query_sub_account_asset = self.send_signed_request_variableParams('GET',endpoint,params)
        return query_sub_account_asset
    
    def query_sub_account_spot_assets_summary(self,email=None,page=None,size=None,recvWindow=None):
        """
        Get BTC valued asset summary of sub-accounts. (For Master Account)
        https://binance-docs.github.io/apidocs/spot/en/#query-sub-account-spot-assets-summary-for-master-account
        """
        endpoint = '/sapi/v1/sub-account/spotSummary'
        params = {
            'email':email,
            'page':page,
            'size':size,
            'recvWindow':recvWindow
        }
        query_sub_account_spot_assets_summary = self.send_signed_request_variableParams('GET',endpoint,params)
        return query_sub_account_spot_assets_summary
    
    def get_sub_account_deposit_address(self,email,coin,network=None,recvWindow=None):
        '''
        Fetch sub-account deposit address. (For Master Account)
        https://binance-docs.github.io/apidocs/spot/en/#get-sub-account-deposit-address-for-master-account
        '''
        endpoint ='/sapi/v1/capital/deposit/subAddress'
        params = {
            'email':email,
            'coin':coin,
            'network':network,
            'recvWindow':recvWindow
        }
        get_sub_account_deposit_address = self.send_signed_request_variableParams('GET',endpoint,params)
        return get_sub_account_deposit_address
    
    def get_sub_account_deposit_history(self,email,coin=None,status=None,startTime=None,endTime=None,limit=None,
                                        offset=None,recvWindow=None,txId=None):
        '''
        Fetch sub-account deposit history (For Master Account)
        https://binance-docs.github.io/apidocs/spot/en/#get-sub-account-deposit-history-for-master-account
        '''
        endpoint = '/sapi/v1/capital/deposit/subHisrec'
        params = {
            'email':email,
            'coin':coin,
            'status':status,
            'startTime':startTime,
            'endTime':endTime,
            'limit':limit,
            'offset':offset,
            'recvWindow':recvWindow,
            'txId':txId
        }
        get_sub_account_deposit_history = self.send_signed_request_variableParams('GET',endpoint, params)
        return get_sub_account_deposit_history
    
    def get_sub_account_status_on_margin_futures(self,email=None,recvWindow=None):
        '''
        Checking sub-account's margin/futures status (For Master Account)
        if no email sent, all sub-account's information will be returned. 
        https://binance-docs.github.io/apidocs/spot/en/#get-sub-account-39-s-status-on-margin-futures-for-master-account
        '''
        endpoint = '/sapi/v1/sub-account/status'
        params = {
            'email':email,
            'recvWindow':recvWindow
        }
        get_sub_account_status_on_margin_futures = self.send_signed_request_variableParams("GET",endpoint,params)
        return get_sub_account_status_on_margin_futures
    
    def enable_margin_for_sub_account(self,email,recvWinow=None):
        '''
        Enable margin trading for sub-account (For Master Account)
        https://binance-docs.github.io/apidocs/spot/en/#enable-margin-for-sub-account-for-master-account
        '''
        endpoint ='/sapi/v1/sub-account/margin/enable'
        params = {
            'email':email,
            'recvWindow':recvWinow
        }
        enable_margin_for_sub_account = self.send_signed_request_variableParams('POST',endpoint,params)
        return enable_margin_for_sub_account
    
    def get_detail_on_sub_account_margin_account(self,email,recvWindow=None):
        '''
        Get detail on sub account margin account (For Master Account)
        https://binance-docs.github.io/apidocs/spot/en/#get-sub-account-39-s-status-on-margin-futures-for-master-account
        '''
        endpoint = '/sapi/v1/sub-account/margin/account'
        params = {
            'email':email,
            'recvWindow':recvWindow
        }
        get_detail_on_sub_account_margin_account = self.send_signed_request_variableParams('GET',endpoint,params)
        return get_detail_on_sub_account_margin_account

    def get_summary_sub_account_margin_account(self,recvWindow=None):
        '''
        Get summary of sub-account's Margin Account (For Master Account)
        https://binance-docs.github.io/apidocs/spot/en/#get-detail-on-sub-account-39-s-margin-account-for-master-account
        '''
        endpoint = '/sapi/v1/sub-account/margin/accountSummary'
        params = {
            'recvWindow':recvWindow
        }
        get_summary_sub_account_margin_account = self.send_signed_request_variableParams("GET",endpoint,params)
        return get_summary_sub_account_margin_account
    
    def enable_futures_for_sub_account(self,email,recvWindow=None):
        '''
        Enable futures function for sub-account (For Master Account)
        https://binance-docs.github.io/apidocs/spot/en/#get-detail-on-sub-account-39-s-margin-account-for-master-account
        '''
        endpoint = '/sapi/v1/sub-account/futures/enable'
        params = {
            'email':email,
            'recvWindow':recvWindow
        }
        enable_futures_for_sub_account = self.send_signed_request_variableParams("POST",endpoint,params)
        return enable_futures_for_sub_account    

    def get_detail_sub_account_futures_account(self,email,recvWindow):
        '''
        Get detail on sub-account's Futures-Account (For Master Account)
        https://binance-docs.github.io/apidocs/spot/en/#get-detail-on-sub-account-39-s-futures-account-for-master-account
        '''

        endpoint = '/sapi/v1/sub-account/futures/enable'
        params = {
            'email':email,
            'recvWindow':recvWindow
        }
        get_detail_sub_account_futures_account = self.send_signed_request_variableParams("GET",endpoint,params)
        return get_detail_sub_account_futures_account  
    
    def get_futures_position_risk_sub_account(self,email,recvWindow=None):
        '''
        Get sub-account's futures position information (For Master Account)
        https://binance-docs.github.io/apidocs/spot/en/#get-futures-position-risk-of-sub-account-for-master-account
        '''
        endpoint = '/sapi/v1/sub-account/futures/positionRisk'
        params = {
            'email':email,
            'recvWindow':recvWindow
        }
        get_futures_position_risk_sub_account = self.send_signed_request_variableParams("GET",endpoint,params)
        return get_futures_position_risk_sub_account
    
    def futures_transfer_for_sub_account(self,email,asset,amount,type,recvWindow=None):
        '''
        Post a asset transfer to sub-account (For Master Account)
        type: 
        1. transfer from subaccount's spot account to its USDT-margined futures account
        2. transfer from subaccount's USDT-margined futures account to its spot account
        3. transfer from subaccount's spot account to its COIN-margined futures account
        4. transfer from subaccount's COIN-margined futures account to its spot account
        https://binance-docs.github.io/apidocs/spot/en/#futures-transfer-for-sub-account-for-master-account
        '''
        endpoint ="/sapi/v1/sub-account/futures/transfer"
        params = {
            'email':email,
            'asset':asset,
            'amount':amount,
            'type':type,
            'recvWindow':recvWindow
        }
        futures_transfer_for_sub_account = self.send_signed_request_variableParams("POST",endpoint,params)
        return futures_transfer_for_sub_account

    def margin_transfer_for_sub_account(self,email,asset,amount,type,recvWindow=None):
        '''
        Post an asset transfer to sub-account (For Master Account)
        type:
        1: transfer from subaccount's spot account to margin account 
        2: transfer from subaccount's margin account to its spot account

        https://binance-docs.github.io/apidocs/spot/en/#margin-transfer-for-sub-account-for-master-account
        '''

        endpoint = "/sapi/v1/sub-account/margin/transfer"
        params = {
            'email':email,
            'asset':asset,
            'amount':amount,
            'type':type,
            'recvWindow':recvWindow
        }
        margin_transfer_for_sub_account = self.send_signed_request_variableParams("POSDT",endpoint,params)
        return margin_transfer_for_sub_account
    
    def transfer_to_sub_account_of_same_master(self,toEmail,asset,amount,recvWindow=None):
        '''
        Transfer assets to sub-accounts under the same master account (For Sub-account)
        https://binance-docs.github.io/apidocs/spot/en/#transfer-to-sub-account-of-same-master-for-sub-account
        '''
        endpoint = "/sapi/v1/sub-account/transfer/subToSub"
        params ={
            'toEmail':toEmail,
            'asset':asset,
            'amount':amount,
            'recvWindow':recvWindow
        }
        transfer_to_sub_account_of_same_master = self.send_signed_request_variableParams("POST",endpoint,params)
        return transfer_to_sub_account_of_same_master
    
    def transfer_to_master(self,asset,amount,recvWindow=None):
        '''
        Transfer assets to master account. (For Sub-account)
        https://binance-docs.github.io/apidocs/spot/en/#transfer-to-master-for-sub-account
        '''
        endpoint = '/sapi/v1/sub-account/transfer/subToMaster'
        params = {
            'assset':asset,
            'amount':amount,
            'recvWindow':recvWindow
        }
        transfer_to_master = self.send_signed_request_variableParams("POST",endpoint,params)
        return transfer_to_master

    def sub_account_transfer_history(self,asset=None,type=None,startTime=None,endTime=None,limit=None,recvWindow=None):
        '''
        Checking sub-account transfer history (For Sub-account)
        type:
        1. transfer in 
        2. transfer out

        https://binance-docs.github.io/apidocs/spot/en/#sub-account-transfer-history-for-sub-account
        '''
        endpoint = "/sapi/v1/sub-account/transfer/subUserHistory"
        params = {
            'asset':asset,
            'type':type,
            'startTime':self.time_ts(startTime),
            'endTime':self.time_ts(endTime),
            'limit':limit,
            'recvWindow':recvWindow
        }
        sub_account_transfer_history = self.send_signed_request_variableParams('GET',endpoint,params)
        return sub_account_transfer_history
    
    def universal_transfer(self,fromAccountType,toAccountType,asset,amount,fromEmail=None, toEmail=None,clientTranId=None,symbol=None,recvWindow=None):
        '''
        Post an universal transfer to sub-account. (For Master Account)
        fromAccountType & toAccountType:
        "SPOT","USDT_FUTURE","COIN_FUTURE","MARGIN"(Cross),"ISOLATED_MARGIN"
        symbol: only supported under ISOLATED_MARGIN type

        https://binance-docs.github.io/apidocs/spot/en/#universal-transfer-for-master-account
        '''
        endpoint ='/sapi/v1/sub-account/universalTransfer'
        params ={
            'fromEmail':fromEmail,
            'toEmail':toEmail,
            'fromAccountType':fromAccountType,
            'toAccountType':toAccountType,
            'clientTranId':clientTranId,
            'symbol':symbol,
            'asset':asset,
            'amount':amount,
            'recvWindow':recvWindow

        }
        universal_transfer = self.send_signed_request_variableParams("POST",endpoint,params)
        return universal_transfer
    
    def query_universal_transfer_history(self,fromEmail=None,toEmail=None,clientTranId=None,startTime=None,endTime=None,page=None,limit=None,recvWindow=None):
        '''
        Query universal transfer history (For Master Account)
        https://binance-docs.github.io/apidocs/spot/en/#query-universal-transfer-history-for-master-account
        '''
        endpoint = "/sapi/v1/sub-account/universalTransfer"
        params = {
            'fromEmail':fromEmail,
            'toEmail':toEmail,
            'clientTranId':clientTranId,
            'startTime':self.time_ts(startTime),
            'endTime':self.time_ts(endTime),
            'page':page,
            'limit':limit,
            'recvWindow':recvWindow
        }
        query_universal_transfer_history = self.send_signed_request_variableParams("GET",endpoint,params)
        return query_universal_transfer_history
    
    def get_detail_on_sub_account_futures_account(self,email,futuresType,recvWindow=None):
        '''
        Get sub-account futures account (For Master Account)
        https://binance-docs.github.io/apidocs/spot/en/#get-detail-on-sub-account-39-s-futures-account-v2-for-master-account
        futuresType: 1:USDT Margined Futures, 2:COIN Margined Futures
        '''
        endpoint = "/sapi/v2/sub-account/futures/account"
        params = {
            'email':email,
            'futuresType':futuresType,
            'recvWindow':recvWindow
        }
        get_detail_on_sub_account_futures_account = self.send_signed_request_variableParams("GET",endpoint,params)
        return get_detail_on_sub_account_futures_account
    
    def get_summary_of_sub_account_futures_account(self,futuresType,page=None,limit=None,recvWindow=None):
        '''
        Query All sub-accounts futures account information (For Master Account)
        futuresType: 1:USDT Margined Futures, 2:COIN Margined Futures
        https://binance-docs.github.io/apidocs/spot/en/#get-summary-of-sub-account-39-s-futures-account-v2-for-master-account
        '''
        endpoint = '/sapi/v2/sub-account/futures/accountSummary'
        params = {
            'futuresType':futuresType,
            'page':page,
            'limit':limit,
            'recvWindow':recvWindow
        }
        get_summary_of_sub_account_futures_account = self.send_signed_request_variableParams("GET",endpoint,params)
        return get_summary_of_sub_account_futures_account
    
    def get_futures_position_risk_of_sub_account(self,email,futuresType,recvWindow):
        '''
        Get futures positions on selected sub-account (For Master Account)
        futuresType: 1:USDT Margined Futures, 2:COIN Margined Futures
        https://binance-docs.github.io/apidocs/spot/en/#get-futures-position-risk-of-sub-account-v2-for-master-account
        '''
        endpoint = "/sapi/v2/sub-account/futures/positionRisk"
        params ={
            'email':email,
            'futuresType':futuresType,
            'recvWindow':recvWindow
        }
        get_futures_position_risk_of_sub_account = self.send_signed_request_variableParams("GET",endpoint,params)
        return get_futures_position_risk_of_sub_account
    
    def enable_leverage_token_for_sub_account(self,email,enableBlvt,recvWindow=None):
        '''
        Enable leverage token for Sub-account (For Master Account)
        https://binance-docs.github.io/apidocs/spot/en/#enable-leverage-token-for-sub-account-for-master-account
        '''
        endpoint = '/sapi/v1/sub-account/blvt/enable'
        params = {
            'email':email,
            'enableBlvt':enableBlvt,
            'recvWindow':recvWindow
        }
        enable_leverage_token_for_sub_account = self.send_signed_request_variableParams("POST",endpoint,params)
        return enable_leverage_token_for_sub_account
    
    def get_ip_restriction_for_sub_account_api_key(self,email,subAccountApiKey,recvWindow=None):
        '''
        Query ip restrictions for sub account's api key. (For Master Account)

        https://binance-docs.github.io/apidocs/spot/en/#get-ip-restriction-for-a-sub-account-api-key-for-master-account
        '''
        endpoint = '/sapi/v1/sub-account/subAccountApi/ipRestriction'
        params = {
            'email':email,
            'subAccountApiKey':subAccountApiKey,
            'recvWindow':recvWindow
        }
        get_ip_restriction_for_sub_account_api_key = self.send_signed_request_variableParams("GET",endpoint,params)
        return get_ip_restriction_for_sub_account_api_key
    
    def delete_ip_list_for_sub_account_api_key(self,email,subAccountApiKey,ipAddress=None,recvWindow=None):
        '''
        Delete IPs for sub-account API key.(For Master Account)

        https://binance-docs.github.io/apidocs/spot/en/#delete-ip-list-for-a-sub-account-api-key-for-master-account
        '''
        endpoint = "/sapi/v1/sub-account/subAccountApi/ipRestriction/ipList"
        params = {
            'email':email,
            'subAccountApiKey':subAccountApiKey,
            'ipAddress':ipAddress,
            'recvWindow':recvWindow
        }
        delete_ip_list_for_sub_account_api_key = self.send_signed_request_variableParams("DELETE",endpoint,params)
        return delete_ip_list_for_sub_account_api_key
    
    def add_ip_restriction_for_sub_account_api_key(self,email,subAccountApiKey,status,ipAddress=None,recvWindow=None):
        '''
        Add IPs for sub-account API key. (For Master Account)

        https://binance-docs.github.io/apidocs/spot/en/#add-ip-restriction-for-sub-account-api-key-for-master-account
        '''
        endpoint = "/sapi/v2/sub-account/subAccountApi/ipRestriction"
        params = {
            'email':email,
            'subAccountApiKey':subAccountApiKey,
            'status':status,
            'ipAddress':ipAddress,
            'recvWindow':recvWindow
        }
        add_ip_restriction_for_sub_account_api_key = self.send_signed_request_variableParams("POST",endpoint,params)
        return add_ip_restriction_for_sub_account_api_key
    
    def deposit_assets_into_the_Managed_sub_account(self,toEmail,asset,amount,recvWindow=None):
        '''
        Desposit assets into Managed sub-account (For Investor Master Account)

        https://binance-docs.github.io/apidocs/spot/en/#deposit-assets-into-the-managed-sub-account-for-investor-master-account
        '''
        endpoint = "/sapi/v1/managed-subaccount/deposit"
        params = {
            'toEmail':toEmail,
            'asset':asset,
            'amount':amount,
            'recvWindow':recvWindow
        }
        deposit_assets_into_the_Managed_sub_account = self.send_signed_request_variableParams('POST',endpoint,params)
        return deposit_assets_into_the_Managed_sub_account
    
    def query_Managed_sub_account_asset_details(self,email,recvWindow=None):
        '''
        Query Managed sub-account asset details  (For Investor Master Account)

        https://binance-docs.github.io/apidocs/spot/en/#query-managed-sub-account-asset-details-for-investor-master-account
        '''
        endpoint ="/sapi/v1/managed-subaccount/asset"
        params = {
            'email':email,
            'recvWindow':recvWindow
        }
        query_Managed_sub_account_asset_details = self.send_signed_request_variableParams('GET',endpoint,params)
        return query_Managed_sub_account_asset_details
    
    def withdraw_assets_from_Managed_sub_account(self,fromEmail,asset,amount,transferDate=None,recvWindow=None):
        '''
        Withdraw assets from Managed Sub-account (For Investor Master Account)

        https://binance-docs.github.io/apidocs/spot/en/#withdrawl-assets-from-the-managed-sub-account-for-investor-master-account
        '''
        endpoint = '/sapi/v1/managed-subaccount/withdraw'
        params ={
            'fromEmail':fromEmail,
            'asset':asset,
            'amount':amount,
            'transferDate':self.time_ts(transferDate)
        }
        withdraw_assets_from_Managed_sub_account = self.send_signed_request_variableParams('POST',endpoint,params)
        return withdraw_assets_from_Managed_sub_account

    def query_Managed_sub_account_snapshot(self,email,type,startTime=None,endTime=None,limit=None,recvWindow=None):
        '''
        Query Managed sub-account snapshot (For Investor Master Account)

        type: SPOT, MARGIN, FUTURES  (MARGIN : cross margin ; FUTURES: UM)

        https://binance-docs.github.io/apidocs/spot/en/#query-managed-sub-account-snapshot-for-investor-master-account
        '''
        endpoint = "/sapi/v1/managed-subaccount/accountSnapshot"
        params = {
            'email':email,
            'type':type,
            'startTime':self.time_ts(startTime),
            'endTime':self.time_ts(endTime),
            'limit':limit,
            'recvWindow':recvWindow
        }
        query_Managed_sub_account_snapshot = self.send_signed_request_variableParams("GET",endpoint,params)
        return query_Managed_sub_account_snapshot
    
    def query_Managed_sub_account_transfer_log_investor_master(self,email,startTime,endTime,page,limit,transfers=None,transferFunctionAccountType=None):
        '''
        Investor can use this api to query managed sub account transfer log. (For Investor Master Account)

        https://binance-docs.github.io/apidocs/spot/en/#query-managed-sub-account-transfer-log-for-investor-master-account-user_data
        '''

        endpoint = "/sapi/v1/managed-subaccount/queryTransLogForInvestor"
        params = {
            'email':email,
            'startTime':startTime,
            'endTime':endTime,
            'page':page,
            'limit':limit,
            'transfers':transfers,
            'transferFunctionAccountType':transferFunctionAccountType
        }
        query_Managed_sub_account_transfer_log = self.send_signed_request_variableParams('GET',endpoint, params)
        return query_Managed_sub_account_transfer_log
    
    def query_Managed_sub_account_transfer_log_trading_master(self,email,startTime,endTime,page,limit,transfers=None,transferFunctionAccountType=None):
        '''
        Trading team can use this api to query managed sub account transfer log. 

        https://binance-docs.github.io/apidocs/spot/en/#query-managed-sub-account-transfer-log-for-trading-team-master-account-user_data
        '''
        endpoint = "/sapi/v1/managed-subaccount/queryTransLogForTradeParent"
        params = {
            'email':email,
            'startTime':startTime,
            'endTime':endTime,
            'page':page,
            'limit':limit,
            'transfers':transfers,
            'transferFunctionAccountType':transferFunctionAccountType
        }
        query_Managed_sub_account_transfer_log_trading_master = self.send_signed_request_variableParams('GET',endpoint, params)
        return query_Managed_sub_account_transfer_log_trading_master
    
    def query_Managed_sub_account_futures_asset_details(self,email):
        '''
        Investor can use this api to query managed sub account futures asset details. (For Investor Master Account)

        https://binance-docs.github.io/apidocs/spot/en/#query-managed-sub-account-futures-asset-details-for-investor-master-account-user_data
        '''
        endpoint = '/sapi/v1/managed-subaccount/fetch-future-asset'
        params = {
            'email':email
        }
        query_Managed_sub_account_futures_asset_details = self.send_signed_request_variableParams('GET',endpoint, params)
        return query_Managed_sub_account_futures_asset_details
    
    def query_Managed_sub_account_margin_asset_details(self,email):
        '''
        Investor can use this api to query managed sub account margin asset details  (For Investor Master Account)

        https://binance-docs.github.io/apidocs/spot/en/#query-managed-sub-account-margin-asset-details-for-investor-master-account-user_data
        '''
        endpoint = "/sapi/v1/managed-subaccount/marginAsset"
        params = {
            'email':email
        }
        query_Managed_sub_account_margin_asset_details = self.send_signed_request_variableParams('GET',endpoint, params)
        return query_Managed_sub_account_margin_asset_details
    
    def query_Managed_sub_account_assets(self,email,recvWindow=None):
        '''
        Fetch managed sub-account assets (For Master Account)

        https://binance-docs.github.io/apidocs/spot/en/#query-sub-account-assets-for-master-account-user_data
        '''
        endpoint = "/sapi/v4/sub-account/assets"
        params = {
            'email':email,
            'recvWindow':recvWindow
        }
        query_Managed_sub_account_assets = self.send_signed_request_variableParams('GET',endpoint, params)
        return query_Managed_sub_account_assets
    
    def query_managed_sub_account_list(self,email=None,page=None,limit=None,recvWindow=None):
        '''
        Get investor's managed sub-account list.(For Investor)

        https://binance-docs.github.io/apidocs/spot/en/#query-managed-sub-account-list-for-investor-user_data
        '''
        endpoint = '/sapi/v1/managed-subaccount/info'
        params = {
            'email':email,
            'page':page,
            'limit':limit,
            'recvWindow':recvWindow
        }
        query_managed_sub_account_list = self.send_signed_request_variableParams('GET',endpoint, params)
        return query_managed_sub_account_list
    
    def query_sub_account_transaction_statisitics(self,email,recvWindow=None):
        '''
        Query Sub-account Transaction Statitics (For Master Account)

        https://binance-docs.github.io/apidocs/spot/en/#query-sub-account-transaction-statistics-for-master-account-user_data
        '''
        endpoint = "/sapi/v1/sub-account/transaction-statistics"
        params = {
            'email':email,
            'recvWindow':recvWindow
        }
        query_sub_account_transaction_statisitics = self.send_signed_request_variableParams('GET',endpoint, params)
        return query_sub_account_transaction_statisitics
    
    def get_Managed_sub_account_deposit_address(self,email,coin,network=None,recvWindow=None):
        """
        Get investor's managed sub-account deposit address. (For Investor)

        https://binance-docs.github.io/apidocs/spot/en/#get-managed-sub-account-deposit-address-for-investor-master-account-user_data
        """
        endpoint = "/sapi/v1/managed-subaccount/deposit/address"
        params = {
            'email':email,
            'coin':coin,
            'network':network,
            'recvWindow':recvWindow
        }
        get_Managed_sub_account_deposit_address = self.send_signed_request_variableParams('GET',endpoint, params)
        return get_Managed_sub_account_deposit_address
    

    """
    Market Data Endpoints
    """
    def test_connectivity(self):
        """
        Ping test to the Rest API
        """
        endpoint = "/api/v3/ping"
        test_connectivity = self.send_public_request('GET',endpoint)
        return test_connectivity

    def check_server_time(self):
        '''
        Get the current server time
        '''
        endpoint = "/api/v3/time"
        check_server_time = self.send_public_request('GET',endpoint)
        return check_server_time
    
    def exchangeInfo(self,symbol=None,symbols=None,permissions=None):
        '''
        Get exchangeInfo 
        '''
        endpoint = "/api/v3/exchangeInfo"
        params = {
            'symbol':symbol,
            'symbols':symbols,
            'permissions':permissions
        }
        exchangeInfo = self.send_public_request("GET",endpoint,params)
        return exchangeInfo
    
    def orderBook(self,symbol,limit=None):
        '''
        Get order book
        https://binance-docs.github.io/apidocs/spot/en/#order-book
        '''
        endpoint = "/api/v3/depth"
        params = {
            'symbol':symbol,
            'limit':limit
        }
        orderBook = self.send_public_request("GET",endpoint,params)
        return orderBook
    
    def recent_trades_list(self,symbol,limit=None):
        '''
        Get recent trades 
        https://binance-docs.github.io/apidocs/spot/en/#recent-trades-list
        '''
        endpoint = "/api/v3/trades"
        params = {
            'symbol':symbol,
            'limit':limit
        }
        recent_trades_list = self.send_public_request("GET",endpoint,params)
        return recent_trades_list
    
    def old_trade_lookup(self,symbol,limit=None,fromId=None):
        '''
        Get old market trades.

        https://binance-docs.github.io/apidocs/spot/en/#old-trade-lookup-market_data
        '''
        endpoint = "/api/v3/historicalTrades"
        params = {
            'symbol':symbol,
            'limit':limit,
            'fromId':fromId
        }
        old_trade_lookup = self.send_public_request("GET",endpoint,params)
        return old_trade_lookup
    
    def aggregate_trades_list(self,symbol,fromId=None,startTime=None,endTime=None,limit=None):
        '''
        Get aggregate trades. Trades that fill at the time, from the same order, with the same price will have the quantity aggregated.

        https://binance-docs.github.io/apidocs/spot/en/#compressed-aggregate-trades-list
        '''
        endpoint = "/api/v3/aggTrades"
        params = {
            'symbol':symbol,
            'fromId':fromId,
            'startTime':self.time_ts(startTime),
            'endTime':self.time_ts(endTime),
            'limit':limit
        }
        aggregate_trades_list = self.send_public_request("GET",endpoint,params)
        return aggregate_trades_list
    
    def Klines(self,symbol,interval,startTime=None,endTime=None,limit=None):
        '''
        Kline/candlestic bar for a symbol,
        Klines are uniquely identified by their open time. 
        '''
        endpoint = "/api/v3/klines"
        params = {
            'symbol':symbol,
            'interval':interval,
            'startTime':self.time_ts(startTime),
            'endTime':self.time_ts(endTime),
            'limit':limit
        }
        Klines = self.send_public_request("GET",endpoint,params)
        return Klines
    
    def UIKlines(self,symbol,interval,startTime=None,endTime=None,limit=None):
        '''
        uiKlines return modified kline data, optimized for presentation of candlestick charts.
        '''
        endpoint = "/api/v3/uiKlines"
        params = {
            'symbol':symbol,
            'interval':interval,
            'startTime':self.time_ts(startTime),
            'endTime':self.time_ts(endTime),
            'limit':limit
        }
        UIKlines = self.send_public_request("GET",endpoint,params)
        return UIKlines
    
    def Klines_download(self,Symbol,Interval,StartTime,EndTime):
        """
        The function is to download the Kline within startTime and endTime, it will return a DataFrame. 
        """
        kline = self.Klines(symbol=Symbol,interval=Interval,startTime=StartTime,limit=1000) 
        kline = pd.DataFrame(kline.get('response'))
        kline.insert(0,column = "symbol",value=Symbol)

        while True:
            klines = self.Klines(symbol=Symbol,interval=Interval,startTime=self.ts_time(kline.iloc[-1,1]),limit=1000)
            new_kline = pd.DataFrame(klines.get('response'))
            new_kline.insert(0,column = "symbol",value=Symbol)
            kline = pd.concat(objs=[kline,new_kline],ignore_index=True)
            if kline.iloc[-1,1] >= int(self.time_ts(EndTime)):
                break 
            time.sleep(3)
            
        kline[0] = pd.to_datetime(kline[0],unit='ms')
        kline.columns = ["symbol","open_time","open","high","low","close","volume","close_time","base_asset_volume","num_of_trades","taker_buy_volume",
                         "taker_buy_base_asset_volume","ignore"]
        return kline  
    
    def current_average_price(self,symbol):
        '''
        Current average price for a symbol
        '''
        endpoint = "api/v3/avgPrice"
        params = {
            'symbol':symbol
        }
        current_average_price = self.send_public_request("GET",endpoint,params)
        return current_average_price
    
    def ticker_price_change_statistics_24hr(self,symbol=None,symbols=None,type=None):
        '''
        24 hour rolling window price change statistics. Careful when accessing this with no symbol.

        https://binance-docs.github.io/apidocs/spot/en/#24hr-ticker-price-change-statistics
        '''
        endpoint = "/api/v3/ticker/24hr"
        params = {
            'symbol':symbol,
            'symbols':symbols,
            'type':type
        }
        ticker_price_change_statistics_24hr = self.send_public_request("GET",endpoint,params)
        return ticker_price_change_statistics_24hr
    
    def symbol_price_ticker(self,symbol=None,symbols=None):
        '''
        Latest price for a symbol or symbols.

        https://binance-docs.github.io/apidocs/spot/en/#symbol-price-ticker
        '''
        endpoint = "/api/v3/ticker/price"
        params = {
            'symbol':symbol,
            'symbols':symbols
        }
        symbol_price_ticker = self.send_public_request('GET',endpoint,params)
        return symbol_price_ticker
    
    def symbol_order_book_ticker(self,symbol=None,symbols=None):
        '''
        Best price/qty on the order book for a symbol or symbols.

        https://binance-docs.github.io/apidocs/spot/en/#symbol-order-book-ticker
        '''
        endpoint = "/api/v3/ticker/bookTicker"
        params = {
            'symbol':symbol,
            'symbols':symbols
        }
        symbol_price_ticker = self.send_public_request('GET',endpoint,params)
        return symbol_price_ticker
    
    def rolling_window_price_statistics(self,symbol=None,symbols=None,windowSize=None,type=None):
        '''
        This endpoint is different from the GET /api/v3/ticker/24hr endpoint.
        https://binance-docs.github.io/apidocs/spot/en/#rolling-window-price-change-statistics
        '''

        endpoint = "/api/v3/ticker"
        params = {
            'symbol':symbol,
            'symbols':symbols,
            'windowSize':windowSize,
            'type':type
        }
        rolling_window_price_statistics = self.send_public_request('GET',endpoint,params)
        return rolling_window_price_statistics
    
    '''
    WebSocket Market Streams
    '''

    """
    Spot Account/Trade
    """
    def test_new_order(self,symbol,side,type,timeInForce=None,quantity=None,quoteOrderQty=None,price=None,
                       newClientOrderId=None,strategyId=None,strategyType=None,stopPrice=None,trailingDelta=None,
                       icebergQty=None,newOrderRespType=None,selfTradePreventionMode=None,recvWindow=None):
        '''
        Test new order creation and signature/recvWindow long. Creates and validates a new order but does not send it into the matching engine.

        https://binance-docs.github.io/apidocs/spot/en/#test-new-order-trade
        '''

        endpoint = "/api/v3/order"
        params = {
            "symbol":symbol,
            "side":side,
            'type':type,
            'timeInForce':timeInForce,
            'quantity':quantity,
            'quoteOrderQty':quoteOrderQty,
            'price':price,
            'newClientOrderId':newClientOrderId,
            "strategyId":strategyId,
            "strategyType":strategyType,
            "stopPrice":stopPrice,
            "trailingDelta":trailingDelta,
            "icebergQty":icebergQty,
            "newOrderRespType":newOrderRespType,
            "selfTradePreventionMode":selfTradePreventionMode,
            "recvWindow":recvWindow
        }
        spot_new_order = self.send_signed_request_variableParams('POST',endpoint,params)
        return spot_new_order
    
    def spot_new_order(self,symbol,side,type,timeInForce=None,quantity=None,quoteOrderQty=None,price=None,
                       newClientOrderId=None,strategyId=None,strategyType=None,stopPrice=None,trailingDelta=None,
                       icebergQty=None,newOrderRespType=None,selfTradePreventionMode=None,recvWindow=None):
        
        '''
        Send in a new order.

        https://binance-docs.github.io/apidocs/spot/en/#new-order-trade
        
        '''
        endpoint = "/api/v3/order"
        params = {
            "symbol":symbol,
            "side":side,
            'type':type,
            'timeInForce':timeInForce,
            'quantity':quantity,
            'quoteOrderQty':quoteOrderQty,
            'price':price,
            'newClientOrderId':newClientOrderId,
            "strategyId":strategyId,
            "strategyType":strategyType,
            "stopPrice":stopPrice,
            "trailingDelta":trailingDelta,
            "icebergQty":icebergQty,
            "newOrderRespType":newOrderRespType,
            "selfTradePreventionMode":selfTradePreventionMode,
            "recvWindow":recvWindow
        }
        spot_new_order = self.send_signed_request_variableParams('POST',endpoint,params)
        return spot_new_order

    def spot_cancel_order(self,symbol,orderId=None,origClientOrderId=None,newClientOrderId=None,cancelRestrictions=None,
                          recvWindow=None):
        """
        Cancel an active order.

        Either orderId or origClientOrderId must be sent. If both orderId and origClientOrderId are provided, orderId takes precedence.

        https://binance-docs.github.io/apidocs/spot/en/#cancel-order-trade
        """
        endpoint = "/api/v3/order"
        params = {
            'symbol':symbol,
            'orderId':orderId,
            'origClientOrderId':origClientOrderId,
            'newClientOrderId':newClientOrderId,
            'cancelRestrictions':cancelRestrictions,
            'recvWindow':recvWindow
        }
        spot_cancel_order = self.send_signed_request_variableParams('DELETE',endpoint,params)
        return spot_cancel_order

    def spot_cancel_all_orders_on_a_symbol(self,symbol,recvWindow=None):
        '''
        Cancels all active orders on a symbol, including OCO orders.

        https://binance-docs.github.io/apidocs/spot/en/#cancel-all-open-orders-on-a-symbol-trade
        '''
        endpoint = "/api/v3/openOrders"
        params ={
            'symbol':symbol,
            'recvWindow':recvWindow
        }
        spot_cancel_all_orders_on_a_symbol = self.send_signed_request_variableParams('DELETE',endpoint,params)
        return spot_cancel_all_orders_on_a_symbol
    
    def query_order(self,symbol,orderId=None,origClientOrderId=None,recvWindow=None):
        '''
        Check an order's status.

        https://binance-docs.github.io/apidocs/spot/en/#query-order-user_data
        '''
        endpoint = "/api/v3/order"
        params = {
            'symbol':symbol,
            'orderId':orderId,
            'origClientOrderId':origClientOrderId,
            'recvWindow':recvWindow

        }
        spot_cancel_all_orders_on_a_symbol = self.send_signed_request_variableParams('GET',endpoint,params)
        return spot_cancel_all_orders_on_a_symbol

    def spot_cancel_and_replace(self,symbol,side,type,cancelReplaceMode,timeInForce=None,quantity=None,quoteOrderQty=None,price=None,cancelNewClientOrderId=None,
                                cancelOrigClientOrderId=None,cancelOrderId=None,newClientOrderId=None,strategyId=None,strategyType=None,stopPrice=None,trailingDelta=None,icebergQty=None,
                                newOrderRespType=None,selfTradePreventionMode=None,cancelRestrictions=None,recvWindow=None):
        
        '''
        Cancels an existing order and places a new order on the same symbol.
        Filters and Order Count are evaluated before the processing of the cancellation and order placement occurs.

        A new order that was not attempted (i.e. when newOrderResult: NOT_ATTEMPTED), will still increase the order count by 1.

        https://binance-docs.github.io/apidocs/spot/en/#cancel-an-existing-order-and-send-a-new-order-trade
        '''
        endpoint = "/api/v3/order/cancelReplace"
        params = {
            'symbol':symbol,
            'side':side,
            'type':type,
            'cancelReplaceMode':cancelReplaceMode,
            'timeInForce':timeInForce,
            'quoteOrderQty':quoteOrderQty,
            'quantity':quantity,
            'price':price,
            'cancelNewClientOrderId':cancelNewClientOrderId,
            'cancelOrigClientOrderId':cancelOrigClientOrderId,
            'cancelOrderId':cancelOrderId,
            'newClientOrderId':newClientOrderId,
            'strategyId':strategyId,
            'strategyType':strategyType,
            'stopPrice':stopPrice,
            'icebergQty':icebergQty,
            'newOrderRespType':newOrderRespType,
            'selfTradePreventionMode':selfTradePreventionMode,
            'cancelRestrictions':cancelRestrictions,
            'recvWindow':recvWindow
            }
        spot_cancel_and_replace = self.send_signed_request_variableParams('POST',endpoint,params)
        return spot_cancel_and_replace

    def spot_open_orders(self,symbol=None,recvWindow=None):
        '''
        Get all open orders on a symbol or symbols 

        https://binance-docs.github.io/apidocs/spot/en/#current-open-orders-user_data
        '''
        endpoint = '/api/v3/openOrders'
        params = {
            'symbol':symbol,
            'recvWindow':recvWindow
        }
        spot_open_orders = self.send_signed_request_variableParams('GET',endpoint,params)
        return spot_open_orders
    

    def spot_all_orders(self,symbol,orderId=None,startTime=None,endTime=None,limit=None,recvWindow=None):
        '''
        Get all account orders; active; canceled, or filled.

        https://binance-docs.github.io/apidocs/spot/en/#all-orders-user_data
        '''
        endpoint = "/api/v3/allOrders"
        params ={
            'symbol':symbol,
            'orderId':orderId,
            'startTime':self.time_ts(startTime),
            'endTime':self.time_ts(endTime),
            'limit':limit,
            'recvWindow':recvWindow
        }
        spot_all_orders = self.send_signed_request_variableParams('GET',endpoint,params)
        return spot_all_orders
    
    def spot_new_oco(self,symbol,side,quantity,price,stopPrice,listClientOrderId=None,limitClientOrderId=None,limitStrategyId=None,limitStrategyType=None,limitIcebergQty=None,
                     trailingDelta=None,stopClientOrderId=None,stopStrategyId=None,stopStrategyType=None,stopLimitPrice=None,stopIcebergQty=None,stopLimitTimeInForce=None,
                     newOrderRespType=None,selfTradePreventionMode=None,recvWindow=None):
        
        '''
        Send in a new OCO order

        Price Restrictions:
            SELL: Limit Price > Last Price > Stop Price
            BUY: Limit Price < Last Price < Stop Price
        Quantity Restrictions:
            Both legs must have the same quantity
            ICEBERG quantities however do not have to be the same.
        Order Rate Limit
            OCO counts as 2 orders against the order rate limit.
        https://binance-docs.github.io/apidocs/spot/en/#new-oco-trade
        '''

        endpoint = '/api/v3/order/oco'
        params = {
            'symbol':symbol,
            'side':side,
            'quantity':quantity,
            'price':price,
            'stopPrice':stopPrice,
            'listClientOrderId':listClientOrderId,
            'limitClientOrderId':limitClientOrderId,
            'limitStrategyId':limitStrategyId,
            'limitStrategyType':limitStrategyType,
            'limitIcebergQty':limitIcebergQty,
            'trailingDelta':trailingDelta,
            'stopClientOrderId':stopClientOrderId,
            'stopStrategyId':stopStrategyId,
            'stopStrategyType':stopStrategyType,
            'stopLimitPrice':stopLimitPrice,
            'stopIcebergQty':stopIcebergQty,
            'stopLimitTimeInForce':stopLimitTimeInForce,
            'newOrderRespType':newOrderRespType,
            'selfTradePreventionMode':selfTradePreventionMode,
            'recvWindow':recvWindow
            }
        spot_new_oco = self.send_signed_request_variableParams('POST',endpoint,params)
        return spot_new_oco
    
    def spot_cancel_oco(self,symbol,orderListId=None,listClientOrderId=None,newClientOrderId=None,recvWindow=None):
        """
        Cancel Spot OCO order 

        https://binance-docs.github.io/apidocs/spot/en/#cancel-oco-trade
        """
        endpoint = "/api/v3/orderList"
        params = {
            'symbol':symbol,
            'orderListId':orderListId,
            'listClientOrderId':listClientOrderId,
            'newClientOrderId':newClientOrderId,
            'recvWindow':recvWindow
        }
        spot_cancel_oco = self.send_signed_request_variableParams('DELETE',endpoint,params)
        return spot_cancel_oco
    
    def spot_query_oco(self,orderListId=None,origClientOrderId=None,recvWindow=None):
        '''
        Retrieves a specfic OCO based on provided optional parameters. 

        https://binance-docs.github.io/apidocs/spot/en/#query-oco-user_data
        '''
        endpoint = '/api/v3/orderList'
        params = {
            'orderListId':orderListId,
            'origClientOrderId':origClientOrderId,
            'recvWindow':recvWindow,
        }
        spot_query_oco = self.send_signed_request_variableParams("GET",endpoint,params)
        return spot_query_oco
    
    def spot_query_all_oco(self,fromId=None,startTime=None,endTime=None,limit=None,recvWindow=None):
        '''
        Retrieves all OCO based on provided optional parameters

        https://binance-docs.github.io/apidocs/spot/en/#query-all-oco-user_data
        '''
        endpoint = "/api/v3/allOrderList"
        params = {
            'fromId':fromId,
            'startTime':self.time_ts(startTime),
            'endTime':self.time_ts(endTime),
            'limit':limit,
            'recvWindow':recvWindow
        }
        spot_query_all_oco = self.send_signed_request_variableParams("GET",endpoint,params)
        return spot_query_all_oco
    
    def spot_query_open_oco(self,recvWindow=None):
        """
        Query open OCO. 

        https://binance-docs.github.io/apidocs/spot/en/#query-open-oco-user_data
        """
        endpoint = "/api/v3/openOrderList"
        params = {
            'recvWindow':recvWindow
        }
        spot_query_open_oco = self.send_signed_request_variableParams("GET",endpoint,params)
        return spot_query_open_oco
    
    def account_information(self,recvWindow=None):
        '''
        Get current account information.
        https://binance-docs.github.io/apidocs/spot/en/#account-information-user_data
        '''
        endpoint = "/api/v3/account"
        params = {
            'recvWindow':recvWindow
        }
        account_information = self.send_signed_request_variableParams("GET",endpoint,params)
        return account_information
    
    def spot_account_trade_list(self,symbol,orderId=None,startTime=None,endTime=None,fromId=None,limit=None,recvWindow=None):
        """
        Get trades for a specific account and symbol.

        https://binance-docs.github.io/apidocs/spot/en/#account-trade-list-user_data
        """
        endpoint = "/api/v3/myTrades"
        params = {
            'symbol':symbol,
            'orderId':orderId,
            'startTime':self.time_ts(startTime),
            'endTime':self.time_ts(endTime),
            'fromId':fromId,
            'limit':limit,
            'recvWindow':recvWindow
        }
        spot_account_trade_list = self.send_signed_request_variableParams("GET",endpoint,params)
        return spot_account_trade_list
    
    def spot_query_current_order_count_usage(self,recvWindow=None):
        """
        Displays the user's current order count usage for all intervals.
        """
        endpoint = "/api/v3/rateLimit/order"
        params = {
            'recvWindow':recvWindow
        }
        spot_query_current_order_count_usage = self.send_signed_request_variableParams("GET",endpoint,params)
        return spot_query_current_order_count_usage
    
    def spot_query_prevented_matches(self,symbol,preventedMatchId=None,orderId=None,fromPreventedMatchId=None,limit=None,recvWindow=None):
        """
        Displays the list of orders that were expired because of STP.
        
        Combinations supported: 
        symbol + preventedMatchId
        symbol + orderId
        symbol + orderId + fromPreventedMatchId (limit will default to 500)
        symbol + orderId + fromPreventedMatchId + limit

        https://binance-docs.github.io/apidocs/spot/en/#query-prevented-matches-user_data
        """
        endpoint = "/api/v3/myPreventedMatches"
        params = {
            "symbol":symbol,
            "preventedMatchId":preventedMatchId,
            "orderId":orderId,
            "fromPreventedMatchId":fromPreventedMatchId,
            "limit":limit,
            'recvWindow':recvWindow
        }
        spot_query_prevented_matches = self.send_signed_request_variableParams("GET",endpoint,params)
        return spot_query_prevented_matches
    
    """
    Margin endpoints
    """

    def margin_get_assets_that_can_be_converted_into_BNB(self,recvWindow=None):
        """
        Get assets can be converted into BNB (Margin)

        https://binance-docs.github.io/apidocs/spot/en/#margin-dustlog-user_data
        """
        endpoint = "/sapi/v1/margin/dust"
        params = {
            "recvWindow":recvWindow
        }
        margin_get_assets_that_can_be_converted_into_BNB = self.send_signed_request_variableParams("GET",endpoint,params)
        return margin_get_assets_that_can_be_converted_into_BNB
    
    def margin_dust_transfer(self,asset,recvWindow=None):
        """
        Convert dust assets to BNB. (Margin)
        """
        endpoint = '/sapi/v1/margin/dust'
        params = {
            "asset":asset,
            "recvWindow":recvWindow
        }
        margin_dust_transfer = self.send_signed_request_variableParams("POST",endpoint,params)
        return margin_dust_transfer

    def cross_margin_account_transfer(self,asset,amount,type,recvWindow=None):
        """
        Execute transfer between spot account and cross margin account. 

        https://binance-docs.github.io/apidocs/spot/en/#cross-margin-account-transfer-margin
        """
        endpoint = "/sapi/v1/margin/transfer"
        params ={
            "asset":asset,
            "amount":amount,
            "type":type,
            "recvWindow":recvWindow
        }
        cross_margin_account_transfer = self.send_signed_request_variableParams('POST',endpoint,params)
        return cross_margin_account_transfer
    
    def margin_account_borrow(self,asset,amount,isIsolated=None,symbol=None,recvWindow=None):
        """
        Apply for a loan.
        isIsolated: True or False, default: False
        
        https://binance-docs.github.io/apidocs/spot/en/#margin-account-borrow-margin
        """
        endpoint = "/sapi/v1/margin/loan"
        params ={
            'asset':asset,
            'amount':amount,
            'isIsolated':isIsolated,
            'symbol':symbol,
            'recvWindow':recvWindow
        }
        margin_account_borrow = self.send_signed_request_variableParams("POST",endpoint,params)
        return margin_account_borrow
    
    def margin_account_repay(self,asset,amount,isIsolated=None,symbol=None,recvWindow=None):
        """
        Repay loan for margin account.
        isIsolated: True or False, default: False
        
        https://binance-docs.github.io/apidocs/spot/en/#margin-account-repay-margin
        """
        endpoint = "/sapi/v1/margin/repay"
        params ={
            'asset':asset,
            'amount':amount,
            'isIsolated':isIsolated,
            'symbol':symbol,
            'recvWindow':recvWindow
        }
        margin_account_repay = self.send_signed_request_variableParams("POST",endpoint,params)
        return margin_account_repay
    
    def query_margin_asset(self,asset):
        """
        Query margin asset (Cross margin)

        https://binance-docs.github.io/apidocs/spot/en/#get-all-margin-assets-market_data
        """
        endpoint = "/sapi/v1/margin/asset"
        params = {
            'asset':asset
        }
        query_margin_asset = self.send_signed_request_variableParams("POST",endpoint,params)
        return query_margin_asset
    
    def margin_query_cross_margin_pair(self,symbol):
        """
        Query Cross Margin Pair
        """
        endpoint = "/sapi/v1/margin/pair"
        params = {
            'symbol':symbol
        }
        margin_query_cross_margin_pair =  self.send_public_request("GET",endpoint,params)
        return margin_query_cross_margin_pair
    
    def get_all_margin_assets(self):
        """
        Get all margin assets 
        """
        endpoint = "/sapi/v1/margin/allAssets"
        get_all_margin_assets =  self.send_public_request("GET",endpoint)
        return get_all_margin_assets


    def get_all_cross_margin_symbols(self):
        '''
        Get all cross margin symbols.
        https://binance-docs.github.io/apidocs/spot/en/#get-all-cross-margin-pairs-market_data
        '''

        endpoint = '/sapi/v1/margin/allPairs'
        get_all_cross_margin_symbols = self.send_public_request("GET",endpoint)
        return get_all_cross_margin_symbols
    
    def query_margin_PriceIndex(self,symbol):
        """
        Query margin PriceIndex by symbol. 
        """
        endpoint = "/sapi/v1/margin/priceIndex"
        params = {
            'symbol':symbol
        }
        query_margin_PriceIndex = self.send_public_request("GET",endpoint)
        return query_margin_PriceIndex
    
    def margin_new_order(self,symbol,side,type,isIsolated=None,quantity=None,price=None,stopPrice=None,
                         newClientOrderId=None,icebergQty=None,newOrderRespType=None,sideEffectType=None,
                         timeInForce=None,autoRepayAtCancel=None,selfTradePreventionMode=None,recvWindow=None):
        """
        Post a new order for margin account 

        autoRepayAtCancel (bool): Only when MARGIN_BUY or AUTO_BORROW_REPAY order takes effect, True means that the debt generated by the order needs to be repay after the order is cancelled. The default setting is the True.
        selfTradePreventionMode (ENUM): The allowed enums is dependent on what is configured on the symbol. The possible supported values are EXPIRE_TAKER, EXPIRE_MAKER, EXPIRE_BOTH, NONE

        https://binance-docs.github.io/apidocs/spot/en/#margin-account-new-order-trade
        """
        endpoint ="/sapi/v1/margin/order"
        params = {
            'symbol':symbol,
            'side':side,
            'type':type,
            'isIsolated':isIsolated,
            'quantity':quantity,
            'price':price,
            'stopPrice':stopPrice,
            'newClientOrderId':newClientOrderId,
            'icebergQty':icebergQty,
            'newOrderRespType':newOrderRespType,
            'sideEffectType':sideEffectType,
            'timeInForce':timeInForce,
            "autoRepayAtCancel":autoRepayAtCancel,
            "selfTradePreventionMode":selfTradePreventionMode,
            'recvWindow':recvWindow
        }
        margin_new_order = self.send_signed_request_variableParams("POST",endpoint,params)
        return margin_new_order
    
    def margin_cancel_order(self,symbol,isIsolated=None,orderId=None,origClientId=None,newClientOrderId=None,recvWindow=None):
        """
        Cancel an active order for margin account.
        https://binance-docs.github.io/apidocs/spot/en/#margin-account-cancel-all-open-orders-on-a-symbol-trade
        """
        endpoint = "/sapi/v1/margin/order"
        params = {
            'symbol':symbol,
            "isIsolated":isIsolated,
            "orderId":orderId,
            "origClientId":origClientId,
            "newClientOrderId":newClientOrderId,
            "recvWindow":recvWindow
        }
        margin_new_order = self.send_signed_request_variableParams("DELETE",endpoint)
        return margin_new_order
    
    def margin_cancel_all_open_orders_on_a_symbol(self,symbol,isIsolated=None,recvWindow=None):
        '''
        Cancel all open orders on a symbol for margin account. 

        https://binance-docs.github.io/apidocs/spot/en/#margin-account-cancel-all-open-orders-on-a-symbol-trade
        '''
        endpoint  = "/sapi/v1/margin/openOrders"
        params = {
            "symbol":symbol,
            'isIsolated':isIsolated,
            "recvWindow":recvWindow
        }
        margin_cancel_all_open_orders_on_a_symbol = self.send_signed_request_variableParams("DELETE",endpoint,params)
        return margin_cancel_all_open_orders_on_a_symbol
    
    def get_cross_margin_transfer_history(self,asset=None,type=None,startTime=None,endTime=None,current=None,
                                          size=None,archived=None,recvWindow=None):
        """
        Fetch cross margin transfer history. 
        Default: false. Set to true for archived data from 6 months ago
        https://binance-docs.github.io/apidocs/spot/en/#get-cross-margin-transfer-history-user_data
        """
        endpoint = "/sapi/v1/margin/transfer"
        params ={
            "asset":asset,
            "type":type,
            "startTime":self.time_ts(startTime),
            "endTime":self.time_ts(endTime),
            "current":current,
            "size":size,
            "archived":archived,
            "recvWindow":recvWindow
            }
        get_cross_margin_transfer_history = self.send_signed_request_variableParams("GET",endpoint,params)
        return get_cross_margin_transfer_history
    
    def query_loan_record(self,asset,isolatedSymbol=None,txId=None,startTime=None,endTime=None,current=None,
                          size=None,archived=None,recvWindow=None):
        """
        Query Loan Record
        https://binance-docs.github.io/apidocs/spot/en/#query-repay-record-user_data
        """
        endpoint ="/sapi/v1/margin/loan"
        params = {
            "asset":asset,
            "isolatedSymbol":isolatedSymbol,
            "txId":txId,
            "startTime":self.time_ts(startTime),
            "endTime":self.time_ts(endTime),
            "current":current,
            "size":size,
            "archived":archived,
            "recvWindow":recvWindow
        }
        query_loan_record = self.send_signed_request_variableParams("GET",endpoint,params)
        return query_loan_record
    
    def query_repay_record(self,asset,isolatedSymbol=None,txId=None,startTime=None,endTime=None,current=None,
                          size=None,archived=None,recvWindow=None):
        """
        Query Loan Record
        https://binance-docs.github.io/apidocs/spot/en/#query-repay-record-user_data
        """
        endpoint ="/sapi/v1/margin/repay"
        params = {
            "asset":asset,
            "isolatedSymbol":isolatedSymbol,
            "txId":txId,
            "startTime":self.time_ts(startTime),
            "endTime":self.time_ts(endTime),
            "current":current,
            "size":size,
            "archived":archived,
            "recvWindow":recvWindow
        }
        query_repay_record = self.send_signed_request_variableParams("GET",endpoint,params)
        return query_repay_record
        
    
    def get_all_isolated_margin_symbol(self,recvWindow=None):
        '''
        Get all isolated margin symbols

        https://binance-docs.github.io/apidocs/spot/en/#get-all-isolated-margin-symbol-user_data
        '''
        endpoint = "/sapi/v1/margin/isolated/allPairs"
        params = {
            'recvWindow':recvWindow
        }
        get_all_isolated_margin_symbol = self.send_signed_request_variableParams("GET",endpoint,params)
        return get_all_isolated_margin_symbol
    
    def get_margin_interest_history(self,asset=None,isolatedSymbol=None,startTime=None,endTime=None,current=None,
                             size=None,archived=None,recvWindow=None):
        '''
        Get interest history

        https://binance-docs.github.io/apidocs/spot/en/#get-interest-history-user_data
        '''
        endpoint = "/sapi/v1/margin/interestHistory"
        params = {
            "asset":asset,
            "isolatedSymbol":isolatedSymbol,
            "startTime":self.time_ts(startTime),
            "endTime":self.time_ts(endTime),
            "current":current,
            "size":size,
            "archived":archived,
            "recvWindow":recvWindow

        }
        get_margin_interest_history = self.send_signed_request_variableParams("GET",endpoint,params)
        return get_margin_interest_history
    
    def get_force_liquidation_record(self,startTime=None,endTime=None,isolatedSymbol=None,current=None,size=None,recvWindow=None):
        '''
        Get liquidation records

        https://binance-docs.github.io/apidocs/spot/en/#get-force-liquidation-record-user_data
        '''
        endpoint = "/sapi/v1/margin/forceLiquidationRec"
        params = {
            'startTime':self.time_ts(startTime),
            'endTime':self.time_ts(endTime),
            'isolatedSymbol':isolatedSymbol,
            'current':current,
            'size':size,
            'recvWindow':recvWindow

        }
        get_force_liquidation_record = self.send_signed_request_variableParams("GET",endpoint,params)
        return get_force_liquidation_record
    
    def query_cross_margin_account_detail(self,recvWindow=None):
        """
        Query cross margin account detail.

        https://binance-docs.github.io/apidocs/spot/en/#query-cross-margin-account-details-user_data
        """
        endpoint = "/sapi/v1/margin/account"
        params = {'recvWindow':recvWindow}
        query_cross_margin_account_detail = self.send_signed_request_variableParams("GET",endpoint,params)
        return query_cross_margin_account_detail
    
    def query_margin_account_order(self,symbol,isIsolated=None,orderId=None,origClientOrderId=None,recvWindow=None):
        """
        Query margin account's order
        https://binance-docs.github.io/apidocs/spot/en/#query-margin-account-39-s-order-user_data
        """
        endpoint = "/sapi/v1/margin/order"
        params = {
            'symbol':symbol,
            'isIsolated':isIsolated,
            'orderId':orderId,
            'origClientOrderId':origClientOrderId,
            'recvWindow':recvWindow
        }
        query_margin_account_order = self.send_signed_request_variableParams("GET",endpoint,params)
        return query_margin_account_order
    
    def query_margin_account_open_orders(self,symbol=None,isIsoloated=None,recvWindow=None):
        """
        Query margin account open orders. 

        https://binance-docs.github.io/apidocs/spot/en/#query-margin-account-39-s-open-orders-user_data
        """
        endpoint = "/sapi/v1/margin/openOrders"
        params = {
            'symbol':symbol,
            'isIsoloated':isIsoloated,
            'recvWindow':recvWindow
        }
        query_margin_account_open_orders = self.send_signed_request_variableParams("GET",endpoint,params)
        return query_margin_account_open_orders
    
    def query_margin_account_all_orders(self,symbol,isIsolated=None,orderId=None,startTime=None,endTime=None,limit=None,recvWindow=None):
        """
        Query margin account's All orders. 

        https://binance-docs.github.io/apidocs/spot/en/#query-margin-account-39-s-all-orders-user_data
        """
        endpoint= "/sapi/v1/margin/allOrders"
        params = {
            'symbol':symbol,
            "isIsolated":isIsolated,
            "orderId":orderId,
            "startTime":self.time_ts(startTime),
            "endTime":self.time_ts(endTime),
            "limit":limit,
            "recvWindow":recvWindow
        }
        query_margin_account_all_orders = self.send_signed_request_variableParams("GET",endpoint,params)
        return query_margin_account_all_orders
    
    def margin_new_oco(self,symbol,side,quantity,price,stopPrice,isIsolated=None,listClientOrderId=None,limitClientOrderId=None,
                       limitIcebergQty=None,stopClientOrderId=None,stopLimitPrice=None,stopIcebergQty=None,stopLimitTimeInForce=None,
                       newOrderRespType=None,sideEffectType=None,autoRepayAtCancel=None,recvWindow=None):
        """
        Send in a new OCO for a margin account

        https://binance-docs.github.io/apidocs/spot/en/#margin-account-new-oco-trade

        Price Restrictions:
            SELL: Limit Price > Last Price > Stop Price
            BUY: Limit Price < Last Price < Stop Price
        Quantity Restrictions:
            Both legs must have the same quantity
            ICEBERG quantities however do not have to be the same.
        Order Rate Limit
            OCO counts as 2 orders against the order rate limit.

        autoRepayAtCancel (bool): Only when MARGIN_BUY or AUTO_BORROW_REPAY order takes effect, True means that the debt generated by the order needs to be repay after the order is cancelled. The default setting is the True.
        """
        endpoint = "/sapi/v1/margin/order/oco"
        params = {
            "symbol":symbol,
            "side":side,
            "quantity":quantity,
            "price":price,
            "stopPrice":stopPrice,
            "isIsolated":isIsolated,
            "listClientOrderId":listClientOrderId,
            "limitClientOrderId":limitClientOrderId,
            "limitIcebergQty":limitIcebergQty,
            "stopClientOrderId":stopClientOrderId,
            "stopLimitPrice":stopLimitPrice,
            "stopIcebergQty":stopIcebergQty,
            "stopLimitTimeInForce":stopLimitTimeInForce,
            "newOrderRespType":newOrderRespType,
            "sideEffectType":sideEffectType,
            "autoRepayAtCancel":autoRepayAtCancel,
            "recvWindow":recvWindow
            }
        margin_new_oco = self.send_signed_request_variableParams("POST",endpoint,params)
        return margin_new_oco
    
    def margin_cancel_oco(self,symbol,isIsolated=None,orderListid=None,listClientOrderId=None,newClientOrderId=None,
                          recvWindow=None):
        """
        Cancel an entire Order List for a margin account.

        https://binance-docs.github.io/apidocs/spot/en/#margin-account-cancel-oco-trade
        """
        endpoint = "/sapi/v1/margin/orderList"
        params = {
            "symbol":symbol,
            "isIsolated":isIsolated,
            "orderListid":orderListid,
            "listClientOrderId":listClientOrderId,
            "newClientOrderId":newClientOrderId,
            "recvWindow":recvWindow
        }
        margin_cancel_oco = self.send_signed_request_variableParams("DELETE",endpoint,params)
        return margin_cancel_oco

    def query_margin_account_oco(self,isIsolated=None,symbol=None,orderListId=None,origClientOrderId=None,recvWindow=None):
        """
        Retrieves a specific OCO based on provided optional parameters

        https://binance-docs.github.io/apidocs/spot/en/#query-margin-account-39-s-oco-user_data
        """
        endpoint = "/sapi/v1/margin/orderList"
        params = {
            "symbol":symbol,
            "isIsolated":isIsolated,
            "orderListId":orderListId,
            "origClientOrderId":origClientOrderId,
            "recvWindow":recvWindow
        }
        query_margin_account_oco = self.send_signed_request_variableParams("GET",endpoint,params)
        return query_margin_account_oco
    
    def query_margin_account_all_oco(self,isIsolated=None,symbol=None,fromId=None,startTime=None,endTime=None,limit=None,recvWindow=None):
        """
        Retrieves all OCO for a specific margin account based on provided optional parameters

        https://binance-docs.github.io/apidocs/spot/en/#query-margin-account-39-s-all-oco-user_data
        """
        endpoint = "/sapi/v1/margin/allOrderList"
        params = {
            "symbol":symbol,
            "isIsolated":isIsolated,
            "fromId":fromId,
            "startTime":self.time_ts(startTime),
            "endTime":self.time_ts(endTime),
            "limit":limit,
            "recvWindow":recvWindow
        }
        query_margin_account_all_oco = self.send_signed_request_variableParams("GET",endpoint,params)
        return query_margin_account_all_oco
    
    def query_margin_account_open_oco(self,isIsolated=False,symbol=None,recvWindow=None):
        """
        Query margin account open OCO orders. 

        https://binance-docs.github.io/apidocs/spot/en/#query-margin-account-39-s-open-oco-user_data
        """
        endpoint = "/sapi/v1/margin/openOrderList"
        params = {
            "isIsolated":isIsolated,
            "symbol":symbol,
            "recvWindow":recvWindow
        }
        query_margin_account_open_oco = self.send_signed_request_variableParams("GET",endpoint,params)
        return query_margin_account_open_oco
    
    def query_margin_account_trade_list(self,symbol,isIsolated=None,orderId=None,startTime=None,endTime=None,fromId=None,limit=None,recvWindow=None):
        """
        Query margin account's trade list 

        https://binance-docs.github.io/apidocs/spot/en/#query-margin-account-39-s-trade-list-user_data
        """
        endpoint = "/sapi/v1/margin/myTrades"
        params = {
            "symbol":symbol,
            "isIsolated":isIsolated,
            "orderId":orderId,
            "startTime":self.time_ts(startTime),
            "endTime":self.time_ts(endTime),
            "fromId":fromId,
            "limit":limit,
            "recvWindow":recvWindow
        }
        query_margin_account_trade_list = self.send_signed_request_variableParams("GET",endpoint,params)
        return query_margin_account_trade_list

    def query_max_borrow(self,asset,isolatedSymbol=None,recvWindow=None):
        """
        Query asset's maximum brrow , same info as https://www.binance.com/en/margin-fee

        https://binance-docs.github.io/apidocs/spot/en/#query-max-borrow-user_data
        """
        endpoint = "/sapi/v1/margin/maxBorrowable"
        params = {
            "asset":asset,
            "isolatedSymbol":isolatedSymbol,
            "recvWindow":recvWindow

        }
        query_max_borrow = self.send_signed_request_variableParams("GET",endpoint,params)
        return query_max_borrow
    
    def query_max_transfer_out_amount(self,asset,isolatedSymbol=None,recvWindow=None):
        """
        Query asset maximum transfer-out amount.  Only when margin level> 2 , users can transfer

        https://binance-docs.github.io/apidocs/spot/en/#query-max-transfer-out-amount-user_data
        """
        endpoint = "/sapi/v1/margin/maxTransferable"
        params = {
            "asset":asset,
            "isolatedSymbol":isolatedSymbol,
            "recvWindow":recvWindow

        }
        query_max_transfer_out_amount = self.send_signed_request_variableParams("GET",endpoint,params)
        return query_max_transfer_out_amount
    
    def summary_of_margin_account(self,recvWindow=None):
        '''
        Get personal margin level information .

        https://binance-docs.github.io/apidocs/spot/en/#get-summary-of-margin-account-user_data
        '''
        endpoint = "/sapi/v1/margin/tradeCoeff"
        params = {
            "recvWindow":recvWindow

        }
        summary_of_margin_account = self.send_signed_request_variableParams("GET",endpoint,params)
        return summary_of_margin_account
    
    def isolated_margin_account_transfer(self,asset,symbol,transFrom,transTo,amount,recvWindow=None):
        """
        Post an Isolated margin account transfer. 

        https://binance-docs.github.io/apidocs/spot/en/#isolated-margin-account-transfer-margin
        """
        endpoint = "/sapi/v1/margin/isolated/transfer"
        params = {
            "asset":asset,
            "symbol":symbol,
            "transFrom":transFrom,
            "transTo":transTo,
            "amount":amount,
            "recvWindow":recvWindow
        }
        isolated_margin_account_transfer = self.send_signed_request_variableParams("POST",endpoint,params)
        return isolated_margin_account_transfer
    
    def get_isolated_margin_transfer_history(self,symbol,asset=None,transFrom=None,transTo=None,startTime=None,endTime=None,current=None,size=None,
                                             archived=None,recvWindow=None):
        """
        Query isoalted margin transfer history

        https://binance-docs.github.io/apidocs/spot/en/#get-isolated-margin-transfer-history-user_data
        """
        endpoint = "/sapi/v1/margin/isolated/transfer"
        params = {
            'symbol':symbol,
            'asset':asset,
            'transFrom':transFrom,
            'transTo':transTo,
            'startTime':self.time_ts(startTime),
            'endTime':self.time_ts(endTime),
            'current':current,
            'size':size,
            'archived':archived,
            "recvWindow":recvWindow
            
        }
        get_isolated_margin_transfer_history = self.send_signed_request_variableParams("GET",endpoint,params)
        return get_isolated_margin_transfer_history
    
    def query_isolated_margin_account_info(self,symbols,recvWindow=None):
        """
        Query isolated margin account information. 

        https://binance-docs.github.io/apidocs/spot/en/#query-isolated-margin-account-info-user_data
        """
        endpoint = "/sapi/v1/margin/isolated/account"
        params = {
            "symbols":symbols,
            "recvWindow":recvWindow
        }
        query_isolated_margin_account_info = self.send_signed_request_variableParams("GET",endpoint,params)
        return query_isolated_margin_account_info
    
    def disable_isolated_margin_account(self,symbol,recvWindow=None):
        """
        Disable isolated margin account for a specific symbol. Each trading pair can only be deactivated once every 24 hours. 

        https://binance-docs.github.io/apidocs/spot/en/#disable-isolated-margin-account-trade
        """
        endpoint = "/sapi/v1/margin/isolated/account"
        params = {
            "symbol":symbol,
            "recvWindow":recvWindow
        }
        disable_isolated_margin_account = self.send_signed_request_variableParams("DELETE",endpoint,params)
        return disable_isolated_margin_account
    
    def enable_isolated_margin_account(self,symbol,recvWindow=None):
        """
        Enable isolated margina account for a specific symbol (Only supports activation of previously disabled accounts)

        https://binance-docs.github.io/apidocs/spot/en/#enable-isolated-margin-account-trade
        """
        endpoint = "/sapi/v1/margin/isolated/account"
        params = {
            "symbol":symbol,
            "recvWindow":recvWindow
        }
        enable_isolated_margin_account = self.send_signed_request_variableParams("POST",endpoint,params)
        return enable_isolated_margin_account
    
    def query_enabled_isoalted_margin_account_limit(self,recvWindow=None):
        """
        Query enabled isolated margin account limit

        https://binance-docs.github.io/apidocs/spot/en/#query-enabled-isolated-margin-account-limit-user_data
        """
        endpoint = "/sapi/v1/margin/isolated/accountLimit"
        params = {
            "recvWindow":recvWindow
        }
        query_enabled_isoalted_margin_account_limit = self.send_signed_request_variableParams("GET",endpoint,params)
        return query_enabled_isoalted_margin_account_limit
    
    def query_isolalted_margin_symbol(self,symbol,recvWindow=None):
        """
        Query isolated margin symbol

        https://binance-docs.github.io/apidocs/spot/en/#query-isolated-margin-symbol-user_data
        """
        endpoint = "/sapi/v1/margin/isolated/pair"
        params = {
            "symbol":symbol,
            "recvWindow":recvWindow
        }
        query_isolalted_margin_symbol = self.send_signed_request_variableParams("GET",endpoint,params)
        return query_isolalted_margin_symbol
    
    def get_all_isolated_margin_symbol(self,recvWindow=None):
        """
        Get all isolated margin symbols. 

        https://binance-docs.github.io/apidocs/spot/en/#get-all-isolated-margin-symbol-user_data
        """
        endpoint = "/sapi/v1/margin/isolated/allPairs"
        params = {
            "recvWindow":recvWindow
        }
        get_all_isolated_margin_symbol = self.send_signed_request_variableParams("GET",endpoint,params)
        return get_all_isolated_margin_symbol
    
    def BNB_burn_on_spot_trade_and_margin_interest(self,spotBNBBurn=None,interestBNBBurn=None,recvWindow=None):
        """
        To change options to pay trading fee on SPOT by BNB / Margin interests counted by BNB. 

        spotBNBBurn: Bool. True: pay trading fee by BNB ; False: pay trading fee by converted assets
        interestBNBBurn: Bool. True: use BNB to pay for margin loan's interest. 

        "spotBNBBurn" and "interestBNBBurn" should be sent at least one.

        https://binance-docs.github.io/apidocs/spot/en/#toggle-bnb-burn-on-spot-trade-and-margin-interest-user_data
        """
        endpoint = "/sapi/v1/bnbBurn"
        params = {
            "spotBNBBurn":spotBNBBurn,
            "interestBNBBurn":interestBNBBurn,
            "recvWindow":recvWindow
        }
        BNB_burn_on_spot_trade_and_margin_interest = self.send_signed_request_variableParams("POST",endpoint,params)
        return BNB_burn_on_spot_trade_and_margin_interest
    
    def get_BNB_burn_status(self,recvWindow=None):
        """
        Query BNB Burn status

        https://binance-docs.github.io/apidocs/spot/en/#get-bnb-burn-status-user_data
        """
        endpoint = "/sapi/v1/bnbBurn"
        params = {
            "recvWindow":recvWindow
        }
        get_BNB_burn_status = self.send_signed_request_variableParams("GET",endpoint,params)
        return get_BNB_burn_status
    
    def query_margin_interest_rate_history(self,asset,vipLevel=None,startTime=None,endTime=None,recvWindow=None):
        """
        Query margin interest rate history

        https://binance-docs.github.io/apidocs/spot/en/#query-margin-interest-rate-history-user_data
        """
        endpoint = "/sapi/v1/margin/interestRateHistory"
        params = {
            "asset":asset,
            "vipLevel":vipLevel,
            "startTime":self.time_ts(startTime),
            "endTime":self.time_ts(endTime),
            "recvWindow":recvWindow
        }
        query_margin_interest_rate_history = self.send_signed_request_variableParams("GET",endpoint,params)
        return query_margin_interest_rate_history
    
    def query_cross_margin_fee_data(self,vipLevel=None,coin=None,recvWindow=None):
        """
        Get cross margin fee data collection with any vip level or user's current specific data as https://www.binance.com/en/margin-fee

        https://binance-docs.github.io/apidocs/spot/en/#query-cross-margin-fee-data-user_data
        """
        endpoint = "/sapi/v1/margin/crossMarginData"
        params = {
            "vipLevel":vipLevel,
            "coin":coin,
            "recvWindow":recvWindow
        }
        query_cross_margin_fee_data = self.send_signed_request_variableParams("GET",endpoint,params)
        return query_cross_margin_fee_data
    

    def query_isolated_margin_fee_data(self,vipLevel=None,symbol=None,recvWindow=None):
        """
        Get isolated margin fee data collection with any vip level or user's current specific data as https://www.binance.com/en/margin-fee

        https://binance-docs.github.io/apidocs/spot/en/#query-isolated-margin-fee-data-user_data
        """
        endpoint = "/sapi/v1/margin/isolatedMarginData"
        params = {
            "vipLevel":vipLevel,
            "symbol":symbol,
            "recvWindow":recvWindow
        }
        query_isolated_margin_fee_data = self.send_signed_request_variableParams("GET",endpoint,params)
        return query_isolated_margin_fee_data
    
    def query_isolated_margin_tier_data(self,symbol,tier=None,recvWindow=None):
        """
        Get isolated margin tier data collection with any tier as https://www.binance.com/en/margin-data

        https://binance-docs.github.io/apidocs/spot/en/#query-isolated-margin-tier-data-user_data
        """
        endpoint= "/sapi/v1/margin/isolatedMarginTier"
        params = {
            "symbol":symbol,
            'tier':tier,
            'recvWindow':recvWindow
        }
        query_isolated_margin_tier_data = self.send_signed_request_variableParams("GET",endpoint,params)
        return query_isolated_margin_tier_data
    
    def query_current_margin_order_count_usage(self,isIsolated=None,symbol=None,recvWindow=None):
        """
        Displays the user's current margin order count usage for all intervals.

        https://binance-docs.github.io/apidocs/spot/en/#query-current-margin-order-count-usage-trade
        """
        endpoint = "/sapi/v1/margin/rateLimit/order"
        params = {
            "isIsolated":isIsolated,
            "symbol":symbol,
            "recvWindow":recvWindow
        }
        query_current_margin_order_count_usage = self.send_signed_request_variableParams("GET",endpoint,params)
        return query_current_margin_order_count_usage
    
    def margin_dustlog(self,startTime=None,endTime=None,recvWindow=None):
        """
        Query the historical information of user's margin account small-value asset conversion BNB. 

        https://binance-docs.github.io/apidocs/spot/en/#margin-dustlog-user_data
        """
        endpoint = "/sapi/v1/margin/dribblet"
        params = {
            "startTime":self.time_ts(startTime),
            "endTime":self.time_ts(endTime),
            "recvWindow":recvWindow
        }
        margin_dustlog = self.send_signed_request_variableParams("GET",endpoint,params)
        return margin_dustlog
    

    def cross_margin_collateral_ratio(self):
        """
        Check margin collateral ratio 
        """
        endpoint = "/sapi/v1/margin/crossMarginCollateralRatio"
        cross_margin_collateral_ratio = self.send_public_request('GET',endpoint)
        return cross_margin_collateral_ratio
    
    def get_small_liability_exchange_coin_list(self,recvWindow=None):
        """
        Query the coins which can be small liability exchange

        https://binance-docs.github.io/apidocs/spot/en/#get-small-liability-exchange-coin-list-user_data
        """
        endpoint = "/sapi/v1/margin/exchange-small-liability"
        params = {
            'recvWinow':recvWindow
        }
        get_small_liability_exchange_coin_list = self.send_signed_request_variableParams('GET',endpoint,params)
        return get_small_liability_exchange_coin_list
    
    def small_liability_exchange(self,assetNames,recvWindow=None):
        """
        Cross Margin Small Liability Exchange

        https://binance-docs.github.io/apidocs/spot/en/#small-liability-exchange-margin
        """
        endpoint = "/sapi/v1/margin/exchange-small-liability"
        params = {
            "assetNames":assetNames,
            'recvWinow':recvWindow
        }
        small_liability_exchange = self.send_signed_request_variableParams('POST',endpoint,params)
        return small_liability_exchange
    
    def get_small_liability_exchange_history(self,current,size,startTime=None,endTime=None,recvWindow=None):
        """
        Get Small liability Exchange History

        https://binance-docs.github.io/apidocs/spot/en/#get-small-liability-exchange-history-user_data
        """
        endpoint = "/sapi/v1/margin/exchange-small-liability-history"
        params = {
            "current":current,
            "size":size,
            "startTime":self.time_ts(startTime),
            "endTime":self.time_ts(endTime),
            'recvWindow':recvWindow
        }
        get_small_liability_exchange_history = self.send_signed_request_variableParams('GET',endpoint,params)
        return get_small_liability_exchange_history
    
    def get_future_hourly_interest_rate(self,assets,isIsolated=bool):
        """
        Get the next hourly estimate interest

        https://binance-docs.github.io/apidocs/spot/en/#get-a-future-hourly-interest-rate-user_data
        """
        endpoint = "/sapi/v1/margin/next-hourly-interest-rate"
        params = {
            'assets':assets,
            "isIsolated":isIsolated
        }
        get_future_hourly_interest_rate = self.send_signed_request_variableParams('GET',endpoint,params)
        return get_future_hourly_interest_rate
    

    """
    User Data Streams
    """
    def create_listen_key_spot(self):
        endpoint = "/api/v3/userDataStream"
        create_listen_key_spot = self.send_public_request('POST',endpoint)
        return create_listen_key_spot
    
    def update_listen_key_spot(self,listenKey):
        endpoint = "/api/v3/userDataStream"
        params = {"listenKey":listenKey}
        update_listen_key_spot = self.send_public_request('PUT',endpoint,payload=params)
        return update_listen_key_spot
    
    def delete_listen_key_spot(self,listenKey):
        endpoint = "/api/v3/userDataStream"
        params = {"listenKey":listenKey}
        delete_listen_key_spot = self.send_public_request('DELETE',endpoint,payload=params)
        return delete_listen_key_spot
    
    def create_listen_key_cross_margin(self):
        endpoint = "/sapi/v1/userDataStream"
        create_listen_key_margin = self.send_public_request('POST',endpoint)
        return create_listen_key_margin
    
    def update_listen_key_cross_margin(self,listenKey):
        endpoint = "/sapi/v1/userDataStream"
        params = {"listenKey":listenKey}
        update_listen_key_cross_margin = self.send_public_request('PUT',endpoint,payload=params)
        return update_listen_key_cross_margin
    
    def delete_listen_key_cross_margin(self,listenKey):
        endpoint = "/sapi/v1/userDataStream"
        params = {"listenKey":listenKey}
        delete_listen_key_cross_margin = self.send_public_request('DELETE',endpoint,payload=params)
        return delete_listen_key_cross_margin
    
    def create_listen_key_isolated_margin(self,symbol):
        endpoint = "/sapi/v1/userDataStream/isolated"
        params = {'symbol':symbol}
        create_listen_key_isolated_margin = self.send_public_request('POST',endpoint,payload=params)
        return create_listen_key_isolated_margin
    
    def update_listen_key_isolated_margin(self,symbol,listenKey):
        endpoint = "/sapi/v1/userDataStream/isolated"
        params = {'symbol':symbol,"listenKey":listenKey}
        create_listen_key_isolated_margin = self.send_public_request('PUT',endpoint,payload=params)
        return create_listen_key_isolated_margin
    
    def delete_listen_key_isolated_margin(self,symbol,listenKey):
        endpoint = "/sapi/v1/userDataStream/isolated"
        params = {'symbol':symbol,"listenKey":listenKey}
        create_listen_key_isolated_margin = self.send_public_request('DELETE',endpoint,payload=params)
        return create_listen_key_isolated_margin
    
    """
    Simple Earn Endpoints
    """
    def get_simple_earn_flexible_product_list(self,asset=None,current=None,size=None,recvWindow=None):
        """
        Get available Simple Earn flexible product list
        https://binance-docs.github.io/apidocs/spot/en/#simple-earn-endpoints
        """
        endpoint = "/sapi/v1/simple-earn/flexible/list"
        params = {
            'asset':asset,
            "current":current,
            "size":size,
            "recvWindow":recvWindow
        }
        get_simple_earn_flexible_product_list = self.send_signed_request_variableParams("GET",endpoint,params)
        return get_simple_earn_flexible_product_list
    
    def get_simple_earn_locked_product_list(self,asset=None,current=None,size=None,recvWindow=None):
        """
        Get simple earning locked product lists. 

        https://binance-docs.github.io/apidocs/spot/en/#get-simple-earn-locked-product-list-user_data
        """
        endpoint = "/sapi/v1/simple-earn/locked/list"
        params = {
            'asset':asset,
            'current':current,
            'size':size,
            'recvWindow':recvWindow
        }
        get_simple_earn_locked_product_list = self.send_signed_request_variableParams("GET",endpoint,params)
        return get_simple_earn_locked_product_list

    def subscribe_flexible_product(self,productId,amount,autoSubscribe=None,channelId=None,recvWindow=None):
        """
        Subscribe flexible simple earn product 

        autoSubscribe (bool): Whether auto subscribe the product when its due. 

        https://binance-docs.github.io/apidocs/spot/en/#subscribe-flexible-product-trade
        """
        endpoint  = "/sapi/v1/simple-earn/flexible/subscribe"
        params = {
            "productId":productId,
            "amount":amount,
            "autoSubscribe":autoSubscribe,
            "channelId":channelId,
            "recvWindow":recvWindow
        }
        subscribe_flexible_product = self.send_signed_request_variableParams("POST",endpoint,params)
        return subscribe_flexible_product
    
    def subscribe_locked_product(self,projectId,amount,autoSubscribe=None,channelId=None,recvWindow=None):
        """
        Purchase locked saving product 

        autoSubscribe (bool): Whether auto subscribe the product when its due. 

        https://binance-docs.github.io/apidocs/spot/en/#subscribe-locked-product-trade
        """
        endpoint  = "/sapi/v1/simple-earn/locked/subscribe"
        params = {
            "projectId":projectId,
            "amount":amount,
            "autoSubscribe":autoSubscribe,
            "channelId":channelId,
            "recvWindow":recvWindow
        }
        subscribe_locked_product = self.send_signed_request_variableParams("POST",endpoint,params)
        return subscribe_locked_product
    
    def redeem_felxible_product(self,productId,redeemAll=None,amount=None,channelId=None,recvWindow=None):
        """
        Redeem a purchased flexible saving product.

        redeemAll (bool) 

        amount (float): if redeemAll is false, amount is mandatory

        https://binance-docs.github.io/apidocs/spot/en/#redeem-flexible-product-user_data
        """
        endpoint = "/sapi/v1/simple-earn/flexible/redeem"
        params = {
            'productId':productId,
            'redeemAll':redeemAll,
            "amount":amount,
            "channelId":channelId,
            "recvWindow":recvWindow
        }
        redeem_felxible_product = self.send_signed_request_variableParams("POST",endpoint,params)
        return redeem_felxible_product
    
    def redeem_locked_product(self,positionId,channelId=None,recvWindow=None):
        """
        Redeem a purchased locked saving product.

        https://binance-docs.github.io/apidocs/spot/en/#redeem-flexible-product-user_data
        """
        endpoint = "/sapi/v1/simple-earn/locked/redeem"
        params = {
            'positionId':positionId,
            'channelId':channelId,
            "recvWindow":recvWindow
        }
        redeem_locked_product = self.send_signed_request_variableParams("POST",endpoint,params)
        return redeem_locked_product
    
    def get_flexible_product_position(self,asset=None,productId=None,current=None,size=None,recvWindow=None):
        """
        Get flexible product position

        https://binance-docs.github.io/apidocs/spot/en/#get-flexible-product-position-user_data
        """
        endpoint = "/sapi/v1/simple-earn/flexible/position"
        params = {
            'asset':asset,
            "productId":productId,
            "current":current,
            "size":size,
            "recvWindow":recvWindow
        }
        get_flexible_product_position = self.send_signed_request_variableParams("GET",endpoint,params)
        return get_flexible_product_position
    
    def get_locked_product_position(self,asset=None,productId=None,projectId=None,current=None,size=None,recvWindow=None):
        """
        Get locked product position

        https://binance-docs.github.io/apidocs/spot/en/#get-flexible-product-position-user_data
        """
        endpoint = "/sapi/v1/simple-earn/locked/position"
        params = {
            'asset':asset,
            "productId":productId,
            "current":current,
            "size":size,
            "projectId":projectId,
            "recvWindow":recvWindow
        }
        get_locked_product_position = self.send_signed_request_variableParams("GET",endpoint,params)
        return get_locked_product_position
    
    def simple_account(self,recvWindow=None):
        """
        Get simple account balance.

        https://binance-docs.github.io/apidocs/spot/en/#simple-account-user_data
        """
        endpoint = "/sapi/v1/simple-earn/account"
        params = {
            "recvWindow":recvWindow
        }
        simple_account = self.send_signed_request_variableParams("GET",endpoint,params)
        return simple_account


    def get_flexible_subscription_record(self,productId=None,purchaseId=None,asset=None,startTime=None,endTime=None,current=None,size=None,recvWindow=None):
        """
        Get flxible subscription record.

        https://binance-docs.github.io/apidocs/spot/en/#get-flexible-subscription-record-user_data
        """
        endpoint = "/sapi/v1/simple-earn/flexible/history/subscriptionRecord"
        params = {
            "productId":productId,
            "purchaseId":purchaseId,
            "asset":asset,
            "startTime":self.time_ts(startTime),
            "endTime":self.time_ts(endTime),
            "current":current,
            "size":size,
            "recvWindow":recvWindow
        }
        get_flexible_subscription_record = self.send_signed_request_variableParams("GET",endpoint,params)
        return get_flexible_subscription_record
    
    def get_locked_subscription_record(self,purchaseId=None,asset=None,startTime=None,endTime=None,current=None,size=None,recvWindow=None):
        """
        Get locked subscription record.

        https://binance-docs.github.io/apidocs/spot/en/#get-flexible-subscription-record-user_data
        """
        endpoint = "/sapi/v1/simple-earn/locked/history/subscriptionRecord"
        params = {
            "purchaseId":purchaseId,
            "asset":asset,
            "startTime":self.time_ts(startTime),
            "endTime":self.time_ts(endTime),
            "current":current,
            "size":size,
            "recvWindow":recvWindow
        }
        get_locked_subscription_record = self.send_signed_request_variableParams("GET",endpoint,params)
        return get_locked_subscription_record
    
    def get_flexible_redemption_record(self,productId=None,redeemId=None,asset=None,startTime=None,endTime=None,current=None,size=None,recvWindow=None):
        """
        Get flexible redemption record

        https://binance-docs.github.io/apidocs/spot/en/#get-flexible-redemption-record-user_data
        """
        endpoint = "/sapi/v1/simple-earn/flexible/history/redemptionRecord"
        params = {
            "productId":productId,
            "redeemId":redeemId,
            "asset":asset,
            "startTime":self.time_ts(startTime),
            "endTime":self.time_ts(endTime),
            "current":current,
            "size":size,
            "recvWindow":recvWindow,

        }
        get_flexible_redemption_record = self.send_signed_request_variableParams("GET",endpoint,params)
        return get_flexible_redemption_record
    
    def get_locked_redemption_record(self,positionId=None,redeemId=None,asset=None,startTime=None,endTime=None,current=None,size=None,recvWindow=None):
        """
        Get flexible redemption record

        https://binance-docs.github.io/apidocs/spot/en/#get-locked-redemption-record-user_data
        """
        endpoint = "/sapi/v1/simple-earn/locked/history/redemptionRecord"
        params = {
            "positionId":positionId,
            "redeemId":redeemId,
            "asset":asset,
            "startTime":self.time_ts(startTime),
            "endTime":self.time_ts(endTime),
            "current":current,
            "size":size,
            "recvWindow":recvWindow,

        }
        get_locked_redemption_record = self.send_signed_request_variableParams("GET",endpoint,params)
        return get_locked_redemption_record
    
    def get_flexible_rewards_history(self,type,productId=None,asset=None,startTime=None,endTime=None,recvWindow=None):
        """
        Get flexible rewards history.

        type (ENUM) : "BONUS", "REALTIME", "REWARDS"

        https://binance-docs.github.io/apidocs/spot/en/#get-flexible-rewards-history-user_data
        """
        endpoint = "/sapi/v1/simple-earn/flexible/history/rewardsRecord"
        params = {
            "type":type,
            "productId":productId,
            "asset":asset,
            "startTime":self.time_ts(startTime),
            "endTime":self.time_ts(endTime),
            "recvWindow": recvWindow
        }
        get_flexible_rewards_history = self.send_signed_request_variableParams("GET",endpoint,params)
        return get_flexible_rewards_history
    
    def get_locked_rewards_history(self,positionId=None,asset=None,startTime=None,endTime=None,current= None,size=None,recvWindow=None):
        """
        Get locked rewards history.

        type (ENUM) : "BONUS", "REALTIME", "REWARDS"

        https://binance-docs.github.io/apidocs/spot/en/#get-locked-rewards-history-user_data
        """
        endpoint = "/sapi/v1/simple-earn/locked/history/rewardsRecord"
        params = {
            "positionId":positionId,
            "asset":asset,
            "startTime":self.time_ts(startTime),
            "endTime":self.time_ts(endTime),
            "current":current,
            "size":size,
            "recvWindow": recvWindow
        }
        get_locked_rewards_history = self.send_signed_request_variableParams("GET",endpoint,params)
        return get_locked_rewards_history
    
    def set_flexible_auto_subscribe(self,productId,autoSubscribe,recvWindow=None):
        """
        set flexible auto subscribe 

        autoSubscribe (bool): Whether to set the flexible to autoSubscribe 

        https://binance-docs.github.io/apidocs/spot/en/#set-flexible-auto-subscribe-user_data
        """
        endpoint = "/sapi/v1/simple-earn/flexible/setAutoSubscribe"
        params = {
            "productId":productId,
            "autoSubscribe":autoSubscribe,
            "recvWindow":recvWindow

        }
        set_flexible_auto_subscribe = self.send_signed_request_variableParams("POST",endpoint,params)
        return set_flexible_auto_subscribe
    
    def set_locked_auto_subscribe(self,productId,autoSubscribe,recvWindow=None):
        """
        set locked auto subscribe 

        autoSubscribe (bool): Whether to set the flexible to autoSubscribe 

        https://binance-docs.github.io/apidocs/spot/en/#set-locked-auto-subscribe-user_data
        """
        endpoint = "/sapi/v1/simple-earn/locked/setAutoSubscribe"
        params = {
            "productId":productId,
            "autoSubscribe":autoSubscribe,
            "recvWindow":recvWindow

        }
        set_locked_auto_subscribe = self.send_signed_request_variableParams("POST",endpoint,params)
        return set_locked_auto_subscribe
    
    def get_flexible_personal_left_quota(self,productId,recvWindow=None):
        """
        Get flexible personal left quota.

        https://binance-docs.github.io/apidocs/spot/en/#get-flexible-personal-left-quota-user_data
        """
        endpoint = "/sapi/v1/simple-earn/flexible/personalLeftQuota"
        params = {
            "productId":productId,
            "recvWindow":recvWindow

        }
        get_flexible_personal_left_quota = self.send_signed_request_variableParams("GET",endpoint,params)
        return get_flexible_personal_left_quota
    
    def get_locked_personal_left_quota(self,productId,recvWindow=None):
        """
        Get locked personal left quota.

        https://binance-docs.github.io/apidocs/spot/en/#get-locked-personal-left-quota-user_data
        """
        endpoint = "/sapi/v1/simple-earn/locked/personalLeftQuota"
        params = {
            "productId":productId,
            "recvWindow":recvWindow

        }
        get_locked_personal_left_quota = self.send_signed_request_variableParams("GET",endpoint,params)
        return get_locked_personal_left_quota
    
    def get_flexible_subscription_preview(self,productId,amount,recvWindow=None):
        """
        Get flexible subscription preview.

        https://binance-docs.github.io/apidocs/spot/en/#get-flexible-subscription-preview-user_data
        """
        endpoint = "/sapi/v1/simple-earn/flexible/subscriptionPreview"
        params = {
            "productId":productId,
            "amount":amount,
            "recvWindow":recvWindow

        }
        get_flexible_subscription_preview = self.send_signed_request_variableParams("GET",endpoint,params)
        return get_flexible_subscription_preview
    
    def get_locked_subscription_preview(self,productId,amount,autoSubscribe=None,recvWindow=None):
        """
        Get flexible subscription preview.

        https://binance-docs.github.io/apidocs/spot/en/#get-flexible-subscription-preview-user_data
        """
        endpoint = "/sapi/v1/simple-earn/locked/subscriptionPreview"
        params = {
            "productId":productId,
            "amount":amount,
            "autoSubscribe":autoSubscribe,
            "recvWindow":recvWindow

        }
        get_locked_subscription_preview = self.send_signed_request_variableParams("GET",endpoint,params)
        return get_locked_subscription_preview
    
    def get_rate_history(self,productId,startTime=None,endTime=None,current=None,size=None,recvWindow=None):
        """
        Get rate history.

        https://binance-docs.github.io/apidocs/spot/en/#get-rate-history-user_data
        """
        endpoint = "/sapi/v1/simple-earn/flexible/history/rateHistory"
        params = {
            "productId":productId,
            "startTime":self.time_ts(startTime),
            "endTime":self.time_ts(endTime),

            "current":current,
            "size":size,
            "recvWindow":recvWindow

        }
        get_rate_history = self.send_signed_request_variableParams("GET",endpoint,params)
        return get_rate_history
    
    def get_collateral_record(self,productId=None,startTime=None,endTime=None,current=None,size=None,recvWindow=None):
        """
        Get Collateral Record.

        https://binance-docs.github.io/apidocs/spot/en/#get-collateral-record-user_data
        """
        endpoint = "/sapi/v1/simple-earn/flexible/history/collateralRecord"
        params = {
            "productId":productId,
            "startTime":self.time_ts(startTime),
            "endTime":self.time_ts(endTime),

            "current":current,
            "size":size,
            "recvWindow":recvWindow

        }
        get_collateral_record = self.send_signed_request_variableParams("GET",endpoint,params)
        return get_collateral_record

    """
    ETH Staking endpoint
    """

    def subscribe_ETH_staking(self,amount,recvWindow=None):
        """
        Subscribe ETH staking 

        amount (float): amount in ETH, limit 4 decimals 

        https://binance-docs.github.io/apidocs/spot/en/#subscribe-eth-staking-trade

        UI path : https://www.binance.com/en/eth2
        """
        endpoint = "/sapi/v1/eth-staking/eth/stake"
        params = {
            "amount":amount,
            "recvWindow":recvWindow
        }
        subscribe_ETH_staking = self.send_signed_request_variableParams("POST",endpoint,params)
        return subscribe_ETH_staking
    
    def redeem_ETH(self,amount,recvwindow=None):
        """
        Redeem ETH 

        amount (float): amount in BETH, limit 8 decimals 

        https://binance-docs.github.io/apidocs/spot/en/#redeem-eth-trade

        UI path: https://www.binance.com/en/eth2
        """
        endpoint = "/sapi/v1/eth-staking/eth/stake"
        params = {
            "amount":amount,
            "recvWindow":recvwindow
        }
        subscribe_ETH_staking = self.send_signed_request_variableParams("POST",endpoint,params)
        return subscribe_ETH_staking
    
    def get_ETH_staking_history(self,startTime=None,endTime=None,current=None,size=None,recvWindow=None):
        """
        Get ETH staking history

        https://binance-docs.github.io/apidocs/spot/en/#get-eth-staking-history-user_data

        UI: https://www.binance.com/en/my/earn/history/staking
        """
        endpoint = "/sapi/v1/eth-staking/eth/history/stakingHistory"
        params = {
            "startTime":self.time_ts(startTime),
            "endTime":self.time_ts(endTime),
            "current":current,
            "size":size,
            "recvWindow":recvWindow
        }
        get_ETH_staking_history = self.send_signed_request_variableParams("GET",endpoint,params)
        return get_ETH_staking_history

    def get_ETH_redemption_history(self,startTime=None,endTime=None,current=None,size=None,recvWindow=None):
        """
        Get ETH redemption history

        https://binance-docs.github.io/apidocs/spot/en/#get-eth-redemption-history-user_data

        UI:  https://www.binance.com/en/my/earn/history/staking
        """
        endpoint = "/sapi/v1/eth-staking/eth/history/redemptionHistory"
        params = {
            "startTime":self.time_ts(startTime),
            "endTime":self.time_ts(endTime),
            "current":current,
            "size":size,
            "recvWindow":recvWindow
        }
        get_ETH_redemption_history = self.send_signed_request_variableParams("GET",endpoint,params)
        return get_ETH_redemption_history
    
    def get_ETH_rewards_distribution_history(self,startTime=None,endTime=None,current=None,size=None,recvWindow=None):
        """
        Get ETH rewards districution history

        https://binance-docs.github.io/apidocs/spot/en/#get-eth-rewards-distribution-history-user_data

        UI: https://www.binance.com/en/my/earn/history/staking
        """
        endpoint = "/sapi/v1/eth-staking/eth/history/rewardsHistory"
        params = {
            "startTime":self.time_ts(startTime),
            "endTime":self.time_ts(endTime),
            "current":current,
            "size":size,
            "recvWindow":recvWindow
        }
        get_ETH_rewards_distribution_history = self.send_signed_request_variableParams("GET",endpoint,params)
        return get_ETH_rewards_distribution_history
    
    def get_current_ETH_staking_quota(self,recvWindow=None):
        """
        Get current ETH staking quota

        https://binance-docs.github.io/apidocs/spot/en/#get-current-eth-staking-quota-user_data
        """
        endpoint = "/sapi/v1/eth-staking/eth/quota"
        params = {
            "recvWindow":recvWindow
        }
        get_current_ETH_staking_quota = self.send_signed_request_variableParams("GET",endpoint,params)
        return get_current_ETH_staking_quota
    
    def get_BETH_rate_history(self,startTime=None,endTime=None,current=None,size=None,recvWindow=None):
        """
        Get BETH Rate History

        https://binance-docs.github.io/apidocs/spot/en/#get-beth-rate-history-user_data
        """
        endpoint = "/sapi/v1/eth-staking/eth/history/rateHistory"
        params = {
            "startTime":self.time_ts(startTime),
            "endTime":self.time_ts(endTime),
            "current":current,
            "size":size,
            "recvWindow":recvWindow
        }
        get_BETH_rate_history = self.send_signed_request_variableParams("GET",endpoint,params)
        return get_BETH_rate_history
    
    def ETH_staking_account(self,recvWindow=None):
        """
        Query ETH staking account 

        https://binance-docs.github.io/apidocs/spot/en/#eth-staking-account-user_data
        """
        endpoint = "/sapi/v1/eth-staking/account"
        params = {
            "recvWindow":recvWindow
        }
        ETH_staking_account = self.send_signed_request_variableParams("GET",endpoint,params)
        return ETH_staking_account
    
    def Wrap_BETH(self,amount,recvWindow=None):
        """
        Wrap BETH 

        https://binance-docs.github.io/apidocs/spot/en/#wrap-beth-trade

        UI: https://www.binance.com/en/wbeth 
        """
        endpoint = "/sapi/v1/eth-staking/wbeth/wrap"
        params = {
            "amount":amount,
            "recvWindow":recvWindow
        }
        Wrap_BETH = self.send_signed_request_variableParams("POST",endpoint,params)
        return Wrap_BETH
    
    def Unwrap_WBETH(self,amount,recvWindow=None):
        """
        Unwrap WBETH
        
        https://binance-docs.github.io/apidocs/spot/en/#unwrap-wbeth-trade
        """
        endpoint = "/sapi/v1/eth-staking/wbeth/unwrap"
        params = {
            "amount":amount,
            "recvWindow":recvWindow
        }
        Unwrap_WBETH = self.send_signed_request_variableParams("POST",endpoint,params)
        return Unwrap_WBETH
    
    def get_WBETH_wrap_history(self,startTime=None,endTime=None,current=None,size=None,recvWindow=None):
        """
        Get WBETH wrap history 

        https://binance-docs.github.io/apidocs/spot/en/#get-wbeth-wrap-history-user_data
        """
        endpoint = "/sapi/v1/eth-staking/wbeth/history/wrapHistory"
        params = {
            "startTime":self.time_ts(startTime),
            "endTime":self.time_ts(endTime),
            "current":current,
            "size":size,
            "recvWindow":recvWindow
        }
        get_WBETH_wrap_history = self.send_signed_request_variableParams("GET",endpoint,params)
        return get_WBETH_wrap_history
    
    def get_WBETH_unwrap_history(self,startTime=None,endTime=None,current=None,size=None,recvWindow=None):
        """
        Get WBETH wrap history 

        https://binance-docs.github.io/apidocs/spot/en/#get-wbeth-unwrap-history-user_data
        """
        endpoint = "/sapi/v1/eth-staking/wbeth/history/unwrapHistory"
        params = {
            "startTime":self.time_ts(startTime),
            "endTime":self.time_ts(endTime),
            "current":current,
            "size":size,
            "recvWindow":recvWindow
        }
        get_WBETH_unwrap_history = self.send_signed_request_variableParams("GET",endpoint,params)
        return get_WBETH_unwrap_history


    
    "========================================================================================"

    """
    Staking Endpoints 
    https://www.binance.com/en/simple-earn
    """
    def get_staking_product_list(self,product,asset=None,current=None,size=None,recvWindow=None):
        """
        Get staking products list 
        Staking includes fixed term saving, DEFI felxible and DEFI locked 

        product:  	"STAKING" for Locked Staking, "F_DEFI" for flexible DeFi Staking, "L_DEFI" for locked DeFi Staking
        """
        endpoint = "/sapi/v1/staking/productList"
        params = {
            "product":product,
            "asset":asset,
            "current":current,
            'size':size,
            "recvWindow":recvWindow
        }
        get_staking_product_list = self.send_signed_request_variableParams("GET",endpoint,params)
        return get_staking_product_list
    
    def purchase_staking_product(self,product,productId,amount,renewable=None,recvWindow=None):
        """
        Purchaase staking product 
        product:  	"STAKING" for Locked Staking, "F_DEFI" for flexible DeFi Staking, "L_DEFI" for locked DeFi Staking
        productId can be get from get_staking_product_list()

        https://binance-docs.github.io/apidocs/spot/en/#purchase-staking-product-user_data
        """
        endpoint = "/sapi/v1/staking/purchase"
        params = {
            "product":product,
            "productId":productId,
            "amount":amount,
            "renewable":renewable,
            "recvWindow":recvWindow
        }
        purchase_staking_product = self.send_signed_request_variableParams("POST",endpoint,params)
        return purchase_staking_product
    
    def redeem_staking_product(self,product,productId,positionId=None,amount=None,recvWindow=None):
        """
        Redeem Staking product. Locked staking and Locked DeFI staking belong to early redemption, redeeming in advance will result in loss of interest that you have earned.
        """
        endpoint = "/sapi/v1/staking/redeem"
        params = {
            "product":product,
            "productId":productId,
            "positionId":positionId,
            "amount":amount,
            "recvWindow":recvWindow
        }
        redeem_staking_product = self.send_signed_request_variableParams("POST",endpoint,params)
        return redeem_staking_product
    
    def get_staking_product_position(self,product,productId=None,asset=None,current=None,size=None,recvWindow=None):
        """
        Query staking products positions

        https://binance-docs.github.io/apidocs/spot/en/#get-staking-product-position-user_data
        """
        endpoint = "/sapi/v1/staking/position"
        params = {
            "product":product,
            "productId":productId,
            "asset":asset,
            "current":current,
            "size":size,
            "recvWindow":recvWindow

        }

        get_staking_product_position = self.send_signed_request_variableParams("GET",endpoint,params)
        return get_staking_product_position
    
    def get_staking_history(self,product,txnType,asset=None,startTime=None,endTime=None,current=None,size=None,recvWindow=None):
        """
        Get staking history

        product: "STAKING" for Locked Staking, "F_DEFI" for flexible DeFi Staking, "L_DEFI" for locked DeFi Staking
        txnType:  "SUBSCRIPTION", "REDEMPTION", "INTEREST"

        https://binance-docs.github.io/apidocs/spot/en/#get-staking-history-user_data

        """
        endpoint = "/sapi/v1/staking/stakingRecord"
        params = {
            "product":product,
            "txnType":txnType,
            "asset":asset,
            "startTime":self.time_ts(startTime),
            "endTime":self.time_ts(endTime),
            "current":current,
            "size":size,
            "recvWindow":recvWindow
        }
        get_staking_history = self.send_signed_request_variableParams("GET",endpoint,params)
        return get_staking_history
    
    def set_auto_staking(self,product,positionId,renewable,recvWindow=None):
        """
        Set auto staking on Locked Staking or Locked DeFi Staking

        product: "STAKING" for Locked Staking, "L_DEFI" for locked DeFi Staking

        renewable: Bool

        https://binance-docs.github.io/apidocs/spot/en/#set-auto-staking-user_data
        """
        endpoint = "/sapi/v1/staking/setAutoStaking"
        params = {
            "product":product,
            "positionId":positionId,
            "renewable":renewable,
            "recvWindow":recvWindow
        }
        set_auto_staking = self.send_signed_request_variableParams("POST",endpoint,params)
        return set_auto_staking
    
    def get_personal_left_quota_of_staking_product(self,product,productId,recvWindow=None):
        """
        Get personal left quota of staking product

        https://binance-docs.github.io/apidocs/spot/en/#set-auto-staking-user_data
        """
        endpoint = "/sapi/v1/staking/personalLeftQuota"
        params ={
            'product':product,
            "productId":productId,
            'recvWindow':recvWindow
        }
        get_personal_left_quota_of_staking_product = self.send_signed_request_variableParams("GET",endpoint,params)
        return get_personal_left_quota_of_staking_product

    """
    Futures endpoints 
    """
    def spot_futures_account_transfer(self,asset,amount,type,recvWindow=None):
        """
        Execute transfer between spot account and futures account.

        type: 1: transfer from spot account to USDT-Ⓜ futures account.

            2: transfer from USDT-Ⓜ futures account to spot account.

            3: transfer from spot account to COIN-Ⓜ futures account.

            4: transfer from COIN-Ⓜ futures account to spot account.

        https://binance-docs.github.io/apidocs/spot/en/#new-future-account-transfer-user_data
        """

        endpoint = "/sapi/v1/futures/transfer"
        params = {
            "asset":asset,
            "amount":amount,
            "type":type,
            "recvWindow":recvWindow
        }
        spot_futures_account_transfer = self.send_signed_request_variableParams("POST",endpoint,params)
        return spot_futures_account_transfer
    
    def get_future_account_transaction_hitory_list(self,startTime,asset=None,endTime=None,current=None,size=None,recvWindow=None):
        """
        Get futures account transaciton history list 

        https://binance-docs.github.io/apidocs/spot/en/#get-future-account-transaction-history-list-user_data
        """
        endpoint = "/sapi/v1/futures/transfer"
        params = {
            "asset":asset,
            "startTime":self.time_ts(startTime),
            "endTime":self.time_ts(endTime),
            "current":current,
            "size":size,
            "recvWindow":recvWindow
        }
        get_future_account_transaction_hitory_list = self.send_signed_request_variableParams("GET",endpoint,params)
        return get_future_account_transaction_hitory_list
    
    """
    Futures Algo Endpoints

    Volume Participation (VP): https://www.binance.com/en/support/faq/how-to-use-volume-participation-algorithm-on-binance-futures-b0b94dcc8eb64c2585763b8747b60702
    Time-Weighted Average Price (Twap): https://www.binance.com/en/support/faq/how-to-use-twap-algorithm-on-binance-futures-093927599fd54fd48857237f6ebec0b0
    """

    def VP_new_order(self,symbol,side,quantity,urgency,positionSide=None,clientAlgoId=None,reduceOnly=None,limitPrice=None,recvWindow=None):
        """
        Send in a VP new order. Only support on USDⓈ-M Contracts.

        https://binance-docs.github.io/apidocs/spot/en/#volume-participation-vp-new-order-trade
        """
        endpoint = "/sapi/v1/algo/futures/newOrderVp"
        params = {
            "symbol":symbol,
            "side":side,
            "quantity":quantity,
            "urgency":urgency,
            "positionSide":positionSide,
            "clientAlgoId":clientAlgoId,
            "reduceOnly":reduceOnly,
            "limitPrice":limitPrice,
            "recvWindow":recvWindow
        }
        VP_new_order = self.send_signed_request_variableParams("POST",endpoint,params)
        return VP_new_order
    
    """
    BLVT endpoints 

    """
    def get_BLVT_info(self,tokenName):
        """
        get Binance Leveraged Token info 
        https://binance-docs.github.io/apidocs/spot/en/#get-blvt-info-market_data
        """
        endpoint = "/sapi/v1/blvt/tokenInfo"
        params = {'tokenName':tokenName}
        get_BLVT_info = self.send_public_request("GET",endpoint,params)
        return get_BLVT_info
    
    def subscribe_BLVT(self,tokenName,cost,recvWindow=None):
        """
        Subscribe BLVT

        https://binance-docs.github.io/apidocs/spot/en/#subscribe-blvt-user_data
        """
        endpoint = "/sapi/v1/blvt/subscribe"
        params = {
            "tokenName":tokenName,
            "cost":cost,
            "recvWindow":recvWindow
        }
        subscribe_BLVT = self.send_signed_request_variableParams("POST",endpoint,params)
        return subscribe_BLVT
    
    def query_BLVT_subscription_record(self,tokenName=None,id=None,startTime=None,endTime=None,limit=None,recvWindow=None):
        """
        Query BLVT suscription record. 

        https://binance-docs.github.io/apidocs/spot/en/#query-subscription-record-user_data
        """
        endpoint ="/sapi/v1/blvt/subscribe/record"
        params = {
            "tokenName":tokenName,
            "id":id,
            "startTime":self.time_ts(startTime),
            "endTime":self.time_ts(endTime),
            "limit":limit,
            "recvWindow":recvWindow
        }
        query_BLVT_subscription_record = self.send_signed_request_variableParams("GET",endpoint,params)
        return query_BLVT_subscription_record
    
    def redeem_BLVT(self,tokenName,amount,recvWindow=None):
        """
        Redeem BLVT.

        https://binance-docs.github.io/apidocs/spot/en/#redeem-blvt-user_data
        """
        endpoint ="/sapi/v1/blvt/redeem"
        params = {
            "tokenName":tokenName,
            "amount":amount,
            "recvWindow":recvWindow
        }
        redeem_BLVT = self.send_signed_request_variableParams("POST",endpoint,params)
        return redeem_BLVT
    
    def query_redemption_record(self,tokenName=None,id=None,startTime=None,endTime=None,limit=None,recvWindow=None):
        """
        Query Redemption Record

        https://binance-docs.github.io/apidocs/spot/en/#query-redemption-record-user_data
        """
        endpoint = "/sapi/v1/blvt/redeem/record"
        params = {
            "tokenName":tokenName,
            "startTime":self.time_ts(startTime),
            "endTime":self.time_ts(endTime),
            "id":id,
            "limit":limit,
            "recvWindow":recvWindow
        }
        query_redemption_record = self.send_signed_request_variableParams("GET",endpoint,params)
        return query_redemption_record
    
    def BLVT_user_limit_info(self,tokenName=None,recvWindow=None):
        """
        Get BLVT user limit info

        https://binance-docs.github.io/apidocs/spot/en/#get-blvt-user-limit-info-user_data
        """
        endpoint = "/sapi/v1/blvt/userLimit"
        params = {
            "tokenName":tokenName,
            'recvWindow':recvWindow
        }
        BLVT_user_limit_info = self.send_signed_request_variableParams("GET",endpoint,params)
        return BLVT_user_limit_info
    
    """
    BSwap Endpoints 

    https://www.binance.com/en/swap
    """
    def list_all_Swap_pools(self):
        """
        Get metadata about all swap pools.

        https://binance-docs.github.io/apidocs/spot/en/#list-all-swap-pools-market_data
        """
        endpoint = "/sapi/v1/bswap/pools"
        return self.send_public_request('GET',endpoint)
    
    def liquidity_information_of_a_pool(self,poolId=None,recvWindow=None):
        """
        Get liquidity information and user share of a pool.

        https://binance-docs.github.io/apidocs/spot/en/#get-liquidity-information-of-a-pool-user_data
        """
        endpoint = "/sapi/v1/bswap/liquidity"
        params = {
            "poolId":poolId,
            "recvWindow":recvWindow
        }
        liquidity_information_of_a_pool = self.send_signed_request_variableParams("GET",endpoint,params)
        return liquidity_information_of_a_pool
    
    def add_liquidity(self,poolId,asset,quantity,recvWindow=None,type=None):
        """
        Regualr users 2 sec per trade. 
        VIP users can apply 0.7 sec per trade. 

        Add liquidity to a pool. 

        https://binance-docs.github.io/apidocs/spot/en/#add-liquidity-trade
        """
        endpoint = "/sapi/v1/bswap/liquidityAdd"
        params = {
            "poolId":poolId,
            "asset":asset,
            "quantity":quantity,
            "type":type,
            "recvWindow":recvWindow
        }
        liquidity_information_of_a_pool = self.send_signed_request_variableParams("POST",endpoint,params)
        return liquidity_information_of_a_pool
    
    def remove_liquidity(self,poolId,type,shareAmount,asset=None,recvWindow=None):
        """
        Remove liquidity from a pool, type include SINGLE and COMBINATION, asset is mandatory for single asset removal

        type: SINGLE for single asset removal, COMBINATION for combination of all coins removal
        asset : Mandatory for single asset removal

        https://binance-docs.github.io/apidocs/spot/en/#remove-liquidity-trade
        """
        endpoint = "/sapi/v1/bswap/liquidityRemove"
        params = {
            "poolId":poolId,
            "asset":asset,
            "shareAmount":shareAmount,
            "type":type,
            "recvWindow":recvWindow
        }

        remove_liquidity = self.send_signed_request_variableParams("POST",endpoint,params)
        return remove_liquidity
    
    """
    ==========================2023-06-19=================
    """

    def websocket_pool_price_streams(self,streams,recvWindow=60000):
        """
        Stream Name: earn_swapprice_<poolid> or earn_swapprice_all
        """
        url ="wss://api.binance.com/sapi/wss"
        random_string = str(uuid.uuid1())[:32]
        timestamp = self.get_timestamp()
        params = {
            "random": random_string,
            "topic": streams,
            "recvWindow":recvWindow,
            "timestamp":timestamp
        }
        querystring = urllib.parse.urlencode(params,safe="|")
        sign = self.hashing(querystring)
        params.update({'signature':sign})
        querystring = urllib.parse.urlencode(params,safe="|")
        url = url+"?"+querystring

        ws1 = websocket.WebSocket()
        try:
            ws1.connect(url, header={"X-MBX-APIKEY": self.api_key, "Content-Type": "application/x-www-form-urlencoded"})
            while True:
                print(json.loads(ws1.recv()))
        except Exception as e:
            print(e)

    """
    Fiat Endpoints
    """
    def get_Fiat_deposit_withdraw_history(self,transactionType,beginTime=None,endTime=None,page=None,rows=None,recvWindow=None):
        """
        Query Fiat deposit / withdraw history

        transactionType:  0 - deposit ; 1 - withdraw

        https://binance-docs.github.io/apidocs/spot/en/#get-fiat-deposit-withdraw-history-user_data
        """
        endpoint = "/sapi/v1/fiat/orders"
        params = {
            "transactionType":transactionType,
            "beginTime":self.time_ts(beginTime),
            "endTime":self.time_ts(endTime),
            "page":page,
            "rows":rows,
            "recvWindow":recvWindow
        }
        get_fiat_deposit_withdraw_history = self.send_signed_request_variableParams("GET",endpoint,params)
        return get_fiat_deposit_withdraw_history

    def get_Fiat_payments_history(self,transactionType,beginTime=None,endTime=None,page=None,rows=None,recvWindow=None):
        """
        Query Fiat payments history 

        transactionType: 0- buy ; 1- sell 

        https://binance-docs.github.io/apidocs/spot/en/#get-fiat-payments-history-user_data
        """
        endpoint = "/sapi/v1/fiat/payments"
        params = {
            "transactionType":transactionType,
            "beginTime":self.time_ts(beginTime),
            "endTime":self.time_ts(endTime),
            "page":page,
            "rows":rows,
            "recvWindow":recvWindow
        }
        get_Fiat_payments_history = self.send_signed_request_variableParams("GET",endpoint,params)
        return get_Fiat_payments_history
    
    """
    C2C Endpoints 
    """
    def get_C2C_trade_history(self,tradeType,startTimestamp=None,endTimestamp=None,page=None,rows=None,recvWindow=None):
        """
        Get C2C trade history

        tradeType: BUY / SELL

        https://binance-docs.github.io/apidocs/spot/en/#get-c2c-trade-history-user_data
        """
        endpoint = "/sapi/v1/c2c/orderMatch/listUserOrderHistory"
        params = {
            "tradeType":tradeType,
            "startTimestamp":self.time_ts(startTimestamp),
            "endTimestamp":self.time_ts(endTimestamp),
            "page":page,
            "rows":rows,
            "recvWindow":recvWindow
        }
        get_C2C_trade_history = self.send_signed_request_variableParams("GET",endpoint,params)
        return get_C2C_trade_history
    
    """
    VIP Loan Endpoints 
    """

    def VIP_loan_query_application_status(self,requestId=None,current=None,limit=None,recvWindow=None):
        """
        Query application status.

        https://binance-docs.github.io/apidocs/spot/en/#query-application-status-user_data
        """
        endpoint = "/sapi/v1/loan/vip/request/data"
        params = {
            "requestId":requestId,
            "current":current,
            "limit":limit,
            "recvWindow":recvWindow
        }
        VIP_loan_query_application_status = self.send_signed_request_variableParams("GET",endpoint,params)
        return VIP_loan_query_application_status

    def get_VIP_loan_ongoing_orders(self,orderId=None,collateralAccountId=None,loanCoin=None,collateralCoin=None,current=None,
                                    limit=None,recvWindow=None):
        """
        VIP loan is available for VIP users only
        https://binance-docs.github.io/apidocs/spot/en/#get-vip-loan-ongoing-orders-user_data
        """
        endpoint = "/sapi/v1/loan/vip/ongoing/orders"
        params = {
            'orderId':orderId,
            'collateralAccountId':collateralAccountId,
            'loanCoin':loanCoin,
            'collateralCoin':collateralCoin,
            'current':current,
            'limit':limit,
            'recvWindow':recvWindow
        }
        get_VIP_loan_ongoing_orders = self.send_signed_request_variableParams("GET",endpoint,params)
        return get_VIP_loan_ongoing_orders
    
    def VIP_loan_repay(self,orderId,amount,recvWindow=None):
        """
        Repay loan (VIP loan is available for VIP users only)

        https://binance-docs.github.io/apidocs/spot/en/#vip-loan-repay-trade
        """
        endpoint = "/sapi/v1/loan/vip/repay"
        params = {
            "orderId":orderId,
            "amount":amount,
            "recvWindow":recvWindow
        }
        VIP_loan_repay = self.send_signed_request_variableParams("POST",endpoint,params)
        return VIP_loan_repay
    
    def get_VIP_loan_repayment_history(self,orderId=None,loanCoin=None,startTime=None,endTime=None,
                                       current=None,limit=None,recvWindow=None):
        """
        Query VIP loan repayment history (VIP loan is available for VIP users only)

        https://binance-docs.github.io/apidocs/spot/en/#get-vip-loan-repayment-history-user_data
        """
        endpoint = "/sapi/v1/loan/vip/repay/history"
        params = {
            "orderId":orderId,
            "loanCoin":loanCoin,
            "startTime":self.time_ts(startTime),
            "endTime":self.time_ts(endTime),
            "current":current,
            "limit":limit,
            "recvWindow":recvWindow
        }
        get_VIP_loan_repayment_history = self.send_signed_request_variableParams("GET",endpoint,params)
        return get_VIP_loan_repayment_history

    def check_locked_value_of_VIP_collateral_account(self,orderId=None,collateralAccountId=None,recvWindow=None):
        """
        Check locked value of VIP collateral account. 

        https://binance-docs.github.io/apidocs/spot/en/#check-locked-value-of-vip-collateral-account-user_data
        """
        endpoint = "/sapi/v1/loan/vip/collateral/account"
        params = {
            "orderId":orderId,
            "collateralAccountId":collateralAccountId,
            "recvWindow":recvWindow
        }
        check_locked_value_of_VIP_collateral_account = self.send_signed_request_variableParams("GET",endpoint,params)
        return check_locked_value_of_VIP_collateral_account

    """
    Crypto Loans Endpoints

    https://www.binance.com/en/loan
    """

    def get_crypto_loans_income_history(self,asset=None,type=None,startTime=None,endTime=None,limit=None,recvWindow=None):
        """
        Query loans transaction history 

        type: By default: all types will be returned. ENUM: borrowIn, collateralSpent,repayAmount, collateralReturn(Collateral return after repayment), addCollateral, removeCollateral, collateralReturnAfterLiquidation

        https://binance-docs.github.io/apidocs/spot/en/#get-crypto-loans-income-history-user_data
        """
        endpoint = "/sapi/v1/loan/income"
        params = {
            "asset":asset,
            "type":type,
            "startTime":self.time_ts(startTime),
            "endTime":self.time_ts(endTime),
            "limit":limit,
            "recvWindow":recvWindow
        }
        get_crypto_loans_income_history = self.send_signed_request_variableParams("GET",endpoint,params)
        return get_crypto_loans_income_history
    
    def crypto_loan_borrow(self,loanCoin,collateralCoin,loanTerm,loanAmount=None,collateralAmount=None,recvWindow=None):
        """
        Apply for Crypto loan 
        loanAmount or collateralAmount must be sent in one of them.  
        LoanTerm (INT): 7/30 days
        Flexible interest rate option is not available 

        https://binance-docs.github.io/apidocs/spot/en/#borrow-crypto-loan-borrow-trade
        """
        endpoint = "/sapi/v1/loan/borrow"
        params = {
            "loanCoin":loanCoin,
            "collateralCoin":collateralCoin,
            "loanTerm":loanTerm,
            "loanAmount":loanAmount,
            "collateralAmount":collateralAmount,
            "recvWindow":recvWindow
        }
        crypto_loan_borrow = self.send_signed_request_variableParams("POST",endpoint,params)
        return crypto_loan_borrow
    
    def get_loan_borrow_history(self,orderId=None,loanCoin=None,collateralCoin=None,startTime=None,
                                endTime=None,current=None,limit=None,recvWindow=None):
        """
        Query Loan borrow History
        orderId in POST /sapi/v1/loan/borrow

        https://binance-docs.github.io/apidocs/spot/en/#borrow-get-loan-borrow-history-user_data
        """
        endpoint = "/sapi/v1/loan/borrow/history"
        params = {
            "orderId":orderId,
            "loanCoin":loanCoin,
            "collateralCoin":collateralCoin,
            "startTime":self.time_ts(startTime),
            "endTime":self.time_ts(endTime),
            "current":current,
            "limit":limit,
            "recvWindow":recvWindow
        }
        get_loan_borrow_history = self.send_signed_request_variableParams("GET",endpoint,params)
        return get_loan_borrow_history
    
    def get_loan_onging_orders(self,orderId=None,loanCoin=None,collateralCoin=None,current=None,limit=None,recvWindow=None):
        """
        Get onging loan orders. 

        https://binance-docs.github.io/apidocs/spot/en/#borrow-get-loan-ongoing-orders-user_data
        """
        endpoint = "/sapi/v1/loan/ongoing/orders"
        params = {
            "orderId":orderId,
            "loanCoin":loanCoin,
            "collateralCoin":collateralCoin,
            "current":current,
            "limit":limit,
            "recvWindow":recvWindow
        }
        get_loan_onging_orders = self.send_signed_request_variableParams("GET",endpoint,params)
        return get_loan_onging_orders
    
    def crypto_loan_repay(self,orderId,amount,type=None,collateralReturn=None,recvWindow=None):
        """
        Repay Crypto loan
        type: 1 for "repay with borrowed coin"  /  2 for "repay with collateral".   (By default: 1 )
        collateralReturn (bool): TRUE: Return extra collateral to spot account; FALSE: Keep extra collateral in the order.  (By default: True)

        https://binance-docs.github.io/apidocs/spot/en/#repay-crypto-loan-repay-trade
        """
        endpoint = "/sapi/v1/loan/repay"
        params = {
            "orderId":orderId,
            "amount":amount,
            "type":type,
            "collateralReturn":collateralReturn,
            "recvWindow":recvWindow
        }
        crypto_loan_repay = self.send_signed_request_variableParams("POST",endpoint,params)
        return crypto_loan_repay
    
    def get_loan_repayment_history(self,orderId=None,loanCoin=None,collateralCoin=None,startTime=None,
                                endTime=None,current=None,limit=None,recvWindow=None):
        """
        Query Loan repayment History
        orderId in POST /sapi/v1/loan/borrow

        https://binance-docs.github.io/apidocs/spot/en/#repay-get-loan-repayment-history-user_data
        """
        endpoint = "/sapi/v1/loan/repay/history"
        params = {
            "orderId":orderId,
            "loanCoin":loanCoin,
            "collateralCoin":collateralCoin,
            "startTime":self.time_ts(startTime),
            "endTime":self.time_ts(endTime),
            "current":current,
            "limit":limit,
            "recvWindow":recvWindow
        }
        get_loan_repayment_history = self.send_signed_request_variableParams("GET",endpoint,params)
        return get_loan_repayment_history

    def crypto_loan_adjust_LTV(self,orderId,amount,direction,recvWindow=None):
        """
        Adjust crypto loan LTV.

        direction (ENUM): "ADDITIONAL", "REDUCED"

        https://binance-docs.github.io/apidocs/spot/en/#adjust-ltv-crypto-loan-adjust-ltv-trade
        """
        endpoint = "/sapi/v1/loan/adjust/ltv"
        params = {
            "orderId":orderId,
            "amount":amount,
            "direction":direction,
            "recvWindow":recvWindow
        }
        crypto_loan_adjust_LTV = self.send_signed_request_variableParams("POST",endpoint,params)
        return crypto_loan_adjust_LTV
    
    def get_loan_LTV_adjustment_history(self,orderId=None,loanCoin=None,collateralCoin=None,startTime=None,
                                endTime=None,current=None,limit=None,recvWindow=None):
        """
        Query adjustment LTV history
        orderId in POST /sapi/v1/loan/borrow

        https://binance-docs.github.io/apidocs/spot/en/#adjust-ltv-get-loan-ltv-adjustment-history-user_data
        """
        endpoint = "/sapi/v1/loan/ltv/adjustment/history"
        params = {
            "orderId":orderId,
            "loanCoin":loanCoin,
            "collateralCoin":collateralCoin,
            "startTime":self.time_ts(startTime),
            "endTime":self.time_ts(endTime),
            "current":current,
            "limit":limit,
            "recvWindow":recvWindow
        }
        get_loan_LTV_adjustment_history = self.send_signed_request_variableParams("GET",endpoint,params)
        return get_loan_LTV_adjustment_history
    
    def get_loanable_assets_data(self,loanCoin=None,vipLevel=None,recvWindow=None):

        """
        Get interest rate and borrow limit of loanable assets. The borrow limit is shown in USD value.

        vipLevel (INT):  Default: user's vip level. Send "-1" to check specified configuration

        https://binance-docs.github.io/apidocs/spot/en/#adjust-ltv-get-loan-ltv-adjustment-history-user_data
        """
        endpoint = "/sapi/v1/loan/loanable/data"
        params ={
            "loanCoin":loanCoin,
            "vipLevel":vipLevel,
            "recvWindow":recvWindow
        }
        get_loanable_assets_data = self.send_signed_request_variableParams("GET",endpoint,params)
        return get_loanable_assets_data
    
    def get_collateral_assets_data(self,collateralCoin=None,vipLevel=None,recvWindow=None):
        """
        Get LTV information and collateral limit of collateral assets. The collateral limit is shown in USD value.

        vipLevel (INT):  Default: user's vip level. Send "-1" to check specified configuration

        https://binance-docs.github.io/apidocs/spot/en/#get-collateral-assets-data-user_data
        """
        endpoint = "/sapi/v1/loan/collateral/data"
        params ={
            "collateralCoin":collateralCoin,
            "vipLevel":vipLevel,
            "recvWindow":recvWindow
        }
        get_collateral_assets_data = self.send_signed_request_variableParams("GET",endpoint,params)
        return get_collateral_assets_data
    
    def check_collateral_repay_rate(self,loanCoin,collateralCoin,repayAmount,recvWindow=None):
        """
        Get the the rate of collateral coin / loan coin when using collateral repay, the rate will be valid within 8 second.

        repayAmount (float): repay amount of loanCoin

        https://binance-docs.github.io/apidocs/spot/en/#check-collateral-repay-rate-user_data
        """
        endpoint = "/sapi/v1/loan/repay/collateral/rate"
        params = {
            "loanCoin":loanCoin,
            "collateralCoin":collateralCoin,
            "repayAmount":repayAmount,
            "recvWindow":recvWindow
        }
        check_collateral_repay_rate = self.send_signed_request_variableParams("GET",endpoint,params)
        return check_collateral_repay_rate
    
    def crypto_loan_customize_margin_call(self,marginCall,orderId=None,collateralCoin=None,recvWindow=None):
        """
        Customize margin call for ongoing orders only.

        orderId / collateralCoin must be given one of them. 

        https://binance-docs.github.io/apidocs/spot/en/#crypto-loan-customize-margin-call-trade
        """
        endpoint = "/sapi/v1/loan/customize/margin_call"
        params = {
            "marginCall":marginCall,
            "orderId":orderId,
            "collateralCoin":collateralCoin,
            "recvWindow":recvWindow
        }
        check_collateral_repay_rate = self.send_signed_request_variableParams("POST",endpoint,params)
        return check_collateral_repay_rate
    
    """
    Pay Endpoints 
    """
    def get_pay_trade_history(self,startTime=None,endTime=None,limit=None,recvWindow=None):
        """
        Query pay trade history.

        https://binance-docs.github.io/apidocs/spot/en/#get-pay-trade-history-user_data
        """
        endpoint = "/sapi/v1/pay/transactions"
        params = {
            "startTime":self.time_ts(startTime),
            "endTime":self.time_ts(endTime),
            'limit':limit,
            "recvWindow":recvWindow
        }
        get_pay_trade_history = self.send_signed_request_variableParams("GET",endpoint,params)
        return get_pay_trade_history
    
    """
    Convert Endpoints 

    To access, users need to submit questionnaire from https://www.binance.com/en/survey/9b262810a04a4d00840e6ec1bb1425d4 
    """

    def list_all_convert_pairs(self,fromAsset=None,toAsset=None):
        """
        Query for all convertible token pairs and the tokens’ respective upper/lower limits

        fromAsset (str): EITHER OR BOTH	
        toAsset (str): EITHER OR BOTH	

        https://binance-docs.github.io/apidocs/spot/en/#list-all-convert-pairs
        """
        endpoint = "/sapi/v1/convert/exchangeInfo"
        params = {
            "fromAsset":fromAsset,
            "toAsset":toAsset
        }
        list_all_convert_pairs = self.send_public_request("GET",endpoint,params)
        return list_all_convert_pairs
    
    def query_order_quantity_precision_per_asset(self,recvWindow=None):
        """
        Query for supported asset’s precision information

        https://binance-docs.github.io/apidocs/spot/en/#query-order-quantity-precision-per-asset-user_data
        """
        endpoint ="/sapi/v1/convert/assetInfo"
        params = {'recvWindow':recvWindow}
        query_order_quantity_precision_per_asset = self.send_signed_request_variableParams("GET",endpoint,params)
        return query_order_quantity_precision_per_asset

    def send_Convert_quote_request(self,fromAsset,toAsset,fromAmount=None,toAmount=None,walletType=None,validTime=None,recvWindow=None):
        """
        Request a quote for the requested token pairs

        fromAmount and toAmount must give one

        walletType: SPOT or FUNDING. Default is SPOT

        validTime: 10s, 30s, 1m, 2m, default 10s

        https://binance-docs.github.io/apidocs/spot/en/#send-quote-request-user_data
        """
        endpoint ="/sapi/v1/convert/getQuote"
        params = {
            "fromAsset":fromAsset,
            "toAsset":toAsset,
            "fromAmount":fromAmount,
            "toAmount":toAmount,
            "walletType":walletType,
            "validTime":validTime,
            'recvWindow':recvWindow
            }
        send_Convert_quote_request = self.send_signed_request_variableParams("POST",endpoint,params)
        return send_Convert_quote_request
    
    def accept_Convert_quote(self,quoteId,recvWindow=None):
        """
        Accept the offered quote by quote ID.

        https://binance-docs.github.io/apidocs/spot/en/#accept-quote-trade
        """
        endpoint = "/sapi/v1/convert/acceptQuote"
        params = {
            "quoteId":quoteId,
            "recvWindow":recvWindow
        }
        accept_Convert_quote = self.send_signed_request_variableParams("POST",endpoint,params)
        return accept_Convert_quote
    
    def Convert_order_status(self,orderId=None,quoteId=None):
        """
        Query order status by order ID.

        orderId and quoteId must give one 

        https://binance-docs.github.io/apidocs/spot/en/#order-status-user_data
        """
        endpoint = "/sapi/v1/convert/orderStatus"
        params = {
            "orderId":orderId,
            "quoteId":quoteId
        }
        Convert_order_status = self.send_signed_request_variableParams("GET",endpoint,params)
        return Convert_order_status
    
    def get_Convert_trade_history(self,startTime,endTime,limit=None,recvWindow=None):
        """
        Query Convert trade history

        https://binance-docs.github.io/apidocs/spot/en/#get-convert-trade-history-user_data
        """
        endpoint = "/sapi/v1/convert/tradeFlow"
        params = {
            "startTime":self.time_ts(startTime),
            "endTime":self.time_ts(endTime),
            "limit":limit,
            "recvWindow":recvWindow
        }
        get_Convert_trade_history = self.send_signed_request_variableParams("GET",endpoint,params)
        return get_Convert_trade_history
    
    """
    Rebate Endpoints 
    """

    def get_spot_rebate_history_records(self,startTime=None,endTime=None,page=None,recvWindow=None):
        """
        Get spot rebate history records

        https://binance-docs.github.io/apidocs/spot/en/#get-spot-rebate-history-records-user_data
        """
        endpoint = "/sapi/v1/rebate/taxQuery"
        params = {
            "startTime":self.time_ts(startTime),
            "endTime":self.time_ts(endTime),
            "page":page,
            "recvWindow":recvWindow
        }
        get_spot_rebate_history_records = self.send_signed_request_variableParams("GET",endpoint,params)
        return get_spot_rebate_history_records
    
    """
    NFT Endpoints 
    """

    def get_NFT_transaction_history(self,orderType,startTime=None,endTime=None,limit=None,page=None,recvWindow=None):
        """
        Query NFT transaction history

        orderType :  {0: purchase order, 1: sell order, 2: royalty income, 3: primary market order, 4: mint fee}

        https://binance-docs.github.io/apidocs/spot/en/#get-nft-transaction-history-user_data
        """
        endpoint = "/sapi/v1/nft/history/transactions"
        params = {
            "orderType":orderType,
            "startTime":self.time_ts(startTime),
            "endTime":self.time_ts(endTime),
            "limit":limit,
            "page":page,
            "recvWindow":recvWindow
        }
        get_NFT_transaction_history = self.send_signed_request_variableParams("GET",endpoint,params)
        return get_NFT_transaction_history

    def get_NFT_deposit_history(self,startTime=None,endTime=None,limit=None,page=None,recvWindow=None):
        """
        Get NFT deposit history

        https://binance-docs.github.io/apidocs/spot/en/#get-nft-deposit-history-user_data
        """
        endpoint = "/sapi/v1/nft/history/deposit"
        params = {
            "startTime":self.time_ts(startTime),
            "endTime":self.time_ts(endTime),
            "limit":limit,
            "page":page,
            "recvWindow":recvWindow
        }
        get_NFT_deposit_history = self.send_signed_request_variableParams("GET",endpoint,params)
        return get_NFT_deposit_history
    
    def get_NFT_withdraw_history(self,startTime=None,endTime=None,limit=None,page=None,recvWindow=None):
        """
        Get NFT withdraw history

        https://binance-docs.github.io/apidocs/spot/en/#get-nft-withdraw-history-user_data
        """
        endpoint = "/sapi/v1/nft/history/withdraw"
        params = {
            "startTime":self.time_ts(startTime),
            "endTime":self.time_ts(endTime),
            "limit":limit,
            "page":page,
            "recvWindow":recvWindow
        }
        get_NFT_deposit_history = self.send_signed_request_variableParams("GET",endpoint,params)
        return get_NFT_deposit_history
    
    def get_NFT_asset(self,limit=None,page=None,recvWindow=None):
        """
        Query NFT asset

        https://binance-docs.github.io/apidocs/spot/en/#get-nft-asset-user_data
        """
        endpoint = "/sapi/v1/nft/user/getAsset"
        params = {
            "limit":limit,
            "page":page,
            "recvWindow":recvWindow
        }
        get_NFT_asset = self.send_signed_request_variableParams("GET",endpoint,params)
        return get_NFT_asset
    
    """
    Binancne Gift Card Endpoints 

    Binance Gift Card allows simple crypto transfer and exchange through secured and prepaid codes. Binance Gift Card API solution is to facilitate instant creation, redemption and value-checking for Binance Gift Card. Binance Gift Card product feature consists of two parts: “Gift Card Number” and “Binance Gift Card Redemption Code”. The Gift Card Number can be circulated in public, and it is used to verify the validity of the Binance Gift Card; Binance Gift Card Redemption Code should be kept confidential, because as long as someone knows the redemption code, that person can redeem it anytime

    """

    def crate_a_signle_token_gift_card(self,token,amount,recvWindow=None):
        """
        This API is for creating a Binance Gift Card.

        You have a Binance account
        You have passed kyc
        You have a sufﬁcient balance in your Binance funding wallet
        You need Enable Withdrawals for the API Key which requests this endpoint.

        Daily creation volume: 2 BTC / 24H / account
        Daily creation quantity: 200 Gift Cards / 24H / account

        https://binance-docs.github.io/apidocs/spot/en/#create-a-single-token-gift-card-user_data
        
        """
        endpoint = "/sapi/v1/giftcard/createCode"
        params = {
            "token":token,
            "amount":amount,
            "recvWindow":recvWindow
        }
        crate_a_signle_token_gift_card = self.send_signed_request_variableParams("POST",endpoint,params)
        return crate_a_signle_token_gift_card
    
    def create_a_dual_token_gift_card(self,baseToken,faceToken,baseTokenAmount,discount=None,recvWindow=None):
        """
        This API is for creating a dual-token ( stablecoin-denominated) Binance Gift Card. You may create a gift card using USDT, BUSD or any supported fiat currency as baseToken, that is redeemable to another designated token (faceToken). For example, you can create a fixed-value BTC gift card and pay with 100 USDT. This gift card can keep the value fixed at 100 USDT before redemption, and will be redeemable to BTC equivalent to 100 USDT upon redemption.
        Once successfully created, the amount of baseToken (e.g. USDT) in the fixed-value gift card would be deducted from your funding wallet.
        On top of the dual-token gift card, the discount option allows you to create Binance Gift Cards at a discount within the designated discount limit. Discounted Binance Gift Cards are only available to selected partners. To apply, please reach out to the GIft Card team via giftcard@binance.com.
        
        baseToken : The token you want to pay, example: BUSD
        faceToken : The token you want to buy, example: BNB. If faceToken = baseToken, it's the same as createCode endpoint.
        baseTokenAmount:  The base token asset quantity, example : 1.002
        discount:  Stablecoin-denominated card discount percentage, Example: 1 for 1% discount. Scale should be less than 6.


        https://binance-docs.github.io/apidocs/spot/en/#create-a-dual-token-gift-card-fixed-value-discount-feature-trade
        """
        endpoint = "/sapi/v1/giftcard/buyCode"
        params = {
            "baseToken":baseToken,
            "faceToken":faceToken,
            "baseTokenAmount":baseTokenAmount,
            "discount":discount,
            "recvWindow":recvWindow

        }
        create_a_dual_token_gift_card = self.send_signed_request_variableParams("POST",endpoint,params)
        return create_a_dual_token_gift_card

    def redeem_a_Binance_gift_card(self,code,extenalUid=None,recvWindow=None):
        """
        This API is for redeeming a Binance Gift Card. 

        Once redeemed, the coins will be deposited in your funding wallet. 

        Please note that if you enter the wrong redemption code 5 times within 24 hours, you will no longer be able to redeem any Binance Gift Cards that day

        https://binance-docs.github.io/apidocs/spot/en/#redeem-a-binance-gift-card-user_data
        """
        endpoint = "/sapi/v1/giftcard/redeemCode"
        params = {
            "code":code,
            "extenalUid":extenalUid,
            "recvWindow":recvWindow
        }
        redeem_a_Binance_gift_card = self.send_signed_request_variableParams("POST",endpoint,params)
        return redeem_a_Binance_gift_card
    
    def verify_Binance_gift_card_by_Gift_Card_number(self,referenceNo,recvWindow=None):
        """
        This API is for verifying whether the Binance Gift Card is valid or not by entering Gift Card Number.

        Please note that if you enter the wrong Gift Card Number 5 times within an hour, you will no longer be able to verify any Gift Card Number for that hour.
        """

        endpoint = "/sapi/v1/giftcard/verify"
        params = {
            "referenceNo":referenceNo,
            "recvWindow":recvWindow
        }
        verify_Binance_gift_card_by_Gift_Card_number = self.send_signed_request_variableParams("GET",endpoint,params)
        return verify_Binance_gift_card_by_Gift_Card_number
    
    def fetch_RSA_public_key(self,recvWindow=None):
        """
        This API is for fetching the RSA Public Key. This RSA Public key will be used to encrypt the card code.
        """
        endpoint = "/sapi/v1/giftcard/cryptography/rsa-public-key"
        params = {
            "recvWindow":recvWindow
        }
        fetch_RSA_public_key = self.send_signed_request_variableParams("GET",endpoint,params)
        return fetch_RSA_public_key
    
    def fetch_token_limit(self,baseToken,recvWindow=None):
        """
        This API is to help you verify which tokens are available for you to create Stablecoin-Denominated gift cards as mentioned in section 2 and its’ limitation.

        https://binance-docs.github.io/apidocs/spot/en/#fetch-token-limit-user_data
        """

        endpoint = "/sapi/v1/giftcard/buyCode/token-limit"
        params = {
            "baseToken":baseToken,
            "recvWindow":recvWindow
        }
        fetch_RSA_public_key = self.send_signed_request_variableParams("GET",endpoint,params)
        return fetch_RSA_public_key
    
    """
    Auto-Invest Endpoints 

    The endpoints below allow you to interact with Binance Auto-Invest.
    """
    def get_target_asset_list(self,targetAsset,size=8,current=None,recvWindow=None):
        """
        Get target asset list 

        https://binance-docs.github.io/apidocs/spot/en/#auto-invest-endpoints
        """
        endpoint = "/sapi/v1/lending/auto-invest/target-asset/list"
        params = {
            "targetAsset":targetAsset,
            "size":size,
            "current":current,
            "recvWindow":recvWindow
        }
        get_target_asset_list = self.send_signed_request_variableParams("GET",endpoint,params)
        return get_target_asset_list
    
    def get_target_asset_ROI_data(self,targetAsset,hisRoiType,recvWindow=None):
        """
        ROI return list for target asset

        hisRoiType (ENUM) :  FIVE_YEAR,THREE_YEAR,ONE_YEAR,SIX_MONTH,THREE_MONTH,SEVEN_DAY

        https://binance-docs.github.io/apidocs/spot/en/#get-target-asset-roi-data-user_data
        """
        endpoint =  "/sapi/v1/lending/auto-invest/target-asset/roi/list"
        params = {
            "targetAsset":targetAsset,
            "hisRoiType":hisRoiType,
            "recvWindow":recvWindow
        }
        get_target_asset_ROI_data = self.send_signed_request_variableParams("GET",endpoint,params)
        return get_target_asset_ROI_data
    
    def query_source_asset_list(self,usageType,targetAsset=None,indexId=None,flexibleAllowedToUse=None,recvWindow=None):
        """
        Query Source Asset to be used for investment 

        https://binance-docs.github.io/apidocs/spot/en/#query-source-asset-list-user_data
        """
        endpoint = "/sapi/v1/lending/auto-invest/source-asset/list"
        params = {
            "usageType":usageType,
            "targetAsset":targetAsset,
            "indexId":indexId,
            "flexibleAllowedToUse":flexibleAllowedToUse,
            "recvWindow":recvWindow
        }
        query_source_asset_list = self.send_signed_request_variableParams("GET",endpoint,params)
        return query_source_asset_list

    def query_all_source_asset_and_target_asset(self,recvWindow=None):
        """
        Query all source assets and target assets

        https://binance-docs.github.io/apidocs/spot/en/#query-all-source-asset-and-target-asset-user_data
        """
        endpoint = "/sapi/v1/lending/auto-invest/all/asset"
        params = {
            "recvWindow":recvWindow
        }
        query_all_source_asset_and_target_asset = self.send_signed_request_variableParams("GET",endpoint,params)
        return query_all_source_asset_and_target_asset
    
    # def sign(self,query_string):
    #     query_string = query_string
    #     return hmac.new(
    #         self.api_secret.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256
    #     ).hexdigest()
    
    def investment_plan_creation(self,sourceType,planType,subscriptionAmount,subscriptionCycle,subscriptionStartTime,sourceAsset,targetAsset=list, percentage=list,
                                      UID=None,requestId=None,IndexId=None,subscriptionStartDay=None,subscriptionStartWeekday=None,flexibleAllowedToUse=None,recvWindow=None):
        
        """
        POST an investment plan creation.

        sourceType (string): "MAIN_SITE",“TR”
        requestId  (string): if not null, must follow businessReference + unique string, e.g: TR12354859
        planType (string): “SINGLE”,”PORTFOLIO”,”INDEX”
        IndexId (int): Only for planType = INDEX , value = 1
        subscriptionAmount (float): BUSD/USDT: 2dp, Fiat:5dp, BNB/ETH/BTC: 4dp
        subscriptionCycle (ENUM): "H1", "H4", "H8","H12", "WEEKLY","DAILY","MONTHLY","BI_WEEKLY"
        subscriptionStartDay (ENUM): “1”,...”31”; Mandatory if “subscriptionCycleNumberUnit” = “MONTHLY”, Must be sent in form of UTC+0
        subscriptionStartWeekday (ENUM):  “MON”,”TUE”,”WED”,”THU”,”FRI”,”SAT”,”SUN”; Mandatory if “subscriptionCycleNumberUnit” = “WEEKLY” or “BI_WEEKLY”, Must be sent in form of UTC+0
        subscriptionStartTime (int): “0,1,2,3,4,5,6,7,8,..23”;Must be sent in form of UTC+0
        sourceAsset (string): eg: USDT
        flexibleAllowedToUse (bool):  True use flexible wallet
        targetAsset (list):  investment target asset 
        percentage (list):  target asset invested by percentage. 

        https://binance-docs.github.io/apidocs/spot/en/#investment-plan-creation-user_data
        
        """
        
        endpoint = "/sapi/v1/lending/auto-invest/plan/add"
        temp_list = []
        for i in range(len(targetAsset)):
            temp_list.append(i)

        length = len(temp_list)
        portfolio = list(zip(targetAsset, percentage))
        params = {
            "sourceType": sourceType,
            'planType': planType,
            'subscriptionAmount': subscriptionAmount,
            'subscriptionCycle': subscriptionCycle,
            'subscriptionStartTime': subscriptionStartTime,
            'sourceAsset': sourceAsset,
            'UID': UID,
            'requestId': requestId,
            'IndexId': IndexId,
            'subscriptionStartDay': subscriptionStartDay,
            'subscriptionStartWeekday': subscriptionStartWeekday,
            'flexibleAllowedToUse': flexibleAllowedToUse,
            "recvWindow":recvWindow
        }
        for i in range(length):
            temp_dict = {f"details[{i}].targetAsset": portfolio[i][0], f"details[{i}].percentage": portfolio[i][1]}
            params.update(temp_dict)
            

        query_string = urlencode({k:v for k,v in params.items() if v is not None},safe="[]=")
        request_params = query_string +f"&timestamp={self.get_timestamp()}"
        request_params = request_params + "&signature=" + self.hashing(request_params)
        url = self.base_url + endpoint
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            'X-MBX-APIKEY': self.api_key
            }

        resp = requests.post(url, headers=headers,data=request_params)

        if self.request_url and self.show_headers == False:
            return {"resp_url": resp.url,"response":resp.json()}
        elif self.show_headers and self.request_url == False:
            return {"response_headers": resp.headers,"response":resp.json()}
        elif self.request_url==False and self.show_headers == False:
            return resp.json()
        elif self.request_url and self.show_headers:
            return {'resp_url':resp.url,"response_headers":resp.headers,'response':resp.json()}


    def investment_plan_adjustment(self,planId,subscriptionAmount,subscriptionCycle,subscriptionStartTime,sourceAsset,planType,
                                   targetAsset=list,percentage=list,subscriptionStartDay=None,subscriptionStartWeekday=None,flexibleAllowedToUse=None,recvWindow=None):
        
        """
        Query Source Asset to be used for investment

        planId (LONG): Plan identifier 
        subscriptionAmount (DECIMAL): BUSD/USDT: 2dp, Fiat:5dp, BNB/ETH/BTC: 4dp
        subscriptionCycle (ENUM): "H1", "H4", "H8","H12", "WEEKLY","DAILY","MONTHLY","BI_WEEKLY"
        subscriptionStartDay (ENUM):  “1”,...”31”;Mandatory if “subscriptionCycleNumberUnit” = “MONTHLY”,Must be sent in form of UTC+0
        subscriptionStartWeekday (ENUM): “MON”,”TUE”,”WED”,”THU”,”FRI”,”SAT”,”SUN”;Mandatory if “subscriptionCycleNumberUnit” = “WEEKLY” or “BI_WEEKLY”, Must be sent in form of UTC+0
        subscriptionStartTime (INT):  “0,1, 2,3,4,5,6,7,8,..23”; Must be sent in form of UTC+0
        flexibleAllowedToUse (bool) :  true/false；true:use flexible wallet
        targetAsset (list):  investment target asset 
        percentage (list):  target asset invested by percentage.


        when in request parameter ,just like this details[0].targetAsset=BTC details[0].percentage=60 details[1].targetAsset=ETH details[1].percentage=40 | | recvWindow | LONG | NO | no more than 60000 | | timestamp | LONG | YES |

        https://binance-docs.github.io/apidocs/spot/en/#investment-plan-adjustment-trade
        
        """
        endpoint = "/sapi/v1/lending/auto-invest/plan/edit"
        temp_list = []
        for i in range(len(targetAsset)):
            temp_list.append(i)

        length = len(temp_list)
        portfolio = list(zip(targetAsset, percentage))
        params = {
            "planId":planId,
            "subscriptionAmount":subscriptionAmount,
            "subscriptionCycle":subscriptionCycle,
            "subscriptionStartTime":subscriptionStartTime,
            "planType":planType,
            "sourceAsset":sourceAsset,
            "subscriptionStartDay":subscriptionStartDay,
            "subscriptionStartWeekday":subscriptionStartWeekday,
            "flexibleAllowedToUse":flexibleAllowedToUse,
            "recvWindow":recvWindow
            }
        for i in range(length):
            temp_dict = {f"details[{i}].targetAsset": portfolio[i][0], f"details[{i}].percentage": portfolio[i][1]}
            params.update(temp_dict)
        query_string = urlencode({k:v for k,v in params.items() if v is not None},safe="[]=")
        request_params = query_string +f"&timestamp={self.get_timestamp()}"
        request_params = request_params + "&signature=" + self.hashing(request_params)
        url = self.base_url + endpoint
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            'X-MBX-APIKEY': self.api_key
            }

        resp = requests.post(url, headers=headers,data=request_params)

        if self.request_url and self.show_headers == False:
            return {"resp_url": resp.url,"response":resp.json()}
        elif self.show_headers and self.request_url == False:
            return {"response_headers": resp.headers,"response":resp.json()}
        elif self.request_url==False and self.show_headers == False:
            return resp.json()
        elif self.request_url and self.show_headers:
            return {'resp_url':resp.url,"response_headers":resp.headers,'response':resp.json()}
    
    def change_plan_status(self,planId,status,recvWindow=None):
        """
        Change plan status 

        https://binance-docs.github.io/apidocs/spot/en/#change-plan-status-trade
        """
        endpoint = "/sapi/v1/lending/auto-invest/plan/edit-status"
        params = {
            "planId":planId,
            "status":status,
            "recvWindow":recvWindow
        }
        change_plan_status = self.send_signed_request_variableParams("POST",endpoint,params)
        return change_plan_status
    
    def get_list_of_plans(self,planType,recvWindow=None):
        """
        Query plan lists.

        https://binance-docs.github.io/apidocs/spot/en/#get-list-of-plans-user_data
        """
        endpoint = "/sapi/v1/lending/auto-invest/plan/list"
        params = {
            "planType":planType,
            "recvWindow":recvWindow
        }
        get_list_of_plans = self.send_signed_request_variableParams("GET",endpoint,params)
        return get_list_of_plans
    
    def query_holding_details_of_the_plan(self,planId=None,requestId=None,recvWindow=None):
        '''
        Query holding details of the plan

        https://binance-docs.github.io/apidocs/spot/en/#query-holding-details-of-the-plan-user_data
        '''
        endpoint = "/sapi/v1/lending/auto-invest/plan/id"
        params = {
            "planId":planId,
            "requestId":requestId,
            "recvWindow":recvWindow
        }
        query_holding_details_of_the_plan = self.send_signed_request_variableParams("GET",endpoint,params)
        return query_holding_details_of_the_plan
    
    def query_subscription_transaction_history(self,planId=None,startTime=None,endTime=None,targetAsset=None,
                                               planType=None,size=None,current=None,recvWindow=None):
        
        """
        Query subscription transaction history of a plan

        https://binance-docs.github.io/apidocs/spot/en/#query-subscription-transaction-history-user_data
        """
        endpoint = "/sapi/v1/lending/auto-invest/plan/id"
        params = {
            "planId":planId,
            "startTime":self.time_ts(startTime),
            "endTime": self.time_ts(endTime),
            "targetAsset": targetAsset,
            "planType": planType,
            "size": size,
            "current": current,
            "recvWindow": recvWindow,

        }
        query_subscription_transaction_history = self.send_signed_request_variableParams("GET",endpoint,params)
        return query_subscription_transaction_history
    
    """
    Broker Link API
    """
    def broker_create_sub_account(self,tag=None,recvWindow=None):
        """
        Create a sub account 

        https://binance-docs.github.io/Brokerage-API/Brokerage_Operation_Endpoints/#create-a-sub-account
        """
        endpoint = "/sapi/v1/broker/subAccount"
        params = {
            "tag":tag,
            "recvWindow":recvWindow
        }
        broker_create_sub_account = self.send_signed_request_variableParams("POST",endpoint,params)
        return broker_create_sub_account
    
    def broker_enable_margin_for_sub_account(self,subAccountId,margin,recvWindow=None):
        """
        enable margin trading for broker sub_account. 

        https://binance-docs.github.io/Brokerage-API/Brokerage_Operation_Endpoints/#enable-margin-for-sub-account

        """
        endpoint = "/sapi/v1/broker/subAccount/margin"
        params = {
            "subAccountId":subAccountId,
            "margin":margin,
            "recvWindow":recvWindow
        }
        broker_enable_margin_for_sub_account = self.send_signed_request_variableParams("POST",endpoint,params)
        return broker_enable_margin_for_sub_account
    
    def broker_enable_futures_for_sub_account(self,subAccountId,futures,recvWindow=None):
        """
        enable futures trading for broker sub_account. 

        https://binance-docs.github.io/Brokerage-API/Brokerage_Operation_Endpoints/#enable-futures-for-sub-account

        """
        endpoint = "/sapi/v1/broker/subAccount/futures"
        params = {
            "subAccountId":subAccountId,
            "futures":futures,
            "recvWindow":recvWindow
        }
        broker_enable_margin_for_sub_account = self.send_signed_request_variableParams("POST",endpoint,params)
        return broker_enable_margin_for_sub_account
    
    def broker_create_api_key_for_sub_account(self,subAccountId,canTrade,marginTrade=None,futuresTrade=None,recvWindow=None):
        """
        Create Api Key for Broker Sub Account
        canTrade (bool) : spot trade (Mandatory)
        marginTrade (bool): margin trade (Optional)
        futuresTrade (bool): futures trade (Optional)

        https://binance-docs.github.io/Brokerage-API/Brokerage_Operation_Endpoints/#create-api-key-for-sub-account
        """
        endpoint = "/sapi/v1/broker/subAccountApi"
        params = {
            "subAccountId":subAccountId,
            "canTrade":canTrade,
            "marginTrade":marginTrade,
            "futuresTrade":futuresTrade,
            "recvWindow":recvWindow
        }
        broker_create_api_key_for_sub_account = self.send_signed_request_variableParams("POST",endpoint,params)
        return broker_create_api_key_for_sub_account
    
    def broker_delete_api_key_for_sub_account(self,subAccountId,subAccountApiKey,recvWindow=None):
        """
        Delete Api Key for Broker Sub Account

        https://binance-docs.github.io/Brokerage-API/Brokerage_Operation_Endpoints/#delete-sub-account-api-key
        """
        endpoint = "/sapi/v1/broker/subAccountApi"
        params = {
            "subAccountId":subAccountId,
            "subAccountApiKey":subAccountApiKey,
            "recvWindow":recvWindow
        }
        broker_delete_api_key_for_sub_account = self.send_signed_request_variableParams("DELETE",endpoint,params)
        return broker_delete_api_key_for_sub_account
    
    def broker_query_sub_account_api_key(self,subAccountId,subAccountApiKey,page=None,size=None,recvWindow=None):
        """
        Query broker sub account API key

        https://binance-docs.github.io/Brokerage-API/Brokerage_Operation_Endpoints/#query-sub-account-api-key
        """
        endpoint = "/sapi/v1/broker/subAccountApi"
        params = {
            "subAccountId":subAccountId,
            "subAccountApiKey":subAccountApiKey,
            "page":page,
            "size":size,
            "recvWindow":recvWindow
        }
        broker_query_sub_account_api_key = self.send_signed_request_variableParams("GET",endpoint,params)
        return broker_query_sub_account_api_key
    

    def broker_change_sub_account_api_permission(self,subAccountId,subAccountApiKey,canTrade,marginTrade,futuresTrade,recvWindow=None):
        '''
        Change Broker Sub Account Api Permission

        https://binance-docs.github.io/Brokerage-API/Brokerage_Operation_Endpoints/#change-sub-account-api-permission
        '''
        endpoint = "/sapi/v1/broker/subAccountApi/permission"
        params = {
            "subAccountId":subAccountId,
            "subAccountApiKey":subAccountApiKey,
            "canTrade":canTrade,
            "marginTrade":marginTrade,
            "futuresTrade":futuresTrade,
            "recvWindow":recvWindow
        }
        broker_change_sub_account_api_permission = self.send_signed_request_variableParams("POST",endpoint,params)
        return broker_change_sub_account_api_permission

    def broker_query_sub_account(self,subAccountId=None,page=None,size=None,recvWindow=None):
        """
        Query Broker sub accounts 

        https://binance-docs.github.io/Brokerage-API/Brokerage_Operation_Endpoints/#query-sub-account
        """
        endpoint = "/sapi/v1/broker/subAccount"
        params = {
            "subAccountId":subAccountId,
            "page":page,
            "size":size,
            'recvWindow':recvWindow
        }
        broker_query_sub_account = self.send_signed_request_variableParams("GET",endpoint,params)
        return broker_query_sub_account
    
    def broker_account_information(self,recvwindow=None):
        """
        Broker Account Information

        https://binance-docs.github.io/Brokerage-API/Brokerage_Operation_Endpoints/#broker-account-information
        """
        endpoint = "/sapi/v1/broker/info"
        params = {
            "recvWindow":recvwindow
        }
        broker_account_information = self.send_signed_request_variableParams("GET",endpoint,params)
        return broker_account_information




    '''
    Websocket Market
    '''
    def websocket_market(self,streams):
        url = self.websocket_url +streams
        ws = self.websocket_connect(url)
        return ws 
