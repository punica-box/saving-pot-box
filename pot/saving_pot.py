#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import stat
import shutil
import binascii

from flask_jsglue import JSGlue
from flask import Flask, request, json, send_from_directory, render_template, redirect, url_for

from ontology.utils import util
from ontology.account.account import Account
from ontology.exception.exception import SDKException
from ontology.wallet.wallet_manager import WalletManager

static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask('Saving-Pot', static_folder=static_folder, template_folder=template_folder)
app.config.from_object('default_settings')
jsglue = JSGlue()
jsglue.init_app(app)
default_identity_account = None
default_wallet_account = None


def remove_file_if_exists(path):
    if os.path.isfile(path):
        os.remove(path)
        return True
    return False


def handle_read_only_remove_error(func, path, exc_info):
    os.chmod(path, stat.S_IWRITE)
    func(path)


def ensure_remove_dir_if_exists(path):
    if os.path.isdir(path):
        shutil.rmtree(path, ignore_errors=False, onerror=handle_read_only_remove_error)
        return True
    return False


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')
    # global default_identity_account
    # if not isinstance(default_identity_account, Account):
    #     return redirect('login')
    # else:
    #     return render_template('index.html')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(static_folder, 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/login')
def login():
    if isinstance(default_identity_account, Account):
        return redirect('')
    else:
        return render_template('login.html')


@app.route('/get_default_wallet_account_data')
def get_default_wallet_account_data():
    if isinstance(app.config['WALLET_MANAGER'], WalletManager):
        try:
            default_wallet_account_data = app.config['WALLET_MANAGER'].get_default_account()
            label = default_wallet_account_data.label
            b58_address = default_wallet_account_data.address
            return json.jsonify({'label': label, 'b58_address': b58_address}), 200
        except SDKException as e:
            return json.jsonify({'result': e.args[1]}), 500
    return json.jsonify({'result': 'WalletManager error'}), 501


@app.route('/get_default_identity_data', methods=['GET'])
def get_default_identity_data():
    wallet_manager = app.config['WALLET_MANAGER']
    if isinstance(wallet_manager, WalletManager):
        try:
            default_identity = wallet_manager.get_default_identity()
            return json.jsonify({'label': default_identity.label, 'ont_id': default_identity.ont_id}), 200
        except SDKException as e:
            return json.jsonify({'result': e.args[1]}), 500
    else:
        return json.jsonify({'result': 'Wallet manager error'}), 501


@app.route('/unlock_identity', methods=['POST'])
def unlock_identity():
    ont_id_selected = request.json.get('ont_id_selected')
    ont_id_password = request.json.get('ont_id_password')
    global default_identity_account
    try:
        default_identity_account = app.config['WALLET_MANAGER'].get_account(ont_id_selected, ont_id_password)
    except SDKException as e:
        redirect_url = request.url.replace('unlock_identity', 'login')
        return json.jsonify({'result': e.args[1], 'redirect_url': redirect_url}), 500
    if isinstance(default_identity_account, Account):
        msg = ''.join(['unlock ', ont_id_selected, ' successful!'])
        redirect_url = request.url.replace('unlock_identity', '')
        return json.jsonify({'result': msg, 'redirect_url': redirect_url}), 200
    else:
        redirect_url = request.url.replace('unlock_identity', 'login')
        return json.jsonify({'result': 'unlock failed!', 'redirect_url': redirect_url}), 501


@app.route('/get_album_array')
def get_album_array():
    global default_identity_account
    if not isinstance(default_identity_account, Account):
        return json.jsonify({'result': 'default identity is locked'}), 500
    item_list = get_item_list_from_contract(default_identity_account)
    get_album_from_ipfs(item_list)
    album_img = os.listdir(app.config['ALBUM_FOLDER'])
    for index in range(len(album_img)):
        album_img[index] = ''.join(['/static/album/', album_img[index]])
    return json.jsonify({'result': album_img}), 200


@app.route('/upload_file', methods=['POST'])
def upload_file():
    file = request.files['file']
    global default_identity_account
    global default_wallet_account
    if not isinstance(default_identity_account, Account):
        return json.jsonify({'result': 'default identity is locked'}), 500
    if not isinstance(default_wallet_account, Account):
        return json.jsonify({'result': 'default account is locked'}), 501
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        img_path = os.path.join(app.config['ASSETS_FOLDER'], filename)
        file.save(img_path)
        tx_hash = add_assets_to_ipfs(img_path, default_identity_account, default_wallet_account)
        remove_file_if_exists(img_path)
        return json.jsonify({'result': filename, 'tx_hash': tx_hash}), 200
    else:
        return json.jsonify({'result': 'file is not allowed'}), 502


