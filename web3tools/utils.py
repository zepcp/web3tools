"""https://web3py.readthedocs.io/en/stable/"""
from os import PathLike
from random import choices
from string import ascii_letters, digits
from typing import Union, Dict, Tuple

from eth_account import Account, messages
from eth_typing import URI
from web3 import Web3, HTTPProvider
from web3.types import Wei, Address, ChecksumAddress, HexBytes, HexStr, \
    TxParams


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
    def from_wei(amount: Wei, unit: str = "ether") -> float:
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
    def create() -> Tuple[ChecksumAddress, HexStr]:
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
