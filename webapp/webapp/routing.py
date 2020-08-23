from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url

from api.consumer import HealthRecordConsumer

application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
    'websocket': URLRouter([
        url(r"^health-record/$", HealthRecordConsumer),
        url(r"", AsgiHandler),
    ])
})
