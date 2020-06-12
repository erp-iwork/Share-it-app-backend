from rest_framework import generics, authentication, permissions
from user.serializers import UserSerializer, LoginSerializer
from django.contrib.auth import get_user_model


class SignupUserView(generics.CreateAPIView):
    """Create a new user in the system"""

    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()


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
        if serializer.is_valid():
            return serializer.validated_data
        else:
            return Response({"errors": serializer.errors}, status=403)


class AuthUserAPIView(generics.RetrieveAPIView):
    """Retrieve and return authentication user"""

    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authentication user"""
        return self.request.user
