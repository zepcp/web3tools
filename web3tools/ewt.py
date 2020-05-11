"""https://jwt.io/"""
from base64 import b64encode, b64decode
from json import dumps, loads
from time import time
from typing import Union, Dict

from web3.types import HexStr

from .utils import Utils


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
