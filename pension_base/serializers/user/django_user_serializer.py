from django.contrib.auth.models import User
from rest_framework import serializers

__author__ = 'Fazlul Kabir shohag'


class DjangoUserSerializer(serializers.ModelSerializer):
    def is_valid(self, raise_exception=False):
        return True

    def update(self, instance, attrs):
        instance = super().update(instance, attrs)
        if attrs.get('password', None):
            instance.set_password(attrs.get('password'))
        instance.save()
        return instance

    def validate_username(self, value):
        user = User.objects.filter(username=value)
        if user.exists():
            raise serializers.ValidationError("Username already exists.")

        return value

    class Meta:
        model = User
        fields = ('id', 'username')
        read_only_fields = ('id',)