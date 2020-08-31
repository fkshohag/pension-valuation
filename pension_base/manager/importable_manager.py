import os
import pandas as pd

from pension_base.engine.utility.Clock import Clock
from pension_base.manager.bulk_create_manager import BulkCreateManager
from pension_base.models import Employee

__author__ = 'Fazlul Kabir Shohag'


class ImportableManager(object):

    def __init__(self):
        self.datetime_fields = []

    def columns_replace(self, fields = None):
        if fields is not None:
            return fields
        return {
            'EMPLOYEE NAME': 'name',
            'EMPLOYEE ID': 'staff_id',
            'RANK': 'designation',
            'POSTING/LOCATION': 'posting_location',
            'DATE OF BIRTH': 'date_of_birth',
            'DATE OF JOINING': 'join_date',
            'SEXUAL STATUS': 'sex',
            'RETIREMENT AGE': 'retirement_age',
            'BASIC SALARY': 'basic_salary',
            'Freedom fighter': 'is_freedom_fighter',
            'PRL?': 'rpl',
        }

    def set_convertable_field(self, fields = None):
        if fields is not None:
            self.datetime_fields = fields

    def prepare_data(self, data, company_id):
        data_dict = {}
        for key, field in self.columns_replace().items():
            field_value = data.__getattribute__(field)
            if not Employee.objects.filter(staff_id=field_value).filter(company_id=company_id).exists():
                if not pd.isna(field_value):
                    if len(self.datetime_fields) > 0 and field in self.datetime_fields:
                        data_dict[field] = Clock.get_timestamp_from_datetime(field_value, "%d-%m-%Y")
                    else:
                        data_dict[field] = field_value
            else:
                return False
        return data_dict


    def importable(self, file, current_user, company):
        extension = os.path.splitext(file.name)[1][1:].strip()
        df = None
        if extension == 'xlsx':
            information = pd.read_excel(file)
            df = pd.DataFrame(information)
            df.rename(columns=self.columns_replace(), inplace=True)
        elif extension == 'csv':
            information = pd.read_csv(file)
            df = pd.DataFrame(information)
            df.rename(columns=self.columns_replace(), inplace=True)

        # Uploaded file
        if df is not None:
            bulk_mgr = BulkCreateManager(chunk_size=100)
            for item in df.itertuples():
                employee = self.prepare_data(data=item, company_id=company.pk)
                if employee:
                    employee['date_created'] = Clock.current_timestamp()
                    employee['created_by'] = current_user
                    employee['last_updated_by'] = current_user
                    employee['company_id'] = int(company.id)
                    bulk_mgr.add(Employee(**employee))
            bulk_mgr.done()





