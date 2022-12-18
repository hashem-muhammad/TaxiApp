from django.db import transaction
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from Api.models import AccountActivation, CarType, Complain, Driver, DriverLocation, DriverReview, Driverbalance, Places, Role, StopPoint, Trip, TripCancellation, TripReview, TripType, Message, Price, Coupon, User


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['id'] = self.user.id
        data['first_name'] = self.user.first_name
        data['last_name'] = self.user.last_name
        data['phone_number'] = self.user.phone_number
        data['birth_date'] = self.user.birth_date
        data['gender'] = self.user.gender
        data['firebase_token'] = self.user.firebase_token
        data['profile_image'] = self.user.profile_image.url if self.user.profile_image else ''
        data['role'] = self.user.role.id
        return data


class UserInfoSerializer(serializers.ModelSerializer):
    profile_image = Base64ImageField(required=False)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name',
                  'phone_number', 'birth_date', 'gender', 'profile_image', 'firebase_token',]


class UserNotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['firebase_token',]

class CustomRegisterSerializer(RegisterSerializer):
    phone_number = serializers.CharField(max_length=30)
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    firebase_token = serializers.CharField(max_length=255)
    role = serializers.IntegerField()

    # Define transaction.atomic to rollback the save operation in case of error
    @transaction.atomic
    def save(self, request):
        user = super().save(request)
        user.phone_number = self.data.get('phone_number')
        user.first_name = self.data.get('first_name')
        user.last_name = self.data.get('last_name')
        user.firebase_token = self.data.get('firebase_token')
        get_role = Role.objects.get(id=self.data.get('role'))
        user.role = get_role
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



class TripSerializer(serializers.ModelSerializer):

    class Meta:
        model = Trip
        fields = ['id', 'start_place', 'final_place',
                  'driver', 'time_ending', 'distance', 'price',
                  'trip_type',
                  'expected_time',
                  'price_after_coupon',
                  'trip_cancellation', 'status', 'user', 'source', 'destination', ]


class DriverLocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = DriverLocation
        fields = ['id', 'lat', 'lng', ]


class DriverSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(
        read_only=True, source='user.first_name')
    last_name = serializers.CharField(read_only=True, source='user.last_name')
    phone = serializers.CharField(read_only=True, source='user.phone_number')
    photo = Base64ImageField(required=False)
    image_car = Base64ImageField(required=False)
    license_image_front = Base64ImageField(required=False)
    license_image_back = Base64ImageField(required=False)

    class Meta:
        model = Driver
        fields = ['id', 'phone', 'image_car', 'first_name', 'last_name', 'user', 'photo',
                  'car_type', 'license_number', 'license_image_front', 'license_image_back', 'available', 'plate_number', 'car_model', 'car_year', 'car_color', 'car_model', 'car_color',
                  'car_year', 'plate_number', 'passengers_number', 'children_seat', ]


class DriverStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Driver
        fields = ['active',]

class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ['id', 'user', 'message', 'status', ]


class CouponSerializer(serializers.ModelSerializer):

    class Meta:
        model = Coupon
        fields = ['id', 'value', 'coupon', 'start_date', 'end_date','status', ]


class PriceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Price
        fields = ['id', 'km_price', 'wait_price',
                  'tax_price', 'extra_price', 'company_per', ]


class ComplainSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False)

    class Meta:
        model = Complain
        fields = ['id', 'user', 'image',
                  'complain', "reason", "name", "phone", ]


class TripReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = TripReview
        fields = ['id', 'user_id', 'trip', 'review', ]


class DriverReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = DriverReview
        fields = ['id', 'user_id', 'driver_id', 'review', ]


class PlacesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Places
        fields = ['id', 'lat', 'lng', 'name', ]


class DriverbalanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Driverbalance
        fields = ['id', 'driver', 'balance', ]


class AccountActivationSerializer(serializers.ModelSerializer):

    class Meta:
        model = AccountActivation
        fields = ['id', 'user', 'status', 'otp',]