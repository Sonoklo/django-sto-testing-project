from django.urls import reverse
from rest_framework.test import APITestCase
from .factories import *
from rest_framework import status
from datetime import timedelta
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from garage.models import Client


class RegisterAPIViewTests(APITestCase):
    def setUp(self):
        self.url = reverse('register')
        self.data = {"username": "username","password": "password123","email": "t@gmail.com","phone": "3800000000","address": "address"}

    def test_register(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Client.objects.count(), 1)

    def test_register_with_fail_data(self):
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.data.pop("password")
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_not_unique_username(self):
        UserFactory(username="username")
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_and_get_user(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.first().username, self.data["username"])

    def test_register_and_check_client_creation(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Client.objects.first().phone, self.data["phone"])

    def test_register_not_unique_email(self):
        UserFactory(email=self.data["email"])
        response = self.client.post(self.url,self.data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

    def test_is_all_right_data_created(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.first()
        client = Client.objects.first()
        self.assertEqual(user.username, self.data["username"])
        self.assertEqual(user.email, self.data["email"])

        self.assertEqual(client.phone, self.data["phone"])
        self.assertEqual(client.address, self.data["address"])

class ProfileAPIViewTests(APITestCase):
    def setUp(self):
        self.client_obj = ClientFactory()
        # self.client.force_authenticate(self.client_obj.user)
        self.user = UserFactory()
        self.url = reverse('profile')
        self.data = {"username":"username_0", "email":"email_0", "phone":"3800000000", "address":"address_0"}

    def test_get_profile(self):
        self.client.force_authenticate(self.client_obj.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"],self.client_obj.user.username)

    def test_without_auth(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_profile(self):
        self.client.force_authenticate(self.client_obj.user)
        data_updated = {"address": "new"}
        phone = self.client_obj.phone
        response = self.client.patch(self.url,data_updated)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client_obj.refresh_from_db()
        self.assertEqual(self.client_obj.address, data_updated["address"])
        self.assertEqual(self.client_obj.phone, phone)

    def test_patch_profile_with_incorrect_data(self):
        self.client.force_authenticate(self.client_obj.user)
        response = self.client.patch(self.url,data={})
        self.assertEqual(response.status_code, status.HTTP_200_OK) 
        response = self.client.patch(self.url,data={"incorrect_field":1})
        self.assertEqual(response.status_code, status.HTTP_200_OK) 

    def test_put_profile(self):
        self.client.force_authenticate(self.client_obj.user)
        response = self.client.put(self.url,data=self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK) 
        self.assertEqual(Client.objects.first().user.username,self.data["username"])

    def test_put_profile_with_incorrect_data(self):
        self.client.force_authenticate(self.client_obj.user)
        response = self.client.put(self.url,data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.data.pop("username")
        response = self.client.put(self.url,data=self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_profile(self):
        self.client.force_authenticate(self.client_obj.user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Client.objects.filter(id=self.client_obj.id).exists())
        

class CarAPIViewTests(APITestCase):
    def setUp(self):
        self.client_obj = ClientFactory()
        
        self.car = CarFactory(client=self.client_obj)
        self.url = reverse("cars")
    def test_car_list(self):
        self.client.force_authenticate(self.client_obj.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_car_create(self):
        self.client.force_authenticate(self.client_obj.user)
        data = {"make": "make_2","model": "model_2","year": 2023,"license_plate": "lic","vin": "VIN123"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Car.objects.count(), 2)

    def test_created_car_is_users(self):
        self.client.force_authenticate(self.client_obj.user)
        self.assertEqual(Car.objects.first().client.id, self.client_obj.id)
    def test_car_create_with_incorrect_data(self):
        self.client.force_authenticate(self.client_obj.user)
        response = self.client.post(self.url,{})
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        data = {"make":"make_0","model":"model_0","year":2020,"license_plate":"license_0"}
        response = self.client.post(self.url,data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

    def test_create_car_without_auth(self):
        data = {"make":"make_0","model":"model_0","year":2020,"license_plate":"license_0","vin":"vin_0"}
        response = self.client.post(self.url,data)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

class CarRetrieveUpdateDestroyAPIView(APITestCase):
    def setUp(self):
        self.client_obj = ClientFactory()
        self.car = CarFactory(client=self.client_obj)
        self.url = reverse("car-deteiled", kwargs={"pk":self.car.id})
        self.data = {"make":"make_0","model":"model_0","year":2020,"license_plate":"AA1111BB","vin":"vin_0"}
    def test_car_get(self):
        self.client.force_authenticate(self.client_obj.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_get_car_by_incorrect_pk(self):
        self.client.force_authenticate(self.client_obj.user)
        response = self.client.get(reverse("car-deteiled",kwargs={"pk":2}))
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
    def test_get_car_another_users(self):
        client = ClientFactory()
        self.client.force_authenticate(client.user)
        response = self.client.get(reverse("car-deteiled",kwargs={"pk":self.car.id}))
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
        
    def test_without_auth(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_car(self):
        self.client.force_authenticate(self.client_obj.user)
        response = self.client.patch(self.url,{"make":"make_0"})
        self.car.refresh_from_db()
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(self.car.make,"make_0")

    def test_patch_car_with_incorrect_data(self):
        self.client.force_authenticate(self.client_obj.user)
        response = self.client.patch(self.url,{})
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        response = self.client.patch(self.url,{"year":-1})
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

    def test_put_car(self):
        self.client.force_authenticate(self.client_obj.user)
        response = self.client.put(self.url,self.data)
        self.car.refresh_from_db()
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(self.car.make,"make_0")
        self.assertEqual(self.car.model,"model_0")
        self.assertEqual(self.car.year,2020)
        self.assertEqual(self.car.license_plate,"AA1111BB")
        self.assertEqual(self.car.vin,"vin_0")

    def test_put_car_with_incorrect_data(self):
        self.client.force_authenticate(self.client_obj.user)
        response = self.client.put(self.url,{})
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        response = self.client.put(self.url,{"make":"make_0"})
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

    def test_delete_car(self):
        self.client.force_authenticate(self.client_obj.user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
        self.assertFalse(Car.objects.filter(id=self.car.id).exists())

class AppointmentsListCreateAPIViewTests(APITestCase):
    def setUp(self):
        self.client_obj = ClientFactory()
        self.client.force_authenticate(self.client_obj.user)
        self.car = CarFactory(client=self.client_obj)
        self.master = MasterFactory()
        self.url = reverse("appointments")
        self.data = {"car":self.car.id,"master":self.master.id,"date":timezone.now()+timedelta(hours=1),"description":"description_0"}

    def test_appointment_list(self):
        AppointmentFactory(client=self.client_obj,car=self.car,master=self.master)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(len(response.data),1)

    def test_appointment_create(self):
        response = self.client.post(self.url,self.data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(Appointment.objects.count(),1)

    def test_appointment_create_with_incorrect_data(self):
        response = self.client.post(self.url,{})
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.data.pop("description")
        response = self.client.post(self.url,self.data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

    def test_create_appointment_without_auth(self):
        self.client.force_authenticate(user=None)
        response = self.client.post(self.url,self.data)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

    def test_without_auth(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

class AppointmentsRetrieveUpdateDestroyAPIViewTest(APITestCase):
    def setUp(self):
        self.client_obj = ClientFactory()
        self.client.force_authenticate(self.client_obj.user)
        self.car = CarFactory(client=self.client_obj)
        self.master = MasterFactory()
        self.appointment = AppointmentFactory(client=self.client_obj,car=self.car,master=self.master)
        self.url = reverse("appointments-deteiled",kwargs={"pk":1})
        self.data = {"car":self.car.id,"master":self.master.id,"date":timezone.now()+timedelta(days=1),"description":"description_0"}

    def test_appointment_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_get_appointment_by_incorrect_pk(self):
        response = self.client.get(reverse("appointments-deteiled",kwargs={"pk":2}))
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)

    def test_get_appointment_another_users(self):
        client = ClientFactory()
        self.client.force_authenticate(client.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)

    def test_without_auth(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

    def test_patch_appointment(self):
        response = self.client.patch(self.url,{"description":"description_1"})
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.appointment.refresh_from_db()
        self.assertEqual(self.appointment.description,"description_1")

    def test_patch_appointment_with_incorrect_data(self):
        response = self.client.patch(self.url,{"date":"incorrect"})
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

    def test_put_appointment(self):
        response = self.client.put(self.url,self.data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.appointment.refresh_from_db()
        self.assertEqual(self.appointment.description,self.data["description"])
        self.assertEqual(self.appointment.car.id,self.data["car"])
        self.assertEqual(self.appointment.master.id,self.data["master"])

    def test_put_appointment_with_incorrect_data(self):
        response = self.client.put(self.url,{})
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.data.pop("description")
        response = self.client.put(self.url,self.data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

    def test_delete_appointment(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
        self.assertFalse(Appointment.objects.filter(id=self.appointment.id).exists())


class ServiceRecordAPIViewTest(APITestCase):
    def setUp(self):
        self.client_obj = ClientFactory()
        self.client.force_authenticate(self.client_obj.user)
        self.car = CarFactory(client=self.client_obj)
        self.master = MasterFactory()
        self.appointment = AppointmentFactory(client=self.client_obj,car=self.car,master=self.master)
        self.record = ServiceRecordFactory(appointment=self.appointment)
        self.url = reverse("history")

    def test_service_record_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(len(response.data),1)
        self.assertEqual(response.data[0]["work_done"],self.record.work_done)
        self.assertEqual(response.data[0]["parts_used"],self.record.parts_used)

    def test_service_record_without_auth(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

    def test_service_record_data(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data[0]["work_done"],self.record.work_done)
        self.assertEqual(response.data[0]["parts_used"],self.record.parts_used)
        self.assertEqual(response.data[0]["total_cost"],self.record.total_cost)
