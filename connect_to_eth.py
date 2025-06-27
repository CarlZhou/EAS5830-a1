import json
from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware
from web3.providers.rpc import HTTPProvider
from web3.middleware import geth_poa_middleware

'''
If you use one of the suggested infrastructure providers, the url will be of the form
now_url  = f"https://eth.nownodes.io/{now_token}"
alchemy_url = f"https://eth-mainnet.alchemyapi.io/v2/{alchemy_token}"
infura_url = f"https://mainnet.infura.io/v3/{infura_token}"
'''

def connect_to_eth():
	url = "https://ethereum-mainnet.core.chainstack.com/92b8d8e613baea1750dc7435f17ceea3"  # FILL THIS IN
	w3 = Web3(HTTPProvider(url))
	assert w3.is_connected(), f"Failed to connect to provider at {url}"
	return w3


def connect_with_middleware(contract_json):
    with open(contract_json, "r") as f:
        d = json.load(f)
        d = d['bsc']
        address = d['address']
        abi = d['abi']

    # First section similar to connect_to_eth but with BNB Chain (Binance Smart Chain) URL
    bnb_url = "https://bsc-testnet.drpc.org"  # FILL THIS IN with BNB provider URL
    w3 = Web3(HTTPProvider(bnb_url))
    assert w3.is_connected(), f"Failed to connect to provider at {bnb_url}"

    # Second section injecting middleware and creating contract object
    # Binance Smart Chain (BSC) uses Proof-of-Authority consensus, so middleware injection is necessary
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    contract = w3.eth.contract(address=Web3.to_checksum_address(address), abi=abi)

    return w3, contract

if __name__ == "__main__":
	connect_to_eth()
