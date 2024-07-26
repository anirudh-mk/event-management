import uuid

from rest_framework import serializers
from .models import User


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
