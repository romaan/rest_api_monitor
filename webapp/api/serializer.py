from rest_framework import serializers


class TaskSerializer(serializers.Serializer):

    url = serializers.CharField()