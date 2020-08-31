"""
Created by Fazlul Kabir Shohag on 01, March, 2020
Email: shohag.fks@gmail.com
"""

__author__ = 'Fazlul Kabir Shohag'

from rest_framework.views import APIView

from pension.serializers.mortality.mortality_serializer import MortalitySerializer
from pension_base.views.domain_entity_view import DomainEntityView


class MortalityCalculationView(DomainEntityView):
    serializer_class = MortalitySerializer


class MortalityCalculationApiView(APIView):
    def post(self, request):
        company_id = request.data.get('company_id', None)
        valuation_date = request.data.get('valuation_date', None)
