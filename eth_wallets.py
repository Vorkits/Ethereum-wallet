from eth_wallet.cli.utils_cli import (
    get_api,
)
from eth_wallet.configuration import (
    Configuration,
)
from eth_wallet.exceptions import (
    InfuraErrorException,
    ERC20NotExistsException,
    InvalidPasswordException,
    InsufficientFundsException,
    InvalidValueException,
    InsufficientERC20FundsException,
    ERC20NotExistsException
)
from web3.exceptions import (
    InvalidAddress,
)

import json

from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/new-wallet', methods=['POST'])
def new_wallet():

	configuration = Configuration().load_configuration()

	proof = request.get_json()

	requiredt = ['password']
	if not all(k in proof for k in requiredt):
		return 'Missing values', 400

	password = proof['password']

	api = get_api()
	wallet = api.new_wallet(configuration, password)
	data = {
		'Account address:': str(wallet.get_address()),
		'Account pub key:': str(wallet.get_public_key()),
		'Keystore path:': configuration.keystore_location + configuration.keystore_filename,
		'Remember these words to restore eth-wallet:': wallet.get_mnemonic()
	}
	json_result = json.dumps(data)

	return jsonify(json_result), 201

@app.route('/get-balance', methods=['POST'])
def get_balance():
	prof = request.get_json()

	configuration = Configuration().load_configuration()

	api = get_api()

	token = prof['token']
	
	try:
		errors = {
			'infuraerrorexception': 'Wallet is not connected to Ethereum network!',
			'erc20notexistsexception': 'This token is not added to the wallet!'
		}
		json_res = json.dumps(errors)
		jsonres = json.loads(json_res)
		if token is None:
			eth_balance, address = api.get_balance(configuration)
			data1 = {
				'eth_balance': 'Balance: ' + str(eth_balance) + ' ETH',
				'address': 'Address: ' + str(address),
			}
			json_result1 = json.dumps(data1)
			jsonresult = json.loads(json_result1)
			return jsonify(jsonresult['eth_balance'], jsonresult['address']), 201
		else:
			token_balance, address = api.get_balance(configuration, token)
			data1 = {
				'address': 'Address: ' + str(address),
				'token_balance': 'Balance: ' + str(token_balance)
			}
			json_result1 = json.dumps(data1)
			jsonresult = json.loads(json_result1)
			return jsonify(jsonresult['address'], jsonresult['token_balance'], token), 201
	except InfuraErrorException:
		return jsonify(jsonres['infuraerrorexception']), 500
	except ERC20NotExistsException:
		return jsonify(jsonres['erc20notexistsexception']), 500

@app.route('/get-wallet', methods=['GET'])
def get_wallet():

	configuration = Configuration().load_configuration()
	api = get_api()

	address, pub_key = api.get_wallet(configuration)
	data2 = {
		'address': 'Address: ' + str(address),
		'pub_key': 'Pub_key: ' + str(pub_key)
	}
	json_result2 = json.dumps(data2)
	jsonres2 = json.loads(json_result2)

	return jsonify(jsonres2['address'], jsonres2['pub_key']), 200

@app.route('/secretkey', methods=['POST'])
def secret_key():
	proofs = request.get_json()

	configuration = Configuration().load_configuration()

	api = get_api()
	
	try:
		requireds = ['password']

		if not all(k in proofs for k in requireds):
			return 'Missing values', 400

		password = proofs['password']

		wallet = api.get_private_key(configuration, password)
		
		secretkey = {
			'Account prv key': wallet.get_private_key().hex()
		}
		respone = json.dumps(secretkey)
		return jsonify(respone), 201
	except InvalidPasswordException:
		error = {
			'invalidpasswordexception': 'Incorrect password!'
		}
		json_error = json.dumps(error)
		return jsonify(json_error), 401

@app.route('/transactions', methods=['POST'])
def new_transaction():

	values = request.get_json()

	configuration = Configuration().load_configuration()
	api = get_api()
	erors = {
		'insufficientfundsexception': 'Insufficient ETH funds! Check balance on your address.',
		'insufficienterc20fundsexception': 'Insufficient ERC20 token funds! Check balance on your address.',
		'invalidaddress': 'Invalid recipient(to) address',
		'invalidvalueexception': 'Invalid value to send!',
		'infuraerrorexception': 'Wallet is not connected to Ethereum network!',
		'erc20notexistsexception': 'This token is not added to the wallet!',
		'invalidpasswordexception': 'Incorrect password!'
	}
	json_eror = json.dumps(erors)
	jsoneror = json.loads(json_eror)

	try:
		required = ['to', 'value', 'password', 'token']
		if not all(k in values for k in required):
			return 'Missing values', 400

		to = values['to']
		value = values['value']
		password = values['password']
		token = values['token']
		if token is None:
			tx_hash, tx_cost_eth = api.send_transaction(configuration,
														password,
														to,
														value)
		else:
			tx_hash, tx_cost_eth = api.send_transaction(configuration,
														password,
														to,
														value,
														token)
		transaction = {
			'Hash of the transaction': tx_hash.hex(),
			'Transaction cost was': str(tx_cost_eth) + 'EHT'
			}
		json_transaction = json.dumps(transaction)
		return jsonify(json_transaction), 201

	except InsufficientFundsException:
		return jsonify(jsoneror['insufficientfundsexception']), 500
	except InsufficientERC20FundsException:
		return jsonify(jsoneror['insufficienterc20fundsexception']), 500
	except InvalidAddress:
		return jsonify(jsoneror['invalidaddress']), 500
	except InvalidValueException:
		return jsonify(jsoneror['invalidvalueexception']), 500
	except InvalidPasswordException:
		return jsonify(jsoneror['invalidpasswordexception']), 500
	except InfuraErrorException:
		return jsonify(jsoneror['infuraerrorexception']), 500
	except ERC20NotExistsException:
		return jsonify(jsoneror['erc20notexistsexception']), 500
		

	

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)
