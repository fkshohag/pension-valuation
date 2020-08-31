from django.core.exceptions import ObjectDoesNotExist
from rest_framework.relations import PrimaryKeyRelatedField

from pension_base.models.base import DomainEntity

__author__ = 'Shohag'


class PrimaryKeyRelatedField(PrimaryKeyRelatedField):
    def __init__(self, accept_disabled_objects=False, **kwargs):
        setattr(self, 'accept_disabled_objects', accept_disabled_objects)
        super(PrimaryKeyRelatedField, self).__init__(**kwargs)

    def to_internal_value(self, data):
        if self.pk_field is not None:
            data = self.pk_field.to_internal_value(data)
        try:
            if getattr(self, "accept_disabled_objects", False):
                model = self.queryset.model
                if issubclass(model, DomainEntity):
                    return model.all_objects.get(pk=data)
            return self.get_queryset().get(pk=data)
        except ObjectDoesNotExist:
            self.fail('does_not_exist', pk_value=data)
        except (TypeError, ValueError):
            self.fail('incorrect_type', data_type=type(data).__name__)
