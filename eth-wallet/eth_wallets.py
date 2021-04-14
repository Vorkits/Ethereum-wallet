from eth_wallet.cli.utils_cli import (
    get_api,
)
from eth_wallet.wallet import (
    Wallet
)
from eth_wallet.contract import (
    Contract,
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
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wallets.db'
db = SQLAlchemy(app)

class Walet(db.Model):
	Id = db.Column(db.Integer, primary_key=True)
	acc_addr = db.Column(db.String)
	acc_prv_key = db.Column(db.String)
	acc_pub_key = db.Column(db.String)
	rem_words = db.Column(db.String)
	acc_paswd = db.Column(db.String)
	acc_balance_eth = db.Column(db.String)
	acc_balance_erc20 = db.Column(db.String)

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
	address = str(wallet.get_address())
	eth_balance = Wallet(configuration).get_balance(address)

	data ={
		'Account address:': str(wallet.get_address()),
		'Account pub key:': str(wallet.get_public_key()),
		'Keystore path:': configuration.keystore_location + configuration.keystore_filename,
		'Remember these words to restore eth-wallet:': wallet.get_mnemonic()
	}

	json_result = json.dumps(data)
	prv_key = api.get_private_key(configuration, password)
	acc_addr = address
	acc_pub_key = str(wallet.get_public_key())
	acc_prv_key = prv_key.get_private_key().hex()
	rem_words = wallet.get_mnemonic()
	acc_balance_eth = eth_balance

	datas = Walet(acc_addr=acc_addr, acc_prv_key=acc_prv_key, acc_pub_key=acc_pub_key, rem_words=rem_words, acc_paswd=password, acc_balance_eth=acc_balance_eth)

	db.session.add(datas)
	db.session.commit()

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
				'eth_balance': 'Balance:' + str(eth_balance) + ' ETH',
				'address': 'Address:' + str(address)
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

@app.route('/get-wallet', methods=['POST'])
def get_wallet():
	profs = request.get_json()

	require = ['account_address']
	if not all(k in profs for k in require):
		return 'Missing values', 400

	acc_addr = profs['account_address']

	configuration = Configuration().load_configuration()
	api = get_api()

	db_walet = Walet.query.filter_by(acc_addr=acc_addr).first()
	db_data = {
	'acc_addr': db_walet.acc_addr,
	'acc_balance': db_walet.acc_balance_eth,
	'acc_balance_erc20': db_walet.acc_balance_erc20
	}
	json_db = json.dumps(db_data)

	return jsonify(db_data), 201


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

		db_walets = Walet.query.filter_by(acc_addr=acc_addr).first()
		proof_pwd = db_walets.acc_paswd
		if password == proof_pwd:
			db_secretkey = db_walets.acc_prv_key
			prvkey = {
				'Private key': db_secretkey
			}
			json_sekretkey = json.dumps(prvkey)
			return jsonify(json_sekretkey), 201
		else:
			return 'Incored password!'
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
		required = ['from_addr', 'to', 'value', 'password', 'token']
		if not all(k in values for k in required):
			return 'Missing values', 400

		from_addr = values['from_addr']
		to = values['to']
		value = values['value']
		password = values['password']
		token = values['token']
		if token is None:
			tx_hash, tx_cost_eth = api.send_transaction(configuration,
														password,
														from_addr,
														to,
														value)
		else:
			tx_hash, tx_cost_eth = api.send_transaction(configuration,
														password,
														from_addr,
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

@app.route('/add-token', methods=['POST'])
def add_token():
	prfs = request.get_json()

	configuration = Configuration().load_configuration()
	api = get_api()

	req = ['contract_address', 'symbol']
	if not all(k in prfs for k in req):
		return 'Missing values', 400

	contract_addr = prfs['contract_address']
	sym = prfs['symbol']
	eror = {
		'insufficientfundsexception': 'Insufficient ETH funds! Check balance on your address.',
		'insufficienterc20fundsexception': 'Insufficient ERC20 token funds! Check balance on your address.',
		'invalidaddress': 'Invalid recipient(to) address',
		'invalidvalueexception': 'Invalid value to send!',
		'infuraerrorexception': 'Wallet is not connected to Ethereum network!',
		'erc20notexistsexception': 'This token is not added to the wallet!',
		'invalidpasswordexception': 'Incorrect password!'
	}
	json_erors = json.dumps(eror)
	jsonerors = json.loads(json_erors)

	try:
		api.add_contract(configuration, sym, contract_addr)
		datax = {
			'Success': 'New coin was added! ' + str(sym) + str(contract_addr)
		}
		json_datax = json.dumps(datax)
		return jsonify(json_datax), 201
	except InvalidAddress:
		return jsonify(jsonerors['invalidaddress'])
	except InfuraErrorException:
		return jsonify(jsonerors['infuraerrorexception'])


	

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)
