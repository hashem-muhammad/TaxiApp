from django.urls import path, include, re_path

from Api.views import CarTypeView, DriverCarView, MyObtainTokenPairView, MessageView, StopPointView, TripTypeView, TripView


from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="TAXI APP API",
        default_version='v1',
        description="API description",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    re_path(r'^docs/$', schema_view.with_ui('redoc',
                                            cache_timeout=0), name='schema-redoc'),
    path('auth/register/', include('dj_rest_auth.registration.urls')),
    path('auth/', include('dj_rest_auth.urls')),
    path('login/', MyObtainTokenPairView.as_view(), name="token_obtain_pair"),
    path('trip_type/', TripTypeView.as_view()),
    path('car_type/', CarTypeView.as_view()),
    path('stop_point/', StopPointView.as_view()),
    path('trip/', TripView.as_view()),
    path('driver_car/', DriverCarView.as_view()),
    path('message/', MessageView.as_view()),

]
