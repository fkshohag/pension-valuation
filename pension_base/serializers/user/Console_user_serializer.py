from pension_base.models import ConsoleUser
from pension_base.serializers.company_domain_entity_serializer import CompanyDomainEntitySerializer
from pension_base.serializers.user.django_user_serializer import DjangoUserSerializer


class ConsoleUserSerializer(CompanyDomainEntitySerializer):
    user = DjangoUserSerializer()

    class Meta:
        model = ConsoleUser
        fields = (
            'id', 'user', 'company', 'name', 'email_address', 'designation', 'male_or_female',
            'last_updated_by', 'date_created', 'last_updated', 'is_active', 'is_deleted', 'is_locked', 'code'
        )
