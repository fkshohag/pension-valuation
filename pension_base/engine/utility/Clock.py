from datetime import datetime

class Clock(object):

    def __init__(self):
        pass
    
    @classmethod
    def get_timestamp_from_date(cls, datetime_string='', format=None):
        '''
        for getting timestamp from date use (datetimeobj).timestamp()*1000
        :param datetime_string:
        :return:
        '''
        if format is None:
            format = "%d/%m/%Y %H:%M:%S"
        return datetime.strptime(datetime_string, format).timestamp() * 1000

    @classmethod
    def get_timestamp_from_datetime(cls, datetime_string='', format=None):
        '''
        for getting timestamp from date use (datetimeobj).timestamp()*1000
        :param datetime_string:
        :return:
        '''
        if format is None:
            format = "%d/%m/%Y %H:%M:%S"
        return datetime.strptime(datetime_string.strftime(format), format).timestamp() * 1000

    @classmethod
    def get_datetime_from_timestamp(cls, timestamp):
        return datetime.fromtimestamp(timestamp * 1e-3)

    @classmethod
    def datetime_from_timestamp(cls, timestamp):
        return datetime.fromtimestamp(timestamp)

    @classmethod
    def get_timestamp_datetime_from(cls, date_time):
        return date_time.timestamp() * 1000

    @staticmethod
    def now():
        return  datetime.now()

    @staticmethod
    def current_timestamp():
        return int(datetime.now().timestamp())