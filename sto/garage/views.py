from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from .models import *
from .forms import *


def register(request):
    if request.method == "POST":
        user_form = RegisterForm(request.POST)
        client_form = ClientForm(request.POST)
        if user_form.is_valid() and client_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data["password"])
            user.save()
            client = client_form.save(commit=False)
            client.user = user
            client.save()
            return redirect("login")
    else:
        user_form = RegisterForm()
        client_form = ClientForm()
    return render(request, "client/register.html", {"user_form": user_form,"client_form": client_form})

@login_required
def dashboard(request):
    return render(request, "client/dashboard.html")

@login_required
def car_list(request):
    cars = request.user.client.cars.all()
    return render(request, "client/car_list.html", {"cars": cars})

@login_required
def car_create(request):
    if request.method == "POST":
        form = CarForm(request.POST)
        if form.is_valid():
            car = form.save(commit=False)
            car.client = request.user.client
            car.save()
            return redirect("cars_temp")
    else:
        form = CarForm()

    return render(request, "client/car_form.html", {"form": form})

@login_required
def make_appointment(request):
    form = AppointmentForm(request.POST or None,client=request.user.client)
    if request.method == "POST" and form.is_valid():
        app = form.save(commit=False)
        app.client = request.user.client
        app.save()
        return redirect("appointments_temp")

    return render(request,"client/appointment_form.html",{"form": form},)

@login_required
def my_appointments(request):
    appointments = Appointment.objects.filter(client=request.user.client)
    return render(request, "client/appointments.html", {"appointments": appointments})

@login_required
def appointment_detail(request, pk):
    appointment = get_object_or_404(Appointment,pk=pk,client=request.user.client)
    return render(request, "client/appointment_detail.html", {"appointment": appointment})