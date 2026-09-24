from django import forms
from django.contrib.auth.models import User
from django.utils import timezone
from .models import *


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password"]


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ["phone", "address"]


class MasterForm(forms.ModelForm):
    class Meta:
        model = Master
        fields = ["first_name", "last_name", "specialization", "phone", "is_active"]


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ["make", "model", "year", "license_plate", "vin"]


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["car", "master", "date", "description"]
    
    def __init__(self, *args, client=None, **kwargs):
        super().__init__(*args, **kwargs)
        if client:
            self.fields["car"].queryset = client.cars.all()

    def clean(self):
        cleaned_data = super().clean()
        master = cleaned_data.get("master")
        date = cleaned_data.get("date")
        widgets = {"date": forms.DateInput(attrs={"type": "date"})}
        if date and date < timezone.now():
            raise forms.ValidationError("Дата не может быть в прошлом")

        if master and Appointment.objects.filter(master=master, status="in_progress").exists():
            raise forms.ValidationError("Мастер занят")

        return cleaned_data


class AppointmentStatusForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["status"]


class ServiceRecordForm(forms.ModelForm):
    class Meta:
        model = ServiceRecord
        fields = ["work_done", "parts_used", "total_cost", "completed_at"]