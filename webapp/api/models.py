import json
import logging

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache


class HealthCheckRecord(models.Model):

    title = models.CharField(max_length=4000, db_index=True)
    url = models.CharField(max_length=4000)
    timestamp = models.DateTimeField()
    response_status = models.IntegerField()
    response_time = models.DecimalField(max_digits=19, decimal_places=10)

    class Meta:
        index_together = (('title', 'timestamp'))


class Config(models.Model):

    key = models.CharField(max_length=255, unique=True)
    value = models.CharField(max_length=1000)


class PostSaveHealthRecord(object):

    @staticmethod
    @receiver(post_save, sender=HealthCheckRecord)
    def post_save_process(sender, instance, **kwargs):
        post_save_health_record = PostSaveHealthRecord()
        post_save_health_record.trigger_error(instance)
        post_save_health_record.push_event(instance)

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

    def trigger_error(self, instance):
        error_count = cache.get(instance.title, default=0)
        config = self.get_cache()
        if instance.response_status != config['monitor'][instance.title]['expected_response']['status_code']:
            error_count += 1
            cache.set(instance.title, error_count)
        elif instance.response_status == config['monitor'][instance.title]['expected_response']['status_code']:
            cache.set(instance.title, 0)

    async def push_event(self, instance):
        from channels.layers import get_channel_layer
        channel_layer = get_channel_layer()
        await channel_layer.group_send('broadcast', {"type": "chat.system_message", "text": 'announcement_text'})
