from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response

from rest_framework import generics

from .models import Block
from .serializers import BlockModelSerializer


class BlockViewApi(generics.RetrieveAPIView):
    queryset = Block.objects.all()
    serializer_class = BlockModelSerializer
