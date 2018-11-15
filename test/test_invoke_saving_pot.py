#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from ontology.ont_sdk import OntologySdk
from ontology.wallet.wallet_manager import WalletManager

from pot.default_settings import (
    CONTRACT_ABI,
    WALLET_PATH,
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
ont_id_acct = wallet_manager.get_account('did:ont:AHBB3LQNpqXjCLathy7vTNgmQ1cGSj8S9Z', password)
saving_pot = InvokeSavingPot(CONTRACT_ABI, CONTRACT_ADDRESS_HEX)


class TestSmartContract(unittest.TestCase):
    def test_create_ont_pot(self):
        time_limit = 60
        saving_pot.create_ong_pot(acct, time_limit)


if __name__ == '__main__':
    unittest.main()
