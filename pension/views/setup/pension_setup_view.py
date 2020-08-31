"""
Created by Fazlul Kabir Shohag on 27, February, 2020
Email: shohag.fks@gmail.com
"""

__author__ = 'Fazlul Kabir Shohag'

from pension.serializers.setup.pension_setup_serializer import PensionSetupSerializer
from pension_base.views.domain_entity_view import DomainEntityView


class PensionSetupView(DomainEntityView):
    serializer_class = PensionSetupSerializer
