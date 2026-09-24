from rest_framework import generics, permissions, status, exceptions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
from .models import Master, Client, Car, Appointment, ServiceRecord
from .serializers import ProfileSerializer,RegisterSerializer,CarSerializer,AppointmentSerializer, AppointmentUpdateSerializer,HistorySerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

class ProfileRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        user = self.request.user

        if not user or not user.is_authenticated:
            raise exceptions.NotFound("User not found")
        return user.client
    
class CarListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CarSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return Car.objects.filter(client=self.request.user.client)
    def perform_create(self, serializer):
        serializer.save(client=self.request.user.client)

class CarRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CarSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return Car.objects.filter(client=self.request.user.client)
    
class AppointmentsListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(client=self.request.user.client)
    def get_queryset(self):
        return Appointment.objects.filter(client=self.request.user.client)

class AppointmentsRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AppointmentUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return Appointment.objects.filter(client=self.request.user.client)
    
class ServiceRecordListAPIView(generics.ListAPIView):
    serializer_class = HistorySerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return ServiceRecord.objects.filter(appointment__client=self.request.user.client)