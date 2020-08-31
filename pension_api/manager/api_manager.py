"""
Created by Fazlul Kabir Shohag on 29, February, 2020
Email: shohag.fks@gmail.com
"""

import datetime
import logging
import re
import pytz

from importlib import util

from dateutil import parser
from dateutil.tz import tz
from django.utils.timezone import now
from django.conf import settings

__author__ = 'Fazlul Kabir Shohag'

from pension_api.constants.range_constants import RangeFilterTypes, PostgresRangeQueryFilterTypes
from pension_api.utility.misc import convert_age_to_date

PSYCOPG2_FOUND = util.find_spec("psycopg2") is not None

if PSYCOPG2_FOUND:
    from psycopg2._range import DateTimeTZRange, NumericRange

logger = logging.getLogger(__name__)
USER_SEARCH_LIST_DEFAULT = ["username", "first_name", "last_name", "email"]

if hasattr(settings, "USER_SEARCH_LIST"):
    USER_SEARCH_LIST = settings.USER_SEARCH_LIST
else:
    USER_SEARCH_LIST = USER_SEARCH_LIST_DEFAULT


class ApiManager(object):
    template_name = None
    model = None
    should_override_pagination = False
    searches = []
    filters = []
    filter_names = []
    sorts = []
    default_sort_by = ["-id"]
    default_pagination = 25
    deferments = []
    show_all_in_filter = True
    show_clear_sorts = True
    using_postgres = False
    postgres_filter_name_query_filter_type_map = {}

    search_by = None
    using_filters = None
    filtered_object_count = None

    def get_search_list(self, search_bys):
        # Determine search_list
        search_list = {}

        if search_bys:
            self.search_by = search_bys

            for field in self.searches:
                field += "__icontains"
                search_list[field] = search_bys
        else:
            self.search_by = ""

        return search_list

    def get_sort_list(self, sort_bys):
        # Determine sort_list
        sort_list = list(sort_bys)
        count = 0

        for i in range(len(sort_bys)):
            if "-" in sort_bys[i]:
                base_sort = sort_bys[i].split("-")[1]
            else:
                base_sort = sort_bys[i]

            if base_sort not in self.sorts:
                sort_list.remove(sort_bys[i])
                logger.debug("Sort of " + base_sort + " is not in the sorts.")
                count -= 1
            elif "last_name" in sort_bys[i]:  # Special clause for last_names/first_names
                sort_list.insert(count, sort_bys[i].replace("last_name", "first_name"))
                count += 1
            elif base_sort == "birthday":  # Special clause for birthday/age. Need to reverse order because it is backwards for some reason.
                if sort_bys[i] == "birthday":
                    sort_list[count] = "-birthday"
                else:
                    sort_list[count] = "birthday"

            count += 1

        return sort_list

    def define_filters(self):
        self.filters = []
        self.filter_names = []

    def get_filter_list(self, filter_names, filter_values):
        # Determine filter_list
        filter_list = {}
        self.define_filters()

        postgres_range_filter_dictionaries = {}
        datetime_range_filter_dictionaries = {}

        for i in range(len(filter_names)):
            filter_name = filter_names[i]

            # This is only false if there are more filter_names than filter_values. Should be equal.
            if i < len(filter_values):
                values = filter_values[i].split(",")
                split_regex = re.compile("__lte|__lt|__gte|__gt")
                split_filter_name = split_regex.split(filter_name)
                filter_type = next(iter(split_regex.findall(filter_name)), None)
                stripped_filter_name = split_filter_name[0]
                stripped_filter_info = None

                if len(split_filter_name) != 1:
                    stripped_filter_info = split_filter_name[1].replace("_", "", 1)

                if stripped_filter_info:
                    if RangeFilterTypes.DATETIME in stripped_filter_info:
                        dates_or_times = stripped_filter_info.split("_")[1] + "s"
                        new_filter_name = stripped_filter_name + filter_type

                        if not datetime_range_filter_dictionaries.get(new_filter_name, None):
                            datetime_range_filter_dictionaries[new_filter_name] = {
                                "times": [],
                                "dates": [],
                                "filter_type": filter_type
                            }

                        datetime_range_filter_dictionaries[new_filter_name][dates_or_times] = self.convert_values(
                            values, stripped_filter_info.split("_")[1])
                        continue

                    if self.using_postgres:
                        self.create_or_edit_postgres_range_filter_dictionary(postgres_range_filter_dictionaries,
                                                                             stripped_filter_name, filter_type,
                                                                             stripped_filter_info, values)
                    else:
                        if stripped_filter_info == RangeFilterTypes.AGE:
                            values = [convert_age_to_date(int(filter_values[i]))]

                        if filter_type:
                            filter_name = stripped_filter_name + filter_type

                        filter_list[filter_name] = self.convert_values(values, stripped_filter_info)
                else:
                    if filter_type:
                        filter_name = stripped_filter_name + filter_type

                    filter_list[filter_name] = self.convert_values(values, stripped_filter_info)
            else:
                break

        for datetime_range_filter_name_and_type, datetime_range_filter_date_and_time_values in datetime_range_filter_dictionaries.items():
            filter_name = datetime_range_filter_name_and_type.split("__")[0]
            filter_type = datetime_range_filter_date_and_time_values["filter_type"]
            datetime_values = []
            dates = datetime_range_filter_date_and_time_values["dates"]
            times = datetime_range_filter_date_and_time_values["times"]

            if not dates:
                self.create_or_edit_postgres_range_filter_dictionary(postgres_range_filter_dictionaries, filter_name,
                                                                     filter_type, RangeFilterTypes.DATETIME, [])
                continue
            if not times:
                times = [date for date in dates]

            date_time_pairs = zip(dates, times)

            for date_time_pair in date_time_pairs:
                datetime_values.append(str(tz.resolve_imaginary(
                    datetime.datetime.combine(date_time_pair[0].date(), date_time_pair[1].time())).replace(
                    tzinfo=date_time_pair[0].tzinfo)))

            if self.using_postgres:
                self.create_or_edit_postgres_range_filter_dictionary(postgres_range_filter_dictionaries, filter_name,
                                                                     filter_type, RangeFilterTypes.DATETIME,
                                                                     datetime_values)
            else:
                filter_list[filter_name] = self.convert_values(datetime_values, RangeFilterTypes.DATETIME)

        for postgres_range_filter_name, postgres_range_filter_dictionary in postgres_range_filter_dictionaries.items():
            postgres_query_filter_type = self.postgres_filter_name_query_filter_type_map.get(postgres_range_filter_name,
                                                                                             PostgresRangeQueryFilterTypes.CONTAINED_BY)
            query_filter_name = postgres_range_filter_name + postgres_query_filter_type
            lowers = postgres_range_filter_dictionary["lowers"]
            uppers = postgres_range_filter_dictionary["uppers"]
            range_type = postgres_range_filter_dictionary["range_type"]
            lower_bound = postgres_range_filter_dictionary.get("lower_bound", "[")
            upper_bound = postgres_range_filter_dictionary.get("upper_bound", "]")

            if not lower_bound:
                lower_bound = "["

            if not upper_bound:
                upper_bound = "]"

            bounds_string = lower_bound + upper_bound
            filter_list[query_filter_name] = self.create_psycopg2_range_object_list(lowers, uppers, range_type,
                                                                                    bounds_string)

        return filter_list

    def create_psycopg2_range_object_list(self, lower_bounds, upper_bounds, range_type, bounds_string):
        bound_value_length = max(len(lower_bounds), len(upper_bounds))

        if not lower_bounds:
            lower_bounds = [None for i in range(0, bound_value_length)]

        if not upper_bounds:
            upper_bounds = [None for i in range(0, bound_value_length)]

        lower_and_upper_pairs = zip(lower_bounds, upper_bounds)
        if range_type in [RangeFilterTypes.DATETIME, RangeFilterTypes.DATE, RangeFilterTypes.TIME]:
            TZ_RANGE_OBJECT = DateTimeTZRange
        elif range_type in [RangeFilterTypes.NUMBER, RangeFilterTypes.AGE]:
            TZ_RANGE_OBJECT = NumericRange
        else:
            raise Exception("Range Type of " + range_type + "does not map to any current psycopg2 range object")

        return [TZ_RANGE_OBJECT(lower_and_upper_pair[0], lower_and_upper_pair[1], bounds=bounds_string) for lower_and_upper_pair in lower_and_upper_pairs]

    def create_or_edit_postgres_range_filter_dictionary(self, postgres_range_filter_dictionaries, filter_name, filter_type, range_type, values):
        if not postgres_range_filter_dictionaries.get(filter_name, None):
            postgres_range_filter_dictionaries[filter_name] = {
                "lowers": [],
                "uppers": [],
                "range_type": range_type,
                "lower_bound": None,
                "upper_bound": None
            }

        if "g" in filter_type:
            upper_or_lower_bound = "lower"
            bound_character = "("

            if "te" in filter_type:
                bound_character = "["
        elif "l" in filter_type:
            upper_or_lower_bound = "upper"
            bound_character = ")"

            if "te" in filter_type:
                bound_character = "]"
        else:
            raise Exception("Invalid bound of " + filter_type)

        postgres_range_filter_dictionaries[filter_name][upper_or_lower_bound + "_bound"] = bound_character
        postgres_range_filter_dictionaries[filter_name][upper_or_lower_bound + "s"] = self.convert_values(values, range_type)

    def convert_values(self, values, range_type):
        the_now = now()
        if settings.TIME_ZONE:
            timezone = pytz.timezone(settings.TIME_ZONE)
            the_now = the_now.astimezone(timezone)

        current_time_zone = the_now.strftime("%z")
        new_values = []

        for value in values:
            if value == "__NONE_OR_BLANK__":
                new_values.append("")
                value = None
            elif value == "__NONE__":
                value = None
            elif value == "__BLANK__":
                value = ""
            elif value == "__TRUE__":
                value = True
            elif value == "__FALSE__":
                value = False
            elif range_type == RangeFilterTypes.DATE:
                value = parser.parse(value + " 00:00:00" + current_time_zone)
            elif range_type == RangeFilterTypes.TIME:
                value = parser.parse(value)
            elif range_type in [RangeFilterTypes.NUMBER, RangeFilterTypes.AGE]:
                try:
                    value = int(value)
                except ValueError:
                    value = float(value)

            new_values.append(value)

        return new_values