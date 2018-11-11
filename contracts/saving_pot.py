#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from boa.interop.System.Runtime import CheckWitness


def revert():
    """
    Revert the transaction. The opcodes of this function is `09f7f6f5f4f3f2f1f000f0`,
    but it will be changed to `ffffffffffffffffffffff` since opcode THROW doesn't
    work, so, revert by calling unused opcode.
    """
    raise Exception(0xF1F1F2F2F3F3F4F4)


def require(condition):
    if not condition:
        revert()


def require_script_hash(key):
    require(len(key) == 20)


def require_witness(witness):
    require(CheckWitness(witness))
