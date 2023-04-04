from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from google_sheets.supplies.models import Supply
from google_sheets.supplies.serializers import SupplySerializer


class IndexView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'index.html'

    def get(self, request, **kwargs):
        return Response({})


class SuppliesView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format='json', **kwargs):
        supplies = SupplySerializer(Supply.objects.all(), many=True)
        return Response(supplies.data, status=status.HTTP_200_OK)
