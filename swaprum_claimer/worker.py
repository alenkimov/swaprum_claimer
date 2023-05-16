from time import sleep
import asyncio

from requests.exceptions import HTTPError
import aiohttp
from tqdm.asyncio import tqdm
from eth_account import Account
from eth_account.signers.local import LocalAccount

from swaprum_claimer.paths import PUBLIC_KEYS_TXT, PRIVATE_KEYS_TXT
from swaprum_claimer.config import DELAY
from swaprum_claimer.logger import logger
from swaprum_claimer import api as swaprum_api
from swaprum_claimer._web3 import w3
from swaprum_claimer.arbitrum import get_arb_balance
from swaprum_claimer.config import CHECK_WALLETS_BALANCE


# Создаю файлы, если отсутствуют
for filepath in [PRIVATE_KEYS_TXT, PUBLIC_KEYS_TXT]:
    if not filepath.exists():
        with open(filepath, "w"):
            pass


async def claim_reward(session: aiohttp.ClientSession, address: str, user_info: dict) -> float:
    claim_info = await swaprum_api.claim(session, address)
    balance_wei = int(user_info["freeClaimBalance"])
    balance = round(w3.from_wei(balance_wei, "ether"), 2)
    if "success" in claim_info:
        logger.success(f"{address} CLAIMED! Swaprum balance: {balance} ARB")
    else:
        logger.info(f"{address} Swaprum balance: {balance} ARB")
    return balance


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


async def process_account(account: LocalAccount, results, session: aiohttp.ClientSession):
    try:
        user_info = await swaprum_api.get_user_info(session, account.address)
        if not is_active_user(user_info):
            return
        swaprum_balance = await claim_reward(session, account.address, user_info)
        await withdraw_reward(session, account, user_info)
        results.append(swaprum_balance)
    except Exception:
        logger.error(f"{account.address}")


async def process_public_key(address: str, results, session: aiohttp.ClientSession):
    try:
        user_info = await swaprum_api.get_user_info(session, address)
        if not is_active_user(user_info):
            return
        swaprum_balance = await claim_reward(session, address, user_info)
        results.append(swaprum_balance)
    except Exception:
        logger.error(f"{address}")


async def work():
    while True:
        with open(PRIVATE_KEYS_TXT, 'r') as file:
            accounts: set[LocalAccount] = {Account.from_key(key.strip()) for key in file.readlines() if key != "\n"}
        with open(PUBLIC_KEYS_TXT, 'r') as file:
            addresses: set[str] = {address.strip() for address in file.readlines() if address != "\n"}
        async with aiohttp.ClientSession() as session:
            logger.info(f"Private_keys: {len(accounts)} | Public_keys: {len(addresses)}")
            tasks = []
            swaprum_balances = []
            for account in accounts:
                tasks.append(asyncio.create_task(process_account(account, swaprum_balances, session)))
            for address in addresses:
                tasks.append(asyncio.create_task(process_public_key(address, swaprum_balances, session)))
            await tqdm.gather(*tasks)

            total_swaprum_balance = 0
            for swaprum_balance in swaprum_balances:
                total_swaprum_balance += swaprum_balance
            if CHECK_WALLETS_BALANCE:
                logger.info(f"Checking wallets total balance..")
                logger.info(f"You can turn on it here: /swaprum_claimer/config.py")
                total_wallets_balance = 0
                for account in accounts:
                    try:
                        wallet_balance = round(get_arb_balance(address), 2)
                        logger.info(f"{account.address} Wallet balance: {wallet_balance} ARB")
                        total_wallets_balance += wallet_balance
                    except HTTPError as error:
                        logger.error(f"{account.address} Failed to request a wallet balance: {error.request}")
                    except Exception as error:
                        logger.error(f"{account.address} Failed to request a wallet balance")
                        logger.exception(error)
                for address in addresses:
                    try:
                        wallet_balance = round(get_arb_balance(address), 2)
                        logger.info(f"{address} Wallet balance: {wallet_balance} ARB")
                        total_wallets_balance += wallet_balance
                    except HTTPError as error:
                        logger.error(f"{account.address} Failed to request a wallet balance: {error.request}")
                    except Exception:
                        logger.error(f"{address} Failed to request a wallet balance")
                logger.info(f"Total wallets balance: {total_wallets_balance} ARB")
            logger.info(f"Total swaprum balance: {total_swaprum_balance} ARB")

            logger.info(f"Sleep {DELAY} secs :)")
            sleep(DELAY)
