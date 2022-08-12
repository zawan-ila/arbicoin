from django.db import models


class Block(models.Model):
    '''
    This represents a block in the blockchain
    '''
    hash = models.CharField(max_length=40)
    merkle_hash = models.CharField(max_length=40)
    prev_block = models.OneToOneField('self', null=True, blank=True, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)
    height = models.PositiveIntegerField()
    num_transactions = models.PositiveIntegerField()
    hash_target_zeros = models.PositiveIntegerField(help_text='difficulty of mining the block', default=0)
    nonce = models.TextField()

    def __str__(self) -> str:
        return f"block hash {self.hash} with {self.num_transactions} transactions inside"
