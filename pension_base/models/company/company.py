from pension_base.models.base import DomainEntity
from django.db import models
from pension_base.models.email.emailaddress import EmailAddress
from django.core.validators import URLValidator

__author__ = 'Fazlul Kabir Shohag'


class Company(DomainEntity):
    name = models.CharField(max_length=255, unique=False)
    address = models.TextField(blank=False)
    email_address = models.ForeignKey(EmailAddress, null=True, on_delete=models.SET_NULL)
    website = models.TextField(validators=[URLValidator()])

    class Meta:
        app_label = 'pension_base'

    def __init__(self, *args, **kwargs):
        super(Company, self).__init__(*args, **kwargs)