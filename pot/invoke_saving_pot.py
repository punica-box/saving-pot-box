#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import binascii

from ontology.account.account import Account


class InvokeSavingPot(object):
    def __init__(self, abi, hex_contract_address: str):
        if not isinstance(hex_contract_address, str):
            pass
        self.__contract_address_bytearray = bytearray(binascii.a2b_hex(hex_contract_address))
        self.__contract_address_bytearray.reverse()
        self.__abi = abi

    def create_ont_pot(self, from_acct: Account, time_limit: int):
        pass

    def create_ong_pot(self, from_acct: Account, time_limit: int):
        pass
