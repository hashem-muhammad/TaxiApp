from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
from Api.FCM_Manager import send_notify
from Api.models import AccountActivation, CarType, Complain, Coupon, Driver, DriverReview, Driverbalance, ExtraForCar, Message, Places, Price, Trip, TripReview, TripType, User
from Api.serializers import AccountActivationSerializer, CarTypeSerializer, ComplainSerializer, CouponSerializer, DriverReviewSerializer, DriverSerializer, DriverStatusSerializer, DriverbalanceSerializer, ExtraForCarSerializer, MessageSerializer, PlacesSerializer, PriceSerializer, StopPointSerializer, TripReviewSerializer, TripSerializer, TripTypeSerializer, MyTokenObtainPairSerializer, UserInfoSerializer, UserNotificationSerializer
from django.db.models import Q
from django.db.models import Sum
import pyotp


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        qs = User.objects.filter(id=request.user.id)
        serializer = UserInfoSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        try:
            get_user = User.objects.get(id=request.user.id)
            serializer = UserInfoSerializer(get_user,data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
            # User.objects.filter(id=request.user.id).update(**request.data)
                return Response({'updated!'}, status=status.HTTP_202_ACCEPTED)
            return Response(serializer.errors)
        except:
            return Response({'User not found'}, status=status.HTTP_400_BAD_REQUEST)


class UserByIdView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        get_user = request.GET.get('user_id', None)
        qs = User.objects.filter(id=get_user)
        serializer = UserInfoSerializer(qs, many=True)
        if qs.exists():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'No data'}, status=status.HTTP_404_NOT_FOUND)


class TripTypeView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        qs = TripType.objects.all()
        serializer = TripTypeSerializer(qs, many=True)
        if qs.exists():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'No data'}, status=status.HTTP_404_NOT_FOUND)


class CarTypeView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        qs = CarType.objects.all()
        serializer = CarTypeSerializer(qs, many=True)
        if qs.exists():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'No data'}, status=status.HTTP_404_NOT_FOUND)


class StopPointView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, *args, **kwargs):
        serializer = StopPointSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TripView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        trip_from_date = request.GET.get('from_date', None)
        trip_until_date = request.GET.get('until_date', None)
        get_trip = request.GET.get('trip_id', None)
        if not trip_from_date:
            qs = Trip.objects.filter(
                Q(user=request.user) | Q(driver=request.user))
            serializer = TripSerializer(qs, many=True)
            if qs.exists():
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'No data'}, status=status.HTTP_200_OK)
        else:
            qs = Trip.objects.filter(
                Q(user=request.user.id) | Q(driver=request.user.id)).filter(Q(created_at__range=[trip_from_date, trip_until_date]))
            serializer = TripSerializer(qs, many=True)
            if qs.exists():
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'No data'}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = TripSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            try:
                get_driver = User.objects.get(id=request.data.get('driver', None)).firebase_token
                if request.data.get('status') == 'new':
                    send_notify(get_driver, 'New order', serializer.data)
            except:
                pass
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        get_trip_id = request.query_params.get('trip_id', None)
        if get_trip_id:
            trip_data = request.data
            get_driver = Trip.objects.filter(id=get_trip_id)
            if get_driver.exists():
                get_driver.update(**trip_data)
                try:
                    get_user = User.objects.get(id=request.data.get('user', None)).firebase_token
                    send_notify(get_user, 'new trip status', trip_data)
                except:
                    pass
                return Response({'data updated'}, status=status.HTTP_202_ACCEPTED)
            return Response({'No data'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error'})


class TripByIdView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        get_trip = request.GET.get('trip_id', None)
        qs = Trip.objects.filter(
            Q(user=request.user) | Q(driver=request.user)).filter(id=get_trip)
        serializer = TripSerializer(qs, many=True)
        if qs.exists():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'No data'}, status=status.HTTP_404_NOT_FOUND)


