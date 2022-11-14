import django
from dotenv import load_dotenv
load_dotenv()
django.setup()
import os

from django.core.asgi import get_asgi_application
from TaxiApp.channelsmiddleware import WebSocketJWTAuthMiddleware
from TaxiApp.routing import websocket_url
from channels.routing import ProtocolTypeRouter, URLRouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TaxiApp.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': WebSocketJWTAuthMiddleware(
        URLRouter(websocket_url)
    )
})
