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


class DriverCounsumer(AsyncWebsocketConsumer):
    # opening connection
    async def connect(self):
        driver = self.scope['url_route']['kwargs']['room_name']
        self.room_name = '{}'.format(driver)

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
        driver = self.scope['url_route']['kwargs']['room_name']
        text_data_json = json.loads(text_data)
        id_key = text_data_json['id_key']
        start_place = text_data_json['start_place']
        source = text_data_json['source']
        destination = text_data_json['destination']
        final_place = text_data_json['final_place']
        user = text_data_json['user']
        time_ending = text_data_json['time_ending']
        expected_time = text_data_json['expected_time']
        distance = text_data_json['distance']
        price = text_data_json['price']
        status = text_data_json['status']
        trip_type = text_data_json['trip_type']
        price_after_coupon = text_data_json['price_after_coupon']
        trip_cancellation = text_data_json['trip_cancellation']
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'id_key':id_key,
                'type': 'tracking',
                'driver_id': driver,
                'start_place': start_place,
                'source': source,
                'status': status,
                'destination':destination,
                'final_place':final_place,
                'user':user,
                'time_ending':time_ending,
                'expected_time':expected_time,
                'distance':distance,
                'price':price,
                'trip_type':trip_type,
                'price_after_coupon':price_after_coupon,
                'trip_cancellation':trip_cancellation
            }
        )

    async def tracking(self, event):
        id_key = event['id_key']
        driver = event['driver_id']
        start_place = event['start_place']
        source = event['source']
        status = event['status']

        destination = event['destination']
        final_place = event['final_place']
        user = event['user']

        time_ending = event['time_ending']
        distance = event['distance']
        price = event['price']
        trip_type = event['trip_type']
        price_after_coupon = event['price_after_coupon']
        trip_cancellation = event['trip_cancellation']
        expected_time = event['expected_time']

        await self.send(text_data=json.dumps({
            'id':id_key,
            'driver_id': driver,
            'start_place': start_place,
            'source': source,
            'status':status,

            'destination': destination,
            'final_place': final_place,
            'user':user,

            'time_ending': time_ending,
            'distance': distance,
            'price':price,
            'trip_type': trip_type,
            'price_after_coupon':price_after_coupon,
            'trip_cancellation':trip_cancellation,
            'expected_time':expected_time
        }))