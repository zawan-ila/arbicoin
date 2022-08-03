from django.db import models

# Create your models here.


class Block(models.Model):
    hash = models.CharField(max_length=100)
    merkle_hash = models.CharField(max_length=100)
    prev_blk_hash = models.CharField(max_length=100)
    unix_timestamp = models.IntegerField()
    height = models.IntegerField()
    num_transactions = models.IntegerField()
    hash_target_zeros = models.IntegerField()
    nonce = models.TextField()

    def __str__(self) -> str:
        return f"block hash {self.hash} with {self.num_transactions} transactions inside"
