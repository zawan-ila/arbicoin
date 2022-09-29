import hashlib
from functools import reduce
from rest_framework.exceptions import ValidationError
from rest_framework import serializers
import ecdsa
from transactions.models import TransactionInput, TransactionOutput, Transaction, AbstractTransactionComponent


class AbstractTransactionComponentModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = AbstractTransactionComponent
        fields = ['value', 'own_addr']


class TransactionOutputModelSerializer(AbstractTransactionComponentModelSerializer):

    gen_transaction_id = serializers.ReadOnlyField(source='gen_transaction.hash')

    class Meta(AbstractTransactionComponentModelSerializer.Meta):
        model = TransactionOutput
        fields = AbstractTransactionComponentModelSerializer.Meta.fields + ['gen_transaction_id', 'gen_transaction_index']


class TransactionInputModelSerializer(AbstractTransactionComponentModelSerializer):
    gen_transaction_id = serializers.CharField(source='gen_transaction.hash')

    class Meta(AbstractTransactionComponentModelSerializer.Meta):
        model = TransactionInput
        fields = AbstractTransactionComponentModelSerializer.Meta.fields + ['gen_transaction_id', 'gen_transaction_index', 'signature']


class TransactionModelSerializer(serializers.ModelSerializer):

    inputs = TransactionInputModelSerializer(many=True)
    outputs = TransactionOutputModelSerializer(many=True)
    block_hash = serializers.ReadOnlyField(source='block.hash')
    block_num = serializers.ReadOnlyField(source='block.height')

    used_outputs = TransactionInputModelSerializer(many=True, read_only=True)

    class Meta:
        model = Transaction
        fields = ['hash', 'timestamp', 'block_hash', 'block_num', 'tx_inputs_count', 'tx_outputs_count', 'inputs', 'outputs', 'used_outputs']

    def validate_input(self, input):
        '''
        Take a serialized instance of TransactionInputModel, check if it is valid(exists) and 
        return its hash
        '''

        # value(worth) of the input
        val = input["value"]
        # address to which the input belongs
        addr = input["own_addr"]
        # hash of the transaction in which this input was created
        gen_tx_hash = input["gen_transaction"]["hash"]
        # index among the outputs of the generating transaction
        idx = input["gen_transaction_index"]

        # Check if the input above is valid i.e it exists in the database as a TransactionOutput
        match_utxos = TransactionOutput.objects.filter(value=val, own_addr=addr, gen_transaction__hash=gen_tx_hash, gen_transaction_index=idx)
        # if a matching output does not exist or it exists but is not mined yet, raise an error
        if not match_utxos:
            raise ValidationError("Referenced input(s) do not exist")

        # Now that the input is valid(no error was raised) we return its hash
        return hashlib.sha1((str(val)+addr+gen_tx_hash+str(idx)).encode()).hexdigest()

    def sign_status(self, msg, pk, sign):
        '''
        Given a message, public key(address), and a digital signature, check
        if the signature is valid 
        '''

        vk = ecdsa.VerifyingKey.from_string(bytes.fromhex(pk))
        return vk.verify(bytes.fromhex(sign), msg.encode())

    def validate(self, validated_data):

        '''
        Custom validation for posted transaction
        '''

        inputs = validated_data['inputs']
        outputs = validated_data['outputs']

        '''
        Check a little bit of structure
        '''

        if not validated_data["tx_inputs_count"] + validated_data["tx_outputs_count"]:
            '''
            Empty transactions not allowed
            '''
            raise ValidationError("Empty Transaction can not be posted")

        try:
            assert validated_data["tx_inputs_count"] == len(inputs)
            assert validated_data["tx_outputs_count"] == len(outputs)

        except AssertionError:
            raise ValidationError("Number of inputs and outputs specified should match the actual number of inputs and outputs")

        '''
        Check if sum of inputs is greater than equal to sum of outputs
        '''
        burnt = reduce(lambda x, y: x + y, map(lambda i: i["value"], inputs), 0)
        minted = reduce(lambda x, y: x + y, map(lambda o: o["value"], outputs), 0)

        if minted > burnt:
            raise ValidationError("Not enough coins")

        '''
        Check if all reference UTXOs are indeed valid, calculate and store hashes
        '''

        input_hashes = list(map(lambda i: self.validate_input(i), inputs))
        output_hashes = list(map(lambda o: hashlib.sha1((str(o["value"]) + o["own_addr"]).encode()).hexdigest(), outputs))

        for idx in range(len(inputs)):
            inputs[idx]['hash'] = input_hashes[idx]

        for idx in range(len(outputs)):
            outputs[idx]['hash'] = output_hashes[idx]

        '''
        Check signatures
        '''

        tx_hash_content = str(validated_data["tx_inputs_count"]) + reduce(lambda a,b: a+b, input_hashes, "") + \
                          str(validated_data["tx_outputs_count"]) + reduce(lambda a,b: a+b, output_hashes, "")
        
        tx_hash = hashlib.sha1(tx_hash_content.encode()).hexdigest()

        sign_statuses = map(lambda i: self.sign_status(tx_hash, i["own_addr"], i["signature"]), inputs)

        if not all(sign_statuses):
            raise ValidationError("One or more Signatures Do not Match")
        
        validated_data["tx_hash"] = tx_hash

        return validated_data

    def create(self, validated_data):
        inputs = validated_data['inputs']
        outputs = validated_data['outputs']

        '''
        Create the posted transaction. Update the database accordingly
        '''

        t = Transaction.objects.create(hash=validated_data['tx_hash'], tx_inputs_count=validated_data['tx_inputs_count'], tx_outputs_count=validated_data['tx_outputs_count'])

        for idx in range(len(inputs)):
            i = inputs[idx]
            gen_tx = Transaction.objects.filter(hash=i['gen_transaction']['hash']).first()
            TransactionInput.objects.create(value=i['value'], own_addr=i['own_addr'], gen_transaction=gen_tx, gen_transaction_index=i['gen_transaction_index'], spend_transaction_index=idx, spend_transaction=t, signature=i['signature'], hash=i['hash'])

            '''
            Now this is a used up utxo. So delete it
            '''
            txouts_to_delete = TransactionOutput.objects.filter(value=i['value'], own_addr=i['own_addr'], gen_transaction=gen_tx, gen_transaction_index=i['gen_transaction_index'])
            txouts_to_delete.delete()

        for idx in range(len(outputs)):
            o = outputs[idx]
            TransactionOutput.objects.create(value=o['value'], own_addr=o['own_addr'], gen_transaction=t, gen_transaction_index=idx, hash=o['hash'])

        return t
