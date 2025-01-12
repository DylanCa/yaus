from django.contrib.auth.models import Group, User
from django.http import HttpResponse, Http404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, viewsets, status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.viewsets import GenericViewSet
from tutorial.quickstart.serializers import GroupSerializer, UserSerializer

from .models import ShortLink
from .serializers import ShortLinkSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class ShortlinkViewSet(viewsets.ModelViewSet):
    queryset = ShortLink.objects.all()
    serializer_class = ShortLinkSerializer

    def ok(self, request, *args, **kwargs):
        sl_list = [
            ShortLink(original_url = "674141414141426e65587039483054524a546e32394d4d68564d6c72632d50595773637132426e33516348476d4d485746375134326b4d535266757064627373374677307069423236465f344b767135484d617761525a526b4a764668783353796664576b6137524d5073567246312d483177636c6e593d",
                      passcode = "473287f8298dba7163a897908958f7c0eae733e25d2e027992ea2edc9bed2fa8",
                      salt = "14993c0aed9d7ee4089f82ac0c14c9b0",
                      redirect_string = "J3JDa",
            )
        ]

        sl = [el for el in sl_list if el.redirect_string == request]
        if len(sl) == 0:
            return Response("no url found")

        return Response(sl[0].decode_url(request))

class RedirectViewSet(GenericViewSet):
    @swagger_auto_schema(
        method="GET",
        manual_parameters=[
            openapi.Parameter(
                'passcode',
                openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
            )
        ],
    )
    @api_view(['GET'])
    @renderer_classes([JSONRenderer])
    def redirect_to(self, redirect_string):
        shortlink = ShortLink.objects.filter(redirect_string=redirect_string).first()
        if shortlink is None:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

        if shortlink.passcode is '':
            serializer = ShortLinkSerializer(shortlink, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)

        passcode = self.query_params.get('passcode')
        if shortlink.passcode and passcode is None:
            return Response({'error': 'No passcode provided'}, status=status.HTTP_400_BAD_REQUEST)

        original_url = shortlink.decode_url(passcode)
        return Response({'original_url': original_url}, status=status.HTTP_200_OK)
