from rest_framework import serializers
from django.db import transaction
from django.db.models.base import Model
from collections import OrderedDict
from django.db.models.manager import Manager
from django.db.models.fields.related import ForeignKey, OneToOneField, ManyToManyField
from pension_base.engine.serializer_fields.primary_key_related_fields import PrimaryKeyRelatedField
from pension_base.generic.serializer_mixin.serializer_view import SerializerView
from pension_base.models import ConsoleUser
from pension_base.models.base import DomainEntity
from django.contrib.auth.models import User

__author__ = 'Shohag'


class DomainEntitySerializer(serializers.ModelSerializer):
    serializer_related_field = PrimaryKeyRelatedField

    def __init__(self, *args, fields=None, context=None, **kwargs):
        super().__init__(*args, context=context, **kwargs)

    def create(self, validated_data):
        with transaction.atomic():
            validated_data = SerializerView.common_field_add(validated_data)
            m2m_fields = [
                (f, f.model if f.model != self.Meta.model else None)
                for f in self.Meta.model._meta.get_fields()
                if (f.one_to_many and f.name in validated_data.keys()) or
                   (f.many_to_many and not f.auto_created)
            ]

            m2m_dict = dict()
            for m in m2m_fields:
                m2m_dict[m[0].name] = validated_data.pop(m[0].name, [])

            attributes = self.Meta.model._meta.fields

            pk = validated_data.pop('id', None)
            if pk:
                current_object = self.Meta.model.objects.get(pk=pk)
            else:
                current_object = self.Meta.model.objects.create(**validated_data)

            for attr in attributes:
                if isinstance(attr, ForeignKey) or isinstance(attr, OneToOneField):
                    value = validated_data.pop(attr.name, None)
                    if isinstance(value, Model) and value.pk is None:
                        value.save()
                        setattr(current_object, attr.name,
                                attr.model.objects.get(pk=value) if isinstance(value, int) else value)
                else:
                    pass

            for m in m2m_fields:
                _field = getattr(current_object, m[0].name)
                _values = m2m_dict[m[0].name]
                for v in _values:
                    if isinstance(v, (dict, OrderedDict)):
                        field_name = m[0].name
                        _serializer = None
                        _serializer_parent_instance = self.fields.get(field_name)
                        if _serializer_parent_instance:
                            _serializer = getattr(_serializer_parent_instance, 'child', None)
                        if not _serializer:
                            _serializer = m[0].related_model.get_serializer()(context=self.context)
                    v = _serializer.create(v)
                    v.save()
                    _field.add(v)

        return current_object

    def update(self, instance, validated_data):
        with transaction.atomic():

            user = self.context['request'].user
            c_user = ConsoleUser.objects.filter(user=user).first()
            instance.last_updated_by = c_user
            m2m_fields = [
                (f, f.model if f.model != self.Meta.model else None)
                for f in self.Meta.model._meta.get_fields()
                if (f.one_to_many and f.name in validated_data.keys()) or
                   (f.many_to_many and not f.auto_created)
            ]
            m2m_dict = dict()
            for m in m2m_fields:
                m2m_dict[m[0].name] = validated_data.pop(m[0].name, [])

            attributes = self.Meta.model._meta.fields

            for attr in attributes:
                if attr.name in validated_data and isinstance(validated_data[attr.name], dict):
                    _obj = getattr(instance, attr.name)
                    field_name = attr.name
                    _serializer = self.fields.get(field_name)
                    if not _serializer:
                        _serializer = attr.related_model.get_serializer()(context=self.context)
                    _serializer.Meta.extra_kwargs = {'id': {'read_only': True}}

                    if _obj is None:
                        if callable(getattr(_serializer, 'create', None)):
                            validated_data[attr.name] = _serializer.create(validated_data[attr.name])
                    else:
                        if callable(getattr(_serializer, 'update', None)):
                            validated_data[attr.name] = _serializer.update(_obj, validated_data[attr.name])

            for attr in attributes:
                if attr.name in validated_data.keys():
                    if isinstance(attr, ForeignKey) or isinstance(attr, OneToOneField):
                        # _obj = getattr(instance, attr.name)
                        value = validated_data.pop(attr.name, None)
                        if isinstance(value, Model) and value.pk is None:
                            value.save()
                        setattr(instance, attr.name,
                                attr.model.objects.get(pk=value) if isinstance(value, int) else value)

            fields_name = [f.name for f in instance.__class__._meta.get_fields()]

            for m in m2m_fields:
                if m[0].name in m2m_dict.keys() and len(m2m_dict[m[0].name]) > 0:
                    _field = getattr(instance, m[0].name)
                    _values = m2m_dict[m[0].name]
                    if m[0].name in fields_name:
                        if isinstance(_values, User):
                            _values.delete()
                        elif isinstance(_values, Model):
                            temp = _values
                            setattr(instance, m[0].name, None)
                            instance.save()
                            temp.delete(force_delete=True)
                        elif isinstance(_values, Manager):
                            items = list(_values.all())
                            _values.clear()
                            for item in items:
                                item.delete(force_delete=True)
                        else:
                            pass

                    if m[0].name in [x for x in fields_name if
                                     isinstance(getattr(instance, x), Manager)]:
                        _field.clear()
                    for v in _values:
                        if isinstance(v, (dict, OrderedDict)):
                            field_name = m[0].name
                            _serializer = None
                            _serializer_parent_instance = self.fields.get(field_name)
                            if _serializer_parent_instance:
                                _serializer = getattr(_serializer_parent_instance, 'child', None)
                            if not _serializer:
                                _serializer = m[0].related_model.get_serializer()(context=self.context)
                            _serializer.Meta.extra_kwargs = {'id': {'read_only': False}}

                            if isinstance(v, int):
                                v = m[0].related_model.objects.get(pk=v)
                            else:
                                try:
                                    # Try to get the object
                                    _instance = None
                                    if 'id' in v.keys():
                                        _instance = m[0].related_model.objects.get(pk=v['id'])
                                    elif 'pk' in v.keys():
                                        _instance = m[0].related_model.objects.get(pk=v['pk'])
                                    if _instance:
                                        v = _serializer.update(instance=_instance, validated_data=v)
                                    else:
                                        if m[0].one_to_many:
                                            v[_field.field.name] = instance
                                        v = _serializer.create(v)
                                except:
                                    if m[0].one_to_many:
                                        v[_field.field.name] = instance
                                    v = _serializer.create(v)
                        v.save()
                        _field.add(v)

            return super().update(instance, validated_data)

    def save(self, **kwargs):
        return super().save(**kwargs)

    class Meta:
        model = DomainEntity
        read_only_fields = (
            'id', 'created_by', 'last_updated_by', 'date_created', 'last_updated', 'is_active',
            'is_deleted', 'is_locked', 'code'
        )

