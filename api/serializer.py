import uuid

from rest_framework import serializers
from .models import User, Event, Registration


class UserRegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField()

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
            'confirm_password'
        ]

    def create(self, validated_data):
        validated_data['id'] = uuid.uuid4()
        validated_data.pop('confirm_password')
        return User.objects.create_user(**validated_data)

    def validated_password(self, password):
        if password != self.initial_data.get('confirm_password'):
            raise serializers.ValidationError('password doesnot match')
        return password


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = '__all__'

    def create(self, validated_data):
        validated_data['id'] = uuid.uuid4()
        return Event.objects.create(**validated_data)


class EventRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = '__all__'

    def create(self, validated_data):
        validated_data['id'] = uuid.uuid4()
        return Registration.objects.create(**validated_data)