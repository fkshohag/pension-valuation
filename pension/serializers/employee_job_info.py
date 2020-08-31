from pension.models.employee_job_info import EmployeeJobInformation
from pension_base.serializers.company_domain_entity_serializer import CompanyDomainEntitySerializer

__author__ = 'Fazlul Kabir Shohag'


class EmployeeJobInfoSerializer(CompanyDomainEntitySerializer):
    class Meta:
        model = EmployeeJobInformation
        fields = (
            'id', 'employee_name', 'date_of_birth', 'join_date', 'exact_age', 'last_birthday', 'next_birthday',
            'age_nearest', 'valuation_datetime', 'retirement_datetime', 'retirement_years', 'retirement_age',
            'exact_service_years', 'total_year_service', 'years_of_service', 'future_service', 'total_future_service',
            'company_name'
        )
