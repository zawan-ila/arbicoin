from rest_framework import generics
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
