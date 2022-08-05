from django.db import models

# Create your models here.


class Block(models.Model):
    '''
    This represents a block in the blockchain
    '''
    hash = models.CharField(max_length=40, editable=False)
    merkle_hash = models.CharField(max_length=40, editable=False)
    prev_block = models.OneToOneField('self', null=True, blank=True, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)
    height = models.PositiveIntegerField()
    num_transactions = models.PositiveIntegerField()
    hash_target_zeros = models.PositiveIntegerField()
    nonce = models.TextField(editable=False)

    def __str__(self) -> str:
        return f"block hash {self.hash} with {self.num_transactions} transactions inside"
