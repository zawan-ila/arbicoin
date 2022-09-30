'''
Views for GETTING information about blocks
'''

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from blocks.serializers import BlockModelSerializer
from blocks.models import Block
from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination


class MyPaginationClass(PageNumberPagination):
    page_size = 7


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
    serializer_class = BlockModelSerializer
    pagination_class = MyPaginationClass

    def get_queryset(self):
        prefix = self.request.query_params['prefix']
        prefix_block_heights= [blk.height for blk in Block.objects.all() if prefix_match(prefix, blk)]
        return Block.objects.filter(height__in=prefix_block_heights)


class BlockHeightView(generics.RetrieveAPIView):
    '''
    Get a block based on its index/height
    '''
    queryset = Block.objects.all()
    serializer_class = BlockModelSerializer
    lookup_field = 'height'


def prefix_match(prefix, blk):
    blk_str_id = str(blk.height)
    return blk_str_id.startswith(prefix)
