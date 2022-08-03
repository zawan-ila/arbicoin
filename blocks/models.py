from django.db import models

# Create your models here.


class Block(models.Model):
    '''
    This represents a block in the blockchain
    '''
    hash = models.CharField(max_length=100)
    merkle_hash = models.CharField(max_length=100)
    prev_block = models.OneToOneField('self', null=True, blank=True, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    height = models.IntegerField()
    num_transactions = models.IntegerField()
    hash_target_zeros = models.IntegerField()
    nonce = models.TextField()

    def __str__(self) -> str:
        return f"block hash {self.hash} with {self.num_transactions} transactions inside"