class DriverView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        qs = Driver.objects.filter(user=request.user, active=True)
        serializer = DriverSerializer(qs, many=True)
        if qs.exists():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'No data'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        serializer = DriverSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        available = request.query_params.get('available', False)
        get_driver = Driver.objects.filter(user=request.user)
        if get_driver.exists():
            get_driver.update(available=available)
            return Response({'status': 'status updated'}, status=status.HTTP_202_ACCEPTED)
        return Response({'No data'}, status=status.HTTP_400_BAD_REQUEST)



class DriverByIdView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        get_driver = request.GET.get('driver_id', None)
        qs = Driver.objects.filter(user__id=get_driver).select_related('user')
        serializer = DriverSerializer(qs, many=True)
        if qs.exists():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'No data'}, status=status.HTTP_404_NOT_FOUND)


class MessageView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        qs = Message.objects.filter(user=request.user)
        serializer = MessageSerializer(qs, many=True)
        if qs.exists():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'No data'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CouponView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, coupon, *args, **kwargs):
        qs = Coupon.objects.filter(coupon=coupon)
        serilaizer = CouponSerializer(qs, many=True)
        if qs.exists():
            return Response(serilaizer.data, status=status.HTTP_200_OK)
        return Response({'No data'}, status=status.HTTP_404_NOT_FOUND)


class PriceView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        qs = Price.objects.all()
        serializer = PriceSerializer(qs, many=True)
        if qs.exists():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'No data'}, status=status.HTTP_404_NOT_FOUND)


class TripReviewView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        qs = TripReview.objects.filter(
            Q(user_id=request.user) | Q(driver_id=request.user))
        serializer = TripReviewSerializer(qs, many=True)
        if qs.exists():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'No data'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        serializer = TripReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DriverReviewView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        qs = DriverReview.objects.filter(
            Q(user_id=request.user) | Q(driver_id=request.user))
        serializer = DriverReviewSerializer(qs, many=True)
        if qs.exists():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'No data'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        serializer = DriverReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ComplainView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        qs = Complain.objects.filter(user=request.user)
        serializer = ComplainSerializer(qs, many=True)
        if qs.exists():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'No data'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        serializer = ComplainSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlacesView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        qs = Places.objects.filter(user=request.user)
        serializer = PlacesSerializer(qs, many=True)
        if qs.exists():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'No data'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        serializer = PlacesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        get_type = request.query_params.get('all', False)
        get_place_id = request.query.params.get('place_id', None)
        if get_type:
            Places.objects.filter(user=request.user).delete()
            return Response({'status':True}, status=status.HTTP_202_ACCEPTED)
        elif get_place_id:
            Places.objects.filter(user=request.user, id=get_place_id).delete()
            return Response({'status':True}, status=status.HTTP_202_ACCEPTED)
        return Response({'status':False}, status=status.HTTP_200_OK)


class DriverbalanceView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        qs = Driverbalance.objects.filter(
            driver=request.user, activate=True).aggregate(total_balance=Sum('balance'))
        return Response(qs, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = DriverbalanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(driver=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DirverStatusView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        try:
            qs = Driver.objects.filter(user=request.user)
            serializer = DriverStatusSerializer(qs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserNotificationView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def patch(self, request, *args, **kwargs):
        qs = User.objects.get(id=request.user.id)
        serializer = UserNotificationSerializer(qs, many=True, partial=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AccountActivationView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        otp = request.query_params.get('otp', None)
        check_otp = AccountActivation.objects.filter(user=request.user, otp=otp).exists()
        if check_otp:
            AccountActivation.objects.filter(user=request.user).update(status=True)
            return Response({'valid':True}, status=status.HTTP_200_OK)
        return Response({'valid':False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        get_request_otp = request.data.get('otp', None)
        totp = pyotp.TOTP('base32secret3232', interval=1080, digits=4)
        otp = totp.now()
        AccountActivation.objects.create(user=request.user, otp=otp)
        return Response({'otp':'created'}, status=status.HTTP_200_OK)



class ExtarForCarView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        qs = ExtraForCar.objects.filter(active=True)
        serializer = ExtraForCarSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    