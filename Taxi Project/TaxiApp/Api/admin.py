import csv
from django import forms
from django.contrib import admin
from django.contrib.sites.models import Site
from django.http import HttpResponse
from Api.models import AccountActivation, CarType, Complain, Coupon, Driver, DriverLocation, DriverReview, Driverbalance, ExtraForCar, Message, Price, Role, StopPoint, Trip, TripReview, TripType, User
from django.utils.html import format_html, urlencode
from django.urls import reverse
from django.db.models import Sum
from allauth.socialaccount.models import SocialApp
from allauth.account.models import EmailAddress
from rest_framework.authtoken.models import Token
from django.contrib.auth.admin import UserAdmin


admin.site.site_header = "Sayara Admin"
admin.site.index_title = "Sayara Admin"
admin.site.site_title = "Sayara Admin"

admin.site.unregister(Site)
# admin.site.unregister(EmailAddress)

def export_as_csv(self, request, queryset):

    meta = self.model._meta
    field_names = [field.name for field in meta.fields]

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
    writer = csv.writer(response)

    writer.writerow(field_names)
    for obj in queryset:
        writer.writerow([getattr(obj, field) for field in field_names])

    return response

export_as_csv.short_description = "Export Selected as CSV"



@ admin.register(User)
class UserAdmin(UserAdmin):

    fieldsets = (
        (None, {'fields': ('phone_number', 'password',)}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'birth_date',)}),
        ('Permissions', {
         'fields': ('is_active', 'is_staff', 'role', 'groups',)}),
        ('Others', {'fields': ('registered_at', 'gender',)}),
    )

    add_fieldsets = (
        (None, {'fields': ('phone_number', 'password1', 'password2')}),
        ('Permissions', {
         'fields': ('is_active', 'is_staff', 'role', 'groups',)}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'birth_date',)}),
        ('Others', {'fields': ('gender',)}),
    )

    list_display = ('phone_number', 'birth_date', 'gender', 'total_trips', 'is_active', 'registered_at',)
    list_filter = ('phone_number', 'gender')
    search_fields = ('phone_number', 'birth_date__date', 'gender', 'total_trips', 'is_active', 'registered_at',)
    list_editable = ('is_active',)
    actions = [export_as_csv]
    ordering = ['phone_number', ]

    def total_trips(self, obj):
        tip = Trip.objects.filter(
            user__id=obj.id).aggregate(trips_count=Sum('user'))
        return tip['trips_count']



@ admin.register(CarType)
class CarTypeAdmin(admin.ModelAdmin):
    list_display = ('type', 'trip_type',)
    list_filter = ('trip_type',)
    search_fields = ('type', 'trip_type',)
    actions = [export_as_csv]


@ admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name',)
    actions = [export_as_csv]


@ admin.register(TripType)
class TripTypeAdmin(admin.ModelAdmin):
    list_display = ('type',)
    actions = [export_as_csv]

# @ admin.register(StopPoint)
# class StopPointAdmin(admin.ModelAdmin):
#     list_display = ('user', 'lat', 'lng',)
#     list_filter = ('user__phone_number',)
#     search_fields = ("user__phone_number", 'user__first_name',)
#     autocomplete_fields = ['user', ]


@ admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('user', 'driver', 'driver_name', 'distance', 'status', 'price', 'created_at',)
    list_filter = ('user__phone_number', 'status',)
    search_fields = ("user__phone_number", 'status', 'driver__phone_number', 'driver__first_name', 'distance', 'price', 'user__first_name')
    autocomplete_fields = ['driver', 'user',]
    actions = [export_as_csv]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['user'].widget.can_delete_related = False
        form.base_fields['user'].widget.can_change_related = False
        form.base_fields['user'].widget.can_add_related = False
        form.base_fields['driver'].widget.can_change_related = False
        form.base_fields['driver'].widget.can_add_related = False
        form.base_fields['driver'].widget.can_delete_related = False
        return form

    def driver_name(self, obj):
        return "{} {}".format(obj.driver.first_name, obj.driver.last_name)


