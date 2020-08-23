from celery import Celery
from django.conf import settings
from collections import namedtuple
import os
import requests

# set the default Django settings module for the 'celery' program.


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webapp.settings')
app = Celery('tasks', broker='redis://localhost:6379/0')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task
def cleanup(*args, **kwargs):
    from django.utils.timezone import now
    from api.models import HealthCheckRecord, Config
    from datetime import timedelta
    config = Config.objects.get(key='retention')
    older_timestamp = now() - timedelta(**{config.value.split(' ')[1]: int(config.value.split(' ')[0])})
    HealthCheckRecord.objects.filter(timestamp__lt=older_timestamp).delete()


@app.task
def rest(*args, **kwargs):
    from django.utils.timezone import now
    from api.models import HealthCheckRecord
    request = kwargs['request']
    method = request.pop('method')
    timestamp = now()
    try:
        if str.lower(method) == 'get':
            response = requests.get(url=request['url'])
        if str.lower(method) == 'post':
            response = requests.post(url=request['url'])
        HealthCheckRecord.objects.create(title=kwargs['title'], url=request['url'], timestamp=timestamp,
                                         response_status=response.status_code,
                                         response_time=response.elapsed.total_seconds() * 1000)
    except Exception as ex:
        HealthCheckRecord.objects.create(title=kwargs['title'], url=request['url'], timestamp=timestamp,
                                         response_status=0,
                                         response_time=0)
