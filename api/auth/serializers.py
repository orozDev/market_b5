from rest_framework import serializers

from account.models import User


class LoginSerializer(serializers.Serializer):

    email = serializers.CharField()
    password = serializers.CharField()


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'get_full_name',
            'first_name',
            'last_name',
            'email',
            'phone',
            'avatar',
            'role',
        )