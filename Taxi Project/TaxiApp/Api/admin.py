import csv
from django import forms
from django.contrib import admin
from django.contrib.sites.models import Site
from django.http import HttpResponse
from Api.models import AccountActivation, CarType, Complain, Coupon, Driver, DriverLocation, DriverReview, Driverbalance, ExtraForCar, Message, Price, Role, StopPoint, Trip, TripReview, TripType, User
from django.utils.html import format_html, urlencode
from django.urls import reverse
from django.db.models import Sum
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter


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

    @admin.action(description='Export Selected as PDF')
    def export_as_pdf(self, request, queryset):
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        textobject = c.beginText()
        textobject.setTextOrigin(10, 730)
        textobject.setFont("Helvetica",24)
        values = []
    

        for obj in queryset:
            values.append(obj.first_name)
            values.append(obj.last_name)
            values.append(obj.phone_numebr)
            values.append(obj.birth_date)
            values.append(obj.gender)
            values.append(obj.role.name)

        for line in values:
            textobject.textLine(line)

        c.drawText(textobject)
        c.showPage()
        c.save()

        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='report.pdf')

    fieldsets = (
        (None, {'fields': ('phone_number', 'password',)}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'birth_date',)}),
        ('Permissions', {
         'fields': ('is_active', 'is_staff', 'role', 'groups',)}),
        ('Others', {'fields': ('gender',)}),
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
    search_fields = ('phone_number', 'birth_date', 'gender', 'is_active', 'registered_at',)
    list_editable = ('is_active',)
    actions = [export_as_csv, export_as_pdf]
    ordering = ['phone_number', ]

    def total_trips(self, obj):
        tip = Trip.objects.filter(
            user__id=obj.id).aggregate(trips_count=Sum('user'))
        return tip['trips_count']



@ admin.register(CarType)
class CarTypeAdmin(admin.ModelAdmin):
    @admin.action(description='Export Selected as PDF')
    def export_as_pdf(self, request, queryset):
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        textobject = c.beginText()
        textobject.setTextOrigin(10, 730)
        textobject.setFont("Helvetica",24)
        values = []
    

        for obj in queryset:
            values.append(obj.trip)
            values.append(obj.trip_type_name.type)


        for line in values:
            textobject.textLine(line)

        c.drawText(textobject)
        c.showPage()
        c.save()

        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='report.pdf')

    list_display = ('type', 'trip_type',)
    list_filter = ('trip_type',)
    search_fields = ('type',)
    actions = [export_as_csv, export_as_pdf]


@ admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    @admin.action(description='Export Selected as PDF')
    def export_as_pdf(self, request, queryset):
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        textobject = c.beginText()
        textobject.setTextOrigin(10, 730)
        textobject.setFont("Helvetica",24)
        values = []
    

        for obj in queryset:
            values.append(obj.role)

        for line in values:
            textobject.textLine(line)

        c.drawText(textobject)
        c.showPage()
        c.save()

        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='report.pdf')
    list_display = ('name', )
    search_fields = ('name',)
    actions = [export_as_csv, export_as_pdf]


@ admin.register(TripType)
class TripTypeAdmin(admin.ModelAdmin):
    @admin.action(description='Export Selected as PDF')
    def export_as_pdf(self, request, queryset):
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        textobject = c.beginText()
        textobject.setTextOrigin(inch, inch)
        textobject.setFont("Helvetica",24)
        values = []
    

        for obj in queryset:
            values.append(obj.type)

        for line in values:
            textobject.textLine(line)

        c.drawText(textobject)
        c.showPage()
        c.save()

        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='report.pdf')
    list_display = ('type', 'price')
    actions = [export_as_csv, export_as_pdf]

# @ admin.register(StopPoint)
# class StopPointAdmin(admin.ModelAdmin):
#     list_display = ('user', 'lat', 'lng',)
#     list_filter = ('user__phone_number',)
#     search_fields = ("user__phone_number", 'user__first_name',)
#     autocomplete_fields = ['user', ]


@ admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    @admin.action(description='Export Selected as PDF')
    def export_as_pdf(self, request, queryset):
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        textobject = c.beginText()
        textobject.setTextOrigin(10, 730)
        textobject.setFont("Helvetica",24)
        values = []
    

        for obj in queryset:
            values.append('User: ' + obj.user._first_name + ' ' + obj.user.last_name)
            values.append('Driver: ' + obj.driver._first_name + ' ' + obj.driver.last_name)
            values.append('start_place: ' + str(obj.start_place))
            values.append('source: ' + str(obj.source))
            values.append('destination: ' + str(obj.destination))
            values.append('final_place: ' + str(obj.final_place))
            values.append('time_ending: ' + str(obj.time_ending))
            values.append('expected_time: ' + str(obj.expected_time))
            values.append('distance: ' + str(obj.distance))
            values.append('price: ' + str(obj.price))
            values.append('status: ' + str(obj.status))
            values.append('trip_type: ' + obj.trip_type.type)
            values.append('price_after_coupon: ' + str(obj.price_after_coupon))
            values.append('trip_cancellation: ' + obj.trip_cancellation)

        for line in values:
            textobject.textLine(line)

        c.drawText(textobject)
        c.showPage()
        c.save()

        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='report.pdf')

    list_display = ('user', 'driver', 'driver_name', 'distance', 'status', 'price', 'created_at',)
    list_filter = ('user__phone_number', 'status',)
    search_fields = ("user__phone_number", 'status', 'driver__phone_number', 'driver__first_name', 'distance', 'price', 'user__first_name')
    autocomplete_fields = ['driver', 'user',]
    actions = [export_as_csv, export_as_pdf]

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


# @ admin.register(DriverLocation)
# class DriverLocationAdmin(admin.ModelAdmin):

#     @admin.action(description='Export Selected as PDF')
#     def export_as_pdf(self, request, queryset):
#         buffer = io.BytesIO()
#         c = canvas.Canvas(buffer, pagesize=letter)
#         textobject = c.beginText()
#         textobject.setTextOrigin(inch, inch)
#         textobject.setFont("Helvetica",24)
#         values = []
    

#         for obj in queryset:
#             values.append('User: ' + obj.user._first_name + ' ' + obj.user.last_name)
#             values.append('license_number: ' + obj.license_number)
#             values.append('car_model: ' + obj.car_model)
#             values.append('car_color: ' + obj.car_color)
#             values.append('car_year: ' + obj.car_year)
#             values.append('plate_number: ' + obj.plate_number)
#             values.append('passengers_number: ' + obj.passengers_number)
#             values.append('car_type: ' + obj.car_type.type)

#         for line in values:
#             textobject.textLine(line)

#         c.drawText(textobject)
#         c.showPage()
#         c.save()

#         buffer.seek(0)
#         return FileResponse(buffer, as_attachment=True, filename='report.pdf')

#     list_display = ('user', 'lat', 'lng',)
#     list_filter = ('user__phone_number',)
#     search_fields = ("user__phone_number", "user__first_name")
#     autocomplete_fields = ['user', ]
#     actions = [export_as_csv, export_as_pdf]


# class DriverForm(forms.ModelForm):
#     driver_balance = forms.IntegerField()
#     try:
#         get_balance = Driverbalance.objects.get(driver=self.id).balance
#     except:
#         get_balance = 0

@ admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):

    @admin.action(description='Export Selected as PDF')
    def export_as_pdf(self, request, queryset):
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        textobject = c.beginText()
        textobject.setTextOrigin(10, 730)
        textobject.setFont("Helvetica",24)
        values = []
    

        for obj in queryset:
            values.append('User: ' + obj.user.first_name + ' ' + obj.user.last_name)
            values.append('license_number: ' + str(obj.license_number))
            values.append('car_model: ' + str(obj.car_model))
            values.append('car_color: ' + str(obj.car_color))
            values.append('car_year: ' + str(obj.car_year))
            values.append('plate_number: ' + str(obj.plate_number))
            values.append('passengers_number: ' + str(obj.passengers_number))
            values.append('car_type: ' + obj.car_type.type)

        for line in values:
            textobject.textLine(line)

        c.drawText(textobject)
        c.showPage()
        c.save()

        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='report.pdf')

    list_display = ('user', 'driver_name', 'car_model','car_color','plate_number', 'license_number', 'available', 'active', "driver_balance", "registered_at", "total_distance", "total_trips", "total_balance", "driver_review",)
    list_filter = ('user__phone_number', 'active',)
    search_fields = ("user__phone_number", 'car_model', 'car_color', 'active', 'available', 'license_number', 'plate_number', 'user__first_name',)
    list_editable = ('active', )
    autocomplete_fields = ['user', ]
    readonly_fields = ('image_photo', 'image_license_image_front', 'image_license_image_front', )
    actions = [export_as_csv, export_as_pdf]

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
    @admin.action(description='Export Selected as PDF')
    def export_as_pdf(self, request, queryset):
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        textobject = c.beginText()
        textobject.setTextOrigin(10, 730)
        textobject.setFont("Helvetica",24)
        values = []
    

        for obj in queryset:
            values.append('User: ' + obj.user._first_name + ' ' + obj.user.last_name)
            values.append('message: ' + obj.message)
            values.append('status: ' + str(obj.status))

        for line in values:
            textobject.textLine(line)

        c.drawText(textobject)
        c.showPage()
        c.save()

        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='report.pdf')

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

    @admin.action(description='Export Selected as PDF')
    def export_as_pdf(self, request, queryset):
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        textobject = c.beginText()
        textobject.setTextOrigin(10, 730)
        textobject.setFont("Helvetica",24)
        values = []
    

        for obj in queryset:
            values.append('km_price: ' + str(obj.km_price))
            values.append('wait_price: ' + str(obj.wait_price))
            values.append('tax_price: ' + str(obj.tax_price))
            values.append('extra_price: ' + str(obj.extra_price))
            values.append('company_perecentage: ' + str(obj.company_per))

        for line in values:
            textobject.textLine(line)

        c.drawText(textobject)
        c.showPage()
        c.save()

        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='report.pdf')

    list_display = ('km_price', 'wait_price', 'tax_price', 'extra_price', 'company_per',)
    search_fields = ('km_price', 'wait_price', 'tax_price', 'extra_price', 'company_per',)
    actions = [export_as_csv, export_as_pdf]

    def has_add_permission(self, request) -> bool:
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        return False


@ admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):

    @admin.action(description='Export Selected as PDF')
    def export_as_pdf(self, request, queryset):
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        textobject = c.beginText()
        textobject.setTextOrigin(10, 730)
        textobject.setFont("Helvetica",24)
        values = []
    

        for obj in queryset:
            values.append('value: ' + str(obj.value))
            values.append('coupon: ' + str(obj.coupon))
            values.append('coupon_type: ' + str(obj.coupon_type))
            values.append('start_date: ' + str(obj.start_date))
            values.append('end_date: ' + str(obj.end_date))
            values.append('active: ' + str(obj.active))
            values.append('status: ' + str(obj.status))

        for line in values:
            textobject.textLine(line)

        c.drawText(textobject)
        c.showPage()
        c.save()

        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='report.pdf')


    list_display = ('value', 'coupon', 'start_date', 'end_date', 'active', 'status', 'created_at',)
    list_filter = ('value', 'active')
    search_fields = ('value', 'coupon', 'start_date__date', 'end_date__date', 'active', 'status', 'created_at',)
    actions = [export_as_csv, export_as_pdf]



