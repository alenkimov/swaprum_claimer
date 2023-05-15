import asyncio

import click

from swaprum_claimer.account_creator import create_accounts
from swaprum_claimer.worker import work


@click.group()
def cli():
    pass


@cli.command()
@click.argument('count', default=1)
def create(count):
    asyncio.run(create_accounts(count))


@cli.command()
def start():
    asyncio.run(work())
