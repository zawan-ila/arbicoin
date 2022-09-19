from django.contrib.auth.hashers import make_password
from rest_framework.generics import CreateAPIView
from auth.serializers import UserSerializer


class SignupView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = []

    def perform_create(self, serializer):
        password = make_password(self.request.data["password"])
        serializer.save(password=password)
