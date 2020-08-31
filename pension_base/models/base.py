from django.db import models

__author__ = 'Shohag'


class DomainEntity(models.Model):
    created_by = models.ForeignKey('pension_base.ConsoleUser', related_name='+', null=True,
                                   on_delete=models.SET_NULL)
    last_updated_by = models.ForeignKey('pension_base.ConsoleUser', related_name='+', null=True,
                                        on_delete=models.SET_NULL)
    date_created = models.BigIntegerField(editable=False, default=0)
    last_updated = models.BigIntegerField(editable=False, default=0)
    is_active = models.BooleanField(default=True, editable=False)
    is_deleted = models.BooleanField(default=False, editable=False)
    is_locked = models.BooleanField(default=False, editable=False)
    code = models.CharField(default='', max_length=200)

    class Meta:
        abstract = True
        app_label = 'pension_base'
