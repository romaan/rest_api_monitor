from django.conf.urls import url
from .views import TaskApi

urlpatterns = [
    url('tasks', TaskApi.as_view())
]