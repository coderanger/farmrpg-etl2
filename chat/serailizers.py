from rest_framework import serializers

from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Message
        fields = [
            "id",
            "room",
            "ts",
            "emblem",
            "username",
            "user_id",
            "content",
            "flags",
            "deleted",
            "deleted_ts",
        ]
