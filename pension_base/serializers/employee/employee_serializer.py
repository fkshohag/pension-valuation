from pension_base.models.employee.Employee import Employee
from pension_base.serializers.company_domain_entity_serializer import CompanyDomainEntitySerializer

__author__ = 'Fazlul Kabir Shohag'


class EmployeeSerializer(CompanyDomainEntitySerializer):
    class Meta:
        model = Employee
        fields = (
            'id', 'name', 'company', 'designation', 'sex', 'date_of_birth', 'join_date', 'basic_salary',
            'is_freedom_fighter', 'retirement_age', 'last_updated_by', 'date_created', 'last_updated', 'is_active',
            'is_deleted', 'is_locked', 'code'
        )