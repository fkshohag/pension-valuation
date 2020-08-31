from pension.models import EmployeeJobInformation
from pension_base.engine.utility.Clock import Clock
from pension_base.manager.bulk_create_manager import BulkCreateManager
from pension_base.manager.pension.employee_pension_base import EmployeePensionBase

__author__ = 'Fazlul Kabir Shohag'


class PensionManager(EmployeePensionBase):

    def __init__(self):
        super().__init__()

    @classmethod
    def generate_employee_data(cls, company_id, current_user, valuation_date, employees):
        manager = PensionManager()
        bulk_mgr = BulkCreateManager(chunk_size=200)
        company_id = int(company_id)
        valuation_date = int(valuation_date)

        for employee in employees:
            if employee.date_of_birth:
                employee_dict = {}
                exact_age = manager.exact_age_calculation(valuation_date=valuation_date,
                                                          dob=int(employee.date_of_birth))

                age_nearest = manager.age_nearest()
                exact_service_year = manager.exact_service_year(valuation_date=valuation_date,
                                                                joining_date=employee.join_date)

                retirement_date = manager.retirement_date_calculation(d_birthday=employee.date_of_birth,
                                                                      retirement_age=employee.retirement_age)
                future_service = manager.future_service(valuation_date=valuation_date)

                employee_dict['employee_id'] = employee.pk
                employee_dict['valuation_date'] = int(valuation_date)
                employee_dict['date_created'] = Clock.current_timestamp()
                employee_dict['exact_age'] = str(abs(exact_age.years)) + ' years ' + str(
                    abs(exact_age.months)) + ' months ' + str(abs(exact_age.days)) + ' days'
                employee_dict['last_birthday'] = abs(manager.last_birthday())
                employee_dict['next_birthday'] = abs(manager.next_birthday())
                employee_dict['age_nearest'] = str(abs(age_nearest.years)) + ' years ' + str(
                    abs(age_nearest.months)) + ' months ' + \
                                               str(abs(age_nearest.days)) + ' days'
                employee_dict['retirement_date'] = retirement_date
                employee_dict['retirement_years'] = manager.calendar_year_of_retirement()
                employee_dict['exact_service_years'] = str(abs(exact_service_year.years)) + ' years ' + str(
                    abs(exact_service_year.months)) + \
                                                       ' months ' + str(abs(exact_service_year.days)) + ' days'
                employee_dict['total_year_service'] = abs(manager.total_years_service())
                employee_dict['years_of_service'] = abs(manager.years_of_service())
                employee_dict['future_service'] = str(abs(future_service.years)) + ' years ' + str(abs(future_service.months)) + \
                                                  ' months ' + str(abs(future_service.days)) + ' days'
                employee_dict['total_future_service'] = manager.total_future_service()
                employee_dict['created_by'] = current_user
                employee_dict['last_updated_by'] = current_user
                employee_dict['company_id'] = int(company_id)

                bulk_mgr.add(EmployeeJobInformation(**employee_dict))

        bulk_mgr.done()
