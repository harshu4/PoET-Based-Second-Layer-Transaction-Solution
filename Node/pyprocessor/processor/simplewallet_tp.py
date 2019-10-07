import requests
import traceback
import sys
import hashlib
import base64
import logging
import cbor
import json
from sawtooth_signing.secp256k1 import Secp256k1PrivateKey
from sawtooth_sdk.processor.handler import TransactionHandler
from sawtooth_sdk.processor.exceptions import InvalidTransaction
from sawtooth_sdk.processor.exceptions import InternalError
from sawtooth_sdk.processor.core import TransactionProcessor
from sawtooth_signing import create_context
from sawtooth_signing import CryptoFactory

LOGGER = logging.getLogger(__name__)

FAMILY_NAME = "bankregister"
def setup_loggers():
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)


def _hash(data):
    '''Compute the SHA-512 hash and return the result as hex characters.'''
    return hashlib.sha512(data).hexdigest()
sw_namespace = _hash(FAMILY_NAME.encode('utf-8'))[0:6]
def main():
    '''Entry-point function for the simplewallet transaction processor.'''
    setup_loggers()
    try:
        # Register the transaction handler and start it.
        processor = TransactionProcessor(url='tcp://validator:4004')

        handler = SimpleWalletTransactionHandler(sw_namespace)

        processor.add_handler(handler)

        processor.start()

    except KeyboardInterrupt:
        pass
    except SystemExit as err:
        raise err
    except BaseException as err:
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)


