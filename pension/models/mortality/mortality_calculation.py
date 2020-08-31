"""
Created by Fazlul Kabir Shohag on 01, March, 2020
Email: shohag.fks@gmail.com
"""

__author__ = 'Fazlul Kabir Shohag'

from django.db import models
from pension_base.models.company.company_entity import CompanyDomainEntity


class MortalityCalculation(CompanyDomainEntity):
    mortality_name = models.CharField(max_length=255, blank=False)
    gender = models.CharField(max_length=30, blank=False)
    file = models.ForeignKey('pension_base.File', null=False)

    class Meta:
        app_label = 'pension'

    def __init__(self, *args, **kwargs):
        super(MortalityCalculation, self).__init__(*args, **kwargs)