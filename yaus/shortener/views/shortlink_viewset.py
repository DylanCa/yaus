from rest_framework import viewsets
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, ListModelMixin, DestroyModelMixin

from yaus.shortener.models.shortlink import ShortLink
from yaus.shortener.serializers.shortlink_serializer import ShortLinkSerializer


class ShortlinkViewSet(viewsets.GenericViewSet, CreateModelMixin, RetrieveModelMixin, ListModelMixin, DestroyModelMixin):
    queryset = ShortLink.objects.all()
    serializer_class = ShortLinkSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return ShortLink.objects.filter(owner=self.request.user).order_by("id")
        return []
