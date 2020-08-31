from django.contrib.auth import authenticate
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import serializers
from django.contrib.auth.models import User

from pension_base.generic.execption.generi_execption import GenericException
from pension_base.models import ConsoleUser

__author__ = 'Falul Kabir Shohag'


class ApiTokenSerializer(AuthTokenSerializer):

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if not (username and password):
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        if not User.objects.filter(username=username).exists():
            raise GenericException(message='Username does not exist in the system.', status_code=470)

        console_user = ConsoleUser.objects.filter(user__username=username).first()
        if not console_user:
            raise GenericException(message="Provided username does not exist in the system.", status_code=470)

        user = authenticate(username=username, password=password)

        if not user:
            raise GenericException(message='Password is incorrect for provided username.', status_code=475)

        attrs['user'] = user
        return attrs
