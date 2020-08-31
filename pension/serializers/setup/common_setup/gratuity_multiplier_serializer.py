"""
Created by Fazlul Kabir Shohag on 27, February, 2020
Email: shohag.fks@gmail.com
"""

__author__ = 'Fazlul Kabir Shohag'

from pension.models import GratuityMultiplier
from pension_base.serializers.company_domain_entity_serializer import CompanyDomainEntitySerializer


class GratuityMultiplierSerializer(CompanyDomainEntitySerializer):
    class Meta:
        model = GratuityMultiplier
        fields = (
            'id', 'start', 'end', 'value'
        )

