from rest_framework import generics
from rest_framework.response import Response
from blocks.models import Block
from transactions.models import Transaction
from transactions.serializers import TransactionModelSerializer


class TransactionHashView(generics.RetrieveAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionModelSerializer
    lookup_field = 'hash'


class UnconfirmedTransactionView(generics.ListAPIView):
    queryset = Transaction.objects.filter(mined=False)
    serializer_class = TransactionModelSerializer


class TransactionIdView(generics.RetrieveAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionModelSerializer


class TransactionsCountView(generics.RetrieveAPIView):
    def get(self, request):
        count = 0
        for blk in Block.objects.all():
            count += blk.transactions.count()
        return Response({"length": count})


class AllTransactionsView(generics.RetrieveAPIView):
    queryset = Transaction.objects.filter(mined=True)

    def get(self, request):
        queryset = Transaction.objects.filter(mined=True)
        return Response(TransactionModelSerializer(queryset, many=True).data)