class SimpleWalletTransactionHandler(TransactionHandler):

    def __init__(self, namespace_prefix):
        self._namespace_prefix = namespace_prefix

    @property
    def family_name(self):
        return FAMILY_NAME

    @property
    def family_versions(self):
        return ['1.0']

    @property
    def namespaces(self):
        return [self._namespace_prefix]
    def _get_wallet_address(self, code):
        return _hash("bankregister".encode('utf-8'))[0:6]+_hash("overclockedbrain".encode('utf-8'))[0:58]+_hash(code.encode('utf-8'))[0:6]


    def apply(self, transaction, context):

        header = transaction.header
        payload_cbor = transaction.payload
        payload = cbor.loads(payload_cbor)
        listo =  payload.split(',')


        if listo[0] == "CREATE":

            amount = listo[2]
            code = listo[3]
            image = listo[1]
            aadhar = listo[4]
            account_number = listo[5]
            name = listo[6]
            message = listo[7]
            key = listo[8]


            LOGGER.info("\n the code is " +code)
            wallet_address = self._get_wallet_address(code)
            LOGGER.info("\n THe code is "+code)
            stop_encode = payload.encode('utf-8')
            current_entry = context.get_state([wallet_address])
            if current_entry == []:
                LOGGER.info('Yes it can be done')
                addresses = context.set_state({wallet_address:stop_encode})
                if len(addresses) < 1:
                    raise InternalError("State Error")
            else:
                raise InternalError("Already built")

        elif listo[0] == "PAY":
            LOGGER.info("The length of the is" + str(len(listo)))
            amount = listo[2]
            image = listo[1]
            code = listo[3]
            pub_pos = listo[4]
            wallet_address = self._get_wallet_address(code)
            pub_pos = self._get_wallet_address(pub_pos)
            current_entry = context.get_state([wallet_address])
            current_entry2 = context.get_state([pub_pos])
            if current_entry == []:
                raise InvalidTransaction('No user with this key was registered')
            elif current_entry2 == []:
                raise InvalidTransaction('No user with this key pos was registered')
            else:
                splito = current_entry[0].data.decode('utf-8')
                splito2 = current_entry2[0].data.decode('utf-8')
                current_list = splito.split(',')
                current_list2 = splito2.split(',')
                LOGGER.info("The amount is " +amount)

                if int(current_list[2]) >= int(amount):
                    image1 = base64.b64decode(current_list[1])
                    image2 = base64.b64decode(image)
                    files = {'image': image1,'image2':image2}
                    text = requests.post("http://finger-api:5000/",files=files).text
                    if text == "true":
                        current_list[2] = str(int(current_list[2])-int(amount))
                        temp = ','.join(current_list).encode('utf-8')
                        current_list2[2] = str(int(current_list2[2])+int(amount))
                        temp2 = ','.join(current_list2).encode('utf-8')
                        context.set_state({wallet_address:temp})
                        context.set_state({pub_pos:temp2})
                        key1 = current_list[8]
                        message1 = current_list[7]
                        key2 = current_list2[8]
                        message2 = current_list2[7]
                        file = open("priv.txt",'r')
                        privkey = file.read()[0:-1]
                        file.close()
                        contexta = create_context('secp256k1')
                        pvkey = Secp256k1PrivateKey.from_hex(privkey)
                        signer = CryptoFactory(contexta).new_signer(pvkey)
                        signer_public_key=signer.get_public_key()
                        #LOGGER.debug("GUCHI "+key1+" "+message1+" "+signer_public_key)
                        dtg=contexta.verify(key1, str.encode(message1), signer_public_key)
                        btg =contexta.verify(key2, str.encode(message2), signer_public_key)

                        if dtg:
                            LOGGER.info("dtg")
                            requests.get("http://bank-api:8080/event?type=withdraw&amount={}&account_no={}".format(amount,current_list[5]))
                        if btg:
                            LOGGER.info("btg")
                            requests.get("http://bank-api:8080/event?type=deposit&amount={}&account_no={}".format(amount,current_list2[5]))
                        LOGGER.info("CURRENT AMOUNT IN CLIENT ADDRESS  "+context.get_state([wallet_address])[0].data.decode('utf-8').split(',')[2])

                    else:
                        raise InvalidTransaction('Fingerprint Does not Match')
                else:
                    raise InvalidTransaction('Less money in bankaccount')
        elif listo[0] == "ADD":

            LOGGER.info("IN the ADD")
            LOGGER.info("The length of the is" + str(len(listo)))

            code = listo[2]
            amount = listo[1]

            wallet_address = self._get_wallet_address(code)
            current_entry = context.get_state([wallet_address])
            if current_entry == []:
                LOGGER.info("This was invalid")
                raise InvalidTransaction('No user with this key was registered')
            else:
                splito = current_entry[0].data.decode('utf-8')
                current_list = splito.split(',')
                current_list[2] = str(int(current_list[2])+int(amount))

                temp = ','.join(current_list).encode('utf-8')
                LOGGER.debug("the amount is " + amount)
                LOGGER.info("the amount is "+ amount)
                context.set_state({wallet_address:temp})
                LOGGER.info("CURRENT AMOUNT IN CLIENT ADDRESS  "+context.get_state([wallet_address])[0].data.decode('utf-8').split(',')[2])
        elif listo[0] == "WITHD":


            code = listo[2]
            amount = listo[1]

            wallet_address = self._get_wallet_address(code)
            current_entry = context.get_state([wallet_address])
            if current_entry == []:
                LOGGER.info("This was invalid")
                raise InvalidTransaction('No user with this key was registered')
            else:
                splito = current_entry[0].data.decode('utf-8')
                current_list = splito.split(',')
                if int(amount) <=int(current_list[2]):
                    current_list[2] = str(int(current_list[2])-int(amount))

                    temp = ','.join(current_list).encode('utf-8')
                    LOGGER.debug("the amount is " + amount)
                    LOGGER.info("the amount is "+ amount)
                    context.set_state({wallet_address:temp})
                    LOGGER.info("CURRENT AMOUNT IN CLIENT ADDRESS  "+context.get_state([wallet_address])[0].data.decode('utf-8').split(',')[2])
                else:
                    raise InvalidTransaction('LOW BALANCE')
