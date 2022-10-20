from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
from Api.models import CarType, Coupon, Driver, DriverCar, Message, Price, Trip, TripType
from Api.serializers import CarTypeSerializer, CouponSerializer, DriverCarSerializer, DriverSerializer, MessageSerializer, PriceSerializer, StopPointSerializer, TripSerializer, TripTypeSerializer, MyTokenObtainPairSerializer


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class TripTypeView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        qs = TripType.objects.all()
        serializer = TripTypeSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CarTypeView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        qs = CarType.objects.all()
        serializer = CarTypeSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
        qs = Trip.objects.all()
        serializer = TripSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DriverCarView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        qs = DriverCar.objects.filter(user=request.user)
        serializer = DriverCarSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = DriverCarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DriverView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        qs = Driver.objects.filter(user=request.user)
        serializer = DriverSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = DriverSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessageView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        qs = Message.objects.filter(user=request.user)
        serializer = MessageSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
        return Response(serilaizer.data, status=status.HTTP_200_OK)


class PriceView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        qs = Price.objects.all()
        serializer = PriceSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
