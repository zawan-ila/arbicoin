from rest_framework import generics
from rest_framework.response import Response
from blocks.models import Block
from transactions.models import Transaction
from transactions.serializers import TransactionModelSerializer
from rest_framework.pagination import PageNumberPagination


class MyPaginationClass(PageNumberPagination):
    page_size = 7


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


class AllTransactionsView(generics.ListAPIView):
    serializer_class = TransactionModelSerializer
    pagination_class = MyPaginationClass

    def get_queryset(self):
        prefix = self.request.query_params['prefix']
        return Transaction.objects.filter(hash__startswith=prefix).order_by('-timestamp')
