from django.contrib.auth.models import Group, User
from rest_framework import serializers

from . import Utils
from .models import ShortLink


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class ShortLinkSerializer(serializers.ModelSerializer):
    passcode = serializers.CharField(required=False, write_only=True)

    class Meta:
        model = ShortLink
        fields = ['original_url', 'passcode', 'redirect_string']
        read_only_fields = ['redirect_string']

    def create(self, validated_data):
        shortlink = ShortLink(**validated_data)
        if validated_data.get('passcode'):
            shortlink.encode_fields()
        shortlink.redirect_string = Utils.generate_redirect_string()
        shortlink.save()
        return shortlink
