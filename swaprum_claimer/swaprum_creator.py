from web3 import Web3
from eth_account.account import LocalAccount

from swaprum_claimer.swaprum_api import get_user_info
from swaprum_claimer.paths import OUTPUT_DIR


OUTPUT_DIR.mkdir(exist_ok=True)
ACCOUNTS_TXT = OUTPUT_DIR / 'accounts.txt'

ACCOUNTS_TO_CREATE = 100

w3 = Web3()

if __name__ == '__main__':
    with open(ACCOUNTS_TXT, "w") as file:
        for i in range(ACCOUNTS_TO_CREATE):
            account: LocalAccount = w3.eth.account.create()
            user_info = get_user_info(account.address)
            code = user_info["code"]
            account_data = ":".join((account.address, w3.to_hex(account.key), f"/active {code}"))
            file.write(account_data)
            file.write("\n")
            print(f"{i}: {account_data}")
