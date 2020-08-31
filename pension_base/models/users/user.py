from django.contrib.auth.models import User
from pension_base.models.company.company_entity import CompanyDomainEntity
from pension_base.models.email.emailaddress import EmailAddress
from django.db import models

__author__ = 'Fazlul Kabir Shohag'


class ConsoleUser(CompanyDomainEntity):
    user = models.OneToOneField(User, null=True)
    is_super = models.BooleanField(default=False)
    name = models.CharField(max_length=200)
    email_address = models.ForeignKey(EmailAddress, null=True, on_delete=models.SET_NULL)
    designation = models.CharField(max_length=200, null=True)
    male_or_female = models.CharField(max_length=2, null=True, default='M',
                                      blank=True)
    class Meta:
        app_label = 'pension_base'

    def __init__(self, *args, **kwargs):
        super(ConsoleUser, self).__init__(*args, **kwargs)
