from rest_framework import generics
from transactions.models import Transaction
from transactions.serializers import TransactionModelSerializer


class TransactionViewApi(generics.RetrieveAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionModelSerializer
