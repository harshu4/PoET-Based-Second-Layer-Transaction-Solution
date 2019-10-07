from flask import Flask,request
import sqlite3
import os
import string
import random
import json
import requests
import urllib.request
import base64
import cbor
import logging
#'''------------------------------------------------------'''
from google.protobuf.json_format import MessageToJson
from google.protobuf.message import DecodeError
import hashlib

from hashlib import sha512

import sawtooth_sdk.protobuf.client_batch_submit_pb2 as cpb
from sawtooth_sdk.protobuf.validator_pb2 import Message
from sawtooth_sdk.protobuf.batch_pb2 import BatchHeader
from sawtooth_sdk.protobuf.batch_pb2 import Batch
from sawtooth_sdk.protobuf.batch_pb2 import BatchList
from sawtooth_sdk.protobuf.transaction_pb2 import TransactionHeader
from sawtooth_sdk.protobuf.transaction_pb2 import Transaction


from sawtooth_signing import create_context
from sawtooth_signing import CryptoFactory
from sawtooth_signing.secp256k1 import Secp256k1PrivateKey
#'''------------------------------------------------------'''
app = Flask(__name__)
LOGGER = logging.getLogger(__name__)


#privatek = "2d7b08282a5d520fd467066b9519d4000a3738ccb89363612821154ff32a61bb"
def hash(data):
    '''Compute the SHA-512 hash and return the result as hex characters.'''
    return hashlib.sha512(data).hexdigest()


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def gogogo(stri,starting_balance,aadhar_number,NAME,account_no):
    LOGGER.info('entered gogogo')
    context = create_context('secp256k1')
    conn = sqlite3.connect('bank.db')
#    cursor = conn.execute("SELECT private_key from key")
#    for row in cursor:
#        privatek=row[0]
    privatek = open("priv.txt",'r').read()[0:-1]

    private_key = Secp256k1PrivateKey.from_hex(privatek)

    signer = CryptoFactory(context).new_signer(private_key)
    message=id_generator()
    key=signer.sign(str.encode(message))
    goyu=True
    while goyu:
        try:
            code=id_generator(size=3,chars=string.digits)+id_generator(size=3,chars=string.ascii_lowercase)
            #code = "234sdf"
            print('a')
            input = hash("bankregister".encode('utf-8'))[0:6]+hash("overclockedbrain".encode('utf-8'))[0:58]+hash(code.encode('utf-8'))[0:6]

            #input = "0fb30d96b1f101ff209462abcce07bb477627730dde6d4284799fcb9f733d2892f3cc9"
            print(input)

            p = json.loads(requests.get("http://rest-api:8008/state/{}".format(input)).text)
            print(p)
            try:
                a = p['data']
                print(a)
            except:
                print("exited")
                goyu= False
                break

        except:
            pass
    conn.execute("UPDATE BANK set code = '{}' where account_no = '{}'".format(code,account_no))
    conn.commit()
    conn.close()
    payload = "CREATE,{},{},{},{},{},{},{},{}".format(stri,starting_balance,code,aadhar_number,account_no,NAME,message,key)
    payload_bytes = cbor.dumps(payload)
    txn_header_bytes = TransactionHeader(
        family_name='bankregister',
        family_version='1.0',
        inputs=[input],
        outputs=[input],
        signer_public_key=signer.get_public_key().as_hex(),
        batcher_public_key=signer.get_public_key().as_hex(),
        dependencies=[],
        payload_sha512=sha512(payload_bytes).hexdigest()
        ).SerializeToString()
    signature = signer.sign(txn_header_bytes)

    txn = Transaction(
        header=txn_header_bytes,
        header_signature=signature,
        payload =payload_bytes
        )
    txns = [txn]

    batch_header_bytes = BatchHeader(
    signer_public_key=signer.get_public_key().as_hex(),
    transaction_ids=[txn.header_signature for txn in txns],
    ).SerializeToString()

    signature = signer.sign(batch_header_bytes)

    batch = Batch(
    header=batch_header_bytes,
    header_signature=signature,
    transactions=txns
    )
    batch_list_bytes = BatchList(batches=[batch]).SerializeToString()
    return code,batch_list_bytes

