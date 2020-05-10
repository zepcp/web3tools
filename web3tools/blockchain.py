"""https://web3py.readthedocs.io/en/stable/"""
from base64 import b64encode, b64decode
from enum import Enum
from json import dumps, loads
from os import PathLike
from random import choices
from string import ascii_letters, digits
from time import time
from typing import Union, Dict, Tuple, Any

from eth_account import Account, messages
from eth_typing import URI
from web3 import Web3, HTTPProvider
from web3.contract import Contract
from web3.types import BlockData, TxReceipt, Nonce, TxData, BlockNumber, Wei, \
    Address, ChecksumAddress, HexBytes, HexStr, TxParams, EventData


class Providers(Enum):
    INFURA_MAINNET = "https://mainnet.infura.io/v3/{}"
    INFURA_ROPSTEN = "https://ropsten.infura.io/v3/{}"
    GETH = "https://{}:8545"


class Utils:
    @staticmethod
    def read_file(filepath: Union[PathLike, str]) -> str:
        return open(filepath).read().strip()

    @staticmethod
    def generate_password(length: int = 16) -> str:
        return "".join(choices(ascii_letters + digits, k=length))

    @staticmethod
    def to_wei(amount: float, unit: str = "ether") -> Wei:
        return Web3.toWei(amount, unit)

    @staticmethod
    def from_wei(amount: float, unit: str = "ether") -> Wei:
        return Web3.fromWei(amount, unit)

    @staticmethod
    def to_checksum(wallet: Union[Address, str]) -> ChecksumAddress:
        return Web3.toChecksumAddress(wallet)

    @staticmethod
    def to_hex(hexbytes: HexBytes = None, hexstr: HexStr = None) -> HexStr:
        return Web3.toHex(hexstr=hexstr) if hexstr else Web3.toHex(hexbytes)

    @staticmethod
    def to_int(hexbytes: HexBytes = None, hexstr: HexStr = None) -> int:
        return Web3.toInt(hexstr=hexstr) if hexstr else Web3.toInt(hexbytes)

    @staticmethod
    def to_text(hexbytes: HexBytes = None, hexstr: HexStr = None) -> str:
        return Web3.toText(hexstr=hexstr) if hexstr else Web3.toText(hexbytes)

    @staticmethod
    def create() -> (ChecksumAddress, HexStr):
        account = Account.create()
        return account.address, Web3.toHex(account.key)

    @staticmethod
    def get_address(private_key: Union[HexStr, str]) -> ChecksumAddress:
        return Account.from_key(private_key).address

    @staticmethod
    def encrypt(private_key: Union[HexStr, str], password: str) -> Dict:
        return Account.encrypt(private_key, password)

    @staticmethod
    def decrypt(keystore: Dict, password: str) -> HexStr:
        return Web3.toHex(Account.decrypt(keystore, password))

    @staticmethod
    def sign_transaction(private_key: Union[HexStr, str],
                         transaction: TxParams) -> HexStr:
        return Web3.toHex(Account.sign_transaction(transaction, private_key
                                                   ).rawTransaction)

    @staticmethod
    def recover_transaction(signed_transaction: Union[HexStr, str]) -> str:
        return Account.recover_transaction(signed_transaction)

    @staticmethod
    def sign_message(private_key: Union[HexStr, str], message: str) -> HexStr:
        message_hash = messages.encode_defunct(text=message)
        return Web3.toHex(Account.sign_message(message_hash, private_key
                                               ).signature)

    @staticmethod
    def recover_message(signature: Union[HexStr, str], message: str) -> str:
        message_hash = messages.encode_defunct(text=message)
        return Account.recover_message(message_hash, signature=signature)

    @staticmethod
    def get_web3_provider(provider: Union[URI, str], timeout: int = 60
                          ) -> Web3:
        return Web3(HTTPProvider(provider,
                                 request_kwargs={"timeout": timeout}))


