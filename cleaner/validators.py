import pandas as pd

# Constant definition for outlier values
min_date = pd.Timestamp('2006-03-21')  # the date when Twitter has started the activity.
max_date = pd.Timestamp('2022-09-28')  # the date when dataset has been collected.


def check_int(label):
    try:
        int(str(label))
        return True
    except ValueError:
        return False


check_positive_int = lambda label: check_int(label) and float(label) >= 0  # checks if label is positive
check_date = lambda label: min_date < pd.Timestamp(label) < max_date  # checks timestamps
check_bot = lambda x: int(x) in [0, 1]  # check bot
check_text = lambda x: not x or len(str(x)) <= 0  # check texts
