from django.db import transaction
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from Api.models import CarType, Complain, Driver, DriverCar, DriverLocation, DriverReview, Role, StopPoint, Trip, TripCancellation, TripReview, TripType, Message, Price, Coupon


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
        fields = ['id', 'type', 'price', ]


class StopPointSerializer(serializers.ModelSerializer):

    class Meta:
        model = StopPoint
        fields = ['id', 'lat', 'lng', ]


class TripCancellationSerializer(serializers.ModelSerializer):

    class Meta:
        model = TripCancellation
        fields = ['id', 'reason', ]


class TripSerializer(serializers.ModelSerializer):
    trip_cancellation = TripCancellationSerializer(many=True)

    class Meta:
        model = Trip
        fields = ['id', 'start_place', 'final_place',
                  'driver', 'time_ending', 'distance', 'price',
                  'trip_type',
                  'expected_time',
                  'price_after_coupon',
                  'trip_cancellation', 'status', 'user', ]

    def create(self, validated_data):
        trip_data = validated_data.pop('trip_cancellation')
        trip = Trip.objects.create(**validated_data)
        for t_data in trip_data:
            TripCancellation.objects.create(trip=trip, **t_data)
        return trip


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
        fields = ['id', 'value', 'coupon', 'start_date', 'end_date', ]


class PriceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Price
        fields = ['id', 'km_price', 'wait_price',
                  'tax_price', 'extra_price', 'company_per', ]


class ComplainSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False)

    class Meta:
        model = Complain
        fields = ['id', 'user', 'image', 'complain', ]


class TripReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = TripReview
        fields = ['id', 'user_id', 'driver_id', 'review', ]


class DriverReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = DriverReview
        fields = ['id', 'user_id', 'driver_id', 'review', ]