def gogogox(todo,amount,account_no):
    print('gogogo')
    context = create_context('secp256k1')
#    conn = sqlite3.connect('bank.db')
#    cursor = conn.execute("SELECT private_key from key")
#    for row in cursor:
#        privatek=row[0]
#    conn.close()
#    private_key = Secp256k1PrivateKey.from_hex(privatek)
    conn = sqlite3.connect('bank.db')

    cursor = conn.execute("SELECT code from BANK WHERE account_no='{}'".format(account_no))
    for row in cursor:
        code = row[0]
    conn.close()
    private_key = context.new_random_private_key()
    signer = CryptoFactory(context).new_signer(private_key)

    input = hash("bankregister".encode('utf-8'))[0:6]+hash("overclockedbrain".encode('utf-8'))[0:58]+hash(code.encode('utf-8'))[0:6]
    payload = "{},{},{}".format(todo,amount,code)
    payload_bytes = cbor.dumps(payload)
    txn_header_bytes = TransactionHeader(
        family_name='bankregister',
        family_version='1.0',
        inputs=[input],
        outputs=[input],
        signer_public_key=signer.get_public_key().as_hex(),
        batcher_public_key=signer.get_public_key().as_hex(),
        dependencies=[],
        payload_sha512=sha512(payload_bytes).hexdigest()
        ).SerializeToString()
    signature = signer.sign(txn_header_bytes)

    txn = Transaction(
        header=txn_header_bytes,
        header_signature=signature,
        payload =payload_bytes
        )
    txns = [txn]

    batch_header_bytes = BatchHeader(
    signer_public_key=signer.get_public_key().as_hex(),
    transaction_ids=[txn.header_signature for txn in txns],
    ).SerializeToString()

    signature = signer.sign(batch_header_bytes)

    batch = Batch(
    header=batch_header_bytes,
    header_signature=signature,
    transactions=txns
    )
    batch_list_bytes = BatchList(batches=[batch]).SerializeToString()
    return batch_list_bytes

@app.route('/get_balance')
def get_balance():
    try:
        conn = sqlite3.connect('bank.db')
        account_no=request.args.get('account_no')
        cursor = conn.execute("SELECT balance from BANK WHERE account_no={}".format(account_no))
        balance=0
        for row in cursor:
            balance=row[0]
        conn.close()
        return str(balance)
    except:
        return "Error while fetching balance"

@app.route('/get_account')
def get_account():
    try:
        conn = sqlite3.connect('bank.db')
        adhar_no = request.args.get('adhar_no')
        cursor = conn.execute("SELECT * from BANK WHERE adhar_no='{}'".format(adhar_no))
        out=""
        for row in cursor:
            for x in row:
                out=out+x+":"
        out[-1]=""
        conn.close()
        return out
    except:
        return "Error fetching account"

@app.route('/link_state',methods=['POST'])
def linktostate():
    img=request.files['img']
    adhar_no=request.args.get('adhar_no')
    account_no=request.args.get('account_no')
    itt = img.read()
    a={'image':itt}
    #p=requests.post("http://aadhar-api:7007?aadharno={}".format(adhar_no),files=a).text
    if True:
        conn = sqlite3.connect('bank.db')
        cursor = conn.execute("SELECT * from BANK WHERE account_no={}".format(account_no))
        balance =0
        ame= 0
        for row in cursor:
            ame=row[2]
            balance=row[5]
        istr=base64.b64encode(itt).decode('utf-8')


        code,batchee = gogogo(istr,balance,adhar_no,ame,account_no)

        requesto = urllib.request.Request(
                'http://rest-api:8008/batches',
                batchee,
                method='POST',
                headers={'Content-Type': 'application/octet-stream'})
        response = urllib.request.urlopen(requesto)
        conn.close()
        return code
    else:
        return "false"

@app.route('/add_account')
def add_account():
    try:
        conn = sqlite3.connect('bank.db')
        account_no=id_generator(size=12,chars=string.digits)
        adhar_no=request.args.get('adhar_no')
        name=request.args.get('name')
        age=request.args.get('age')
        phone_no=request.args.get('phone_no')
        conn.execute("INSERT INTO BANK (account_no,adhar_no,NAME,AGE,phone_no,balance,code) \
              VALUES ('{}', '{}', '{}', {}, '{}',0,'0')".format(account_no, adhar_no, name, age, phone_no));
        conn.commit()
        conn.close()
        return account_no
    except Exception as e:
        return "false"

