"""
Created by Fazlul Kabir Shohag on 29, February, 2020
Email: shohag.fks@gmail.com
"""

__author__ = 'Fazlul Kabir Shohag'


class RangeFilterTypes:
    DATE = "date"
    TIME = "time"
    AGE = "age"
    NUMBER = "number"
    DATETIME = "datetime"


class PostgresRangeQueryFilterTypes:
    CONTAINED_BY = "__contained_by"
    CONTAINS = "__contains"
    OVERLAP = "__overlap"
    NOT_LESS_THAN = "__not_lt"
    NOT_GREATER_THAN = "__not_gt"
    FULLY_LESS_THAN = "__fully_lt"
    FULLY_GREATER_THAN = "__fully_gt"
