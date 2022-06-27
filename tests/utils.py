import unittest

from web3 import Web3

from web3tools import Utils


utils = Utils()


class TestUtils(unittest.TestCase):
    def test_unit_conversion(self):
        self.assertEqual(utils.to_wei(1), 10**18)
        self.assertEqual(utils.from_wei(10**18), 1)
        self.assertEqual(utils.to_wei(1, "gwei"), 10**9)
        self.assertEqual(utils.from_wei(10**9, "gwei"), 1)

    def test_wallet(self):
        address, key = utils.create()
        password = utils.generate_password()
        keystore = utils.encrypt(key, password)

        self.assertTrue(Web3.isAddress(address))
        self.assertEqual(utils.to_checksum(address.lower()), address)
        self.assertEqual(utils.decrypt(keystore, password), key)

    def test_signatures(self):
        address, key = utils.create()
        transaction = {
            "from": address,
            "chainId": 3,
            "gas": 1,
            "gasPrice": 1,
            "nonce": 1,
            "to": address,
            "value": 1,
        }
        signed_transaction = utils.sign_transaction(key, transaction)
        signed_message = utils.sign_message(key, "message")

        self.assertEqual(utils.recover_transaction(signed_transaction), address)
        self.assertEqual(utils.recover_message(signed_message, "message"), address)
