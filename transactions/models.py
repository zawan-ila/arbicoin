from django.db import models

# Create your models here.
from blocks.models import Block


class Transaction(models.Model):
    '''
    This represents a transaction(exchange of coins) on the blockchain
    '''
    hash = models.CharField(max_length=100, blank=True, null=True)
    block = models.ForeignKey(Block, blank=True, null=True, on_delete=models.CASCADE, related_name='transactions')
    tx_ins_ct = models.IntegerField(blank=True, default=0)
    tx_outs_ct = models.IntegerField(blank=True, default=0)
    mined = models.BooleanField(default=False)

    def __str__(self):
        return f"tx hash {self.hash} in block {self.block}"


class AbstractTransactionComponent(models.Model):
    '''
    This is an abstract model specifying the common functionality
    of transaction inputs and transaction outputs
    '''
    hash = models.CharField(max_length=100, blank=True, null=True)
    value = models.IntegerField(default=0)
    own_addr = models.CharField(max_length=100)
    gen_tx_idx = models.IntegerField(blank=True, null=True)

    class Meta:
        abstract = True


class TxIn(AbstractTransactionComponent):
    '''
    This represents the inputs to a transactions. Inputs are coins that
    are spent in a transaction (i.e sent to somebody else)
    '''
    gen_tx = models.ForeignKey(Transaction, blank=True, null=True, on_delete=models.CASCADE)
    spend_tx = models.ForeignKey(Transaction, blank=True, null=True, on_delete=models.CASCADE, related_name='inputs')
    spend_tx_idx = models.IntegerField(default=0)
    signature = models.TextField()

    def __str__(self):
        return f"gen in {self.gen_tx} spent in {self.spend_tx} value {self.value} \
        owner {self.own_addr}"


class TxOut(AbstractTransactionComponent):
    '''
    This represents the outputs to a transaction. Outputs are the coins
    that are "created" in a transaction.
    '''
    gen_tx = models.ForeignKey(Transaction, blank=True, null=True, on_delete=models.CASCADE, related_name='outputs')
    blk_height = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"gen in {self.gen_tx} value {self.value} owner {self.own_addr}"
