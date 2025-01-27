
from django.utils.timezone import make_aware
from datetime import datetime


def get_date_from_str(date_str):
    try:
        date_obj = make_aware(datetime.strptime(date_str, '%Y-%m-%d'))
    except ValueError:
        return None
    return date_obj
