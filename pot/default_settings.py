#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import binascii
import os

import json

from ontology.ont_sdk import OntologySdk
from ontology.wallet.wallet_manager import WalletManager
from ontology.smart_contract.neo_contract.abi.abi_info import AbiInfo

ROOT_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WALLET_PATH = os.path.join(ROOT_FOLDER, 'wallet', 'wallet.json')
STATIC_FOLDER = os.path.join(ROOT_FOLDER, 'pot', 'static')
CONTRACTS_FOLDER = os.path.join(ROOT_FOLDER, 'contracts')
TEMPLATE_FOLDER = os.path.join(STATIC_FOLDER, 'templates')
GAS_LIMIT = 20000000
GAS_PRICE = 500
ONT_RPC_ADDRESS = 'http://polaris3.ont.io:20336'
CONTRACT_ADDRESS_HEX = '9560fa0de1fe4440d29d032323698da935aea585'
ONTOLOGY = OntologySdk()
ONTOLOGY.rpc.set_address(ONT_RPC_ADDRESS)
with open(os.path.join(CONTRACTS_FOLDER, 'saving-pot.abi.json')) as f:
    CONTRACT_ABI = json.loads(f.read())
WALLET_MANAGER = WalletManager()
WALLET_MANAGER.open_wallet(WALLET_PATH)
