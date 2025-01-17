import uuid

from rest_framework import serializers
from .models import User, Event, Registration


class UserRegisterSerializer(serializers.ModelSerializer):
    # define confirm password in serializer
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
        # remove confirm password from validate data
        validated_data.pop('confirm_password')
        return User.objects.create_user(**validated_data)

    # validate password
    def validated_password(self, password):
        # compare password with confirm password
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


class ReportSerializer(serializers.ModelSerializer):
    # define serilizer variables
    event = serializers.CharField(source='event.title')
    event_date = serializers.CharField(source='event.date')
    user = serializers.CharField(source='user.full_name')
    username = serializers.CharField(source='user.username')
    email = serializers.CharField(source='user.email')

    class Meta:
        model = Registration
        fields = [
            'id',
            'event',
            'event_date',
            'user',
            'username',
            'email',
            'created_at'
        ]
