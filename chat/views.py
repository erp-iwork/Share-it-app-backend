import json

from django_filters import rest_framework as filters
from main.models import Message, User
from rest_framework import (
    authentication,
    generics,
    permissions,
    status,
    pagination,
)


from .serializers import MessageSerializer, UserListSerializers
from user.serializers import UserSerializer
from django.db.models import Q
from django.db.models import Max, Subquery, OuterRef, Count, Min, Value, F, Case, When
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models.functions import Coalesce


class MessageList(generics.ListAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def get_queryset(self):
        userOne = self.request.GET.get("sender")
        userTwo = self.request.GET.get("receiver")
        self.queryset.filter(Q(sender=userOne) | Q(receiver=userOne)).filter(
            Q(sender=userTwo) | Q(receiver=userTwo)
        ).update(is_read=True)
        return (
            self.queryset.filter(Q(sender=userOne) | Q(receiver=userOne))
            .filter(Q(sender=userTwo) | Q(receiver=userTwo))
            .order_by("-timestamp")
        )


class UserList(APIView):
    def get(self, request):

        id = self.request.GET.get("id")
        users = (
            User.objects.exclude(id=id)
            .annotate(receiver_message_time=Max("sender_user__timestamp"))
            .order_by("-receiver_message_time")
        )

        qs = UserListSerializers(users, many=True, context={"id": id})

        return Response(qs.data)

