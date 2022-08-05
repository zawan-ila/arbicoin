from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response

from rest_framework import generics

from .models import Transaction
from .serializers import TransactionModelSerializer


class TransactionViewApi(generics.RetrieveAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionModelSerializer
