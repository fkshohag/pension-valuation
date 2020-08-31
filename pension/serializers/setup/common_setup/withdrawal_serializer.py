"""
Created by Fazlul Kabir Shohag on 27, February, 2020
Email: shohag.fks@gmail.com
"""

__author__ = 'Fazlul Kabir Shohag'

from pension.models.setup.common_setup.withdrawal_setup import WithdrawalSetup
from pension_base.serializers.company_domain_entity_serializer import CompanyDomainEntitySerializer


class WithdrawalSerializer(CompanyDomainEntitySerializer):
    class Meta:
        model = WithdrawalSetup
        fields = (
            'id', 'start', 'end', 'value'
        )