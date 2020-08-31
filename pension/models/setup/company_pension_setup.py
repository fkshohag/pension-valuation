"""
Created by Fazlul Kabir Shohag on 27, February, 2020
Email: shohag.fks@gmail.com
"""

__author__ = 'Fazlul Kabir Shohag'

from django.db import models
from pension_base.models.company.company_entity import CompanyDomainEntity


class PensionSetup(CompanyDomainEntity):
    valuation_date = models.BigIntegerField(default=0)
    interest_salary = models.DecimalField(max_digits=7, decimal_places=2)
    salary_growth = models.DecimalField(max_digits=5, decimal_places=2)
    retirement_age = models.BigIntegerField(default=0)
    special_retirement_age = models.BigIntegerField(default=0)
    gratuity_multiplier = models.ManyToManyField('pension.GratuityMultiplier')
    dbr = models.ManyToManyField('pension.DebtBurdenRatio')
    withdrawal = models.ManyToManyField('pension.WithdrawalSetup')
    min_service_years = models.BigIntegerField(default=0)
    exchange_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    total_assets = models.BigIntegerField(default=0)


    class Meta:
        app_label = 'pension'

    def __init__(self, *args, **kwargs):
        super(PensionSetup, self).__init__(*args, **kwargs)