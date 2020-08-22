from celery import Celery
from django.conf import settings
import os
import requests

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webapp.settings')
app = Celery('tasks', broker='redis://localhost:6379/0')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


@app.task
def rest(*args, **kwargs):
    response = requests.get("https://www.dollarmates.com")
    print(response.status_code)
    print(response.elapsed.total_seconds())