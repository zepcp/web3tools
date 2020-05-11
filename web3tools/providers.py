"""https://web3py.readthedocs.io/en/stable/"""
from enum import Enum


class Providers(Enum):
    INFURA_MAINNET = "https://mainnet.infura.io/v3/{}"
    INFURA_ROPSTEN = "https://ropsten.infura.io/v3/{}"
    GETH = "https://{}:8545"
