from rest_framework import serializers

from .models import Location


class LocationHTMLSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = [
            "game_id",
            "type",
            "name",
            "image",
        ]
