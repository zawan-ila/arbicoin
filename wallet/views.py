from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from transactions.models import Transaction, TransactionOutput
from transactions.serializers import TransactionModelSerializer, TransactionOutputModelSerializer


class TransactionCreateApiView(generics.CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionModelSerializer


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


class UnspentOutputsView(APIView):

    def get(self, request, own_addr):
        qs = TransactionOutput.objects.filter(own_addr=own_addr).filter(gen_transaction__mined=True)
        return Response(TransactionOutputModelSerializer(qs, many=True).data)
