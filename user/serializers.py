from django.contrib.auth import authenticate, get_user_model
from django.contrib.postgres.fields import JSONField
from main.models import User, Follow
from rest_framework import serializers, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.validators import UniqueValidator
from utilities.exception_handler import CustomValidation


class UserSerializer(serializers.ModelSerializer):
    """serializer for the users objects"""

    image = serializers.ImageField(
        max_length=None, use_url=True, allow_null=True, required=False
    )
    following = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "image",
            "password",
            "name",
            "location",
            "following",
            "followers",
            "following_count",
            "followers_count",
        )
        extra_kwargs = {
            "password": {"write_only": True, "min_length": 8},
            "id": {"read_only": True},
        }

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        user = get_user_model().objects.create_user(**validated_data)
        token, created = Token.objects.get_or_create(user=user)
        data = LoggedInUserSerializer(user)
        return {
            "user": data.data,
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

    def get_following(self, obj):
        return FollowingSerializer(obj.following.all(), many=True).data

    def get_followers(self, obj):
        return FollowersSerializer(obj.followers.all(), many=True).data

    def get_following_count(self, instance):
        return instance.following.count()

    def get_followers_count(self, instance):
        return instance.followers.count()


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
        data = LoggedInUserSerializer(user)
        return Response(
            {"user": data.data, "token": token.key,}, status=status.HTTP_200_OK,
        )


class LoggedInUserSerializer(serializers.ModelSerializer):
    """
    return the logged in user info
    """

    class Meta:
        model = User
        fields = ("id", "name", "location", "image", "zip_code")


class FollowingSerializer(serializers.ModelSerializer):
    """
    list the users followed by this user
    """

    class Meta:
        model = Follow
        fields = ("id", "following", "follow_time")


class FollowersSerializer(serializers.ModelSerializer):
    """
    list the users followers
    """

    class Meta:
        model = Follow
        fields = ("id", "follower", "follow_time")


class FollowSerializer(serializers.ModelSerializer):
    """
    Follow and UnFollow serializer
    """

    class Meta:
        model = Follow
        fields = "__all__"

    def validate(self, data):
        """
        validate self follow
        """
        following = data.get("following", None)
        follower = data.get("follower", None)
        if following == follower:
            raise serializers.ValidationError(
                {"follow": "users can't follow themselves"}
            )
        data = Follow.objects.create(**data)
        return Response(
            {"follow": f"You are now following {data.following}"},
            status=status.HTTP_200_OK,
        )

