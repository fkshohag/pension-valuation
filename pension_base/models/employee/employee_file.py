from pension_base.models.company.company_entity import CompanyDomainEntity
from django.core.validators import FileExtensionValidator
from django.db import models

__author__ = 'Fazlul Kabir Shohag'


class EmployeeFile(CompanyDomainEntity):
    name = models.CharField(max_length=255, blank=True)
    path = models.CharField(max_length=255, blank=True)
    extension = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=255, blank=True)
    file = models.FileField(max_length=16000, null=False, blank=False,
                            validators=[FileExtensionValidator(allowed_extensions=['csv','xlsx', 'xls'])])
    order = models.BigIntegerField(default=0)

    class Meta:
        app_label = 'pension_base'
