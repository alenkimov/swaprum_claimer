from time import sleep
import asyncio

import aiohttp
from eth_account import Account
from eth_account.signers.local import LocalAccount

from swaprum_claimer.paths import PUBLIC_KEYS_TXT, PRIVATE_KEYS_TXT
from swaprum_claimer.config import DELAY
from swaprum_claimer.logger import logger
from swaprum_claimer import swaprum_api
from swaprum_claimer._web3 import w3


async def claim_reward(session: aiohttp.ClientSession, address: str, user_info: dict):
    claim_info = await swaprum_api.claim(session, address)
    balance_wei = int(user_info["freeClaimBalance"])
    balance = round(w3.from_wei(balance_wei, "ether"), 2)
    if "success" in claim_info:
        logger.success(f"{address} CLAIMED! Swaprum balance: {balance} ARB")
    else:
        logger.info(f"{address} Swaprum balance: {balance} ARB")


async def withdraw_reward(session: aiohttp.ClientSession, account: LocalAccount, user_info: dict):
    address = account.address
    balance_wei = int(user_info["freeClaimBalance"])
    withdrawal_info = await swaprum_api.withdrawal(session, account)
    mining_info = await swaprum_api.get_mining_info(session, address)
    rate_hour = int(mining_info["freeInfo"]["rateHour"])
    hours_to_withdrawal = int((500000000000000000 - balance_wei) / rate_hour)
    if "success" in withdrawal_info:
        logger.success(f"{address} WITHDRAWN!")
    else:
        logger.info(f"{address} Next withdrawal in {hours_to_withdrawal}h.")


def is_active_user(user_info: dict):
    prelaunch_active: dict = user_info["preLaunchActive"]
    if False in prelaunch_active.values():
        code = user_info["code"]
        address = user_info["address"]
        logger.warning(f"{address} Activate account with /active {code} here: https://t.me/swaprum_arb_bot")
        return False
    return True


async def process_account(account: LocalAccount, session: aiohttp.ClientSession):
    try:
        user_info = await swaprum_api.get_user_info(session, account.address)
        if not is_active_user(user_info):
            return
        await claim_reward(session, account.address, user_info)
        await withdraw_reward(session, account, user_info)
    except Exception as error:
        logger.error(f"{account.address}")
        logger.exception(error)


async def process_public_key(address: str, session: aiohttp.ClientSession):
    try:
        user_info = await swaprum_api.get_user_info(session, address)
        if not is_active_user(user_info):
            return
        await claim_reward(session, address, user_info)
    except Exception:
        logger.error(f"{address}")


async def async_main():
    with open(PRIVATE_KEYS_TXT, 'r') as file:
        accounts: set[LocalAccount] = {Account.from_key(key.strip()) for key in file.readlines() if key != "\n"}
    with open(PUBLIC_KEYS_TXT, 'r') as file:
        addresses: set[str] = {address.strip() for address in file.readlines() if address != "\n"}
    while True:
        async with aiohttp.ClientSession() as session:
            logger.info(f"Public_keys: {len(addresses)}")
            logger.info(f"Private_keys: {len(accounts)}")
            tasks = []
            for account in accounts:
                tasks.append(asyncio.create_task(process_account(account, session)))
            for address in addresses:
                tasks.append(asyncio.create_task(process_public_key(address, session)))
            await asyncio.gather(*tasks)
            logger.info(f"Сплю {DELAY} секунд :)")
            sleep(DELAY)


def main():
    asyncio.run(async_main())
