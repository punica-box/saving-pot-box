#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import binascii

from ontology.ont_sdk import OntologySdk
from ontology.account.account import Account
from ontology.smart_contract.neo_contract.abi.abi_info import AbiInfo

from pot.pot_exception import (
    PotException,
    PotError
)


class InvokeSavingPot(object):
    def __init__(self, sdk: OntologySdk, abi: dict, hex_contract_address: str):
        if not isinstance(sdk, OntologySdk):
            raise PotException(PotError.invalid_sdk)
        if not isinstance(abi, dict):
            raise PotException(PotError.invalid_abi_type)
        if not isinstance(hex_contract_address, str):
            raise PotException(PotError.invalid_contract_address_hex_type)
        if len(hex_contract_address) != 40:
            raise PotException(PotError.invalid_contract_address_hex_len)
        self.__sdk = sdk
        self.__contract_address_hex = hex_contract_address
        self.__contract_address_bytearray = bytearray(binascii.a2b_hex(hex_contract_address))
        self.__contract_address_bytearray.reverse()
        self.__abi = abi
        entry_point = self.__abi.get('entrypoint', '')
        functions = self.__abi['abi']['functions']
        events = self.__abi.get('events', list())
        self.__abi_info = AbiInfo(hex_contract_address, entry_point, functions, events)

    def get_contract_address_hex(self):
        return self.__contract_address_hex

    def create_ont_pot(self, from_acct: Account, time_limit: int, gas_limit: int = 20000000, gas_price: int = 500):
        create_function = self.__abi_info.get_function('create_ont_pot')
        create_function.set_params_value((from_acct.get_address().to_array(), time_limit))
        tx_hash = self.__sdk.neo_vm().send_transaction(self.__contract_address_bytearray, from_acct, from_acct,
                                                       gas_limit, gas_price, create_function, False)
        return tx_hash

    def create_ong_pot(self, from_acct: Account, time_limit: int, gas_limit: int, gas_price: int):
        create_function = self.__abi_info.get_function('create_ong_pot')
        create_function.set_params_value((from_acct.get_address().to_array(), time_limit))
        tx_hash = self.__sdk.neo_vm().send_transaction(self.__contract_address_bytearray, from_acct, from_acct,
                                                       gas_limit, gas_price, create_function, False)
        return tx_hash
