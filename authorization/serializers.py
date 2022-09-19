from authorization.models import MyUser
from rest_framework import serializers


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['username', 'password', 'pubkey']
        extra_kwargs = {
            'password': {
                'write_only': True
            },
            'pubkey': {
                'read_only': True
            }
        }
