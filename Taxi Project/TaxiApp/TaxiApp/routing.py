from django.urls import re_path
from Api.tracking import TrackingCounsumer, TrackingDriverCounsumer

websocket_url = [
    re_path(r'ws/tracking/(?P<room_name>\w+)/$', TrackingCounsumer.as_asgi()),
    re_path(r'ws/tracking/driver/(?P<room_name>\w+)/$', TrackingDriverCounsumer.as_asgi()),
]
