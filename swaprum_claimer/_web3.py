from web3 import Web3

from swaprum_claimer.config import RPC


w3 = Web3(Web3.HTTPProvider(RPC))
