from django.db import models
from blocks.models import Block


class Transaction(models.Model):
    '''
    This represents a transaction(exchange of coins) on the blockchain
    '''

    hash = models.CharField(help_text='hash of the transaction for identification',max_length=40, editable=False, blank=True, null=True)
    block = models.ForeignKey(Block, help_text='block this transaction is part of', blank=True, null=True, on_delete=models.CASCADE, related_name='transactions')
    tx_inputs_count = models.PositiveIntegerField(blank=True, default=0, help_text='number of inputs in the transaction')
    tx_outputs_count = models.PositiveIntegerField(blank=True, default=0, help_text='number of outputs in the transaction')
    mined = models.BooleanField(default=False, help_text='has the transaction been mined')

    def __str__(self):
        block_info = self.block.hash if self.block else 'unmined'
        return f"transaction hash {self.hash} in block {block_info}"


class AbstractTransactionComponent(models.Model):
    '''
    This is an abstract model specifying the common functionality
    of transaction inputs and transaction outputs
    '''

    hash = models.CharField(max_length=40, editable=False, blank=True, null=True, help_text='hash of the transaction component')
    value = models.PositiveIntegerField(default=0, help_text='value of the component i.e how much is it worth')
    own_addr = models.CharField(max_length=100, help_text='owner of this component')
    gen_transaction_index = models.PositiveIntegerField(blank=True, null=True, help_text='output index in generating transaction')

    class Meta:
        abstract = True


class TransactionInput(AbstractTransactionComponent):
    '''
    This represents the inputs to a transactions. Inputs are coins that
    are spent in a transaction (i.e sent to somebody else)
    '''
    gen_transaction = models.ForeignKey(Transaction, blank=True, null=True, on_delete=models.CASCADE, help_text='transaction that generated this input')
    spend_transaction = models.ForeignKey(Transaction, blank=True, null=True, on_delete=models.CASCADE, related_name='inputs', help_text='transcation that spent this input')
    spend_transaction_index = models.PositiveIntegerField(default=0, help_text='input index in spending transaction')
    signature = models.TextField(help_text='digital signature for verification')

    def __str__(self):
        return f"generated in {self.gen_transaction.hash} spent in {self.spend_transaction.hash} value {self.value} \
        owner {self.own_addr}"


class TransactionOutput(AbstractTransactionComponent):
    '''
    This represents the outputs to a transaction. Outputs are the coins
    that are "created" in a transaction.
    '''
    gen_transaction = models.ForeignKey(Transaction, blank=True, null=True, on_delete=models.CASCADE, related_name='outputs')
    blk_height = models.PositiveIntegerField(blank=True, null=True, help_text='height of the block')

    def __str__(self):
        if self.gen_transaction:
            return f"gen in {self.gen_transaction.hash} value {self.value} owner {self.own_addr}"
        else:
            return f"output: value {self.value} owner {self.own_addr}"

