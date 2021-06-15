from re import X
from typing import Collection
from xrpl.clients import JsonRpcClient
from xrpl.wallet import generate_faucet_wallet
from xrpl.models.transactions import Payment
from xrpl.utils import xrp_to_drops
from xrpl.utils import drops_to_xrp
from xrpl.transaction import safe_sign_and_autofill_transaction
from xrpl.wallet import Wallet
from xrpl.transaction import send_reliable_submission
from xrpl.models.requests.account_info import AccountInfo
import json

class XRP(object):
    client = None
    JSON_RPC_URL = "https://s.altnet.rippletest.net:51234/"  # test_net
    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            
            cls.instance = super(cls, cls).__new__(cls)
            self=cls.instance
            self.client=JsonRpcClient(self.JSON_RPC_URL)
        return cls.instance
    
    def new_wallet(self)->dict:
        
        test_wallet = generate_faucet_wallet(self.client, debug=False)
        return {'private_key':test_wallet.private_key,'classic_address':test_wallet.classic_address,'public_key':test_wallet.public_key ,\
               'sequence':test_wallet.sequence,'seed':test_wallet.seed }
    
    def payment(self,destination,sender,amount,sequence,seed)->bool:
        my_tx_payment = Payment(
                        account=sender,
                        amount=xrp_to_drops(amount),
                        destination=destination,
                        sequence=sequence,
                    )
        sign_wallet=Wallet(seed,sequence)
        my_tx_payment_signed = safe_sign_and_autofill_transaction(my_tx_payment,sign_wallet, self.client)
        tx_response = send_reliable_submission(my_tx_payment_signed, self.client)
        return True 
        
    def get_balance(self,sender):

        acct_info = AccountInfo(
            account=sender,
            ledger_index="validated",
            strict=True,
        )
        response = self.client.request(acct_info)
        result = response.result
        print("response.status: ", response.status)
        balance=drops_to_xrp(response.result['account_data']['Balance'])
        print(balance)
        return balance
        

    
    
first_wallet=(XRP().new_wallet())
XRP().get_balance(first_wallet['classic_address'])

second_wallet=(XRP().new_wallet())
XRP().payment(second_wallet['classic_address'],first_wallet['classic_address'],333,first_wallet['sequence'],first_wallet['seed'])
XRP().get_balance(first_wallet['classic_address'])
