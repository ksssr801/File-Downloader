from django.conf.urls import url
# from channels.auth import AuthMiddlewareStack
# from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator
from channels.routing import ProtocolTypeRouter, URLRouter
from filedownloadmanager.consumers import DownloadStreamer

application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
    'websocket': URLRouter(
        [url(r'ws/status', DownloadStreamer)]
        )

})