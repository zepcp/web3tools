"""https://web3py.readthedocs.io/en/stable/"""
from enum import Enum


class Providers(Enum):
    GANACHE_CLI = "http://localhost:8545"
    GETH = "https://{}:8545"
    INFURA_MAINNET = "https://mainnet.infura.io/v3/{}"
    INFURA_ROPSTEN = "https://ropsten.infura.io/v3/{}"
    ALCHEMY_MUMBAI = "https://polygon-mumbai.g.alchemy.com/v2/{}"
    ALCHEMY_POLYGON = "https://polygon-mainnet.g.alchemy.com/v2/{}"
    GENERIC_HTTPS = "https://{}:{}"
    GENERIC_HTTP = "http://{}:{}"
