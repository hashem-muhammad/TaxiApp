from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
from Api.models import CarType, Complain, Coupon, Driver, DriverReview, Driverbalance, Message, Places, Price, Trip, TripReview, TripType, User
from Api.serializers import CarTypeSerializer, ComplainSerializer, CouponSerializer, DriverReviewSerializer, DriverSerializer, DriverbalanceSerializer, MessageSerializer, PlacesSerializer, PriceSerializer, StopPointSerializer, TripReviewSerializer, TripSerializer, TripTypeSerializer, MyTokenObtainPairSerializer, UserInfoSerializer
from django.db.models import Q


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
        print(request.data)
        User.objects.filter(id=request.user.id).update(**request.data)
        return Response({'updated!'}, status=status.HTTP_202_ACCEPTED)


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
        if not trip_from_date:
            qs = Trip.objects.filter(
                Q(user=request.user.id) | Q(driver=request.user.id))
            serializer = TripSerializer(qs, many=True)
            if qs.exists():
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'No data'}, status=status.HTTP_404_NOT_FOUND)
        else:
            qs = Trip.objects.filter(
                Q(user=request.user.id) | Q(driver=request.user.id)).filter(Q(created_at__range=[trip_from_date, trip_until_date]))
            serializer = TripSerializer(qs, many=True)
            if qs.exists():
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'No data'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        serializer = TripSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        get_trip_id = request.query_params.get('trip_id', None)
        if get_trip_id:
            trip_data = request.data
            get_driver = Trip.objects.filter(id=get_trip_id)
            if get_driver.exists():
                get_driver.update(**trip_data)
                return Response({'data updated'}, status=status.HTTP_202_ACCEPTED)
            return Response({'No data'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error'})


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


class DriverbalanceView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        qs = Driverbalance.objects.filter(
            driver=request.user, activate=True).last()
        serializer = DriverbalanceSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = DriverbalanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(driver=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
