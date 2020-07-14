import json

from django_filters import rest_framework as filters
from main.models import Message, User
from rest_framework import authentication, generics, permissions, status, pagination


from .serializers import MessageSerializer, TestS
from user.serializers import UserSerializer
from django.db.models import Q


class ChatUsersList(generics.ListAPIView):
    queryset = Message.objects.all()
    # User.objects.all()
    serializer_class = MessageSerializer

    # def get_queryset(self):
    #     return self.queryset.filter(Q(sender_user__sender="92c502a1-fc44-4f67-b016-98b4909c3bc5") | Q(receiver_user__receiver="92c502a1-fc44-4f67-b016-98b4909c3bc5"))


class Test(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = TestS

    def get_queryset(self):
        return self.queryset.filter().order_by("receiver_user__timestamp")
