from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import (
    get_object_or_404,
    GenericAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveAPIView,
    RetrieveDestroyAPIView,
    RetrieveUpdateDestroyAPIView,
    DestroyAPIView,
    UpdateAPIView,
)
from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
    UpdateModelMixin,
)

from api.auth.serializers import LoginSerializer, ProfileSerializer


@api_view(["POST"])
def login_api(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    email = serializer.validated_data.get("email")
    password = serializer.validated_data.get("password")

    user = authenticate(email=email, password=password)
    if user:
        read_serializer = ProfileSerializer(instance=user, context={"request": request})
        # token, created = Token.objects.get_or_create(user=user)
        token = Token.objects.get_or_create(user=user)[0].key

        data = {**read_serializer.data, "token": token}

        return Response(data)

    return Response(
        {"detail": "The user does not exist or the password is incorrect"},
        status.HTTP_401_UNAUTHORIZED,
    )


class LoginApiViews(GenericAPIView):
    serializer_class = [LoginSerializer, ProfileSerializer]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")

        user = authenticate(email=email, password=password)

        if not user:
            return Response(
                {"detail": "The user does not exist or the password is incorrect"},
                status.HTTP_401_UNAUTHORIZED,
            )
        
        read_serializer = self.get_serializer(index=1,instance=user)
        
        token = Token.objects.get_or_create(user=user)[0].key

        data = {**read_serializer.data, "token": token}

        return Response(data)
        


    def get_serializer(self, index=0, *args, **kwargs):

        serializer_class = self.get_serializer_class()
        kwargs.setdefault("context", self.get_serializer_context())
        return serializer_class[index](*args, **kwargs)