class Ewt(Utils):
    def __init__(self, expiration: int = 30) -> None:
        self.expiration = expiration
        self.url_compatible = [("+", "-"), ("/", "_")]

    def urlencode(self, value: Dict) -> str:
        encoded = b64encode(dumps(value).encode("utf8")).decode("utf-8")
        for k, v in self.url_compatible:
            encoded = encoded.replace(k, v)
        return encoded.strip("=")

    def urldecode(self, value: str) -> Dict:
        for k, v in self.url_compatible:
            value = value.replace(v, k)
        value += "==" if len(value) % 4 == 2 \
            else "=" if len(value) % 4 == 3 else ""
        return loads(b64decode(value))

    def generate(self, private_key: Union[HexStr, str]) -> str:
        """EWT sign method"""
        header = {"typ": "EWT"}
        payload = {"iss": self.get_address(private_key),
                   "exp": int(time() + self.expiration)}

        return ".".join([self.urlencode(header), self.urlencode(payload),
                         self.sign_message(private_key, dumps(payload))])

    def validate(self, token: str) -> bool:
        """EWT verify method"""
        header, payload, sig = token.split(".")
        if self.urldecode(header)["typ"] != "EWT":
            return False

        decoded = self.urldecode(payload)
        if self.recover_message(sig, decoded["iss"]) \
                and int(decoded["exp"]) > time():
            return True
        return False


class Reader(Utils):
    def __init__(self, provider: Union[URI, str], timeout: int = 60) -> None:
        self.web3 = self.get_web3_provider(provider, timeout)

    def get_current_block_number(self) -> BlockNumber:
        return self.web3.eth.blockNumber

    def get_block(self, block: Union[BlockNumber, int]) -> BlockData:
        return self.web3.eth.getBlock(block)

    def get_transaction(self, txid: Union[HexStr, str]) -> TxData:
        return self.web3.eth.getTransaction(txid)

    def get_receipt(self, txid: Union[HexStr, str]) -> TxReceipt:
        return self.web3.eth.getTransactionReceipt(txid)

    def get_balance(self, wallet: Union[Address, str]) -> Wei:
        return self.web3.eth.getBalance(self.to_checksum(wallet))

    def get_nonce(self, wallet: Union[Address, str]) -> Nonce:
        return self.web3.eth.getTransactionCount(self.to_checksum(wallet))

    def get_gas_price(self, max_price: Wei = None) -> Wei:
        if not max_price or self.web3.eth.gasPrice < max_price:
            return self.web3.eth.gasPrice
        return max_price

    def get_params(self, sender: Union[Address, ChecksumAddress, str],
                   max_price: Wei = None, nonce: int = None) -> TxParams:
        return {"from": self.to_checksum(sender),
                "chainId": self.web3.eth.chainId,
                "gasPrice": self.get_gas_price(max_price=max_price),
                "nonce": self.get_nonce(sender) if not nonce else nonce}

    def get_contract_instance(self, abi: str, address: Union[Address, str]
                              ) -> Contract:
        return self.web3.eth.contract(address=self.to_checksum(address),
                                      abi=abi)

    def call_view(self, instance: Contract, function_name: str, *args: Any):
        if not args:
            return instance.functions.__dict__[function_name]().call()
        return instance.functions.__dict__[function_name](*args).call()

    def find_event_receipt(self, instance: Contract, event_name: str,
                           txid: Union[HexStr, str]) -> Tuple[EventData]:
        return instance.events.__dict__[event_name]().processReceipt(
            self.get_receipt(txid))

    def find_events(self, instance: Contract, event_name: str,
                    from_block: int = 0, to_block: int = "latest",
                    filters: Dict = None) -> Tuple[EventData]:
        return instance.events.__dict__[event_name].getLogs(
            fromBlock=from_block, toBlock=to_block, argument_filters=filters)


class Transactor(Reader):
    def __init__(self, provider: Union[URI, str], timeout: int = 60) -> None:
        super().__init__(provider, timeout)

    def launch_transaction(self, private_key: Union[HexStr, str],
                           to: Union[Address, str], amount: Wei,
                           max_price: Wei = None, nonce: int = None) -> HexStr:
        sender = self.get_address(private_key)
        params = self.get_params(sender, max_price, nonce)
        transaction = {**params, "to": self.to_checksum(to), "value": amount}
        transaction["gas"] = self.web3.eth.estimateGas(transaction)
        return self.send_raw(private_key, transaction)

    def launch_function(self, instance: Contract,
                        private_key: Union[HexStr, str], function_name: str,
                        *args: Any, max_price: Wei = None, nonce: int = None
                        ) -> HexStr:
        sender = self.get_address(private_key)
        params = self.get_params(sender, max_price, nonce)
        transaction = instance.functions.__dict__[function_name](
            *args).buildTransaction(params)
        return self.send_raw(private_key, transaction)

    def send_raw(self, private_key: Union[HexStr, str],
                 transaction: TxParams) -> HexStr:
        raw_tx = self.sign_transaction(private_key, transaction)
        return self.to_hex(self.web3.eth.sendRawTransaction(raw_tx))
