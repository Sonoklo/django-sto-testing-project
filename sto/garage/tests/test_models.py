
from django.urls import reverse
from rest_framework.test import APITestCase
from .factories import *
from rest_framework import status
from datetime import timedelta
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.test import TestCase
from django.core.exceptions import ValidationError
from garage.models import *


class MasterTest(TestCase):
    def setUp(self):
        self.data = {"first_name": "first_name_0", "last_name": "last_name_0","specialization": "specialization_0", "phone": "1" * 10}

    def test_create_master(self):
        master = Master.objects.create(**self.data)
        self.assertEqual(master.first_name, self.data["first_name"])
        self.assertEqual(master.last_name, self.data["last_name"])
        self.assertEqual(master.specialization, self.data["specialization"])
        self.assertEqual(master.phone, self.data["phone"])
        self.assertFalse(master.is_active)

    def test_get_master(self):
        master_fac = MasterFactory()
        master = Master.objects.first()
        self.assertEqual(master.first_name, master_fac.first_name)
        self.assertEqual(master.last_name, master_fac.last_name)
        self.assertEqual(master.specialization, master_fac.specialization)
        self.assertEqual(master.phone, master_fac.phone)
        self.assertFalse(master.is_active)

    def test_get_master_str(self):
        master = MasterFactory()
        self.assertEqual(str(master), master.specialization)

    def test_phone_is_unique(self):
        master = MasterFactory()
        with self.assertRaises(IntegrityError):
            MasterFactory(phone=master.phone)

    def test_clean(self):
        master = MasterFactory(phone="123")
        with self.assertRaises(ValidationError):
            master.clean()

    def test_default_is_active_false(self):
        master = Master.objects.create(**self.data)
        self.assertFalse(master.is_active)

class ClientTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.data = {"user":self.user, "phone":"1111111111", "address":"address_0"}

    def test_create_client(self):
        client = Client.objects.create(**self.data)
        self.assertEqual(client.user, self.user)
        self.assertEqual(client.phone, self.data["phone"])
        self.assertEqual(client.address, self.data["address"])

    def test_get_client(self):
        Client.objects.create(**self.data)
        client = Client.objects.first()
        self.assertEqual(client.user, self.user)
        self.assertEqual(client.phone, self.data["phone"])
        self.assertEqual(client.address, self.data["address"])

    def test_get_client_str(self):
        client = ClientFactory()
        self.assertEqual(str(client), client.user.first_name)

    def test_clean(self):
        client = ClientFactory(phone="123")
        with self.assertRaises(ValidationError):
            client.clean()

    def test_client_user_connection(self):
        client = Client.objects.create(**self.data)
        self.assertEqual(client.user.id, self.user.id)

    def test_client_on_delete(self):
        client = Client.objects.create(**self.data)
        client_id = client.id
        self.user.delete()
        self.assertIsNone(Client.objects.filter(id=client_id).first())

    def test_phone_is_unique(self):
        Client.objects.create(**self.data)
        other_user = UserFactory()
        with self.assertRaises(IntegrityError):
            Client.objects.create(user=other_user, phone=self.data["phone"], address="a")

class CarTest(TestCase):
    def setUp(self):
        self.client_obj = ClientFactory()
        self.data = {"client": self.client_obj, "make": "make_0", "model": "model_0","year": 2020, "license_plate": "AA1234AA", "vin": "vin123"}

    def test_create_car(self):
        car = Car.objects.create(**self.data)
        self.assertEqual(car.client, self.data["client"])
        self.assertEqual(car.make, self.data["make"])
        self.assertEqual(car.model, self.data["model"])
        self.assertEqual(car.year, self.data["year"])
        self.assertEqual(car.license_plate, self.data["license_plate"])
        self.assertEqual(car.vin, self.data["vin"])

    def test_get_car(self):
        Car.objects.create(**self.data)
        car = Car.objects.first()
        self.assertEqual(car.client, self.data["client"])
        self.assertEqual(car.make, self.data["make"])
        self.assertEqual(car.model, self.data["model"])
        self.assertEqual(car.year, self.data["year"])
        self.assertEqual(car.license_plate, self.data["license_plate"])
        self.assertEqual(car.vin, self.data["vin"])

    def test_get_car_str(self):
        car = CarFactory()
        self.assertEqual(str(car), car.model)

    def test_year_negativ_number(self):
        with self.assertRaises(IntegrityError):
            CarFactory(year=-1)

    def test_car_client_connection(self):
        car = Car.objects.create(**self.data)
        self.assertEqual(car.client.id, self.data["client"].id)

    def test_car_on_delete(self):
        car = Car.objects.create(**self.data)
        car_id = car.id
        self.client_obj.delete()
        self.assertIsNone(Car.objects.filter(id=car_id).first())

    def test_car_unique_license_plate(self):
        car = CarFactory()
        with self.assertRaises(IntegrityError):
            CarFactory(license_plate=car.license_plate)

    def test_car_unique_vin(self):
        car = CarFactory()
        with self.assertRaises(IntegrityError):
            CarFactory(vin=car.vin)

