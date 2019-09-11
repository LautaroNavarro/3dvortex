import pytz
from datetime import datetime


def get_current_utc_datetime():
    return datetime.now(pytz.utc)
