from rest_framework import serializers
from .models import TxIn, TxOut, Transaction


class TxOutModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = TxOut
        fields = ['value', 'own_addr']


class TxInModelSerializer(serializers.ModelSerializer):
    gen_tx_id = serializers.CharField(source='gen_tx.hash')

    class Meta:
        model = TxIn
        fields = ['value', 'own_addr', 'gen_tx_id', 'gen_tx_idx', 'signature']


class TransactionModelSerializer(serializers.ModelSerializer):

    inputs = TxInModelSerializer(many=True)
    outputs = TxOutModelSerializer(many=True)
    blk_hash = serializers.ReadOnlyField(source='block.hash')

    class Meta:
        model = Transaction
        fields = ['hash', 'blk_hash', 'tx_ins_ct', 'tx_outs_ct', 'inputs', 'outputs']