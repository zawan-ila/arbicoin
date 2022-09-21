from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import generics, status

from rest_framework.exceptions import ValidationError
from transactions.models import Transaction, TransactionOutput
from rest_framework import permissions

from rest_framework.decorators import permission_classes


from transactions.serializers import TransactionModelSerializer, TransactionOutputModelSerializer

from .wallet_utils import create_simple_raw_transaction, owns


class TransactionCreateRawApiView(generics.CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionModelSerializer


@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated, ))
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
        return Response({"error": raw_tx_content})

    try:
        serializer = TransactionModelSerializer(data=raw_tx_content)
        serializer.is_valid(raise_exception=True)
        serializer.save()

    except ValidationError as e:
        return Response({"error": str(e.args[0]['non_field_errors'][0])})

    return Response({"success": "Your transaction is successful!"}, status=status.HTTP_201_CREATED)


class WalletInfoView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        addr = kwargs['own_addr']
        transactions = Transaction.objects.all()
        received = 0
        sent = 0
        for tx in transactions:
            for input in tx.inputs.all():
                if input.own_addr == addr:
                    sent += input.value
            for output in tx.outputs.all():
                if output.own_addr == addr:
                    received += output.value

        return Response({'received': received + sent, 'sent': sent, 'balance': received})


class WalletOwnView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]

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


class WalletTransactionsView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        wallet_addr = self.request.user.pubkey

        wallet_transactions = [tx.id for tx in Transaction.objects.all() if owns(wallet_addr, tx)]
        return Transaction.objects.filter(id__in=wallet_transactions)

    serializer_class = TransactionModelSerializer


class UnspentOutputsView(APIView):

    def get(self, request, own_addr):
        qs = TransactionOutput.objects.filter(own_addr=own_addr)
        return Response(TransactionOutputModelSerializer(qs, many=True).data)
