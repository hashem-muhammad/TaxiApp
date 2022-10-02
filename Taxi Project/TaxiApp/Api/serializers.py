from django.db import transaction
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from Api.models import CarType, Driver, DriverCar, DriverLocation, Role, StopPoint, Trip, TripType, Message, Price, Coupon


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        data['phone_number'] = self.user.phone_number
        data['role'] = self.user.role.id
        return data


class CustomRegisterSerializer(RegisterSerializer):
    name = serializers.CharField(max_length=150)
    phone_number = serializers.CharField(max_length=30)
    role = serializers.IntegerField()

    # Define transaction.atomic to rollback the save operation in case of error
    @transaction.atomic
    def save(self, request):
        user = super().save(request)
        user.phone_number = self.data.get('phone_number')
        get_role = Role.objects.get(id=self.data.get('role'))
        user.role = get_role
        user.name = self.data.get('name')
        user.save()
        return user


class TripTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = TripType
        fields = ['id', 'type', ]


class CarTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = CarType
        fields = ['id', 'type', ]


class StopPointSerializer(serializers.ModelSerializer):

    class Meta:
        model = StopPoint
        fields = ['id', 'lat', 'lng', ]


class TripSerializer(serializers.ModelSerializer):

    class Meta:
        model = Trip
        fields = ['id', 'start_place', 'final_place',
                  'driver', 'time', 'distance', 'price', ]


class DriverLocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = DriverLocation
        fields = ['id', 'lat', 'lng', ]


class DriverCarSerializer(serializers.ModelSerializer):

    class Meta:
        model = DriverCar
        fields = ['id', 'car_model', 'car_color',
                  'car_year', 'plate_number', 'passengers_number', 'children_seat', ]


class DriverSerializer(serializers.ModelSerializer):

    class Meta:
        model = Driver
        fields = ['id', 'user', 'photo',
                  'car_type', 'car', 'license_number', 'license_image_front', 'license_image_back', 'available', ]


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ['id', 'user', 'message', 'status', ]


class CouponSerializer(serializers.ModelSerializer):

    class Meta:
        model = Coupon
        fields = ['id', 'fixed', 'start_date', 'end_date', ]
