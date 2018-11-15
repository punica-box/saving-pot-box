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
