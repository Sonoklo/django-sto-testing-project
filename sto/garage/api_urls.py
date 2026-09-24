from django.urls import path
from . import api_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path("register/", api_views.RegisterAPIView.as_view(), name="register"),
    path("profile/", api_views.ProfileRetrieveUpdateDestroyAPIView.as_view(), name="profile"),
    path("token/", TokenObtainPairView.as_view(), name="token"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("cars/", api_views.CarListCreateAPIView.as_view(), name="cars"),
    path("cars/<int:pk>/", api_views.CarRetrieveUpdateDestroyAPIView.as_view(), name="car-deteiled"),
    path("appointments/", api_views.AppointmentsListCreateAPIView.as_view(), name="appointments"),
    path("appointments/<int:pk>/", api_views.AppointmentsRetrieveUpdateDestroyAPIView.as_view(), name="appointments-deteiled"),
    path("history/", api_views.ServiceRecordListAPIView.as_view(), name="history")
]