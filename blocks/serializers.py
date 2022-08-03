
from rest_framework import serializers

from transactions.serializers import TransactionModelSerializer
from .models import Block



class BlockModelSerializer(serializers.ModelSerializer):
    transactions = TransactionModelSerializer(many=True)

    class Meta:
        model = Block
        # fields = ['blk_hash', 'merkle_hash', 'prev_blk_hash', 'unix_timestamp', 'height', 'num_transactions', 'hash_target_zeros', 'nonce', 'transactions']
        fields = '__all__'