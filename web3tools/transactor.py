"""https://web3py.readthedocs.io/en/stable/"""
from typing import Union, Any

from eth_typing import URI
from web3.contract import Contract
from web3.types import Wei, Address, HexStr, TxParams

from .reader import Reader


class Transactor(Reader):
    def __init__(self, provider: Union[URI, str], timeout: int = 60) -> None:
        super().__init__(provider, timeout)

    def launch_transaction(
        self,
        private_key: Union[HexStr, str],
        to: Union[Address, str],
        value: Wei = 0,
        max_price: Wei = None,
        nonce: int = None,
    ) -> HexStr:
        sender = self.get_address(private_key)
        params = self.get_params(sender, max_price, nonce, value)
        transaction = {**params, "to": self.to_checksum(to)}
        transaction["gas"] = self.web3.eth.estimateGas(transaction)
        return self.send_raw(private_key, transaction)

    def launch_function(
        self,
        instance: Contract,
        private_key: Union[HexStr, str],
        function_name: str,
        *args: Any,
        value: Wei = 0,
        max_price: Wei = None,
        nonce: int = None
    ) -> HexStr:
        sender = self.get_address(private_key)
        params = self.get_params(sender, max_price, nonce, value)
        transaction = instance.functions.__dict__[function_name](
            *args
        ).buildTransaction(params)
        return self.send_raw(private_key, transaction)

    def send_raw(
        self, private_key: Union[HexStr, str], transaction: TxParams
    ) -> HexStr:
        raw_tx = self.sign_transaction(private_key, transaction)
        return self.to_hex(self.web3.eth.sendRawTransaction(raw_tx))
