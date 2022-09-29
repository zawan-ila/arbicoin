from django.contrib.auth.hashers import make_password
from rest_framework.generics import CreateAPIView
from authorization.serializers import MyUserSerializer

import ecdsa


class SignupView(CreateAPIView):
    serializer_class = MyUserSerializer
    permission_classes = []

    def perform_create(self, serializer):
        password = make_password(self.request.data["password"])
        sk = ecdsa.SigningKey.generate()
        pk = sk.verifying_key
        skhex = sk.to_string().hex()
        pkhex = pk.to_string().hex()

        serializer.save(password=password, pubkey=pkhex, privkey=skhex)
