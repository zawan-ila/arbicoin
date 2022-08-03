from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
from rest_framework import generics
from .serializers import TransactionModelSerializer
from .models import TxOut, TxIn, Transaction


class TransactionHashView(generics.RetrieveAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionModelSerializer
    lookup_field = 'hash'


class UnconfirmedTransactionView(generics.ListAPIView):
    queryset = Transaction.objects.filter(mined=False)
    serializer_class = TransactionModelSerializer


class TransactionViewApi(generics.RetrieveAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionModelSerializer