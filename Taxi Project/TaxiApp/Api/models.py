from django.db import models
from django.contrib.auth.models import AbstractUser
from Api.Manager.UserManager import UserManager
# Create your models here.


class Role(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f'{self.name}'


class User(AbstractUser):
    USERNAME_FIELD = 'phone_number'
    username = None
    name = models.CharField(max_length=150, null=True)
    phone_number = models.CharField(max_length=14, unique=True)
    birth_date = models.DateField(blank=True, null=True)
    role = models.ForeignKey(
        Role, on_delete=models.SET_NULL, null=True, blank=True)
    note = models.TextField(blank=True, null=True)

    objects = UserManager()

    def __str__(self):
        return f'{self.phone_number} - {self.name}'


class TripType(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=100)

    def __str__(self) -> str:
        return "{}".format(self.type)


class CarType(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=100)
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


class Trip(models.Model):
    id = models.AutoField(primary_key=True)
    start_place = models.CharField(max_length=255)
    final_place = models.CharField(max_length=255)
    stop_point = models.ForeignKey(
        StopPoint, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    driver = models.ForeignKey('Driver', on_delete=models.SET_NULL, null=True)
    user_location = models.CharField(max_length=255)
    time = models.DateTimeField()
    distance = models.FloatField()
    price = models.FloatField()

    def __str__(self) -> str:
        return "{}".format(self.user)


class DriverLocation(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    lat = models.FloatField()
    lng = models.FloatField()

    def __str__(self) -> str:
        return "{}-{}".format(self.lat, self.lng)


class DriverCar(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    car_model = models.CharField(max_length=255)
    car_color = models.CharField(max_length=255)
    car_year = models.DateField()
    plate_number = models.PositiveSmallIntegerField()
    passengers_number = models.PositiveSmallIntegerField()
    children_seat = models.BooleanField()

    def __str__(self) -> str:
        return "{} - {}".format(self.car_model, self.user)


class Driver(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    photo = models.ImageField(upload_to='uploads/')
    car_type = models.ForeignKey(CarType, on_delete=models.SET_NULL, null=True)
    car = models.ForeignKey(DriverCar, on_delete=models.SET_NULL, null=True)
    license_number = models.CharField(max_length=50)
    license_image_front = models.ImageField(upload_to='licenses/')
    license_image_back = models.ImageField(upload_to='licenses/')
    active = models.BooleanField()
    available = models.BooleanField()

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
    km_price = models.FloatField()
    wait_price = models.FloatField()
    tax_price = models.FloatField()
    extra_price = models.FloatField()
    company_per = models.SmallIntegerField()

    def __str__(self) -> str:
        return "{}".format(self.km_price)


class Coupon(models.Model):
    id = models.AutoField(primary_key=True)
    fixed = models.BooleanField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    active = models.BooleanField()

    def __str__(self) -> str:
        return "{}-{}".format(self.start_date, self.end_date)
