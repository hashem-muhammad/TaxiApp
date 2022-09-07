from django.urls import path, include

from Api.views import CarTypeView, DriverCarView, DriverView, MessageView, StopPointView, TripTypeView, TripView


urlpatterns = [
    path('auth/register/', include('dj_rest_auth.registration.urls')),
    path('auth/', include('dj_rest_auth.urls')),
    path('trip_type/', TripTypeView.as_view()),
    path('car_type/', CarTypeView.as_view()),
    path('stop_point/', StopPointView.as_view()),
    path('trip/', TripView.as_view()),
    path('driver_car/', DriverCarView.as_view()),
    path('message/', MessageView.as_view()),

]
