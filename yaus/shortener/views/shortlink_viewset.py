from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, renderer_classes, action
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    ListModelMixin,
    DestroyModelMixin,
)
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from yaus.shortener.models.shortlink import ShortLink
from yaus.shortener.serializers.shortlink_serializer import ShortLinkSerializer
from yaus.shortener.utils import Utils


class ShortlinkViewSet(
    viewsets.GenericViewSet, CreateModelMixin, ListModelMixin, DestroyModelMixin
):
    queryset = ShortLink.objects.all()
    serializer_class = ShortLinkSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return ShortLink.objects.filter(
                owner=self.request.user, deleted_at__isnull=True
            ).order_by("id")
        return []

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "passcode",
                openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
            )
        ],
    )
    @action(detail=False, methods=["GET"])
    @renderer_classes([JSONRenderer])
    def batch_unlock(self, request):
        passcode = request.query_params.get("passcode")

        if passcode is None:
            return Response(
                {"error": "Missing passcode"}, status=status.HTTP_400_BAD_REQUEST
            )

        encoded_passcode = Utils.encode_sha256(passcode)
        queryset = self.get_queryset()
        if len(queryset) > 0:
            shortlinks = queryset.filter(passcode=encoded_passcode)

            for link in shortlinks:
                link.original_url = link.decode_url(passcode)

            serializer = ShortLinkSerializer(shortlinks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_200_OK)
