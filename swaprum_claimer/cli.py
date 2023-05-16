import asyncio

import click

from swaprum_claimer.account_creator import create_accounts
from swaprum_claimer.worker import work


@click.group()
def cli():
    pass


@cli.command()
@click.argument('count', default=1)
@click.option('--ref', default=None, help='Ref code.')
def create(count, ref):
    asyncio.run(create_accounts(count, ref=ref))


@cli.command()
def start():
    asyncio.run(work())
