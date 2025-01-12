from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from yaus.shortener.models.shortlink import ShortLink
from yaus.shortener.serializers.shortlink_serializer import ShortLinkSerializer


class RedirectViewSet(GenericViewSet):
    @swagger_auto_schema(
        method="GET",
        manual_parameters=[
            openapi.Parameter(
                "passcode",
                openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
            )
        ],
    )
    @api_view(["GET"])
    @renderer_classes([JSONRenderer])
    def redirect_to(self, redirect_string):
        shortlink = ShortLink.objects.filter(redirect_string=redirect_string).first()
        if shortlink is None:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

        if shortlink.passcode is "":
            shortlink.increase_usage_count()
            return Response({"url": shortlink.original_url}, status=status.HTTP_200_OK)

        passcode = self.query_params.get("passcode")
        if shortlink.passcode and passcode is None:
            return Response(
                {"error": "No passcode provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        original_url = shortlink.decode_url(passcode)
        shortlink.increase_usage_count()
        return Response({"url": original_url}, status=status.HTTP_200_OK)