@app.route('/add_balance')
def add_balance():
    try:
        amount = request.args.get('amount')
        account_no = request.args.get('account_no')
        batchee = gogogox("ADD",amount,account_no)

        conn = sqlite3.connect('bank.db')
        cursor = conn.execute("SELECT balance from BANK WHERE account_no='{}'".format(account_no))
        print("above cursor")
        for row in cursor:
            print(row)
            old=row[0]

        print("after cursor")
        new=int(old)+int(amount)

        conn.execute("UPDATE BANK set balance = {} where account_no='{}'".format(new,account_no))
        conn.commit()
        conn.close()
        requesto = urllib.request.Request(
            'http://rest-api:8008/batches',
            batchee,
            method='POST',
            headers={'Content-Type': 'application/octet-stream'})
        response = urllib.request.urlopen(requesto)
        return 'abc'
    except Exception as e:
        print(e)
        return "Error occured while exicuting request"


@app.route('/withdraw')
def withdraw_balance():
    try:
        amount = request.args.get('amount')
        account_no = request.args.get('account_no')
        batchee = gogogox("WITHD",amount,account_no)
        conn = sqlite3.connect('bank.db')
        cursor = conn.execute("SELECT balance from BANK WHERE account_no='{}'".format(account_no))
        old=0
        for row in cursor:
            old=row[0]
        new=old-int(amount)
        if new <=0:
            return "your account balance is low"
        #remaining
        conn.execute("UPDATE BANK set balance = {} where account_no='{}'".format(new,account_no))
        conn.commit()
        conn.close()
        requesto = urllib.request.Request(
            'http://rest-api:8008/batches',
            batchee,
            method='POST',
            headers={'Content-Type': 'application/octet-stream'})
        response = urllib.request.urlopen(requesto)
        return 'abc'
    except Exception as e:
        print(e)
        return "Error occured while exicuting request"


def add_balancex(amount,account_no):
    try:
        conn = sqlite3.connect('bank.db')
        cursor = conn.execute("SELECT balance from BANK WHERE account_no='{}'".format(account_no))
        print("above cursor")
        for row in cursor:
            print(row)
            old=row[0]

        print("after cursor")
        new=int(old)+int(amount)

        conn.execute("UPDATE BANK set balance = {} where account_no='{}'".format(new,account_no))
        conn.commit()
        conn.close()
        return 'abc'
    except Exception as e:
        print(e)
        return "Error occured while exicuting request"


def withdrawx_balance(amount,account_no):
    try:

        conn = sqlite3.connect('bank.db')
        cursor = conn.execute("SELECT balance from BANK WHERE account_no='{}'".format(account_no))
        old=0
        for row in cursor:
            old=row[0]
        new=old-int(amount)
        if new <=0:
            return "your account balance is low"
        #remaining
        conn.execute("UPDATE BANK set balance = {} where account_no='{}'".format(new,account_no))
        conn.commit()
        conn.close()

        return 'abc'
    except Exception as e:
        print(e)
        return "Error occured while exicuting request"

@app.route('/event')
def event_occur():
    event_type = request.args.get('type')
    account_no = request.args.get('account_no')
    amount = request.args.get('amount')
    if event_type =="deposit":
        add_balancex(amount,account_no)
    elif event_type =="withdraw":
        withdrawx(amount,account_no)



if __name__ == '__main__':
    print("fresh run")
    if not os.path.exists("bank.db"):

        conn = sqlite3.connect('bank.db')
        conn.execute('''CREATE TABLE BANK
             (account_no  TEXT    NOT NULL,
             adhar_no     TEXT    NOT NULL,
             NAME         TEXT    NOT NULL,
             AGE          INT     NOT NULL,
             phone_no     TEXT    NOT NULL,
             balance      INT     NOT NULL,
             code         TEXT    NOT NULL);''')
        conn.close()
    app.run(host="0.0.0.0",port=8080)
