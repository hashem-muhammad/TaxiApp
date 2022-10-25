from django.urls import path, include

from Api.views import CarTypeView, ComplainView, CouponView, DriverCarView, DriverReviewView, DriverView, MyObtainTokenPairView, MessageView, PriceView, StopPointView, TripReviewView, TripTypeView, TripView

urlpatterns = [
    path('auth/register/', include('dj_rest_auth.registration.urls')),
    path('auth/', include('dj_rest_auth.urls')),
    path('login/', MyObtainTokenPairView.as_view(), name="token_obtain_pair"),
    path('trip_type/', TripTypeView.as_view()),
    path('trip/', TripView.as_view()),
    path('car_type/', CarTypeView.as_view()),
    path('stop_point/', StopPointView.as_view()),
    path('driver_car/', DriverCarView.as_view()),
    path('driver/', DriverView.as_view()),
    path('driver_review/', DriverReviewView.as_view()),
    path('trip_review/', TripReviewView.as_view()),
    path('message/', MessageView.as_view()),
    path('complain/', ComplainView.as_view()),
    path('coupon/<str:coupon>/', CouponView.as_view()),
    path('price/', PriceView.as_view()),

]
