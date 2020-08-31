from pension_base.models.base import DomainEntity
from django.db import models

__author__ = 'Fazlul Kabir Shohag'


class CompanyDomainEntity(DomainEntity):
    company = models.ForeignKey('pension_base.Company', null=True, on_delete=models.SET_NULL)

    class Meta:
        abstract = True
        app_label = 'pension_base'
