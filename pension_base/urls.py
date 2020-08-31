from pension_api.routes.router import CustomRouter
from pension_base.models import ConsoleUser, Company, EmployeeFile
from pension_base.views.company.company_view import CompanyView
from pension_base.views.employee.employee_file_view import EmployeeFileView
from pension_base.views.user.console_user_view import ConsoleUserView
from pension_base.views.employee.employee_view import EmployeeView
from pension_base.models.employee.Employee import Employee

router = CustomRouter()

router.register('user', ConsoleUserView, basename=ConsoleUser.__name__)
router.register('company', CompanyView, basename=Company.__name__)
router.register('employee', EmployeeView, basename=Employee)
router.register('employee-file', EmployeeFileView, basename=EmployeeFile)

urlpatterns = router.urls
