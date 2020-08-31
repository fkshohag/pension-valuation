from pension_base.views.domain_entity_view import DomainEntityView
from pension_base.serializers.employee.employee_serializer import EmployeeSerializer


class EmployeeView(DomainEntityView):
    serializer_class = EmployeeSerializer


