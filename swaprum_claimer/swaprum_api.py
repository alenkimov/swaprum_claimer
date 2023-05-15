import requests
from eth_account.signers.local import LocalAccount
from eth_account.messages import encode_defunct

from swaprum_claimer._web3 import w3


def claim(address: str) -> dict:
    url = "https://swaprum.finance/server/claim-free"
    querystring = {"address": address}
    response = requests.request("GET", url, params=querystring)
    data = response.json()
    return data


def get_user_info(address: str) -> dict:
    url = "https://swaprum.finance/server/user"
    querystring = {"address": address}
    response = requests.request("GET", url, params=querystring)
    data = response.json()
    return data


def get_mining_info(address: str) -> dict:
    url = "https://swaprum.finance/server/free-token"
    querystring = {"address": address}
    response = requests.request("GET", url, params=querystring)
    data = response.json()
    return data


def withdrawal(account: LocalAccount) -> dict:
    message_text = f"{account.address[-10:]}-free-claim-balance"
    message = encode_defunct(text=message_text)
    signed_message = w3.eth.account.sign_message(message, private_key=account.key)
    url = "https://swaprum.finance/server/withdrawal"

    querystring = {"address": account.address,
                   "type": "free-claim",
                   "sig": signed_message.signature.hex()}

    response = requests.request("GET", url, params=querystring)
    data = response.json()
    return data
