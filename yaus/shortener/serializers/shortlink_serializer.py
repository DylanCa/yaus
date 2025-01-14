from datetime import datetime

from rest_framework import serializers

from yaus.shortener.models.shortlink import ShortLink
from yaus.shortener.utils import Utils


class ShortLinkSerializer(serializers.ModelSerializer):
    passcode = serializers.CharField(required=False, write_only=True)
    owner = serializers.ReadOnlyField(source="owner.id")

    class Meta:
        model = ShortLink
        fields = [
            "id",
            "original_url",
            "passcode",
            "redirect_string",
            "owner",
            "usage_count",
        ]
        read_only_fields = ["id", "redirect_string", "usage_count"]

    def validate(self, attrs):
        user = self.context["request"].user
        if user.is_authenticated:
            attrs["owner"] = user

        return attrs

    def create(self, validated_data):
        shortlink = ShortLink(**validated_data)
        if validated_data.get("passcode"):
            shortlink.encode_fields()
        shortlink.save()
        return shortlink
