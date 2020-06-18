from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import UniqueValidator
from django.contrib.postgres.fields import JSONField
from utilities.exception_handler import CustomValidation
from main.models import User


class UserSerializer(serializers.ModelSerializer):
    """serializer for the users objects"""

    class Meta:
        model = User
        fields = ("id", "email", "password", "name", "location")
        extra_kwargs = {
            "password": {"write_only": True, "min_length": 8},
            "id": {"read_only": True},
        }

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        user = get_user_model().objects.create_user(**validated_data)
        token, created = Token.objects.get_or_create(user=user)
        return {
            "user": {"id": user.id, "name": user.name, "location": user.location},
            "token": token.key,
        }

    def update(self, instance, validated_data):
        """Update a user """
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class LoginSerializer(serializers.ModelSerializer):
    """serializer for user login"""

    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": "password"}, trim_whitespace=False
    )

    class Meta:
        model = get_user_model()
        fields = ("email", "password")

    def validate(self, data):
        """Validate user data"""
        user = authenticate(
            email=data.get("email", None), password=data.get("password", None)
        )

        if not user:
            raise CustomValidation(
                "detail", "Invalid Credentials", status.HTTP_401_UNAUTHORIZED
            )

        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                "user": {"id": user.id, "name": user.name, "location": user.location},
                "token": token.key,
            },
            status=status.HTTP_200_OK,
        )
