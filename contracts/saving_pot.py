from boa.interop.Ontology.Native import Invoke
from boa.builtins import ToScriptHash, concat, state
from boa.interop.System.Storage import GetContext, Get, Put, Delete
from boa.interop.System.Runtime import CheckWitness, GetTime, Notify
from boa.interop.System.ExecutionEngine import GetExecutingScriptHash

ONT_ADDRESS = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01')
ONG_ADDRESS = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02')
SAVING_POT_ADDRESS = GetExecutingScriptHash()

CTX = GetContext()
SAVING_ONT_TIME_PREFIX = 'STT'
SAVING_ONT_AMOUNT_PREFIX = 'STA'
SAVING_ONG_TIME_PREFIX = 'SGT'
SAVING_ONG_AMOUNT_PREFIX = 'SGA'
SAVING_ONT_TX_HASH_PREFIX = 'ONTTH'
SAVING_ONG_TX_HASH_PREFIX = 'ONGTH'


def main(operation, args):
    if operation == 'saving_ont':
        return saving_ont(args[0], args[1])
    elif operation == 'saving_ong':
        return saving_ong(args[0], args[1])
    elif operation == 'create_ont_pot':
        return create_ont_pot(args[0], args[1])
    elif operation == 'create_ong_pot':
        return create_ong_pot(args[0], args[1])
    elif operation == 'query_ont_pot_saving_time':
        return query_ont_pot_saving_time(args[0])
    elif operation == 'query_ong_pot_saving_time':
        return query_ong_pot_saving_time(args[0])
    elif operation == 'take_ont_out':
        return take_ont_out(args[0])
    elif operation == 'take_ong_out':
        return take_ong_out(args[0])
    elif operation == 'put_ont_pot_tx_hash':
        return put_ont_pot_tx_hash(args[0], args[1])
    elif operation == 'get_ont_pot_tx_hash':
        return get_ont_pot_tx_hash(args[0])
    elif operation == 'put_ong_pot_tx_hash':
        return put_ong_pot_tx_hash(args[0], args[1])
    elif operation == 'get_ong_pot_tx_hash':
        return get_ong_pot_tx_hash(args[0])
    else:
        return revert()


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


def add(a, b):
    c = a + b
    require(c >= a)
    return c


def sub(a, b):
    require(a >= b)
    c = a - b
    return c


def concat_key(str1, str2):
    return concat(concat(str1, '_'), str2)


def transfer_ont(from_acct, to_acct, amount):
    require_witness(from_acct)
    transfer_param = state(from_acct, to_acct, amount)
    res = Invoke(0, ONT_ADDRESS, 'transfer', [transfer_param])
    if res == b'\x01':
        return True
    else:
        return False


def transfer_ong(from_acct, to_acct, amount):
    require_witness(from_acct)
    transfer_param = state(from_acct, to_acct, amount)
    res = Invoke(0, ONG_ADDRESS, 'transfer', [transfer_param])
    if res == b'\x01':
        return True
    else:
        return False


def put_ont_pot_tx_hash(from_acct, tx_hash):
    require_witness(from_acct)
    saving_tx_hash_key = concat_key(SAVING_ONT_TX_HASH_PREFIX, from_acct)
    Put(CTX, saving_tx_hash_key, tx_hash)


def get_ont_pot_tx_hash(from_acct):
    saving_tx_hash_key = concat_key(SAVING_ONT_TX_HASH_PREFIX, from_acct)
    return Get(CTX, saving_tx_hash_key)


def put_ong_pot_tx_hash(from_acct, tx_hash):
    require_witness(from_acct)
    saving_tx_hash_key = concat_key(SAVING_ONG_TX_HASH_PREFIX, from_acct)
    Put(CTX, saving_tx_hash_key, tx_hash)


def get_ong_pot_tx_hash(from_acct):
    saving_tx_hash_key = concat_key(SAVING_ONG_TX_HASH_PREFIX, from_acct)
    return Get(CTX, saving_tx_hash_key)


