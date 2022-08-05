from rest_framework import serializers
from .models import TxIn, TxOut, Transaction, AbstractTransactionComponent


class AbstractTransactionComponentModelSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AbstractTransactionComponent
        fields = ['value', 'own_addr']


class TxOutModelSerializer(AbstractTransactionComponentModelSerializer):

    class Meta(AbstractTransactionComponentModelSerializer.Meta):
        model = TxOut


class TxInModelSerializer(AbstractTransactionComponentModelSerializer):
    gen_tx_id = serializers.CharField(source='gen_tx.hash')

    class Meta(AbstractTransactionComponentModelSerializer.Meta):
        model = TxIn
        fields = AbstractTransactionComponentModelSerializer.Meta.fields + ['gen_tx_id', 'gen_tx_idx', 'signature']


class TransactionModelSerializer(serializers.ModelSerializer):

    inputs = TxInModelSerializer(many=True)
    outputs = TxOutModelSerializer(many=True)
    block_hash = serializers.ReadOnlyField(source='block.hash')

    class Meta:
        model = Transaction
        fields = ['hash', 'block_hash', 'tx_ins_ct', 'tx_outs_ct', 'inputs', 'outputs']
