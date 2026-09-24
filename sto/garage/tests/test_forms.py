from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from garage.tests.factories import *
from garage.forms import *

class RegisterFormTests(TestCase):
    def test_is_valid_form(self):
        form = RegisterForm(data={"username":"username","first_name":"first_name","last_name":"last_name","email":"t@gmail.com","password":"password123"})
        self.assertTrue(form.is_valid())

    def test_is_valid_form_with_incorrect_data(self):
        form = RegisterForm(data={"username":1,"last_name":1,"email":"email","password":123})
        self.assertFalse(form.is_valid())
    def test_without_username(self):
        form = RegisterForm(data={"email":"t@gmail.com","password":"password123"})
        self.assertFalse(form.is_valid())
    def test_form_with_non_existen_data(self):
        form = RegisterForm(data={"no_exist1":"1","no_exist2":"2"})
        self.assertFalse(form.is_valid())

class ClientFormTests(TestCase):
    def test_valid_form(self):
        user = UserFactory()
        form = ClientForm(data={"user": user.id, "phone": "3800000000", "address": "address"})
        self.assertTrue(form.is_valid())

    def test_without_phone(self):
        user = UserFactory()
        form = ClientForm(data={"user": user.id, "address": "address"})
        self.assertFalse(form.is_valid())

    def test_without_user(self):
        form = ClientForm(data={"phone": "3800000000", "address": "address"})
        self.assertTrue(form.is_valid())

class MasterFormTests(TestCase):
    def test_valid_form(self):
        form = MasterForm(data={"first_name": "first_name", "last_name": "last_name","specialization": "specialization", "phone": "3800000000","is_active": True})
        self.assertTrue(form.is_valid())

    def test_without_specialization(self):
        form = MasterForm(data={"first_name": "first_name", "last_name": "last_name","phone": "3800000000", "is_active": True})
        self.assertFalse(form.is_valid())

class CarFormTests(TestCase):
    def test_valid_form(self):
        form = CarForm(data={"make": "make", "model": "model", "year": 2022, "license_plate": "aa2222cc", "vin": "vin123"})
        self.assertTrue(form.is_valid())
    def test_without_make(self):
        form = CarForm(data={"model":"model","year":2025,"license_plate":"aa2223cc", "vin": "vin123"})
        self.assertFalse(form.is_valid())
    def test_invalid_year(self):
        form = CarForm(data={"make": "make", "model": "model", "year": "year", "license_plate":"aa2224cc", "vin": "vin123"})
        self.assertFalse(form.is_valid())

class AppointmentFormTests(TestCase):
    def setUp(self):
        self.client_obj = ClientFactory()
        self.car = CarFactory(client=self.client_obj)
        self.master = MasterFactory()
        self.data={"car": self.car.id,"master": self.master.id,"date": timezone.now()+timedelta(days=2),"description": "description"}
    def test_valid_form(self):
        form = AppointmentForm(data={"car": self.car.id, "master": self.master.id, "date": timezone.now() + timedelta(days=1), "description": "description"}, client=self.client_obj)
        self.assertTrue(form.is_valid())

    def test_date_in_past(self):
        form = AppointmentForm(data={"car": self.car.id, "master": self.master.id, "date": timezone.now()-timedelta(days=1), "description": "description"}, client=self.client_obj)
        self.assertFalse(form.is_valid())

    def test_master_is_busy(self):
        AppointmentFactory(master=self.master,status="in_progress",date=timezone.now() + timedelta(days=1))
        form = AppointmentForm(data=self.data,client=self.client_obj)
        self.assertFalse(form.is_valid())
        
class AppointmentStatusFormTests(TestCase):
    def test_valid_form(self):
        form = AppointmentStatusForm(data={"status": "pending"})
        self.assertTrue(form.is_valid())
    def test_empty_status(self):
        form = AppointmentStatusForm(data={})
        self.assertFalse(form.is_valid())
    def test_completed_status(self):
        form = AppointmentStatusForm(data={"status": "completed"})
        self.assertTrue(form.is_valid())

class ServiceRecordFormTests(TestCase):
    def test_valid_form(self):
        form = ServiceRecordForm(data={"work_done": "work_done", "parts_used": "parts_used", "total_cost": 100, "completed_at": timezone.now()})
        self.assertTrue(form.is_valid())

    def test_without_work_done(self):
        form = ServiceRecordForm(data={"parts_used": "parts_used", "total_cost": 100, "completed_at": timezone.now()})
        self.assertFalse(form.is_valid())

    def test_negative_cost(self):
        form = ServiceRecordForm(data={"work_done": "work_done", "parts_used": "parts_used", "total_cost": -100, "completed_at": timezone.now()})
        self.assertFalse(form.is_valid())