@app.route('/query_balance', methods=['POST'])
def query_balance():
    b58_address = request.json.get('b58_address')
    asset_select = request.json.get('asset_select')
    try:
        if asset_select == 'ONT':
            balance = app.config['ONTOLOGY'].rpc.get_balance(b58_address)
            return json.jsonify({'result': str(balance['ont'])}), 200
        elif asset_select == 'ONG':
            balance = app.config['ONTOLOGY'].rpc.get_balance(b58_address)
            return json.jsonify({'result': str(balance['ong'])}), 200
        else:
            return json.jsonify({'result': 'query balance failed'}), 500
    except SDKException as e:
        return json.jsonify({'result': e.args[1]}), 500


@app.route('/get_contract_address', methods=['GET'])
def get_contract_address():
    contract_address = app.config['CONTRACT_ADDRESS_HEX']
    return json.jsonify({'result': contract_address}), 200


@app.route('/get_accounts', methods=['GET'])
def get_accounts():
    account_list = app.config['WALLET_MANAGER'].get_wallet().get_accounts()
    address_list = list()
    for acct in account_list:
        acct_item = {'b58_address': acct.address, 'label': acct.label}
        address_list.append(acct_item)
    return json.jsonify({'result': address_list}), 200


@app.route('/is_default_wallet_account_unlock', methods=['GET'])
def is_default_wallet_account_unlock():
    global default_wallet_account
    if isinstance(default_wallet_account, Account):
        return json.jsonify({'result': True}), 200
    else:
        return json.jsonify({'result': False}), 200


@app.route('/create_account', methods=['POST'])
def create_account():
    password = request.json.get('password')
    label = request.json.get('label')
    hex_private_key = util.get_random_bytes(32).hex()
    app.config['WALLET_MANAGER'].create_account_from_private_key(label, password, hex_private_key)
    app.config['WALLET_MANAGER'].save()
    return json.jsonify({'hex_private_key': hex_private_key})


@app.route('/import_account', methods=['POST'])
def import_account():
    label = request.json.get('label')
    password = request.json.get('password')
    hex_private_key = request.json.get('hex_private_key')
    try:
        account = app.config['WALLET_MANAGER'].create_account_from_private_key(label, password, hex_private_key)
    except ValueError as e:
        return json.jsonify({'msg': 'account exists.'}), 500
    b58_address = account.get_address()
    app.config['WALLET_MANAGER'].save()
    return json.jsonify({'result': b58_address}), 200


@app.route('/remove_account', methods=['POST'])
def remove_account():
    b58_address_remove = request.json.get('b58_address_remove')
    password = request.json.get('password')
    try:
        acct = app.config['WALLET_MANAGER'].get_account(b58_address_remove, password)
        if acct is None:
            return json.jsonify({'result': ''.join(['remove ', b58_address_remove, ' failed!'])}), 500
        app.config['WALLET_MANAGER'].get_wallet().remove_account(b58_address_remove)
    except SDKException or RuntimeError:
        return json.jsonify({'result': ''.join(['remove ', b58_address_remove, ' failed!'])}), 500
    app.config['WALLET_MANAGER'].save()
    return json.jsonify({'result': ''.join(['remove ', b58_address_remove, ' successful!'])}), 200


@app.route('/account_change', methods=['POST'])
def account_change():
    b58_address_selected = request.json.get('b58_address_selected')
    password = request.json.get('password')
    global default_wallet_account
    old_wallet_account = default_wallet_account
    try:
        default_wallet_account = app.config['WALLET_MANAGER'].get_account(b58_address_selected, password)
    except SDKException:
        default_wallet_account = old_wallet_account
        return json.jsonify({'result': 'invalid password'}), 400
    try:
        app.config['WALLET_MANAGER'].get_wallet().set_default_account_by_address(b58_address_selected)
    except SDKException:
        return json.jsonify({'result': 'invalid base58 address'})
    app.config['WALLET_MANAGER'].save()
    return json.jsonify({'result': 'Change successful'}), 200


@app.route('/get_identities', methods=['GET'])
def get_identities():
    identities = app.config['WALLET_MANAGER'].get_wallet().get_identities()
    ont_id_list = list()
    for item in identities:
        ont_id_item = {'ont_id': item.ont_id, 'label': item.label}
        ont_id_list.append(ont_id_item)
    return json.jsonify({'result': ont_id_list}), 200


