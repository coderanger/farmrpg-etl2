from rest_framework import serializers

from .models import Emblem, Message


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


class EmblemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Emblem
        fields = [
            "id",
            "name",
            "image",
            "type",
            "keywords",
        ]
