from django.contrib import admin

from Api.models import CarType, Complain, Coupon, Driver, DriverLocation, DriverReview, Driverbalance, Message, Price, Role, StopPoint, Trip, TripReview, TripType, User



@ admin.register(CarType)
class CarTypeAdmin(admin.ModelAdmin):
    list_display = ('type', 'trip_type',)
    list_filter = ('trip_type',)
    search_fields = ("package_name__startswith",)


@ admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', )


@ admin.register(TripType)
class TripTypeAdmin(admin.ModelAdmin):
    list_display = ('type',)

@ admin.register(StopPoint)
class StopPointAdmin(admin.ModelAdmin):
    list_display = ('user', 'lat', 'lng',)
    list_filter = ('user__phone_number',)
    search_fields = ("user__phone_number",)


@ admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('user', 'driver', 'distance', 'status', 'price', 'created_at',)
    list_filter = ('user__phone_number', 'status',)
    search_fields = ("user__phone_number", 'status',)


@ admin.register(DriverLocation)
class DriverLocationAdmin(admin.ModelAdmin):
    list_display = ('user', 'lat', 'lng',)
    list_filter = ('user__phone_number',)
    search_fields = ("user__phone_number",)


@ admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('user', 'car_model','car_color','plate_number', 'license_number', 'available', 'active')
    list_filter = ('user__phone_number', 'active',)
    search_fields = ("user__phone_number", 'car_model', 'car_color', 'active',)
    list_editable = ('active',)

    readonly_fields = ('image_photo', 'image_license_image_front', 'image_license_image_front', )

    def image_photo(self, obj):
        return obj.image_photo
    
    def image_license_image_front(self, obj):
        return obj.image_li_front
    
    def image_license_image_back(self, obj):
        return obj.image_li_back

    image_photo.short_description = 'Image Preview'
    image_photo.allow_tags = True

    image_license_image_front.short_description = 'Image Preview'
    image_license_image_front.allow_tags = True

    image_license_image_back.short_description = 'Image Preview'
    image_license_image_back.allow_tags = True


    


@ admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'created_at',)
    list_filter = ('user__phone_number', 'status')
    search_fields = ("user__phone_number", 'status',)

    readonly_fields = ('image_img', )

    def image_img(self, obj):
        return obj.image_img

    image_img.short_description = 'Image Preview'
    image_img.allow_tags = True

@ admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ('km_price', 'wait_price', 'tax_price', 'extra_price', 'company_per',)


@ admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('value', 'coupon', 'start_date', 'end_date', 'active',)
    list_filter = ('value', 'active')
    search_fields = ("value", 'active',)


@ admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'birth_date', 'gender', )
    list_filter = ('phone_number', 'gender')
    search_fields = ("phone_number", 'gender',)


@ admin.register(DriverReview)
class DriverReviewAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'driver_id', 'review', )
    search_fields = ("user_id", 'driver_id',)


@ admin.register(TripReview)
class TripReviewAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'trip', 'review', )
    search_fields = ("user_id", 'trip',)


@ admin.register(Complain)
class ComplainAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'reason', 'complain')
    search_fields = ("user", 'phone', 'reason',)

    readonly_fields = ('image_img', )

    def image_img(self, obj):
        return obj.image_img

    image_img.short_description = 'Image Preview'
    image_img.allow_tags = True


@ admin.register(Driverbalance)
class DriverbalanceAdmin(admin.ModelAdmin):
    list_display = ('driver', 'balance', 'activate', )
    search_fields = ("driver", 'activate',)
# Register your models here.
# admin.site.register(CarType)
# admin.site.register(Role)
# admin.site.register(TripType)
# admin.site.register(StopPoint)
# admin.site.register(Trip)
# admin.site.register(DriverLocation)
# admin.site.register(Driver)
# admin.site.register(Message)
# admin.site.register(Price)
# admin.site.register(Coupon)
# admin.site.register(User)
# admin.site.register(DriverReview)
# admin.site.register(TripReview)
# admin.site.register(Complain)
# admin.site.register(Driverbalance)