@app.route('/create_identity', methods=['POST'])
def create_identity():
    label = request.json.get('label')
    password = request.json.get('password')
    hex_private_key = util.get_random_bytes(32).hex()
    try:
        new_identity = app.config['WALLET_MANAGER'].create_identity_from_private_key(label, password,
                                                                                     hex_private_key)
    except SDKException as e:
        return json.jsonify({'result': e}), 500
    app.config['WALLET_MANAGER'].save()
    return json.jsonify({'hex_private_key': hex_private_key, 'ont_id': new_identity.ont_id}), 200


@app.route('/import_identity', methods=['POST'])
def import_identity():
    label = request.json.get('label')
    password = request.json.get('password')
    hex_private_key = request.json.get('hex_private_key')
    try:
        new_identity = app.config['WALLET_MANAGER'].create_identity_from_private_key(label, password,
                                                                                     hex_private_key)
    except SDKException as e:
        return json.jsonify({'result': e}), 500
    app.config['WALLET_MANAGER'].save()
    return json.jsonify({'hex_private_key': hex_private_key, 'ont_id': new_identity.ont_id}), 200


@app.route('/remove_identity', methods=['POST'])
def remove_identity():
    ont_id_remove = request.json.get('ont_id_remove')
    password = request.json.get('password')
    try:
        acct = app.config['WALLET_MANAGER'].get_account(ont_id_remove, password)
        if acct is None:
            return json.jsonify({'result': ''.join(['remove ', ont_id_remove, ' failed!'])}), 500
        app.config['WALLET_MANAGER'].get_wallet().remove_identity(ont_id_remove)
    except SDKException or RuntimeError:
        return json.jsonify({'result': ''.join(['remove ', ont_id_remove, ' failed!'])}), 500
    app.config['WALLET_MANAGER'].save()
    return json.jsonify({'result': ''.join(['remove ', ont_id_remove, ' successful!'])}), 200


@app.route('/identity_change', methods=['POST'])
def identity_change():
    ont_id_selected = request.json.get('ont_id_selected')
    password = request.json.get('password')
    global default_identity_account
    old_identity_account = default_identity_account
    try:
        default_identity_account = app.config['WALLET_MANAGER'].get_account(ont_id_selected, password)
    except SDKException:
        default_identity_account = old_identity_account
        return json.jsonify({'result': 'Invalid Password'}), 501
    try:
        app.config['WALLET_MANAGER'].get_wallet().set_default_identity_by_ont_id(ont_id_selected)
    except SDKException:
        return json.jsonify({'result': 'Invalid OntId'}), 500
    app.config['WALLET_MANAGER'].save()
    return json.jsonify({'result': 'Change Successful'}), 200


@app.route('/change_net', methods=['POST'])
def change_net():
    network_selected = request.json.get('network_selected')
    if network_selected == 'MainNet':
        remote_rpc_address = 'http://dappnode1.ont.io:20336'
        app.config['ONTOLOGY'].set_rpc(remote_rpc_address)
        sdk_rpc_address = app.config['ONTOLOGY'].get_rpc().addr
        if sdk_rpc_address != remote_rpc_address:
            result = ''.join(['remote rpc address set failed. the rpc address now used is ', sdk_rpc_address])
            return json.jsonify({'result': result}), 409
    elif network_selected == 'TestNet':
        remote_rpc_address = 'http://polaris3.ont.io:20336'
        app.config['ONTOLOGY'].set_rpc(remote_rpc_address)
        sdk_rpc_address = app.config['ONTOLOGY'].get_rpc().addr
        if sdk_rpc_address != remote_rpc_address:
            result = ''.join(['remote rpc address set failed. the rpc address now used is ', sdk_rpc_address])
            return json.jsonify({'result': result}), 409
    elif network_selected == 'Localhost':
        remote_rpc_address = 'http://localhost:20336'
        app.config['ONTOLOGY'].set_rpc(remote_rpc_address)
        old_remote_rpc_address = app.config['ONTOLOGY'].get_rpc()
        sdk_rpc_address = app.config['ONTOLOGY'].get_rpc().addr
        if sdk_rpc_address != remote_rpc_address:
            result = ''.join(['remote rpc address set failed. the rpc address now used is ', sdk_rpc_address])
            return json.jsonify({'result': result}), 409
        try:
            app.config['ONTOLOGY'].rpc.get_version()
        except SDKException as e:
            app.config['ONTOLOGY'].set_rpc(old_remote_rpc_address)
            error_msg = 'Other Error, ConnectionError'
            if error_msg in e.args[1]:
                return json.jsonify({'result': 'Connection to localhost node failed.'}), 400
            else:
                return json.jsonify({'result': e.args[1]}), 500
    else:
        return json.jsonify({'result': 'unsupported network.'}), 501
    return json.jsonify({'result': 'succeed'}), 200


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
