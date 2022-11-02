"""
Definition of validators.
Validator is a function that takes as input a value and returns True if and only if the value is
in the domain of values.
"""
import pandas as pd

MIN_DATE = pd.Timestamp('2006-03-21')  # the date when Twitter has started the activity.
MAX_DATE = pd.Timestamp('2022-09-28')  # the date when dataset has been collected.


def check_int(value):
    if pd.isna(value):
        return False

    try:
        return float(str(value)).is_integer()
    except ValueError:
        return False


def check_positive_int(value):
    if not check_int(value):
        return False

    return int(value) >= 0


def check_text(value) -> bool:
    if pd.isna(value):
        return False

    # empty strings are not valid
    return len(str(value)) > 0


def check_bot(value):
    if not check_positive_int(value):
        return False

    return int(value) in [0, 1]


def check_date(value):
    try:
        date = pd.Timestamp(value)
    except ValueError:
        return False

    return MIN_DATE < date < MAX_DATE
