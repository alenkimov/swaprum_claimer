import aiohttp

from eth_account.messages import encode_defunct
from eth_account.account import LocalAccount

from swaprum_claimer._web3 import w3


async def claim(session: aiohttp.ClientSession, address: str) -> dict:
    url = "https://swaprum.finance/server/claim-free"
    querystring = {"address": address}
    response = await session.request("GET", url, params=querystring)
    data = await response.json()
    return data


async def get_user_info(session: aiohttp.ClientSession, address: str, ref=None) -> dict:
    url = "https://swaprum.finance/server/user"
    querystring = {"address": address}
    if ref is not None:
        querystring.update({"ref": ref})
    response = await session.request("GET", url, params=querystring)
    data = await response.json()
    return data


async def get_mining_info(session: aiohttp.ClientSession, address: str) -> dict:
    url = "https://swaprum.finance/server/free-token"
    querystring = {"address": address}
    response = await session.request("GET", url, params=querystring)
    data = await response.json()
    return data


async def withdrawal(session: aiohttp.ClientSession, account: LocalAccount) -> dict:
    message_text = f"{account.address[-10:]}-free-claim-balance"
    message = encode_defunct(text=message_text)
    signed_message = w3.eth.account.sign_message(message, private_key=account.key)
    url = "https://swaprum.finance/server/withdrawal"

    querystring = {"address": account.address,
                   "type": "free-claim",
                   "sig": signed_message.signature.hex()}

    response = await session.request("GET", url, params=querystring)
    data = await response.json()
    return data


async def create_account(session: aiohttp.ClientSession, ref=None) -> tuple[LocalAccount, str]:
    account: LocalAccount = w3.eth.account.create()
    user_info = await get_user_info(session, account.address, ref=ref)
    code = user_info["code"]
    await claim(session, account.address)
    return account, code
