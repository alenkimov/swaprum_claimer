import json

from swaprum_claimer.paths import ABI_DIR
from swaprum_claimer._web3 import w3


with open(ABI_DIR / 'arb.json', 'r') as file:
    arb_abi = json.load(file)

arb_address = "0x912CE59144191C1204E64559FE8253a0e49E6548"
arb = w3.eth.contract(address=arb_address, abi=arb_abi)
decimals = arb.functions.decimals().call()
DECIMALS = 10 ** decimals


def get_arb_balance(address: str) -> float:
    raw_balance = arb.functions.balanceOf(w3.to_checksum_address(address)).call()
    return raw_balance / DECIMALS
