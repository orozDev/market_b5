from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.auth.serializers import LoginSerializer, ProfileSerializer


@api_view(['POST'])
def login_api(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    email = serializer.validated_data.get('email')
    password = serializer.validated_data.get('password')

    user = authenticate(email=email, password=password)
    if user:
        read_serializer = ProfileSerializer(instance=user, context={'request': request})
        # token, created = Token.objects.get_or_create(user=user)
        token = Token.objects.get_or_create(user=user)[0].key

        data = {
            **read_serializer.data,
            'token': token
        }

        return Response(data)

    return Response({'detail': 'The user does not exist or the password is incorrect'}, status.HTTP_401_UNAUTHORIZED)