from rest_framework import serializers, status
from main.models import Message, User
from django.db.models import Q


class Test(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("avatar",)


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"


class UserListSerializers(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField("get_message")
    unread = serializers.SerializerMethodField("get_unread_message")

    class Meta:
        model = User
        fields = ("id", "name", "email", "avatar", "unread", "last_message")

    def get_unread_message(self, obj):
        return (
            Message.objects.filter(Q(receiver=obj) | Q(sender=obj))
            .filter(Q(receiver=self.context["id"]))
            .filter(Q(is_read=False))
            .count()
        )

    def get_message(self, obj):
        return (
            Message.objects.filter(Q(sender=obj) | Q(receiver=obj))
            .filter(Q(sender=self.context["id"]) | Q(receiver=self.context["id"]))
            .values()
            .last()
        )
