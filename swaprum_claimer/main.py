from time import sleep

from eth_account import Account
from eth_account.signers.local import LocalAccount

from swaprum_claimer.paths import PUBLIC_KEYS_TXT, PRIVATE_KEYS_TXT
from swaprum_claimer.config import DELAY
from swaprum_claimer.logger import logger
from swaprum_claimer.arbitrum import get_arb_balance
from swaprum_claimer import swaprum_api
from swaprum_claimer._web3 import w3


def main():
    with open(PRIVATE_KEYS_TXT, 'r') as file:
        accounts: set[LocalAccount] = {Account.from_key(key.strip()) for key in file.readlines() if key != "\n"}
    with open(PUBLIC_KEYS_TXT, 'r') as file:
        addresses: set[str] = {address.strip() for address in file.readlines() if address != "\n"}
    while True:
        for account in accounts:
            address = account.address
            try:
                # Сбор награды
                claim_info = swaprum_api.claim(address)
                user_info = swaprum_api.get_user_info(address)
                balance_wei = int(user_info["freeClaimBalance"])
                balance = round(w3.from_wei(balance_wei, "ether"), 2)
                if "success" in claim_info:
                    logger.success(f"{address} CLAIMED! Swaprum balance: {balance} ARB")
                else:
                    logger.info(f"{address} Swaprum balance: {balance} ARB")
                # Вывод средств
                withdrawal_info = swaprum_api.withdrawal(account)
                mining_info = swaprum_api.get_mining_info(address)
                rate_hour = int(mining_info["freeInfo"]["rateHour"])
                hours_to_withdrawal = int((500000000000000000 - balance_wei) / rate_hour)
                wallet_balance = round(get_arb_balance(address), 2)
                if "success" in withdrawal_info:
                    logger.success(f"{address} WITHDRAWN!")
                else:
                    logger.info(f"{address} Wallet balance: {wallet_balance} ARB. Next withdrawal in {hours_to_withdrawal}h.")
            except Exception:
                logger.error(f"{address}")
        for address in addresses:
            try:
                # Сбор награды
                claim_info = swaprum_api.claim(address)
                user_info = swaprum_api.get_user_info(address)
                balance_wei = int(user_info["freeClaimBalance"])
                balance = round(w3.from_wei(balance_wei, "ether"), 2)
                if "success" in claim_info:
                    logger.success(f"{address} CLAIMED! Swaprum balance: {balance} ARB")
                else:
                    logger.info(f"{address} Swaprum balance: {balance} ARB")
            except Exception:
                logger.error(f"{address}")
        logger.info(f"Сплю {DELAY} секунд :)")
        sleep(DELAY)
