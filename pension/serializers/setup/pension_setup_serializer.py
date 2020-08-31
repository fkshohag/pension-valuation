"""
Created by Fazlul Kabir Shohag on 27, February, 2020
Email: shohag.fks@gmail.com
"""

__author__ = 'Fazlul Kabir Shohag'

from pension.models import PensionSetup
from pension.serializers.setup.common_setup.dbr_serializer import DbrMultiplierSerializer
from pension.serializers.setup.common_setup.gratuity_multiplier_serializer import GratuityMultiplierSerializer
from pension.serializers.setup.common_setup.withdrawal_serializer import WithdrawalSerializer
from pension_base.serializers.company_domain_entity_serializer import CompanyDomainEntitySerializer

class PensionSetupSerializer(CompanyDomainEntitySerializer):
    gratuity_multiplier = GratuityMultiplierSerializer(many=True, read_only=False)
    dbr = DbrMultiplierSerializer(many=True, read_only=False)
    withdrawal = WithdrawalSerializer(many=True, read_only=False)

    class Meta:
        model = PensionSetup
        fields = (
            'id', 'company', 'interest_salary', 'salary_growth', 'retirement_age', 'special_retirement_age',
            'gratuity_multiplier', 'dbr', 'withdrawal', 'min_service_years', 'exchange_rate'
        )