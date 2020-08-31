from pension_base.engine.utility.Clock import Clock
from pension_base.models.company.company_entity import CompanyDomainEntity
from django.db import models

__author__ = "Fazlul Kabir Shohag"


class EmployeeJobInformation(CompanyDomainEntity):
    employee = models.ForeignKey('pension_base.Employee', related_name='+', null=True,
                                   on_delete=models.SET_NULL)
    exact_age = models.CharField(max_length=255, blank=True)
    last_birthday = models.IntegerField(null=True)
    next_birthday = models.IntegerField(null=True)
    age_nearest = models.CharField(max_length=255, blank=True)
    retirement_date = models.BigIntegerField(null=True)
    retirement_years = models.IntegerField(null=True)
    exact_service_years = models.CharField(max_length=255, blank=True)
    total_year_service = models.IntegerField(null=True)
    years_of_service = models.IntegerField(null=True)
    future_service = models.CharField(max_length=255, blank=True)
    total_future_service = models.IntegerField(null=True)
    valuation_date = models.BigIntegerField(default=0, null=True)

    class Meta:
        app_label = 'pension'

    def __init__(self, *args, **kwargs):
        super(EmployeeJobInformation, self).__init__(*args, **kwargs)

    @property
    def company_name(self):
        return self.company.name

    @property
    def employee_name(self):
        return self.employee.name

    @property
    def retirement_age(self):
        return self.employee.retirement_age

    @property
    def date_of_birth(self):
        return Clock.get_datetime_from_timestamp(self.employee.date_of_birth)

    @property
    def join_date(self):
        return Clock.get_datetime_from_timestamp(self.employee.join_date)

    @property
    def retirement_datetime(self):
        return Clock.get_datetime_from_timestamp(self.retirement_date)

    @property
    def valuation_datetime(self):
        return Clock.datetime_from_timestamp(self.valuation_date)