@ admin.register(DriverLocation)
class DriverLocationAdmin(admin.ModelAdmin):
    list_display = ('user', 'lat', 'lng',)
    list_filter = ('user__phone_number',)
    search_fields = ("user__phone_number", "user__first_name")
    autocomplete_fields = ['user', ]
    actions = [export_as_csv]


# class DriverForm(forms.ModelForm):
#     driver_balance = forms.IntegerField()
#     try:
#         get_balance = Driverbalance.objects.get(driver=self.id).balance
#     except:
#         get_balance = 0

@ admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):

    list_display = ('user', 'driver_name', 'car_model','car_color','plate_number', 'license_number', 'available', 'active', "driver_balance", "registered_at", "total_distance", "total_trips", "total_balance", "driver_review",)
    list_filter = ('user__phone_number', 'active',)
    search_fields = ("user__phone_number", 'car_model', 'car_color', 'active', 'total_trips', 'available', 'license_number', 'plate_number', 'user__first_name',)
    list_editable = ('active', )
    autocomplete_fields = ['user', ]
    readonly_fields = ('image_photo', 'image_license_image_front', 'image_license_image_front', )
    actions = [export_as_csv]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['car_type'].widget.can_delete_related = False
        form.base_fields['car_type'].widget.can_change_related = False
        form.base_fields['car_type'].widget.can_add_related = False
        form.base_fields['user'].widget.can_change_related = False
        form.base_fields['user'].widget.can_add_related = False
        form.base_fields['user'].widget.can_delete_related = False
        return form

    def driver_review(self, obj):
        review_count = DriverReview.objects.filter(
            driver_id=obj.user).count()
        driver_review = DriverReview.objects.filter(
            driver_id=obj.user).aggregate(review_count=Sum('review'))
        return driver_review['review_count'] / review_count if driver_review['review_count'] else 0

    def total_balance(self, obj):
        tip = Trip.objects.filter(
            driver=obj.user).aggregate(balance_count=Sum('price_after_coupon'))
        return tip['balance_count']

    def total_distance(self, obj):
        tip = Trip.objects.filter(
            driver=obj.user).aggregate(distance_count=Sum('distance'))
        return tip['distance_count']

    def total_trips(self, obj):
        tip = Trip.objects.filter(
            driver=obj.user).aggregate(trips_count=Sum('driver'))
        return tip['trips_count']

    def driver_balance(self, obj):
        try:
            get_balance = Driverbalance.objects.filter(driver=obj.user.id, activate=True).last()
            url = reverse('admin:Api_driverbalance_changelist') + '?' + urlencode({
            'driver__id__exact': str(get_balance.driver.id)
            })
            return format_html('<a href="{}">{}</a>', url, get_balance.balance)
            # return get_balance
        except:
            return 0

    def driver_name(self, obj):
        return "{} {}".format(obj.user.first_name, obj.user.last_name)

    def image_photo(self, obj):
        return obj.image_photo
    
    def image_license_image_front(self, obj):
        return obj.image_li_front
    
    def image_license_image_back(self, obj):
        return obj.image_li_back

    image_photo.short_description = 'Driver Photo'
    image_photo.allow_tags = True

    image_license_image_front.short_description = 'License image front'
    image_license_image_front.allow_tags = True

    image_license_image_back.short_description = 'License image back'
    image_license_image_back.allow_tags = True


    


@ admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'created_at',)
    list_filter = ('user__phone_number', 'status')
    search_fields = ("user__phone_number", 'user__first_name', 'status', 'created_at',)
    autocomplete_fields = ['user', ]
    readonly_fields = ('image_img', )
    actions = [export_as_csv]

    def image_img(self, obj):
        return obj.image_img

    image_img.short_description = 'Image Preview'
    image_img.allow_tags = True

@ admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ('km_price', 'wait_price', 'tax_price', 'extra_price', 'company_per',)
    search_fields = ('km_price', 'wait_price', 'tax_price', 'extra_price', 'company_per',)
    actions = [export_as_csv]

    def has_add_permission(self, request) -> bool:
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        return False


@ admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('value', 'coupon', 'start_date', 'end_date', 'active', 'status', 'created_at',)
    list_filter = ('value', 'active')
    search_fields = ('value', 'coupon', 'start_date__date', 'end_date__date', 'active', 'status', 'created_at',)
    actions = [export_as_csv]



@ admin.register(DriverReview)
class DriverReviewAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'driver_id', 'review', )
    search_fields = ("user_id__phone_number", 'driver_id__phone_number', 'review', 'user_id__first_name', 'driver_id__first_name',)
    autocomplete_fields = ['driver_id', 'user_id',]
    actions = [export_as_csv]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['user_id'].widget.can_delete_related = False
        form.base_fields['user_id'].widget.can_change_related = False
        form.base_fields['user_id'].widget.can_add_related = False
        form.base_fields['driver_id'].widget.can_change_related = False
        form.base_fields['driver_id'].widget.can_add_related = False
        form.base_fields['driver_id'].widget.can_delete_related = False
        return form


@ admin.register(TripReview)
class TripReviewAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'trip', 'review', )
    search_fields = ("user_id__phone_number", 'user_id__first_name', 'trip', 'review',)
    autocomplete_fields = ['user_id', ]
    actions = [export_as_csv]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['user_id'].widget.can_delete_related = False
        form.base_fields['user_id'].widget.can_change_related = False
        form.base_fields['user_id'].widget.can_add_related = False
        form.base_fields['trip'].widget.can_change_related = False
        form.base_fields['trip'].widget.can_add_related = False
        form.base_fields['trip'].widget.can_delete_related = False
        return form


@ admin.register(Complain)
class ComplainAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'created_at', 'user_profile',)
    search_fields = ("user__phone_number", 'user__first_name', 'phone', 'reason',)
    autocomplete_fields = ['user', ]
    readonly_fields = ('image_img', )
    actions = [export_as_csv]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['user'].widget.can_change_related = False
        form.base_fields['user'].widget.can_add_related = False
        form.base_fields['user'].widget.can_delete_related = False
        return form

    def user_profile(self, obj):
        try:
            get_profile = User.objects.get(id=obj.user.id).id
            url = reverse('admin:Api_user_changelist') + '?' + urlencode({
            'id__exact': str(get_profile)
            })
            return format_html('<a href="{}">{}</a>', url, "Open User Profile")
            # return get_balance
        except:
            return "Profile Not Exists"

    def image_img(self, obj):
        return obj.image_img

    image_img.short_description = 'Image Preview'
    image_img.allow_tags = True


@ admin.register(Driverbalance)
class DriverbalanceAdmin(admin.ModelAdmin):
    list_display = ('driver', 'balance', 'activate', )
    search_fields = ("driver__phone_number", 'driver__first_name', 'activate', 'balance',)
    autocomplete_fields = ['driver', ]
    actions = [export_as_csv]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['driver'].widget.can_change_related = False
        form.base_fields['driver'].widget.can_add_related = False
        form.base_fields['driver'].widget.can_delete_related = False
        return form


@ admin.register(AccountActivation)
class AccountActivationAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'otp', )
    search_fields = ("user__phone_number", 'user__first_name', 'status', 'otp',)
    autocomplete_fields = ['user', ]
    actions = [export_as_csv]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['user'].widget.can_change_related = False
        form.base_fields['user'].widget.can_add_related = False
        form.base_fields['user'].widget.can_delete_related = False
        return form


@ admin.register(ExtraForCar)
class ExtraForCarAdmin(admin.ModelAdmin):
    list_display = ('extra', 'extra_arabic', 'active', )
    search_fields = ('extra', 'extra_arabic', 'active',)
    actions = [export_as_csv]


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
