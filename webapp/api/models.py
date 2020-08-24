import json
import logging

from django.db import models



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

