from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import TaskSerializer


class TaskApi(ListCreateAPIView):

    serializer_class = TaskSerializer

    def get(self, request, *args, **kwargs):
        return Response({"status": "ok"})

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_201_CREATED)