class AppointmentTest(TestCase):
    def setUp(self):
        self.client_obj = ClientFactory()
        self.car = CarFactory(client=self.client_obj)
        self.master = MasterFactory()
        self.data = {"client": self.client_obj, "car": self.car, "master": self.master,"date": timezone.now() + timedelta(days=1), "description": "description_0"}

    def test_create_appointment(self):
        appointment = Appointment.objects.create(**self.data)
        self.assertEqual(appointment.client, self.data["client"])
        self.assertEqual(appointment.car, self.data["car"])
        self.assertEqual(appointment.master, self.data["master"])
        self.assertEqual(appointment.date, self.data["date"])
        self.assertEqual(appointment.description, self.data["description"])

    def test_get_appointment(self):
        Appointment.objects.create(**self.data)
        appointment = Appointment.objects.first()
        self.assertEqual(appointment.client, self.data["client"])
        self.assertEqual(appointment.car, self.data["car"])
        self.assertEqual(appointment.master, self.data["master"])
        self.assertEqual(appointment.date, self.data["date"])
        self.assertEqual(appointment.description, self.data["description"])

    def test_get_appointment_str(self):
        appointment = AppointmentFactory()
        self.assertEqual(str(appointment), appointment.status)

    def test_default_status_pending(self):
        appointment = Appointment.objects.create(**self.data)
        self.assertEqual(appointment.status, "pending")

    def test_appointment_client_on_delete(self):
        appointment = Appointment.objects.create(**self.data)
        app_id = appointment.id
        self.client_obj.delete()
        self.assertIsNone(Appointment.objects.filter(id=app_id).first())

    def test_appointment_car_on_delete(self):
        appointment = Appointment.objects.create(**self.data)
        app_id = appointment.id
        self.car.delete()
        self.assertIsNone(Appointment.objects.filter(id=app_id).first())

    def test_appointment_master_on_delete(self):
        appointment = Appointment.objects.create(**self.data)
        app_id = appointment.id
        self.master.delete()
        self.assertIsNone(Appointment.objects.filter(id=app_id).first())

    def test_appointment_valid_statuses(self):
        for status_value in ["pending", "in_progress", "completed"]:
            app = AppointmentFactory(status=status_value)
            self.assertEqual(app.status, status_value)

class ServiceRecordTest(TestCase):
    def setUp(self):
        self.appointment = AppointmentFactory()
        self.data = {"appointment": self.appointment, "work_done": "work_done_0","parts_used": "parts_used_0", "total_cost": 100,"completed_at": timezone.now()}

    def test_create_service_record(self):
        service_record = ServiceRecord.objects.create(**self.data)
        self.assertEqual(service_record.appointment, self.data["appointment"])
        self.assertEqual(service_record.work_done, self.data["work_done"])
        self.assertEqual(service_record.parts_used, self.data["parts_used"])
        self.assertEqual(service_record.total_cost, self.data["total_cost"])
        self.assertEqual(service_record.completed_at, self.data["completed_at"])

    def test_get_service_record(self):
        ServiceRecord.objects.create(**self.data)
        service_record = ServiceRecord.objects.first()
        self.assertEqual(service_record.appointment, self.data["appointment"])
        self.assertEqual(service_record.work_done, self.data["work_done"])
        self.assertEqual(service_record.parts_used, self.data["parts_used"])
        self.assertEqual(service_record.total_cost, self.data["total_cost"])
        self.assertEqual(service_record.completed_at, self.data["completed_at"])

    def test_service_record_appointment_connection(self):
        service_record = ServiceRecord.objects.create(**self.data)
        self.assertEqual(service_record.appointment.id, self.data["appointment"].id)

    def test_service_record_appointment_on_delete(self):
        service_record = ServiceRecord.objects.create(**self.data)
        record_id = service_record.id
        self.appointment.delete()
        self.assertIsNone(ServiceRecord.objects.filter(id=record_id).first())

    def test_service_record_negative_total_cost(self):
        with self.assertRaises(IntegrityError):
            ServiceRecordFactory(total_cost=-100)