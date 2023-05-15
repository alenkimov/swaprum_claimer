import asyncio

import aiohttp

from swaprum_claimer.swaprum_api import create_account
from swaprum_claimer.paths import OUTPUT_DIR
from swaprum_claimer._web3 import w3


OUTPUT_DIR.mkdir(exist_ok=True)
ACCOUNTS_TXT = OUTPUT_DIR / 'accounts.txt'

ACCOUNTS_TO_CREATE = 1000


async def _create_and_write(session, file):
    await create_account(session)
    account, code = await create_account(session)
    account_data = ":".join((account.address, w3.to_hex(account.key), f"/active {code}"))
    file.write(account_data)
    file.write("\n")
    print(f"{account_data}")


async def main():
    with open(ACCOUNTS_TXT, "w") as file:
        async with aiohttp.ClientSession() as session:
            tasks = []
            for i in range(ACCOUNTS_TO_CREATE):
                tasks.append(asyncio.create_task(_create_and_write(session, file)))
            await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(main())
