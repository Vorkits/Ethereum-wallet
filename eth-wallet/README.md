# eth-wallet 
```
Run eth_wallets.py
```

## Installation
1. Clone this repository  
2. Optionally set virtual environment  
3. Navigate to the project's root dir and run `pip3 install .`   
 
## Usage



### Create wallet
Create new wallet:
```
$ curl -X POST -H"Content-Type: application/json" -d'{
  "password": "password"
}' "http://127.0.0.1:5000/new-wallet"

"{\"Account address:\": \"0xf85148e43E82a6C850A0dEaA02BDbf01A41e8110\", 
\"Account pub key:\": \"0xe5adac4287917f1de76b0da640c162d96437c79fbe9e3334b2c9bb8e21258ce26ca094ed22fb7420ab2efea59750408bd0f28ae6f14bf39056ac95b8b4c289ef\", 
\"Keystore path:\": \"C:\\\\Users\\\\\Д\а\н\и\л/.eth-wallet/keystore\", 
\"Remember these words to restore eth-wallet:\": \"enact amount arctic slam muffin regular word devote dutch afford opinion cheap\"}"
```
![Alt text](doc/imgs/postman-new-wallet.png?raw=true "Create new wallets!")

Show wallet:
```
$curl http://127.0.0.1:5000/get-wallet


[
    "Address: 0xf85148e43E82a6C850A0dEaA02BDbf01A41e8110",
    "Pub_key: 0xe5adac4287917f1de76b0da640c162d96437c79fbe9e3334b2c9bb8e21258ce26ca094ed22fb7420ab2efea59750408bd0f28ae6f14bf39056ac95b8b4c289ef"
]
```
![Alt text](doc/imgs/postman-get-wallet.png?raw=true "Get wallet!")

### Balances
Get ETH wallet balance:
```
$ curl -X POST -H"Content-Type: application/json" -d'{
  "token": null
  }' "http://127.0.0.1:5000/get-balance"


[
    "Balance: 0 ETH",
    "Address: 0xf85148e43E82a6C850A0dEaA02BDbf01A41e8110"
]
```
![Alt text](doc/imgs/postman-get-balance.png?raw=true "Wallet's get balance!")

### Transactions
Send ether to another wallet
```
$ curl -X POST -H"Content-Type: application/json" -d'{
  "to": address(0x5586f0B3585d25a46242A08Bc9D8e7ce56F7b0cE),
  "value": num(2),
  "password": password(12354768),
  "token": null
  }'

```
![Alt text](doc/imgs/postman-transactions.png?raw=true "Wallet's send transaction!")

### Wallet utils

Reveal wallet master private key:
```
$ curl -X POST -H"Content-Type: application/json" -d'{
  "password": "12354768"
  }'  
  
"{\"Account prv key\": \"0xfe550e37c68a8f43b9eed9cd7d9da665c1f5a9bc88358120213a1ed919cfa6ec\"}"
``` 
![Alt text](doc/imgs/postman-secretkey.png?raw=true "Wallet's Secret key!")  

