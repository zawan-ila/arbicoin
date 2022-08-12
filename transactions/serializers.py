from rest_framework import serializers
from transactions.models import TransactionInput, TransactionOutput, Transaction, AbstractTransactionComponent


class AbstractTransactionComponentModelSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AbstractTransactionComponent
        fields = ['value', 'own_addr']


class TransactionOutputModelSerializer(AbstractTransactionComponentModelSerializer):

    class Meta(AbstractTransactionComponentModelSerializer.Meta):
        model = TransactionOutput


class TransactionInputModelSerializer(AbstractTransactionComponentModelSerializer):
    gen_tx_id = serializers.CharField(source='gen_transaction.hash')

    class Meta(AbstractTransactionComponentModelSerializer.Meta):
        model = TransactionInput
        fields = AbstractTransactionComponentModelSerializer.Meta.fields + ['gen_tx_id', 'gen_transaction_index', 'signature']


class TransactionModelSerializer(serializers.ModelSerializer):

    inputs = TransactionInputModelSerializer(many=True)
    outputs = TransactionOutputModelSerializer(many=True)
    block_hash = serializers.ReadOnlyField(source='block.hash')

    class Meta:
        model = Transaction
        fields = ['hash', 'block_hash', 'tx_inputs_count', 'tx_outputs_count', 'inputs', 'outputs']
