from django.urls import path
from . import views
from django.contrib.auth.views import LoginView,LogoutView

urlpatterns = [
    path("register/", views.register, name="register_temp"),
    path("login/", LoginView.as_view(template_name="client/login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),

    path("cars/", views.car_list, name="cars_temp"),
    path("cars/add/", views.car_create, name="car_add"),

    path("appointments/", views.my_appointments, name="appointments_temp"),
    path("appointments/add/", views.make_appointment, name="appointment_add"),
    path("appointments/<int:pk>/", views.appointment_detail, name="appointment_detail_temp")
]