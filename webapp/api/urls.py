from django.conf.urls import url
from .views import ConfigApi, HealthApi

urlpatterns = [
    url('config', ConfigApi.as_view()),
    url('health/(?P<title>.*)', HealthApi.as_view(), name='get-health-record')
]