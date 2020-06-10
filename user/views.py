from rest_framework import generics
from user.serializers import UserSerializer
from django.contrib.auth import get_user_model


class CreateUserView(generics.ListCreateAPIView):
    """Create a new user in the system"""

    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()

    def get(self, request):
        return self.list(request)


class GetUpdateDeleteUserView(generics.RetrieveUpdateDestroyAPIView):
    """Update, Delete and Get single user from the system"""

    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()
    lookup_field = "id"

    def get(self, request, id=None):
        return self.retrieve(request, id)

    def put(self, request, id=None):
        return self.update(request, id)

    def delete(self, request, id=None):
        return self.destroy(request, id)
