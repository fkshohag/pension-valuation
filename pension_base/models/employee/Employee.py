from django.db import models
from pension_base.models.company.company_entity import CompanyDomainEntity

__author__ = 'Fazlul Kabir Shohag'


class Employee(CompanyDomainEntity):
    name = models.CharField(max_length=255, unique=False)
    staff_id = models.CharField(max_length=60, null=True, blank=True, unique=False)
    designation = models.CharField(max_length=200, null=True)
    sex = models.CharField(max_length=2, null=True, default='M',
                           blank=True)
    posting_location = models.CharField(max_length=300, blank=True)
    date_of_birth = models.BigIntegerField(null=False, default=0)
    join_date = models.BigIntegerField(null=False, default=0)
    basic_salary = models.BigIntegerField(null=True, default=0)
    is_freedom_fighter = models.BooleanField(default=False, editable=False)
    retirement_age = models.BigIntegerField(null=True, default=0)
    retirement_date = models.BigIntegerField(null=True, default=0)
    rpl = models.SmallIntegerField(default=0)

    class Meta:
        app_label = 'pension_base'

    def __init__(self, *args, **kwargs):
        super(Employee, self).__init__(*args, **kwargs)
