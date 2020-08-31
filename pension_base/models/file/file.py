from django.db import models
from pension_base.models.company.company_entity import CompanyDomainEntity

__author__ = 'Fazlul Kabir Shohag'


class File(CompanyDomainEntity):
    name = models.CharField(max_length=255, blank=False)
    path = models.CharField(max_length=255, blank=False)
    extension = models.CharField(max_length=50, blank=False)
    description = models.CharField(max_length=255, blank=True)
    file = models.FileField(default=None, max_length=16000, null= True, blank=True)
    order = models.BigIntegerField(default=0)

    class Meta:
        app_label = 'pension_base'