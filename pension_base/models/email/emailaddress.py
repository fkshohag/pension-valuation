from pension_base.models.base import DomainEntity

__author__ = 'Fazlul Kabir Shohag'

from django.db import models
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class EmailAddress(DomainEntity):
    email = models.EmailField(max_length=100)
    is_primary = models.BooleanField(default=0)

    class Meta:
        app_label = 'pension_base'

    @staticmethod
    def is_email_valid(self, email):
        try:
            validate_email(email)
            return True
        except ValidationError:
            return False
