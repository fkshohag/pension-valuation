from pension_base.models.company.company_entity import CompanyDomainEntity
from pension_base.serializers.domain_entity_serializer import DomainEntitySerializer


class CompanyDomainEntitySerializer(DomainEntitySerializer):
    class Meta(DomainEntitySerializer.Meta):
        model = CompanyDomainEntity
        fields = DomainEntitySerializer.Meta.read_only_fields + ('company',)