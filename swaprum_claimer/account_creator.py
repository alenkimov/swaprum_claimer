import asyncio

import aiohttp
from tqdm.asyncio import tqdm

from swaprum_claimer.api import create_account as create_swaprum_account
from swaprum_claimer.paths import OUTPUT_DIR
from swaprum_claimer._web3 import w3
from swaprum_claimer.logger import logger


OUTPUT_DIR.mkdir(exist_ok=True)
ACCOUNTS_TXT = OUTPUT_DIR / 'accounts.txt'


async def _create_and_write(session, file):
    account, code = await create_swaprum_account(session)
    account_data = ":".join((account.address, w3.to_hex(account.key), f"/active {code}"))
    file.write(account_data)
    file.write("\n")


async def create_accounts(count):
    logger.info(f"Creating {count} accounts..")
    with open(ACCOUNTS_TXT, "w") as file:
        async with aiohttp.ClientSession() as session:
            tasks = []
            for i in range(count):
                tasks.append(asyncio.create_task(_create_and_write(session, file)))
            await tqdm.gather(*tasks)
    logger.info(f"{count} accounts >>> {ACCOUNTS_TXT}")
