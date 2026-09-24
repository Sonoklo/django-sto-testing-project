from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory
from garage.tests.factories import *
from garage.serializers import *
from garage.models import *

class RegisterSerializerTests(TestCase):
    def setUp(self):
        self.data = {'username': 'username_0', 'password': 'password_0','email': 'email@gmail.com', 'phone': "0" * 10,'address': 'address_0'}
    def test_serializer_is_valid(self):
        register_sr = RegisterSerializer(data=self.data)
        self.assertTrue(register_sr.is_valid())

    def test_models_creation(self):
        register_sr = RegisterSerializer(data=self.data)
        self.assertTrue(register_sr.is_valid())
        register_sr.save()
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Client.objects.count(), 1)

    def test_check_password(self):
        register_sr = RegisterSerializer(data=self.data)
        self.assertTrue(register_sr.is_valid())
        register_sr.save()
        user = User.objects.first()
        self.assertTrue(user.check_password(self.data["password"]))
        self.assertNotEqual(user.password, self.data["password"])

    def test_required_fields(self):
        for field in ["username", "password", "phone", "address"]:
            data = self.data.copy()
            data.pop(field)
            register_sr = RegisterSerializer(data=data)
            self.assertFalse(register_sr.is_valid(), f"{field} должен быть обязательным")

    def test_unique_username(self):
        register_sr = RegisterSerializer(data=self.data)
        self.assertTrue(register_sr.is_valid())
        register_sr.save()
        data = self.data.copy()
        data["email"] = "email_0@gmail.com"
        register_sr = RegisterSerializer(data=data)
        self.assertFalse(register_sr.is_valid())

    def test_invalid_email(self):
        self.data["email"] = "email"
        register_sr = RegisterSerializer(data=self.data)
        self.assertFalse(register_sr.is_valid())

    def test_invalid_phone(self):
        self.data["phone"] = "0"
        register_sr = RegisterSerializer(data=self.data)
        self.assertFalse(register_sr.is_valid())

class ProfileSerializerTests(TestCase):
    def setUp(self):
        self.data = {'username': 'username_0', 'email': 'email@gmail.com','phone': "0"*10, 'address': 'address_0'}
        self.client_obj = ClientFactory()

    def test_serializer_is_valid(self):
        profile_sr = ProfileSerializer(data=self.data)
        self.assertTrue(profile_sr.is_valid())

    def test_patch_update(self):
        data = {"username": "new"}
        profile_sr = ProfileSerializer(self.client_obj, data=data, partial=True)
        self.assertTrue(profile_sr.is_valid())
        profile = profile_sr.save()
        self.assertEqual(profile.user.username, data['username'])

    def test_put_update(self):
        profile_sr = ProfileSerializer(self.client_obj, data=self.data, partial=True)
        self.assertTrue(profile_sr.is_valid())
        profile = profile_sr.save()
        self.assertEqual(profile.user.username, self.data['username'])
        self.assertEqual(profile.user.email, self.data['email'])
        self.assertEqual(profile.phone, self.data['phone'])
        self.assertEqual(profile.address, self.data['address'])

    def test_serializer_return_right_fields(self):
        fields = ["username", "email", "phone", "address"]
        profile_sr = ProfileSerializer(self.client_obj)
        self.assertEqual(list(profile_sr.data.keys()), fields)

class CarSerializerTests(TestCase):
    def setUp(self):
        self.data = {'make':'make_0','model':'model_0','year': 2019,'license_plate': 'DF4532AW', 'vin': 'VIN123'}
    def test_serializer_is_valid(self):
        car_sr = CarSerializer(data=self.data)
        self.assertTrue(car_sr.is_valid())

    def test_model_creation(self):
        car_sr = CarSerializer(data=self.data)
        self.assertTrue(car_sr.is_valid())
        car_sr.save(client=ClientFactory())
        self.assertEqual(Car.objects.count(), 1)

    def test_client_read_only(self):
        data = self.data.copy()
        data["client"] = ClientFactory().id
        car_sr = CarSerializer(data=data)
        self.assertTrue(car_sr.is_valid())


class AppointmentSerializerTests(TestCase):
    def setUp(self):
        self.client = ClientFactory()
        self.car = CarFactory()
        self.master = MasterFactory()
        self.data = {"car":self.car,"master":self.master,"date":timezone.now()+timedelta(days=1),"description":"description_0"}

    def test_serializer_is_valid(self):
        appointment_sr = AppointmentSerializer(data=self.data)
        self.assertTrue(appointment_sr.is_valid())

    def test_model_creation(self):
        appointment_sr = AppointmentSerializer(data=self.data)
        self.assertTrue(appointment_sr.is_valid())
        appointment_sr.save(client=self.client_obj)
        self.assertEqual(Appointment.objects.count(), 1)

    def test_validate_date_with_incorect_date(self):
        self.data["date"] = timezone.now() - timedelta(days=1)
        appointment_sr = AppointmentSerializer(data=self.data)
        self.assertFalse(appointment_sr.is_valid())

    def test_validate_master(self):
        AppointmentFactory(master=self.master, status="in_progress")
        appointment_sr = AppointmentSerializer(data=self.data)
        self.assertFalse(appointment_sr.is_valid())

class AppointmentUpdateSerializerTests(TestCase):
    def setUp(self):
        self.client_obj = ClientFactory()
        self.car = CarFactory(client=self.client_obj)
        self.master = MasterFactory()
        self.data = {"car": self.car.id, "master": self.master.id,"status": "pending","date": timezone.now() + timedelta(days=1),"description": "description_0"}
    def test_serializer_is_valid(self):
        appointment_sr = AppointmentUpdateSerializer(data=self.data)
        self.assertTrue(appointment_sr.is_valid())

    def test_model_creation(self):
        appointment_sr = AppointmentUpdateSerializer(data=self.data)
        self.assertTrue(appointment_sr.is_valid())
        appointment_sr.save(client=self.client_obj)
        self.assertEqual(Appointment.objects.count(), 1)

    def test_car_read_only(self):
        appointment = AppointmentFactory(car=self.car)
        other_car = CarFactory(client=self.client_obj)
        appointment_sr = AppointmentUpdateSerializer(appointment, data={"car": other_car.id}, partial=True)
        self.assertTrue(appointment_sr.is_valid())
        updated = appointment_sr.save()
        self.assertEqual(updated.car, self.car)

class HistorySerializerTests(TestCase):
    def setUp(self):
        self.appointment = AppointmentFactory()
        self.data = {"appointment": self.appointment.id, "work_done": "work_done_0","parts_used": "parts_used_0", "total_cost": 100,"completed_at": timezone.now()}
    def test_serializer_is_valid(self):
        history_sr = HistorySerializer(data=self.data)
        self.assertTrue(history_sr.is_valid())

    def test_model_creation(self):
        history_sr = HistorySerializer(data=self.data)
        self.assertTrue(history_sr.is_valid())
        history_sr.save()
        self.assertEqual(ServiceRecord.objects.count(), 1)

    def test_fields_in_response(self):
        record = ServiceRecordFactory()
        history_sr = HistorySerializer(record)
        for field in ["appointment", "work_done", "parts_used", "total_cost", "completed_at"]:
            self.assertIn(field, history_sr.data)