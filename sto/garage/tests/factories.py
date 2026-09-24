import factory
from factory.django import DjangoModelFactory
from django.contrib.auth.models import User
from garage.models import Master, Client, Car, Appointment, ServiceRecord
from django.utils import timezone

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.Sequence(lambda n: f"user{n}@gmail.com")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    password = factory.PostGenerationMethodCall("set_password", "testpass123")


class ClientFactory(DjangoModelFactory):
    class Meta:
        model = Client
    user = factory.SubFactory(UserFactory)
    phone = factory.Sequence(lambda n: f"{3800000000+n}")
    address = factory.Faker("address")


class MasterFactory(DjangoModelFactory):
    class Meta:
        model = Master
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    specialization = factory.Sequence(lambda n: f"spec_{n}")
    phone = factory.Sequence(lambda n: f"{3800000000+n}")
    is_active = False


class CarFactory(DjangoModelFactory):
    class Meta:
        model = Car
    client = factory.SubFactory(ClientFactory)
    make = factory.Sequence(lambda n: f"make_{n}")
    model = factory.Sequence(lambda n: f"model_{n}")
    year = 2022
    license_plate = factory.Sequence(lambda n: f"AA{n:04}AA")
    vin = factory.Sequence(lambda n: f"VIN{n}")


class AppointmentFactory(DjangoModelFactory):
    class Meta:
        model = Appointment
    client = factory.SubFactory(ClientFactory)
    car = factory.SubFactory(CarFactory)
    master = factory.SubFactory(MasterFactory)
    date = factory.LazyFunction(timezone.now)
    description = factory.Sequence(lambda n: f"description_{n}")
    status = "pending"


class ServiceRecordFactory(DjangoModelFactory):
    class Meta:
        model = ServiceRecord
    appointment = factory.SubFactory(AppointmentFactory)
    work_done = factory.Sequence(lambda n: f"work_done_{n}")
    parts_used = factory.Sequence(lambda n: f"parts_used_{n}")
    total_cost = 100
    completed_at = factory.LazyFunction(timezone.now)