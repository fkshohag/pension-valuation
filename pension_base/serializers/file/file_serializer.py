from pension_base.serializers.company_domain_entity_serializer import CompanyDomainEntitySerializer
from pension_base.models.file.file import File

__author__ = 'Fazlul Kabir Shohag'


class FileSerializer(CompanyDomainEntitySerializer):
    class Meta:
        model = File
        fields = (
            'id', 'name', 'path', 'extension', 'description', 'file', 'order'
        )