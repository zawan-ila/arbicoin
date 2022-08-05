from django.db import models

# Create your models here.
from blocks.models import Block


class Transaction(models.Model):
    '''
    This represents a transaction(exchange of coins) on the blockchain
    '''

    # hash of the transaction uniquely identifies it
    hash = models.CharField(max_length=40, editable=False, blank=True, null=True)

    # block this transaction is part of (if it has been mined that is)
    block = models.ForeignKey(Block, blank=True, null=True, on_delete=models.CASCADE, related_name='transactions')

    # number of inputs in the transaction
    tx_ins_ct = models.PositiveIntegerField(blank=True, default=0)

    # number of outputs in the transaction
    tx_outs_ct = models.PositiveIntegerField(blank=True, default=0)

    # track if the transaction has been mined
    mined = models.BooleanField(default=False)

    def __str__(self):
        return f"tx hash {self.hash} in block {self.block.hash}"


class AbstractTransactionComponent(models.Model):
    '''
    This is an abstract model specifying the common functionality
    of transaction inputs and transaction outputs
    '''

    # hash of the transaction component
    hash = models.CharField(max_length=40, editable=False, blank=True, null=True)

    # value of the component i.e how much is it worth
    value = models.PositiveIntegerField(default=0)

    # who owns/owned this component
    own_addr = models.CharField(max_length=100)

    # in the transaction that generated this component, what was its index among all outputs
    gen_tx_idx = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        abstract = True


class TxIn(AbstractTransactionComponent):
    '''
    This represents the inputs to a transactions. Inputs are coins that
    are spent in a transaction (i.e sent to somebody else)
    '''
    gen_tx = models.ForeignKey(Transaction, blank=True, null=True, on_delete=models.CASCADE)
    spend_tx = models.ForeignKey(Transaction, blank=True, null=True, on_delete=models.CASCADE, related_name='inputs')
    spend_tx_idx = models.PositiveIntegerField(default=0)
    signature = models.TextField()

    def __str__(self):
        return f"generated in {self.gen_tx.hash} spent in {self.spend_tx.hash} value {self.value} \
        owner {self.own_addr}"


class TxOut(AbstractTransactionComponent):
    '''
    This represents the outputs to a transaction. Outputs are the coins
    that are "created" in a transaction.
    '''
    gen_tx = models.ForeignKey(Transaction, blank=True, null=True, on_delete=models.CASCADE, related_name='outputs')
    blk_height = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return f"gen in {self.gen_tx.hash} value {self.value} owner {self.own_addr}"
