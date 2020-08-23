from rest_framework import filters
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView

from api.models import HealthCheckRecord
from api.serializer import HealthCheckRecordSerializer
import json


class ConfigApi(APIView):

    def get(self, request, *args, **kwargs):
        with open('config.json', 'r') as f:
            json_data = json.load(f)
        return Response(data=json_data, status=status.HTTP_200_OK)


class HealthApi(ListAPIView):

    serializer_class = HealthCheckRecordSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['=url']
    ordering_fields = ['timestamp']
    default_limit = 10

    def get_queryset(self):
        return HealthCheckRecord.objects.filter(title=self.kwargs['title'])


