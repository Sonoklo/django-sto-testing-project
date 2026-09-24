from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Master(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=30)
    specialization = models.CharField(max_length=50)
    phone = models.CharField(max_length=10, unique=True) 
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True) 

    def clean(self):
        if len(self.phone) != 10:
            raise ValidationError({"phone": "Номер телефона должен быть ровно 10 символов"})
    def __str__(self):
        return self.specialization
    
class Client(models.Model):
    user = models.OneToOneField(User,  on_delete=models.CASCADE, related_name="client")
    phone = models.CharField(max_length=20, unique=True)
    address = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if len(self.phone) != 10:
            raise ValidationError({"phone": "Номер телефона должен бфть ровно 10 символов"})
    
    def __str__(self):
        return self.user.first_name
    
class Car(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="cars")
    make = models.CharField(max_length=25)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    license_plate = models.CharField(max_length=8, unique=True)
    vin = models.CharField(max_length=30, blank=True, unique=True)

    def __str__(self):
        return self.model

class Appointment(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="appointments")
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="appointments")
    master = models.ForeignKey(Master, on_delete=models.CASCADE, related_name="appointments")
    date = models.DateTimeField()
    description = models.CharField(max_length=200)
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("in_progress", "In progress"),
        ("completed", "Completed"),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.status
class ServiceRecord(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    work_done = models.CharField(max_length=500)
    parts_used = models.CharField(max_length=200)
    total_cost = models.PositiveIntegerField()
    completed_at = models.DateTimeField()