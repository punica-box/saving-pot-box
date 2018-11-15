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
