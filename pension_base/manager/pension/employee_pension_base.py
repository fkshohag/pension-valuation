from dateutil.relativedelta import relativedelta
from pension_base.engine.utility.Clock import Clock
import copy

__author__ = 'Fazlul Kabir Shohag'


class EmployeePensionBase(object):

    def __init__(self):
        self.exact_age = None
        self.retirement_date = None
        self.service_age = None
        self.f_service = None

    def exact_age_calculation(self, valuation_date, dob):
        valuation_date = Clock.datetime_from_timestamp(valuation_date)
        dob = Clock.get_datetime_from_timestamp(dob)
        difference = relativedelta(valuation_date, dob)
        self.exact_age = difference
        return difference

    def last_birthday(self, last_birthday=None):
        if self.exact_age is not None:
            return int(self.exact_age.years)
        else:
            return int(last_birthday)

    def next_birthday(self, current_birthday=None):
        if self.exact_age is not None:
            return int(self.exact_age.years + 1)
        else:
            return int(current_birthday+1)

    def age_nearest(self, nearest_age=None):
        if self.exact_age is not None:
            nearest_age = copy.copy(self.exact_age)
            if self.exact_age.months > 6:
                nearest_age.years += 1
            if self.exact_age.days > 15:
                nearest_age.months += 1
            return nearest_age
        else:
            return nearest_age

    def retirement_date_calculation(self, d_birthday, retirement_age):
        joining_date = Clock.get_datetime_from_timestamp(d_birthday)
        last_date = joining_date + relativedelta(years=retirement_age)
        self.retirement_date = last_date # last date tracking
        last_date = Clock.get_timestamp_datetime_from(last_date)
        return  last_date

    def calendar_year_of_retirement(self):
        if self.retirement_date is not None:
            return self.retirement_date.year


    # Member service related

    def exact_service_year(self, valuation_date, joining_date):
        valuation_date = Clock.datetime_from_timestamp(valuation_date)
        joining_date = Clock.get_datetime_from_timestamp(joining_date)

        difference = relativedelta(valuation_date, joining_date)
        self.service_age = difference
        return difference

    def total_years_service(self):
        if self.service_age is not None:
            return int(self.service_age.years)


    def years_of_service(self):
        if self.service_age is not None:
            if self.service_age.months > 6:
                return self.service_age.years+1
            else:
                return self.service_age.years

    def future_service(self, valuation_date):
        if self.service_age is not None and self.retirement_date is not None:
            valuation_date = Clock.datetime_from_timestamp(valuation_date)
            future_service = relativedelta(self.retirement_date, valuation_date)
            self.f_service = future_service
            return  future_service

    def total_future_service(self):
        if self.f_service is not None:
            return self.f_service.years


