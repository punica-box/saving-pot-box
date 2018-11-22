#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class PotException(Exception):
    def __init__(self, error: dict):
        super().__init__(error['code'], error['msg'])


class PotError(object):
    @staticmethod
    def get_error(code: int, msg: str) -> dict:
        error = dict(zip(['code', 'msg'], [code, msg]))
        return error

    @staticmethod
    def other_error(msg: str) -> dict:
        if isinstance(msg, bytes):
            try:
                msg = msg.decode()
                msg = 'Other Error, ' + msg
            except UnicodeDecodeError:
                msg = 'Other Error'
        return PotError.get_error(60000, msg)

    invalid_contract_address_hex_type = get_error.__func__(1000, 'the type of contract address should be string ')
    invalid_contract_address_hex_len = get_error.__func__(1001, 'the length of contract address should be 40')
    invalid_abi_type = get_error.__func__(1002, 'the type of contract address should be dict')
    invalid_sdk = get_error.__func__(1003, 'the type of sdk is error')

    create_ong_pot_failed = get_error.__func__(2000, 'create ong saving pot failed')
    create_ont_pot_failed = get_error.__func__(2001, 'create ont saving pot failed')

    query_create_pot_event_failed = get_error.__func__(3000, 'query pot event failed')

    saving_ont_failed = get_error.__func__(4000, 'saving ont failed')
    saving_ong_failed = get_error.__func__(40001, 'saving ong failed')

    take_ont_out_failed = get_error.__func__(5000, 'take ont out failed')
    take_ong_out_failed = get_error.__func__(5001, 'take ong out failed')
