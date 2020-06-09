from rest_framework import generics
from user.serializers import UserSerializer
from django.contrib.auth import get_user_model


class CreateUserView(generics.ListCreateAPIView):
    """Create a new user in the system"""

    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()

    def get(self, request):
        return self.list(request)
