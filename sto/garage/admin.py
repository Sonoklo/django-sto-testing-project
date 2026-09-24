from django.contrib import admin
from .models import Master, Client, Car, Appointment, ServiceRecord



@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    pass

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    pass

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    pass

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    pass

@admin.register(ServiceRecord)
class ServiceRecordAdmin(admin.ModelAdmin):
    pass