from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate
from utils.exceptions import ApiException


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200, required=True, write_only=True)
    password = serializers.CharField(max_length=200, required=True, write_only=True)

    def create(self, validated_data):
        user = authenticate(**validated_data)
        if not user:
            raise ApiException(message='Invalid credentials', status=401)
        return user
