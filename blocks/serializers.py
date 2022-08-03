
from rest_framework import serializers

from transactions.serializers import TransactionModelSerializer
from .models import Block


class BlockModelSerializer(serializers.ModelSerializer):
    transactions = TransactionModelSerializer(many=True)
    prev_block_hash = serializers.ReadOnlyField(source='prev_block.hash')

    class Meta:
        model = Block
        fields = ['hash', 'merkle_hash', 'prev_block_hash', 'timestamp', 'height', 'num_transactions', 'hash_target_zeros', 'nonce', 'transactions']
