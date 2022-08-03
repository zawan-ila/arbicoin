import sys
from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
from rest_framework import generics
from rest_framework.response import Response
from .serializers import BlockModelSerializer
from .models import Block


class BlockHashView(generics.RetrieveAPIView):
    queryset = Block.objects.all()
    serializer_class = BlockModelSerializer
    lookup_field = 'hash'


class ChainLengthView(generics.RetrieveAPIView):
    queryset = Block.objects.all()
    serializer_class = BlockModelSerializer
    print('Hello', file=sys.stderr)

    def get(self, request):
        len = self.queryset.count()
        print('Hello', file=sys.stderr)
        return Response({"length": len})


class BlockLatestView(generics.RetrieveAPIView):
    queryset = Block.objects.all()
    # serializer_class = BlockModelSerializer

    def get(self, request, *args, **kwargs):
        latest_block = self.queryset.order_by("-unix_timestamp").first()
        return Response(BlockModelSerializer(latest_block).data)


class AllBlocksView(generics.ListAPIView):
    queryset = Block.objects.all()
    serializer_class = BlockModelSerializer
    # model = Block
    # print('Hello', file=sys.stderr)


class BlockViewApi(generics.RetrieveAPIView):
    queryset = Block.objects.all()
    serializer_class = BlockModelSerializer
