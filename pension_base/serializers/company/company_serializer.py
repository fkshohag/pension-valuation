from pension_base.models import Company
from pension_base.serializers.domain_entity_serializer import DomainEntitySerializer


class CompanySerializer(DomainEntitySerializer):
    class Meta:
        model = Company
        fields = (
            'id', 'name', 'address', 'email_address', 'website', 'last_updated_by', 'date_created', 'last_updated',
            'is_active', 'is_deleted', 'is_locked', 'code'
        )