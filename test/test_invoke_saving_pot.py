#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import binascii
import time
import unittest
from unittest.mock import patch

from ontology.ont_sdk import OntologySdk
from ontology.smart_contract.neo_contract.abi.abi_function import AbiFunction
from ontology.smart_contract.neo_contract.abi.abi_info import AbiInfo
from ontology.wallet.wallet_manager import WalletManager

from pot.default_settings import (
    GAS_LIMIT,
    GAS_PRICE,
    WALLET_PATH,
    CONTRACT_ABI,
    ONT_RPC_ADDRESS,
    CONTRACT_ADDRESS_HEX
)
from pot.invoke_saving_pot import InvokeSavingPot

ontology = OntologySdk()
remote_rpc_address = 'http://polaris3.ont.io:20336'
ontology.set_rpc(remote_rpc_address)
wallet_manager = WalletManager()
wallet_manager.open_wallet(WALLET_PATH)
password = input('password: ')
gas_limit = 20000000
gas_price = 500
acct = wallet_manager.get_account('AKeDu9QW6hfAhwpvCwNNwkEQt1LkUQpBpW', password)
saving_pot = InvokeSavingPot(ontology, CONTRACT_ABI, CONTRACT_ADDRESS_HEX)


class TestInvokeSavingPot(unittest.TestCase):
    def test_create_ont_pot(self):
        time_limit = 60
        tx_hash = saving_pot.create_ont_pot(acct, time_limit, GAS_LIMIT, GAS_PRICE)
        self.assertEqual(64, len(tx_hash))

    def test_create_ong_pot(self):
        time_limit = 60
        tx_hash = saving_pot.create_ong_pot(acct, time_limit, GAS_LIMIT, GAS_PRICE)
        self.assertEqual(64, len(tx_hash))
        print(tx_hash)

    def test_put_get_ont_pot_tx_hash(self):
        tx_hash = '88ba0f7d36aaaad08b9fa23bd85f202da64eb8baa2ed9204f9a89b1882a34dd8'
        saving_pot.put_ont_pot_tx_hash(acct, tx_hash, GAS_LIMIT, GAS_PRICE)
        data = saving_pot.get_ont_pot_tx_hash(acct.get_address().to_array())
        self.assertEqual(tx_hash, data)

    def test_put_get_ong_pot_tx_hash(self):
        tx_hash = '861d6ecfca6413639f753d53d1267637a410930552546443f287f43af6877181'
        saving_pot.put_ong_pot_tx_hash(acct, tx_hash, GAS_LIMIT, GAS_PRICE)
        data = saving_pot.get_ong_pot_tx_hash(acct.get_address().to_array())
        self.assertEqual(tx_hash, data)

    def test_saving_ont(self):
        amount = 1
        balance1 = ontology.rpc.get_balance(acct.get_address_base58())
        tx_hash = saving_pot.saving_ont(acct, amount, GAS_LIMIT, GAS_PRICE)
        self.assertEqual(64, len(tx_hash))
        time.sleep(6)
        print(ontology.rpc.get_smart_contract_event_by_tx_hash(tx_hash))
        balance2 = ontology.rpc.get_balance(acct.get_address_base58())
        self.assertEqual(balance1, balance2 + 1)

    def test_saving_ong(self):
        amount = 1
        print(ontology.rpc.get_balance(acct.get_address_base58()))
        tx_hash = saving_pot.saving_ong(acct, amount, GAS_LIMIT, GAS_PRICE)
        self.assertEqual(64, len(tx_hash))
        time.sleep(6)
        print(ontology.rpc.get_smart_contract_event_by_tx_hash(tx_hash))
        print(ontology.rpc.get_balance(acct.get_address_base58()))

    def test_take_ont_out(self):
        tx_hash = saving_pot.take_ong_out(acct, GAS_LIMIT, GAS_PRICE)
        print(tx_hash)

    def test_take_ong_out(self):
        tx_hash = saving_pot.take_ong_out(acct, GAS_LIMIT, GAS_PRICE)
        print(tx_hash)

    def test_query_ont_pot_saving_time(self):
        saving_time = saving_pot.query_ont_pot_saving_time(acct.get_address().to_array())
        self.assertEqual(60, saving_time)

    def test_query_ong_pot_saving_time(self):
        saving_time = saving_pot.query_ong_pot_saving_time(acct.get_address().to_array())
        self.assertEqual(60, saving_time)

    def test_query_create_pot_event(self):
        tx_hash = 'a772593b4755c0d412b824617a8cc5564ef75f20623417a6cc97cf3a727819a0'
        event = saving_pot.query_create_pot_event(tx_hash)
        self.assertIn('saving time', event)
        self.assertIn('2018-11-22 20:14:32', event)
        tx_hash = '25224b02bd5d89b4c5f4a1da322162ffc4fe0c2a1c7ab1dc3f8a0c080be63eca'
        event = saving_pot.query_create_pot_event(tx_hash)
        self.assertIn('saving time', event)
        self.assertIn('2018-11-22 20:58:30', event)


if __name__ == '__main__':
    unittest.main()
