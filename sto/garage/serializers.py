from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Master, Client, Car, Appointment, ServiceRecord
from django.utils import timezone


class RegisterSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(write_only=True)
    address = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'phone', 'address')
        extra_kwargs = {'password': {'write_only': True}}

    def validate_phone(self, value):
        if len(value) != 10:
            raise serializers.ValidationError("Номер телефона должен быть ровно 10 символов")
        return value
    
    def create(self, validated_data):
        phone = validated_data.pop('phone')
        address = validated_data.pop('address')
        user = User.objects.create_user(**validated_data)
        Client.objects.create(user=user,phone=phone,address=address)
        return user
    
class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username",required=True)
    email = serializers.EmailField(source="user.email", required=True)
    phone = serializers.CharField(required=True)
    address = serializers.CharField()

    class Meta:
        model = Client
        fields = ("username", "email", "phone", "address")

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", {})

        instance.user.username = user_data.get("username",instance.user.username)
        instance.user.email = user_data.get("email",instance.user.email)
        instance.user.save()

        instance.phone = validated_data.get("phone",instance.phone)
        instance.address = validated_data.get("address",instance.address)

        instance.save()
        return instance

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = "__all__"
        read_only_fields = ["client"]


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ["car", "master", "status", "date", "description"]

    def validate_date(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Дата не может быть в прошлом")
        return value

    def validate_car(self, value):
        request = self.context.get("request")
        if request is not None:
            if value.client != request.user.client:
                raise serializers.ValidationError("Это не ваша машина")
        return value

    def validate_master(self, value):
        if Appointment.objects.filter(master=value,status="in_progress").exists():
            raise serializers.ValidationError("У мастера уже есть заказ")
        return value

    def create(self, validated_data):
        car = validated_data["car"]
        validated_data["client"] = car.client
        return Appointment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        validated_data.pop("car", None)
        return super().update(instance, validated_data)

class AppointmentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ["car", "master", "status", "date", "description"]

    def validate_date(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Дата не может быть в прошлом")
        return value

    def validate_master(self, value):
        if Appointment.objects.filter(master=value,status="in_progress").exists():
            raise serializers.ValidationError("У мастера уже есть заказ")
        return value

    def create(self, validated_data):
        car = validated_data["car"]
        validated_data["client"] = car.client
        return Appointment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        validated_data.pop("car", None)
        return super().update(instance, validated_data)
    
class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRecord
        fields = "__all__"