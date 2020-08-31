from pension_base.models import EmployeeFile
from pension_base.serializers.company_domain_entity_serializer import CompanyDomainEntitySerializer
import os.path

__author__ = 'Fazlul Kabir Shohag'


class EmployeeFileSerializer(CompanyDomainEntitySerializer):
    def create(self, validated_data):
        validated_data['name'] = validated_data['file'].name
        validated_data['extension'] = os.path.splitext(validated_data['name'])[1][1:].strip()
        return super(EmployeeFileSerializer, self).create(validated_data)

    class Meta:
        model = EmployeeFile
        fields = (
            'pk', 'name', 'path', 'extension', 'description', 'file', 'order', 'company'
        )