@ admin.register(DriverReview)
class DriverReviewAdmin(admin.ModelAdmin):

    @admin.action(description='Export Selected as PDF')
    def export_as_pdf(self, request, queryset):
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        textobject = c.beginText()
        textobject.setTextOrigin(10, 730)
        textobject.setFont("Helvetica",24)
        values = []
    

        for obj in queryset:
            values.append('user: ' + obj.user_id.frist_name + ' ' + obj.user_id.last_name)
            values.append('driver: ' + obj.driver_id.first_name + ' ' + obj.driver_id.last_name)
            values.append('review: ' + obj.review)

        for line in values:
            textobject.textLine(line)

        c.drawText(textobject)
        c.showPage()
        c.save()

        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='report.pdf')


    list_display = ('user_id', 'driver_id', 'review', )
    search_fields = ("user_id__phone_number", 'driver_id__phone_number', 'review', 'user_id__first_name', 'driver_id__first_name',)
    autocomplete_fields = ['driver_id', 'user_id',]
    actions = [export_as_csv, export_as_pdf]

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

    @admin.action(description='Export Selected as PDF')
    def export_as_pdf(self, request, queryset):
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        textobject = c.beginText()
        textobject.setTextOrigin(10, 730)
        textobject.setFont("Helvetica",24)
        values = []
    

        for obj in queryset:
            values.append('user: ' + obj.user_id.frist_name + ' ' + obj.user_id.last_name)
            values.append('Trip number: ' + obj.trip.id)
            values.append('review: ' + obj.review)

        for line in values:
            textobject.textLine(line)

        c.drawText(textobject)
        c.showPage()
        c.save()

        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='report.pdf')



    list_display = ('user_id', 'trip', 'review', )
    search_fields = ("user_id__phone_number", 'user_id__first_name', 'review',)
    autocomplete_fields = ['user_id', ]
    actions = [export_as_csv, export_as_pdf]

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

    @admin.action(description='Export Selected as PDF')
    def export_as_pdf(self, request, queryset):
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        textobject = c.beginText()
        textobject.setTextOrigin(10, 730)
        textobject.setFont("Helvetica",24)
        values = []
    

        for obj in queryset:
            values.append('user: ' + obj.user.frist_name + ' ' + obj.user.last_name)
            values.append('name: ' + obj.name)
            values.append('review: ' + obj.review)
            values.append('reason: ' + obj.reason)
            values.append('complain: ' + obj.complain)

        for line in values:
            textobject.textLine(line)

        c.drawText(textobject)
        c.showPage()
        c.save()

        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='report.pdf')


    list_display = ('user', 'phone', 'created_at', 'user_profile',)
    search_fields = ("user__phone_number", 'user__first_name', 'phone', 'reason',)
    autocomplete_fields = ['user', ]
    readonly_fields = ('image_img', )
    actions = [export_as_csv, export_as_pdf]

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

    @admin.action(description='Export Selected as PDF')
    def export_as_pdf(self, request, queryset):
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        textobject = c.beginText()
        textobject.setTextOrigin(10, 730)
        textobject.setFont("Helvetica",24)
        values = []
    

        for obj in queryset:
            values.append('driver: ' + obj.driver.frist_name + ' ' + obj.driver.last_name)
            values.append('balance: ' + str(obj.balance))
            values.append('activate: ' + str(obj.activate))

        for line in values:
            textobject.textLine(line)

        c.drawText(textobject)
        c.showPage()
        c.save()

        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='report.pdf')


    list_display = ('driver', 'balance', 'activate', )
    search_fields = ("driver__phone_number", 'driver__first_name', 'activate', 'balance',)
    autocomplete_fields = ['driver', ]
    actions = [export_as_csv, export_as_pdf]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['driver'].widget.can_change_related = False
        form.base_fields['driver'].widget.can_add_related = False
        form.base_fields['driver'].widget.can_delete_related = False
        return form


@ admin.register(AccountActivation)
class AccountActivationAdmin(admin.ModelAdmin):

    @admin.action(description='Export Selected as PDF')
    def export_as_pdf(self, request, queryset):
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        textobject = c.beginText()
        textobject.setTextOrigin(10, 730)
        textobject.setFont("Helvetica",24)
        values = []
    

        for obj in queryset:
            values.append('driver: ' + obj.user.frist_name + ' ' + obj.user.last_name)
            values.append('otp: ' + str(obj.otp))
            values.append('status: ' + obj.status)

        for line in values:
            textobject.textLine(line)

        c.drawText(textobject)
        c.showPage()
        c.save()

        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='report.pdf')


    list_display = ('user', 'status', 'otp', )
    search_fields = ("user__phone_number", 'user__first_name', 'status', 'otp',)
    autocomplete_fields = ['user', ]
    actions = [export_as_csv, export_as_pdf]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['user'].widget.can_change_related = False
        form.base_fields['user'].widget.can_add_related = False
        form.base_fields['user'].widget.can_delete_related = False
        return form


@ admin.register(ExtraForCar)
class ExtraForCarAdmin(admin.ModelAdmin):

    @admin.action(description='Export Selected as PDF')
    def export_as_pdf(self, request, queryset):
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        textobject = c.beginText()
        textobject.setTextOrigin(10, 730)
        textobject.setFont("Helvetica",24)
        values = []
    

        for obj in queryset:
            values.append('extra: ' + str(obj.extra))
            values.append('active: ' + str(obj.active))

        for line in values:
            textobject.textLine(line)

        c.drawText(textobject)
        c.showPage()
        c.save()

        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='report.pdf')


    list_display = ('extra', 'extra_arabic', 'active', )
    search_fields = ('extra', 'extra_arabic', 'active',)
    actions = [export_as_csv, export_as_pdf]


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
