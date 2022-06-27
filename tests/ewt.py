import unittest
from time import sleep

from web3tools import Ewt

ewt = Ewt()


class TestEwt(unittest.TestCase):
    def test_ewt(self):
        address, key = ewt.create()
        token = ewt.generate(key)
        header, payload, sig = token.split(".")
        self.assertEqual(ewt.urldecode(header), {"typ": "EWT"})
        self.assertEqual(ewt.urldecode(header), {'typ': 'EWT'})
        self.assertEqual(ewt.validate(token), True)
        sleep(1)
        self.assertEqual(ewt.validate(token), False)
