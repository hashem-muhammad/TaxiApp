from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from Api.views import CarTypeView, ComplainView, CouponView, DriverByIdView, DriverReviewView, DriverView, DriverbalanceView, MyObtainTokenPairView, MessageView, PlacesView, PriceView, StopPointView, TripByIdView, TripReviewView, TripTypeView, TripView, UserByIdView, UserInfoView

urlpatterns = [
    path('auth/register/', include('dj_rest_auth.registration.urls')),
    path('auth/', include('dj_rest_auth.urls')),
    path('login/', MyObtainTokenPairView.as_view(), name="token_obtain_pair"),
    path('user_info/', UserInfoView.as_view()),
    path('user_by_id/', UserByIdView.as_view()),
    path('trip_type/', TripTypeView.as_view()),
    path('trip/', TripView.as_view()),
    path('trip_id/', TripByIdView.as_view()),
    path('car_type/', CarTypeView.as_view()),
    path('stop_point/', StopPointView.as_view()),
    path('driver_balance/', DriverbalanceView.as_view()),
    path('driver/', DriverView.as_view()),
    path('driver_by_id/', DriverByIdView.as_view()),
    path('driver_review/', DriverReviewView.as_view()),
    path('trip_review/', TripReviewView.as_view()),
    path('message/', MessageView.as_view()),
    path('complain/', ComplainView.as_view()),
    path('coupon/<str:coupon>/', CouponView.as_view()),
    path('price/', PriceView.as_view()),
    path('places/', PlacesView.as_view()),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)