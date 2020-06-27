from django.contrib.auth import get_user_model
from rest_framework import authentication, generics, permissions, status
from rest_framework.response import Response
from user.serializers import (
    LoginSerializer,
    UserSerializer,
    FollowSerializer,
    UnFollowSerializer,
    RatingSerializer,
    ProfileSerializer,
    AddProfileSerializer,
)
from main.models import Follow


from django.contrib.gis.geoip2 import GeoIP2


class SignupUserView(generics.CreateAPIView):
    """Create a new user in the system"""

    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response(user)


class UpdateDeleteUserView(generics.RetrieveUpdateDestroyAPIView):
    """Update, Delete signup user info"""

    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()
    lookup_field = "id"

    def put(self, request, id=None):
        return self.update(request, id)

    def delete(self, request, id=None):
        return self.destroy(request, id)


class LoginAPIView(generics.CreateAPIView):
    """Login users with valid credintials"""

    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return serializer.validated_data


class AuthUserAPIView(generics.RetrieveAPIView):
    """Retrieve and return authentication user"""

    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authentication user"""
        return self.request.user


class FollowAPIView(generics.CreateAPIView):
    """
    View that hanldes user followers and followings
    """

    serializer_class = FollowSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        data = {
            "follower": self.request.user.id,
            "following": request.data["following"],
        }
        serializer = FollowSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            return serializer.validated_data


class UnfollowAPIView(generics.CreateAPIView):
    """
    View that hanldes user followers and followings
    """

    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UnFollowSerializer

    def post(self, request):
        data = {
            "follower": self.request.user.id,
            "following": request.data["following"],
        }
        serializer = UnFollowSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            return serializer.validated_data


class RagingAPIView(generics.CreateAPIView):
    """
    View to add new rating to the user
    """

    serializer_class = RatingSerializer


class AddProfileInfoAPIView(generics.CreateAPIView):
    """
    View to add new rating to the user
    """

    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = AddProfileSerializer

    def post(self, request):
        data = {
            "user": self.request.user.id,
            "telegram": request.data["telegram"],
            "facebook": request.data["facebook"],
        }

        g = GeoIP2()
        g.country(ip)
        g.country("google.com")

        serializer = AddProfileSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            return serializer.validated_data


class PrifileAPIView(generics.RetrieveUpdateAPIView):
    """Retrieve and return authentication user"""

    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProfileSerializer

    def get_object(self):
        """Retrieve and return authentication user"""
        return self.request.user


def get_client_ip(request):
    if "HTTP_X_FORWARDED_FOR" in request.META:
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip

