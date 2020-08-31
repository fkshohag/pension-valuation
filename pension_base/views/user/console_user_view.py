from pension_base.engine.pagination.standard_pagination import StandardResultsSetPagination
from pension_base.serializers.user.Console_user_serializer import ConsoleUserSerializer

from pension_base.views.company_domain_entity_view import CompanyDomainEntityView


class ConsoleUserView(CompanyDomainEntityView):
    serializer_class = ConsoleUserSerializer
    pagination_class = StandardResultsSetPagination


