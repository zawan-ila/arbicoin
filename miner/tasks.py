import os
import time
import hashlib
import math
from functools import reduce
from celery import signals
from transactions.models import Transaction
from transactions.models import TransactionOutput
from blocks.models import Block


def gen_reward_transaction(val, blk_h):
    # address for the block reward
    reward_addr = os.environ.get("REWARD_ADDR", "a5a5da92a90a9ee3b1c640b18be05be07d335127a231ce631b503bfca76876dd3eb871dfaabd5aafe1f749a828577a9d")
    # hash of the reward output
    reward_output_hash = hashlib.sha1((str(val) + reward_addr + str(blk_h)).encode()).hexdigest()
    # hash of the transaction(i.e the block reward transaction)
    tx_hash = hashlib.sha1(('01'+reward_output_hash).encode()).hexdigest()
    # save the block reward transaction
    tx = Transaction.objects.create(hash=tx_hash, tx_inputs_count=0, tx_outputs_count=1)
    # save the block reward transaction output
    tout = TransactionOutput.objects.create(blk_height=blk_h, value=val, own_addr=reward_addr, hash=reward_output_hash, gen_transaction=tx, gen_transaction_index=0)
    # return the block reward transaction
    return tx


@signals.worker_ready.connect
def mine(**kwargs):
    while True:
        print('Trying a block')
        unconfirmed_tx = Transaction.objects.filter(mined=False)

        if unconfirmed_tx:
            '''
            Handle race conditions (double spends)
            '''
            used_up_inputs = []
            to_del = []
            for tx in unconfirmed_tx:
                for inp in tx.inputs.all():
                    if inp.hash in used_up_inputs:
                        to_del.append(tx)
                        break
                    used_up_inputs.append(inp.hash)

            if to_del:
                for tx in to_del:
                    tx.delete()
                continue
            
            '''
            find the nonce
            '''
            nonce = 1
            prev_blk = Block.objects.first()
            block_idx = prev_blk.height + 1
            difficulty = math.ceil(block_idx / 5)
            block_reward = math.ceil(100/block_idx)

            reward_tx = gen_reward_transaction(block_reward, block_idx)

            unconfirmed_tx_hashed = map(lambda uncon_tx: uncon_tx.hash, unconfirmed_tx)
            hash_content = reward_tx.hash + reduce(lambda a,b: a+b, unconfirmed_tx_hashed, '')
            merkle_hash = hashlib.sha1(hash_content.encode()).hexdigest()

            num_transactions = unconfirmed_tx.count()+1

            while True:
                block_content = merkle_hash + str(block_idx) + str(num_transactions) + str(nonce)
                hash_with_nonce = hashlib.sha1(block_content.encode()).hexdigest()

                '''
                if nonce works, save the block. Else, try again.
                '''

                if hash_with_nonce.startswith('0'*difficulty):
                    print("Wooho...Block mined")
                    blk = Block.objects.create(hash=hash_with_nonce, merkle_hash=merkle_hash, prev_block=prev_blk, height=block_idx, num_transactions=num_transactions, hash_target_zeros=difficulty, nonce=str(nonce))
                    for tx in unconfirmed_tx:
                        tx.block = blk
                        tx.mined = True
                        tx.save()
                    reward_tx.block = blk
                    reward_tx.mined = True
                    reward_tx.save()
                    break
                else:
                    nonce += 1

        '''
        Some wait time between mining successive blocks
        '''
        time.sleep(60)
