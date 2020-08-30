import json
import logging

from asgiref.sync import async_to_sync
from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework import serializers
from .models import HealthCheckRecord


class HealthCheckRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = HealthCheckRecord
        fields = ['url', 'title', 'timestamp', 'response_status', 'response_time']


class PostSaveHealthRecord(object):

    @staticmethod
    @receiver(post_save, sender=HealthCheckRecord)
    def post_save_process(sender, instance, **kwargs):
        post_save_health_record = PostSaveHealthRecord()
        error_count = post_save_health_record.trigger_error(instance)
        post_save_health_record.push_event(instance, error_count)

    def get_cache(self):
        config = cache.get('config')
        if config is not None:
            return config
        with open('config.json', 'r') as f:
            try:
                json_data = json.load(f)
                cache.set('config', json_data)
            except Exception as e:
                logging.critical("Unable to load config.json data")
                logging.critical(e)

    def trigger_error(self, instance) -> int:
        error_count = cache.get(instance.title, default=0)
        config = self.get_cache()
        if instance.response_status != config['monitor'][instance.title]['expected_response']['status_code']:
            error_count += 1
            cache.set(instance.title, error_count)
        elif instance.response_status == config['monitor'][instance.title]['expected_response']['status_code']:
            cache.set(instance.title, 0)
        return error_count

    def push_event(self, instance, trigger_result):
        from channels.layers import get_channel_layer
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)('broadcast', {"type": "receive", "text": HealthCheckRecordSerializer(instance=instance).data, "status": self.get_status(trigger_result)})

    def get_status(self, trigger_result):
        if trigger_result >= self.get_cache()['config']['total_consecutive_failures_2_alert']:
            return 'Down'
        return 'Up'
