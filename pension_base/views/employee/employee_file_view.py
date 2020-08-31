from rest_framework.parsers import MultiPartParser, FormParser
from pension_base.manager.importable_manager import ImportableManager
from pension_base.models import ConsoleUser
from django.contrib.auth.models import User
from pension_base.serializers.employee.employee_file_serializer import EmployeeFileSerializer
from pension_base.views.domain_entity_view import DomainEntityView
import multiprocessing

class EmployeeFileView(DomainEntityView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = EmployeeFileSerializer

    def perform_create(self, serializer):
        if self.request.user and User.objects.filter(pk=self.request.user.pk).exists():
            current_user = ConsoleUser.objects.filter(user=self.request.user).first()
            serializer.validated_data['created_by'] = current_user
            serializer.validated_data['last_updated_by'] = current_user
            company = serializer.validated_data['company']

            # employee uploaded file read
            import_file = ImportableManager()
            import_file.set_convertable_field(fields=['date_of_birth', 'join_date'])
            # file importing
            # closing db connection to recreate db connection for every instance
            from django import db
            db.connections.close_all()
            process = multiprocessing.Process(target=import_file.importable, args=(serializer.validated_data['file'],
                                                                                current_user, company ,))
            process.start()

        return super(EmployeeFileView, self).perform_create(serializer)
