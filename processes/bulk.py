from pynostr.event import EventKind
from pynostr.relay_manager import RelayManager
from pynostr.filters import FiltersList, Filters
from constants import RELAY_LIST, EPOCH_START
from datetime import datetime
from utils import get_yesterday_raw, convert_date_str_to_datetime, \
    convert_datetime_to_date_str, handle_date_string, get_last_second_of_date

class TestBulkProcess:
    """
        Responsible for the historical load / onboarding
        of a newly registered relay
    """
    def __init__(self, url: str, start: str = None, end: str = None):
        """
            param url   relay url
            param start date fmt "MM/DD/YYYY"
            param end   date fmt "MM/DD/YYY"
        """
        self.url = url
        # Set start TODO make a setter method
        if start is None:
            self.start = convert_date_str_to_datetime(EPOCH_START)
        else:
            self.start = handle_date_string(start)
        # Set end TODO make a setter method
        if end is None:
            self.end = get_last_second_of_date(get_yesterday_raw())
        else:
            self.end = get_last_second_of_date(handle_date_string(end))

    def set_date_range():
        pass

    def get_stepped_filters():
        pass

    def process():
        pass

    def run():
        """
            Controller
        """
        pass