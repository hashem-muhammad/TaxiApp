from django.contrib import admin

from Api.models import CarType, Complain, Coupon, Driver, DriverLocation, DriverReview, Message, Price, Role, StopPoint, Trip, TripCancellation, TripReview, TripType, User

# Register your models here.
admin.site.register(CarType)
admin.site.register(Role)
admin.site.register(TripType)
admin.site.register(StopPoint)
admin.site.register(Trip)
admin.site.register(DriverLocation)
admin.site.register(Driver)
admin.site.register(Message)
admin.site.register(Price)
admin.site.register(Coupon)
admin.site.register(User)
admin.site.register(TripCancellation)
admin.site.register(DriverReview)
admin.site.register(TripReview)
admin.site.register(Complain)
