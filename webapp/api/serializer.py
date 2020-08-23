from rest_framework import serializers

from api.models import HealthCheckRecord


class HealthCheckRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = HealthCheckRecord
        fields = ['url', 'timestamp', 'response_status', 'response_time']
