"""https://jwt.io/"""
from base64 import b64encode, b64decode
from json import dumps, loads
from time import time
from typing import Union, Dict, Any, Tuple, Optional
from enum import Enum

from web3.types import HexStr

from .utils import Utils


class ValidationErrors(str, Enum):
    INVALID_TYP = "INVALID_TYP"
    INVALID_ISS = "INVALID_ISS"
    INVALID_EXP = "INVALID_EXP"


class Ewt(Utils):
    url_compatible = [("+", "-"), ("/", "_")]

    def urlencode(self, value: Dict) -> str:
        encoded = b64encode(dumps(value).encode("utf8")).decode("utf-8")
        for k, v in self.url_compatible:
            encoded = encoded.replace(k, v)
        return encoded.strip("=")

    def urldecode(self, value: str) -> Dict:
        for k, v in self.url_compatible:
            value = value.replace(v, k)
        value += "==" if len(value) % 4 == 2 else "=" if len(value) % 4 == 3 else ""
        return loads(b64decode(value))

    def generate(
        self,
        private_key: Union[HexStr, str],
        duration: int = 30,
        fields: Dict[str, Any] = None,
    ) -> str:
        """EWT sign method"""
        header = {"typ": "EWT"}
        base_payload = {
            "iss": self.get_address(private_key),
            "exp": int(time() + duration),
        }
        payload = {**base_payload, **fields} if fields else base_payload

        return ".".join(
            [
                self.urlencode(header),
                self.urlencode(payload),
                self.sign_message(private_key, dumps(payload)),
            ]
        )

    def validate(self, token: str) -> Tuple[bool, Optional[ValidationErrors]]:
        """EWT verify method"""
        header, payload, sig = token.split(".")
        if self.urldecode(header).get("typ") != "EWT":
            return False, ValidationErrors.INVALID_TYP.value

        decoded_payload = self.urldecode(payload)
        issuer = self.to_checksum(decoded_payload.get("iss"))
        if self.recover_message(sig, dumps(decoded_payload)) != issuer:
            return False, ValidationErrors.INVALID_ISS.value

        if int(decoded_payload.get("exp")) < time():
            return False, ValidationErrors.INVALID_EXP.value
        return True, None
