"""
Created by Fazlul Kabir Shohag on 27, February, 2020
Email: shohag.fks@gmail.com
"""

__author__ = 'Fazlul Kabir Shohag'

from pension.models import DebtBurdenRatio
from pension_base.serializers.company_domain_entity_serializer import CompanyDomainEntitySerializer


class DbrMultiplierSerializer(CompanyDomainEntitySerializer):
    class Meta:
        model = DebtBurdenRatio
        fields = (
            'id', 'start', 'end', 'value'
        )