# eth-wallet 

## Installation
1. Clone this repository  
2. Optionally set virtual environment  
3. Navigate to the project's root dir and run `pip3 install .`   
 
## Usage
```
Run eth_wallets.py

```

### Create wallet
Create new wallet:
POST method
```
/new-wallet

{
    "password": "12354768"
}

"{"Account address:": "0xf85148e43E82a6C850A0dEaA02BDbf01A41e8110", 
"Account pub key:": "0xe5adac4287917f1de76b0da640c162d96437c79fbe9e3334b2c9bb8e21258ce26ca094ed22fb7420ab2efea59750408bd0f28ae6f14bf39056ac95b8b4c289ef", 
"Keystore path:": "C:\Users\Данил/.eth-wallet/keystore", 
"Remember these words to restore eth-wallet:": "enact amount arctic slam muffin regular word devote dutch afford opinion cheap"}"
```
![Alt text](eth-wallet/doc/imgs/postman-new-wallet.png?raw=true "Create new wallets!")

Show wallet:
POST method
```
/get-wallet
{
    "account_address": "0x08fA7C442f6b77973B191AA54FD5D6C6407A0D1C"
}

{
    "acc_addr": "0x08fA7C442f6b77973B191AA54FD5D6C6407A0D1C",
    "acc_balance": "0",
    "acc_balance_erc20": null
}
```

### Balances
Get ETH wallet balance:
POST method
```
/get-balance"
{
    "password": "12354768"
}

[
    "Balance: 0 ETH",
    "Address: 0xf85148e43E82a6C850A0dEaA02BDbf01A41e8110"
]
```
![Alt text](eth-wallet/doc/imgs/postman-get-balance.png?raw=true "Wallet's get balance!")

### Transactions
Send ether to another wallet
POST method
```
/transactions
{
    "from_addr": "0x08fA7C442f6b77973B191AA54FD5D6C6407A0D1C",
    "to": "0x7592320E8FB43b56d645601E3D9c358231886734",
    "value": 0,
    "password": "123457698",
    "token": null
}

```
### Wallet utils

Reveal wallet master private key:
POST method
```
/secretkey
{
    "account_address": "0x08fA7C442f6b77973B191AA54FD5D6C6407A0D1C"
    "password": "12354768"
}
  
"{\"Private key\": \"0x013db3340c6ff17b579c017499b47ceae2f6d210d0c7d858d8d20ad62cddaddf\"}"
``` 

