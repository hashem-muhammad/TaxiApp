import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async


class TrackingCounsumer(AsyncWebsocketConsumer):
    # opening connection
    async def connect(self):

        self.room_group_name = 'track_all_driver'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None):
        user = self.scope['user'].id
        text_data_json = json.loads(text_data)
        lat = text_data_json['lat']
        lng = text_data_json['lng']
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'tracking',
                'driver_id': user,
                'lat': lat,
                'lng': lng
            }
        )

    async def tracking(self, event):
        user = event['driver_id']
        lat = event['lat']
        lng = event['lng']

        await self.send(text_data=json.dumps({
            'driver_id': user,
            'lat': lat,
            'lng': lng
        }))


class TrackingDriverCounsumer(AsyncWebsocketConsumer):
    # opening connection
    async def connect(self):
        user = self.scope['user'].id
        other_user = self.scope['url_route']['kwargs']['room_name']
        if int(user) > int(other_user):
            self.room_name = '{}-{}'.format(user, other_user)
        else:
            self.room_name = '{}-{}'.format(other_user, user)

        self.room_group_name = self.room_name
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None):
        user = self.scope['user'].id
        text_data_json = json.loads(text_data)
        lat = text_data_json['lat']
        lng = text_data_json['lng']
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'tracking',
                'driver_id': user,
                'lat': lat,
                'lng': lng
            }
        )

    async def tracking(self, event):
        user = event['driver_id']
        lat = event['lat']
        lng = event['lng']

        await self.send(text_data=json.dumps({
            'driver_id': user,
            'lat': lat,
            'lng': lng
        }))