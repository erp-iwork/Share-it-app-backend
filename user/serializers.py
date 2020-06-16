from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from django.contrib.postgres.fields import JSONField


class UserSerializer(serializers.ModelSerializer):
    """serializer for the users objects"""

    email = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    name = serializers.CharField(write_only=True)
    location = serializers.CharField(write_only=True)
    user = serializers.JSONField(read_only=True)
    token = serializers.CharField(read_only=True)

    class Meta:
        model = get_user_model()
        fields = ("email", "password", "name", "location", "user", "token")
        extra_kwargs = {"password": {"write_only": True, "min_length": 8}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        user = get_user_model().objects.create_user(**validated_data)
        token, created = Token.objects.get_or_create(user=user)
        return {
            "user": {"name": user.name, "location": user.location},
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

    email = serializers.CharField()
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
            return Response(
                {"errors": {"Unauthorized": "Invalid Credentials"}},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        if not user.is_active:
            return Response({"errors": "This user has been deactivated."})

        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                "user": {"name": user.name, "location": user.location},
                "token": token.key,
            },
            status=status.HTTP_200_OK,
        )
