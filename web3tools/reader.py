"""https://web3py.readthedocs.io/en/stable/"""
from typing import Union, Dict, Tuple, Any

from eth_typing import URI
from web3.contract import Contract
from web3.types import (
    BlockData,
    TxReceipt,
    Nonce,
    TxData,
    BlockNumber,
    Wei,
    Address,
    ChecksumAddress,
    HexStr,
    TxParams,
    EventData,
)

from .utils import Utils


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

    def get_params(
        self,
        sender: Union[Address, ChecksumAddress, str],
        max_price: Wei = None,
        nonce: int = None,
        value: int = 0,
    ) -> TxParams:
        return {
            "from": self.to_checksum(sender),
            "chainId": self.web3.eth.chainId,
            "gasPrice": self.get_gas_price(max_price=max_price),
            "nonce": self.get_nonce(sender) if not nonce else nonce,
            "value": value,
        }

    def get_contract_instance(self, abi: str, address: Union[Address, str]) -> Contract:
        return self.web3.eth.contract(address=self.to_checksum(address), abi=abi)

    def call_view(self, instance: Contract, function_name: str, *args: Any):
        if not args:
            return instance.functions.__dict__[function_name]().call()
        return instance.functions.__dict__[function_name](*args).call()

    def find_event_receipt(
        self, instance: Contract, event_name: str, txid: Union[HexStr, str]
    ) -> Tuple[EventData]:
        return instance.events.__dict__[event_name]().processReceipt(
            self.get_receipt(txid)
        )

    def find_events(
        self,
        instance: Contract,
        event_name: str,
        from_block: int = 0,
        to_block: int = "latest",
        filters: Dict = None,
    ) -> Tuple[EventData]:
        return instance.events.__dict__[event_name].getLogs(
            fromBlock=from_block, toBlock=to_block, argument_filters=filters
        )
