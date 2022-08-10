from rest_framework import generics
from blocks.models import Block
from blocks.serializers import BlockModelSerializer


class BlockViewApi(generics.RetrieveAPIView):
    queryset = Block.objects.all()
    serializer_class = BlockModelSerializer
