'''
Views for GETTING information about blocks
'''

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from blocks.serializers import BlockModelSerializer
from blocks.models import Block
from rest_framework import permissions


class BlockHashView(generics.RetrieveAPIView):
    '''
    Given the hash of a block, retrieve the block
    '''
    queryset = Block.objects.all()
    serializer_class = BlockModelSerializer
    lookup_field = 'hash'


class ChainLengthView(APIView):
    '''
    Get the length of the blockchain
    '''
    queryset = Block.objects.all()
    serializer_class = BlockModelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        len = self.queryset.count()
        return Response({"length": len})


class BlockLatestView(generics.GenericAPIView):
    '''
    Get the last mined block
    '''
    queryset = Block.objects.all()

    def get(self, request, *args, **kwargs):
        latest_block = self.queryset.order_by("-timestamp").first()
        return Response(BlockModelSerializer(latest_block).data)


class AllBlocksView(generics.ListAPIView):
    '''
    Get the whole blockchain i.e all the blocks 
    '''
    queryset = Block.objects.all()
    serializer_class = BlockModelSerializer
    permission_classes = [permissions.IsAuthenticated]


class BlockHeightView(generics.RetrieveAPIView):
    '''
    Get a block based on its index/height
    '''
    queryset = Block.objects.all()
    serializer_class = BlockModelSerializer
    lookup_field = 'height'
