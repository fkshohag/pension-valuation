from pension_base.serializers.company.company_serializer import CompanySerializer
from pension_base.views.domain_entity_view import DomainEntityView


class CompanyView(DomainEntityView):
    serializer_class = CompanySerializer


