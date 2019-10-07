#FAMILY NAME IS bankregister

from sawtooth_signing import create_context
from sawtooth_signing import CryptoFactory
import cbor
import base64
import hashlib
import sys
from hashlib import sha512
from sawtooth_sdk.protobuf.transaction_pb2 import TransactionHeader
from sawtooth_sdk.protobuf.transaction_pb2 import Transaction
from sawtooth_sdk.protobuf.batch_pb2 import BatchHeader
from sawtooth_sdk.protobuf.batch_pb2 import Batch
from sawtooth_sdk.protobuf.batch_pb2 import BatchList
import urllib.request
from urllib.error import HTTPError
def hash(data):
    '''Compute the SHA-512 hash and return the result as hex characters.'''
    return hashlib.sha512(data).hexdigest()
file = open(argv[2],"rb")
str = base64.b64encode(file.read()).decode('utf-8')
context = create_context('secp256k1')
private_key = context.new_random_private_key()
signer = CryptoFactory(context).new_signer(private_key)
todo = "PAY"
code = argv[1]
code2 = "123fbo"
amount = input("Enter the amount \n")
#aadhar_number = "3934232342334123"
#first_name = "John"
#last_name = "Doe"
pub_pos = hash("bankregister".encode('utf-8'))[0:6]+hash("overclockedbrain".encode('utf-8'))[0:58]+hash(code2.encode('utf-8'))[0:6]
#payload = f"{todo},{str},{starting_balance},{code},{aadhar_number},{first_name},{last_name}"
payload = f"{todo},{str},{amount},{code},{code2}"
payload_bytes = cbor.dumps(payload)
input = hash("bankregister".encode('utf-8'))[0:6]+hash("overclockedbrain".encode('utf-8'))[0:58]+hash(code.encode('utf-8'))[0:6]
print(input)

def banktransfer(family,input,pubpos,signer):
    txn_header_bytes = TransactionHeader(
    family_name=family,
    family_version='1.0',
    inputs=[input,pubpos],
    outputs=[input,pubpos],
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
try:
    batchee = banktransfer("bankregister",input,pub_pos,signer)
    request = urllib.request.Request(
        'http://localhost:8008/batches',
        batchee,
        method='POST',
        headers={'Content-Type': 'application/octet-stream'})
    response = urllib.request.urlopen(request)
    print(response.read())

except HTTPError as e:
    response = e.file
