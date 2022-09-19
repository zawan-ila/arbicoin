from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import generics, status

from rest_framework.exceptions import ValidationError
from transactions.models import Transaction, TransactionOutput


from transactions.serializers import TransactionModelSerializer, TransactionOutputModelSerializer

from .wallet_utils import create_simple_raw_transaction


class TransactionCreateRawApiView(generics.CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionModelSerializer


@api_view(['POST'])
def TransactionCreateApiView(request):
    receiver = request.data['address']
    amount = request.data['value']

    try:
        amount = int(amount)
        if (amount <= 0):
            raise ValueError
    except ValueError:
        return Response({"error": "Amount should be a Positive Integer"})

    raw_tx_content = create_simple_raw_transaction(request.user.privkey, receiver, amount)

    if (isinstance(raw_tx_content, str)):
        return Response({"error": "Not enough coins available"})

    try:
        serializer = TransactionModelSerializer(data=raw_tx_content)
        serializer.is_valid(raise_exception=True)
        serializer.save()

    except ValidationError as e:
        return Response({"error": str(e.args[0]['non_field_errors'][0])})

    return Response({"success": "Your transaction is successful!"}, status=status.HTTP_201_CREATED)


class WalletInfoView(generics.RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        addr = kwargs['own_addr']
        confirmed_transactions = Transaction.objects.filter(mined=True)
        received = 0
        sent = 0
        for tx in confirmed_transactions:
            for input in tx.inputs.all():
                if input.own_addr == addr:
                    sent += input.value
            for output in tx.outputs.all():
                if output.own_addr == addr:
                    received += output.value

        return Response({'received': received + sent, 'sent': sent, 'balance': received})


class WalletOwnView(generics.RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        transactions = Transaction.objects.all()
        received = 0
        sent = 0
        addr = self.request.user.pubkey

        if addr:
            for tx in transactions:
                for input in tx.inputs.all():
                    if input.own_addr == addr:
                        sent += input.value
                for output in tx.outputs.all():
                    if output.own_addr == addr:
                        received += output.value

        return Response({'received': received + sent, 'sent': sent, 'balance': received, 'address': addr})


class UnspentOutputsView(APIView):

    def get(self, request, own_addr):
        qs = TransactionOutput.objects.filter(own_addr=own_addr).filter(gen_transaction__mined=True)
        return Response(TransactionOutputModelSerializer(qs, many=True).data)
