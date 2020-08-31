from pension_base.engine.utility.Clock import Clock


class SerializerView(object):

    @classmethod
    def common_field_add(cls, validated_data):
        validated_data['date_created'] = Clock.current_timestamp()
        validated_data['last_updated'] = Clock.current_timestamp()
        return validated_data