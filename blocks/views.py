from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from blocks.serializers import BlockModelSerializer
from blocks.models import Block


class BlockHashView(generics.RetrieveAPIView):
    queryset = Block.objects.all()
    serializer_class = BlockModelSerializer
    lookup_field = 'hash'


class ChainLengthView(APIView):
    queryset = Block.objects.all()
    serializer_class = BlockModelSerializer

    def get(self, request):
        len = self.queryset.count()
        return Response({"length": len})


class BlockLatestView(generics.GenericAPIView):
    queryset = Block.objects.all()

    def get(self, request, *args, **kwargs):
        latest_block = self.queryset.order_by("-timestamp").first()
        return Response(BlockModelSerializer(latest_block).data)


class AllBlocksView(generics.ListAPIView):
    queryset = Block.objects.all()
    serializer_class = BlockModelSerializer


class BlockIdView(generics.RetrieveAPIView):
    queryset = Block.objects.all()
    serializer_class = BlockModelSerializer
