from django.contrib.auth import get_user_model
from rest_framework import authentication, generics, permissions, status
from rest_framework.response import Response
from user.serializers import (
    LoginSerializer,
    UserSerializer,
    FollowSerializer,
    RatingSerializer,
    ProfileSerializer,
    MyProfileSerializer,
)

from main.models import Follow, Profile, User, Rating


class SignupUserView(generics.ListCreateAPIView):
    """Create a new user in the system"""

    serializer_class = UserSerializer
    queryset = User.objects.all()

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response(user)

    def get(self, request):
        return self.list(request)


class UserCRUD(generics.RetrieveUpdateDestroyAPIView):
    """Create a new user in the system"""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "id"


class UpdateDeleteUserView(generics.RetrieveUpdateDestroyAPIView):
    """Update, Delete signup user info"""

    # authentication_classes = (authentication.TokenAuthentication,)
    # permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()
    lookup_field = "id"

    def put(self, request, id=None):

        return self.partial_update(request, id)

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

    serializer_class = MyProfileSerializer
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
    View that hanldes user unfollowing previous following
    """

    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        following = (request.data["following"],)
        data = Follow.objects.filter(
            following=following, follower=self.request.user.id
        ).delete()
        return Response({"follow": f"Unfollow successfull"}, status=status.HTTP_200_OK,)


class RatingAPIView(generics.ListCreateAPIView):
    """
    View to add new rating to the user
    """

    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def get_queryset(self):
        user_id = self.request.GET.get("user_id")
        return self.queryset.filter(user=user_id)


class RatingRUD(generics.RetrieveUpdateDestroyAPIView):
    """
    View to add new rating to the user
    """

    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    lookup_field = "ratingId"

    def get(self, request, ratingId=None):
        return self.retrieve(request, ratingId)

    def put(self, request, ratingId=None):
        return self.partial_update(request, ratingId)

    def delete(self, request, ratingId=None):
        # send custom deletion success message
        return self.destroy(request, ratingId)


class ProfileAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve and return authentication user"""

    # authentication_classes = (authentication.TokenAuthentication,)
    # permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    lookup_field = "user"
