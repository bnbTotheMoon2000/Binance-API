from main import Client 
import requests
import datetime as dt

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
            self.websocket_url = "wss://stream.binance.com:9443/ws"

    def time_ts(self,time_obj):   # 2023-06-14 00:00:00
        if time_obj == None:
            return None 
        else:
            obj = dt.datetime.strptime(time_obj,"%Y-%m-%d %H:%M:%S")
            timestamp = str(int(obj.timestamp()*1000))
            return timestamp


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


    """
    ============================ 2023-06-15 =========================
    """
   
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
    
    '''
    Websocket Market
    '''
    def websocket_market(self,streams):
        url = self.websocket_url + '/'+streams
        ws = self.websocket_connect(url)
        return ws 
