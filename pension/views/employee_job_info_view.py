from rest_framework import status

from pension.serializers.employee_job_info import EmployeeJobInfoSerializer
from pension_base.manager.pension.pension_manager import PensionManager
from pension_base.models import ConsoleUser
from pension_base.models.employee.Employee import Employee
from pension_base.views.domain_entity_view import DomainEntityView
from rest_framework.views import APIView
from rest_framework.response import Response
import multiprocessing


class EmployeeJobInfoView(DomainEntityView):
    serializer_class = EmployeeJobInfoSerializer


class EmployeeJobInfoApiView(APIView):
    def post(self, request):
        company_id = request.data.get('company_id', None)
        valuation_date = request.data.get('valuation_date', None)
        current_user = ConsoleUser.objects.filter(user=self.request.user).first()
        if company_id is None:
            _response = {
                'errors': 'company_id is required field'
            }
            return Response(_response, status=status.HTTP_406_NOT_ACCEPTABLE)
        elif valuation_date is None:
            _response = {
                'errors': 'valuation_date is required field'
            }
            return Response(_response, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            employees = Employee.objects.filter(company_id=company_id)
            PensionManager.generate_employee_data(company_id, current_user, valuation_date, employees)
            # employees info data generate:
            # from django import db
            # db.connections.close_all()
            # process = multiprocessing.Process(target=PensionManager.generate_employee_data,
            #                                   args=(company_id, current_user, valuation_date, employees, ))
            # process.start()

            return Response({'Employee information generated successfully'}, status=status.HTTP_200_OK)
