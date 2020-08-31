"""
Created by Fazlul Kabir Shohag on 01, March, 2020
Email: shohag.fks@gmail.com
"""

__author__ = 'Fazlul Kabir Shohag'

from pension.models import MortalityCalculation
from pension_base.serializers.company_domain_entity_serializer import CompanyDomainEntitySerializer
from pension_base.serializers.file.file_serializer import FileSerializer


class MortalitySerializer(CompanyDomainEntitySerializer):
    file = FileSerializer()
    class Meta:
        model = MortalityCalculation
        fields = (
            'id', 'company', 'mortality_name', 'gender', 'file'
        )