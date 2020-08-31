"""
Created by Fazlul Kabir Shohag on 27, February, 2020
Email: shohag.fks@gmail.com
"""

__author__ = 'Fazlul Kabir Shohag'

from django.db import models
from pension_base.models.company.company_entity import CompanyDomainEntity


class WithdrawalSetup(CompanyDomainEntity):
    start = models.DecimalField(max_digits=3, decimal_places=2)
    end = models.DecimalField(max_digits=3, decimal_places=2)
    value = models.DecimalField(max_digits=3, decimal_places=2)

    class Meta:
        app_label = 'pension'

    def __init__(self, *args, **kwargs):
        super(WithdrawalSetup, self).__init__(*args, **kwargs)