from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser
from Api.Manager.UserManager import UserManager
# Create your models here.


class Role(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f'{self.name}-{self.id}'


class User(AbstractUser):
    USERNAME_FIELD = 'phone_number'
    username = None
    phone_number = models.CharField(max_length=14, unique=True)
    birth_date = models.DateField(null=True, default=None)
    gender = models.CharField(max_length=10, null=True, default='')
    profile_image = models.ImageField(
        upload_to='profiles_image/', null=True, default=None)
    role = models.ForeignKey(
        Role, on_delete=models.SET_NULL, null=True, blank=True)
    firebase_token = models.TextField(null=True, blank=True)
    objects = UserManager()

    def __str__(self):
        return f'{self.phone_number}'


class TripType(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=100)

    def __str__(self) -> str:
        return "{}".format(self.type)


class CarType(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=100)
    price = models.FloatField(default=0.0)
    trip_type = models.ForeignKey(
        TripType, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return "{}".format(self.type)


class StopPoint(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    lat = models.CharField(max_length=255, null=True)
    lng = models.CharField(max_length=255, null=True)

    def __str__(self) -> str:
        return "{}".format(self.point)


class TripCancellation(models.Model):
    id = models.AutoField(primary_key=True)
    reason = models.CharField(max_length=255)
    trip = models.ForeignKey('Trip', on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return "{}".format(self.reason)


class Trip(models.Model):
    id = models.AutoField(primary_key=True)
    start_place = models.CharField(max_length=255)
    source = models.CharField(max_length=255, default='')
    destination = models.CharField(max_length=255, default='')
    final_place = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    driver = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='Driver')
    time_ending = models.DateTimeField()
    expected_time = models.DateTimeField(null=True)
    distance = models.FloatField()
    price = models.FloatField()
    status = models.CharField(max_length=30, default='')
    trip_type = models.ForeignKey(
        TripType, on_delete=models.SET_NULL, null=True)
    price_after_coupon = models.FloatField(null=True)
    trip_cancellation = models.TextField(default='', null=True)
    created_at = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return "{}".format(self.user)


class DriverLocation(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    lat = models.FloatField()
    lng = models.FloatField()

    def __str__(self) -> str:
        return "{}-{}".format(self.lat, self.lng)


class Driver(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    photo = models.ImageField(upload_to='uploads/')
    car_type = models.ForeignKey(CarType, on_delete=models.SET_NULL, null=True)
    license_number = models.CharField(max_length=50)
    license_image_front = models.ImageField(upload_to='licenses/')
    license_image_back = models.ImageField(upload_to='licenses/')
    image_car = models.ImageField(upload_to='image_car/', default='')
    car_model = models.CharField(max_length=255, default='')
    car_color = models.CharField(max_length=255, default='')
    car_year = models.CharField(max_length=255, default='')
    plate_number = models.PositiveSmallIntegerField(default=4)
    passengers_number = models.PositiveSmallIntegerField(default=4)
    children_seat = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    available = models.BooleanField(default=True)

    def __str__(self) -> str:
        return "{}".format(self.user)


class Message(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    message = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='uploads/')
    status = models.SmallIntegerField(null=True, blank=True, default=0)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return "{}".format(self.user)


class Price(models.Model):
    id = models.AutoField(primary_key=True)
    km_price = models.FloatField(default=0.0)
    wait_price = models.FloatField(default=0.0)
    tax_price = models.FloatField(default=0.0)
    extra_price = models.FloatField(default=0.0)
    company_per = models.SmallIntegerField(default=0.0)

    def __str__(self) -> str:
        return "{}".format(self.km_price)


class Coupon(models.Model):
    id = models.AutoField(primary_key=True)
    value = models.FloatField(default=0.0)
    coupon = models.CharField(max_length=60, default='')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    active = models.BooleanField()

    def __str__(self) -> str:
        return "{}-{}".format(self.start_date, self.end_date)


class DriverReview(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    driver_id = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='driver_review')
    review = models.FloatField()

    def __str__(self) -> str:
        return "{}".format(self.user_id)


class TripReview(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    trip = models.ForeignKey(
        Trip, on_delete=models.SET_NULL, null=True)
    review = models.TextField()

    def __str__(self) -> str:
        return "{}".format(self.user_id)


class Complain(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255, null=True, default='')
    phone = models.CharField(max_length=255, null=True, default='')
    image = models.ImageField(upload_to='complains/', default='')
    reason = models.TextField(default='')
    complain = models.TextField()

    def __str__(self) -> str:
        return "{}".format(self.user)


class Places(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    lat = models.FloatField()
    lng = models.FloatField()
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return "{}".format(self.name)


class Driverbalance(models.Model):
    id = models.AutoField(primary_key=True)
    driver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    balance = models.FloatField()
    activate = models.BooleanField(default=False)

    def __str__(self) -> str:
        return "{}-{}".format(self.driver, self.balance)
