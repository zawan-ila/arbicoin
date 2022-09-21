import ecdsa
import hashlib
from functools import reduce

from transactions.serializers import TransactionOutputModelSerializer
from transactions.models import TransactionOutput


def create_simple_raw_transaction(priv_key, rcvr_key, amount):

    try:
        int(rcvr_key, 16)
        ecdsa.VerifyingKey.from_string(bytes.fromhex(rcvr_key))
    except (ecdsa.MalformedPointError, ValueError):
        return 'Receiver Address does not exist'

    priv_keys = [priv_key]

    pub_keys = list(map(lambda pk: ecdsa.SigningKey.from_string(bytes.fromhex(pk)).verifying_key.to_string().hex(), priv_keys))
    receivers = [{"own_addr": rcvr_key, "value": amount}]

    amount_required = amount

    owned_utxos = []

    for pub_key in pub_keys:
        qs = TransactionOutput.objects.filter(own_addr=pub_key)
        owned_utxo = TransactionOutputModelSerializer(qs, many=True).data
        owned_utxos += [*owned_utxo]

    available = 0

    for idx, utxo in enumerate(owned_utxos):
        available += utxo["value"]
        if available >= amount_required:
            break

    if not owned_utxos or idx == len(owned_utxos):
        '''
        Not enough money available
        '''

        return 'Not enough coins'

    else:
        utxos_to_spend = owned_utxos[:idx+1]

    '''
    Calculate change we will get to keep
    '''

    amount_to_ourselves = available - amount_required

    if amount_to_ourselves > 0:
        receivers.append({"own_addr": pub_keys[0], "value": amount_to_ourselves})

    '''
    Add appropriate signatures and post
    '''

    utxos_to_spend_hashes = list(map(lambda i: hashlib.sha1((str(i["value"]) + i["own_addr"] + i["gen_transaction_id"] + str(i["gen_transaction_index"])).encode()).hexdigest(), utxos_to_spend))
    utxos_to_make_hashes = list(map(lambda o: hashlib.sha1((str(o["value"]) + o["own_addr"]).encode()).hexdigest(), receivers))

    to_hash_content = str(len(utxos_to_spend_hashes)) + reduce(lambda a, b: a+b, utxos_to_spend_hashes, '') + str(len(utxos_to_make_hashes)) + reduce(lambda a,b: a+b, utxos_to_make_hashes, '')
    hash_tx = hashlib.sha1(to_hash_content.encode()).hexdigest()

    for utxo in utxos_to_spend:
        pk = utxo["own_addr"]
        sk = priv_keys[pub_keys.index(pk)]
        utxo["signature"] = ecdsa.SigningKey.from_string(bytes.fromhex(sk)).sign(hash_tx.encode()).hex()

    to_post = {'inputs': utxos_to_spend, 'outputs': receivers, 'tx_inputs_count': len(utxos_to_spend), 'tx_outputs_count': len(receivers)}

    return to_post


def owns(wallet_addr, tx):
    for input in tx.inputs.all():
        if input.own_addr == wallet_addr:
            return True
    for output in tx.outputs.all():
        if output.own_addr == wallet_addr:
            return True
    for used_output in tx.used_outputs.all():
        if used_output.own_addr == wallet_addr:
            return True
    return False
