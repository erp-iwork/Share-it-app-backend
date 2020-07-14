from rest_framework import serializers, status
from main.models import Message, User


# from drf_extra_fields.geo_fields import PointField


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"
        depth = 1


class TestS(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