def create_ont_pot(from_acct, time_limit):
    require_witness(from_acct)
    saving_time_key = concat_key(SAVING_ONT_TIME_PREFIX, from_acct)
    if Get(CTX, saving_time_key):
        revert()
    else:
        saving_time = add(GetTime(), time_limit)
        Put(CTX, saving_time_key, time_limit)
        Notify(['saving time', saving_time])
        saving_amount_key = concat_key(SAVING_ONT_AMOUNT_PREFIX, from_acct)
        Put(CTX, saving_amount_key, 0)


def create_ong_pot(from_acct, time_limit):
    require_witness(from_acct)
    saving_time_key = concat_key(SAVING_ONG_TIME_PREFIX, from_acct)
    if Get(CTX, saving_time_key):
        revert()
    else:
        saving_time = add(GetTime(), time_limit)
        Put(CTX, saving_time_key, time_limit)
        Notify(['saving time', saving_time])
        saving_amount_key = concat_key(SAVING_ONG_AMOUNT_PREFIX, from_acct)
        Put(CTX, saving_amount_key, 0)


def query_ont_pot_saving_time(from_acct):
    saving_time_key = concat_key(SAVING_ONT_TIME_PREFIX, from_acct)
    saving_time = Get(CTX, saving_time_key)
    if saving_time:
        return saving_time
    else:
        return 0


def query_ong_pot_saving_time(from_acct):
    saving_time_key = concat_key(SAVING_ONG_TIME_PREFIX, from_acct)
    saving_time = Get(CTX, saving_time_key)
    if saving_time:
        return saving_time
    else:
        return 0


def saving_ont(from_acct, amount):
    if amount < 0:
        revert()
    saving_time_key = concat_key(SAVING_ONT_TIME_PREFIX, from_acct)
    saving_time = Get(CTX, saving_time_key)
    if saving_time <= GetTime():
        transfer_ont(from_acct, SAVING_POT_ADDRESS, amount)
        saving_amount_key = concat_key(SAVING_ONT_AMOUNT_PREFIX, from_acct)
        saving_amount = Get(CTX, saving_amount_key)
        saving_amount = add(saving_amount, amount)
        Put(CTX, saving_amount_key, saving_amount)
    else:
        revert()


def saving_ong(from_acct, amount):
    saving_time_key = concat_key(SAVING_ONG_TIME_PREFIX, from_acct)
    saving_time = Get(CTX, saving_time_key)
    Notify([saving_time, GetTime()])
    if saving_time <= GetTime():
        transfer_ong(from_acct, SAVING_POT_ADDRESS, amount)
        saving_amount_key = concat_key(SAVING_ONG_AMOUNT_PREFIX, from_acct)
        saving_amount = Get(CTX, saving_amount_key)
        saving_amount = add(saving_amount, amount)
        Put(CTX, saving_amount_key, saving_amount)
    else:
        revert()


def take_ont_out(to_acct):
    require_witness(to_acct)
    saving_time_key = concat_key(SAVING_ONT_TIME_PREFIX, to_acct)
    saving_time = Get(CTX, saving_time_key)
    if saving_time < GetTime():
        saving_amount_key = concat_key(SAVING_ONG_AMOUNT_PREFIX, to_acct)
        saving_amount = Get(CTX, saving_amount_key)
        transfer_ont(SAVING_POT_ADDRESS, to_acct, saving_amount)
        Delete(CTX, saving_amount_key)
    else:
        revert()


def take_ong_out(to_acct):
    require_witness(to_acct)
    saving_time_key = concat_key(SAVING_ONT_TIME_PREFIX, to_acct)
    saving_time = Get(CTX, saving_time_key)
    if saving_time < GetTime():
        saving_amount_key = concat_key(SAVING_ONG_AMOUNT_PREFIX, to_acct)
        saving_amount = Get(CTX, saving_amount_key)
        transfer_ong(SAVING_POT_ADDRESS, to_acct, saving_amount)
        Delete(CTX, saving_amount_key)
    else:
        revert()
