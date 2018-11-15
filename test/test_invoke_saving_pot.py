#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import unittest
from unittest.mock import patch

from ontology.ont_sdk import OntologySdk
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
        tx_hash = saving_pot.create_ong_pot(acct, time_limit, GAS_LIMIT, GAS_PRICE)
        time.sleep(6)
        event = ontology.rpc.get_smart_contract_event_by_tx_hash(tx_hash)
        print(event)


if __name__ == '__main__':
    unittest.main()
