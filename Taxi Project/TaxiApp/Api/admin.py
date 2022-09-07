from django.contrib import admin

from Api.models import CarType, Coupon, Driver, DriverCar, DriverLocation, Message, Price, Role, StopPoint, Trip, TripType, User

# Register your models here.
admin.site.register(CarType)
admin.site.register(Role)
admin.site.register(TripType)
admin.site.register(StopPoint)
admin.site.register(Trip)
admin.site.register(DriverLocation)
admin.site.register(DriverCar)
admin.site.register(Driver)
admin.site.register(Message)
admin.site.register(Price)
admin.site.register(Coupon)
admin.site.register(User)
