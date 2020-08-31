from django.conf.urls import include, url
from pension.models import PensionSetup, MortalityCalculation
from pension.models.employee_job_info import EmployeeJobInformation
from pension.views.employee_job_info_view import EmployeeJobInfoView, EmployeeJobInfoApiView
from pension.views.mortality.mortality_view import MortalityCalculationView, MortalityCalculationApiView
from pension.views.setup.pension_setup_view import PensionSetupView
from pension_api.routes.router import CustomRouter

router = CustomRouter()

router.register('employee-job-info', EmployeeJobInfoView, basename=EmployeeJobInformation.__name__)
router.register('pension-setup', PensionSetupView, basename=PensionSetup.__name__)
router.register('mortality', MortalityCalculationView, basename=MortalityCalculation.__name__)

urlpatterns = [
    url(r'^employee-info-generate/$', EmployeeJobInfoApiView.as_view()),
    url(r'^mortality-calculation/$', MortalityCalculationApiView.as_view()),
    url(r'^', include(router.urls)),
]
