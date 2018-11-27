# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import binascii
import time

from ontology.exception.exception import SDKException
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
        try:
            tx_hash = self.__sdk.neo_vm().send_transaction(self.__contract_address_bytearray, from_acct, from_acct,
                                                           gas_limit, gas_price, create_function, False)
            return tx_hash
        except SDKException as e:
            if 'vm execute state fault' in e.args[1]:
                return False
            else:
                raise PotException(PotError.create_ont_pot_failed)

    def create_ong_pot(self, from_acct: Account, time_limit: int, gas_limit: int, gas_price: int):
        create_function = self.__abi_info.get_function('create_ong_pot')
        create_function.set_params_value((from_acct.get_address().to_array(), time_limit))
        try:
            tx_hash = self.__sdk.neo_vm().send_transaction(self.__contract_address_bytearray, from_acct, from_acct,
                                                           gas_limit, gas_price, create_function, False)
            return tx_hash
        except SDKException as e:
            if 'vm execute state fault' in e.args[1]:
                return False
            else:
                raise PotException(PotError.create_ong_pot_failed)

    def put_ont_pot_tx_hash(self, from_acct: Account, tx_hash: str, gas_limit: int, gas_price: int):
        put_ont_pot_tx_hash = self.__abi_info.get_function('put_ont_pot_tx_hash')
        put_ont_pot_tx_hash.set_params_value((from_acct.get_address().to_array(), tx_hash))
        try:
            tx_hash = self.__sdk.neo_vm().send_transaction(self.__contract_address_bytearray, from_acct, from_acct,
                                                           gas_limit, gas_price, put_ont_pot_tx_hash, False)
            return tx_hash
        except SDKException as e:
            if 'vm execute state fault' in e.args[1]:
                return False
            else:
                raise PotException(PotError.create_ong_pot_failed)

    def get_ont_pot_tx_hash(self, bytearray_address: bytearray):
        get_ont_pot_tx_hash = self.__abi_info.get_function('get_ont_pot_tx_hash')
        get_ont_pot_tx_hash.set_params_value((bytearray_address,))
        try:
            data = self.__sdk.neo_vm().send_transaction(self.__contract_address_bytearray, None, None,
                                                        0, 0, get_ont_pot_tx_hash, True)
            data = binascii.a2b_hex(data).decode('ascii')
            return data
        except SDKException as e:
            if 'vm execute state fault' in e.args[1]:
                return False
            else:
                raise PotException(PotError.create_ong_pot_failed)

    def put_ong_pot_tx_hash(self, from_acct: Account, tx_hash: str, gas_limit: int, gas_price: int):
        put_ont_pot_tx_hash = self.__abi_info.get_function('put_ong_pot_tx_hash')
        put_ont_pot_tx_hash.set_params_value((from_acct.get_address().to_array(), tx_hash))
        try:
            return self.__sdk.neo_vm().send_transaction(self.__contract_address_bytearray, from_acct, from_acct,
                                                        gas_limit, gas_price, put_ont_pot_tx_hash, False)
        except SDKException as e:
            if 'vm execute state fault' in e.args[1]:
                return False
            else:
                raise PotException(PotError.create_ong_pot_failed)

    def get_ong_pot_tx_hash(self, bytearray_address: bytearray):
        get_ont_pot_tx_hash = self.__abi_info.get_function('get_ong_pot_tx_hash')
        get_ont_pot_tx_hash.set_params_value((bytearray_address,))
        try:
            data = self.__sdk.neo_vm().send_transaction(self.__contract_address_bytearray, None, None,
                                                        0, 0, get_ont_pot_tx_hash, True)
            data = binascii.a2b_hex(data).decode('ascii')
            return data
        except SDKException as e:
            if 'vm execute state fault' in e.args[1]:
                return False
            else:
                raise PotException(PotError.create_ong_pot_failed)

    def saving_ont(self, from_acct: Account, amount: int, gas_limit: int, gas_price: int):
        saving_ont = self.__abi_info.get_function('saving_ont')
        saving_ont.set_params_value((from_acct.get_address().to_array(), amount))
        try:
            return self.__sdk.neo_vm().send_transaction(self.__contract_address_bytearray, from_acct, from_acct,
                                                        gas_limit, gas_price, saving_ont, False)
        except SDKException as e:
            if 'vm execute state fault' in e.args[1]:
                return False
            else:
                raise PotException(PotError.create_ong_pot_failed)

    def saving_ong(self, from_acct: Account, amount: int, gas_limit: int, gas_price: int):
        saving_ong = self.__abi_info.get_function('saving_ong')
        saving_ong.set_params_value((from_acct.get_address().to_array(), amount))
        try:
            return self.__sdk.neo_vm().send_transaction(self.__contract_address_bytearray, from_acct, from_acct,
                                                        gas_limit, gas_price, saving_ong, False)
        except SDKException as e:
            if 'vm execute state fault' in e.args[1]:
                return False
            else:
                raise PotException(PotError.create_ong_pot_failed)

    def take_ong_out(self, from_acct: Account, gas_limit: int, gas_price: int):
        take_ong_out = self.__abi_info.get_function('take_ong_out')
        take_ong_out.set_params_value((from_acct.get_address().to_array(),))
        try:
            tx_hash = self.__sdk.neo_vm().send_transaction(self.__contract_address_bytearray, from_acct, from_acct,
                                                           gas_limit, gas_price, take_ong_out, False)
            return tx_hash
        except SDKException as e:
            if 'vm execute state fault' in e.args[1]:
                return False
            else:
                raise PotException(PotError.create_ong_pot_failed)

    def query_ont_pot_saving_time(self, address_bytes: bytes) -> int:
        query_function = self.__abi_info.get_function('query_ont_pot_saving_time')
        query_function.set_params_value((address_bytes,))
        saving_time = self.__sdk.neo_vm().send_transaction(self.__contract_address_bytearray, None, None, 0, 0,
                                                           query_function, True)
        saving_time = int(''.join(reversed([saving_time[i:i + 2] for i in range(0, len(saving_time), 2)])), 16)
        return saving_time

    def query_ong_pot_saving_time(self, address_bytes: bytes) -> int:
        query_function = self.__abi_info.get_function('query_ong_pot_saving_time')
        query_function.set_params_value((address_bytes,))
        saving_time = self.__sdk.neo_vm().send_transaction(self.__contract_address_bytearray, None, None, 0, 0,
                                                           query_function, True)
        saving_time = int(''.join(reversed([saving_time[i:i + 2] for i in range(0, len(saving_time), 2)])), 16)
        return saving_time

    def query_create_pot_event(self, tx_hash: str):
        event = self.__sdk.rpc.get_smart_contract_event_by_tx_hash(tx_hash)
        if event == '':
            return list()
        event = event.get('Notify', list())
        if len(event) == 0:
            return event
        event = event[0].get('States', list())
        if len(event) == 0:
            return event
        event[0] = binascii.a2b_hex(event[0]).decode('ascii')
        event[1] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(
            int(''.join(reversed([event[1][i:i + 2] for i in range(0, len(event[1]), 2)])), 16)))
        return event
