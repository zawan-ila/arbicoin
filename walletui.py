import ecdsa
import hashlib
import os
import requests
from functools import reduce


KEYSTORE = "keys.txt"


def gen_key_pairs(n):
    with open(KEYSTORE, "w") as keyfile:
        for i in range(n):
            sk = ecdsa.SigningKey.generate()
            pk = sk.verifying_key
            skhex = sk.to_string().hex()
            pkhex = pk.to_string().hex()
            keyfile.write(f"{pkhex}\n{skhex}\n\n")


def main():
    host = os.environ.get('ROOT_URL', "http://127.0.0.1:8000/")

    priv_keys = []
    priv_key = input("Please enter your private keys. Enter an empty line when you are done. \n")

    while True:
        if not priv_key:
            break
        else:
            priv_keys.append(priv_key)
            priv_key = input()

    pub_keys = list(map(lambda pk: ecdsa.SigningKey.from_string(bytes.fromhex(pk)).verifying_key.to_string().hex(),priv_keys))
    receivers = []

    rcvr = input("Please enter the recipient addresses and the amount you wish to send them <space separated>. Enter an empty line when you are done. \n")

    while True:
        if not rcvr:
            break
        else:
            addr, amount = rcvr.split()
            receivers.append({"own_addr":addr, "value": int(amount)})
            rcvr = input()

    amount_required = reduce(lambda a,b: a + b["value"],receivers,0)

    owned_utxos = []

    for pub_key in pub_keys:
        owned_utxo = requests.get(host + f'wallet/unspent/{pub_key}/').json()
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
        print('Not enough coins')
        return

    else:
        utxos_to_spend = owned_utxos[:idx+1]

    '''
    Calculate change we will get to keep
    '''

    amount_to_ourselves = available - amount_required

    if amount_to_ourselves:
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

    resp = requests.post(host + "wallet/post/", json=to_post)

    print('Received response')
    print(resp.json())


main()
