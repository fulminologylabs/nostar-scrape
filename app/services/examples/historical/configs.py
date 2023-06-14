from datetime import datetime
from pynostr.event import EventKind
from pynostr.filters import Filters, FiltersList

LIMIT = 3

START_DATE = "05/12/2023"
END_DATE = "05/13/2023"

SINCE = int(datetime.strptime(START_DATE, "%m/%d/%Y").strftime("%s")) 
UNTIL = int(datetime.strptime(END_DATE, "%m/%d/%Y").strftime("%s"))

FILTER_TEMPLATE = {
    "ids": [],
    "kinds": [EventKind.TEXT_NOTE,],
    "authors": [],
    "since": SINCE, # TODO this represents a state that it will be appended in the future
    "until": UNTIL, # TODO this represents a state that it will be appended in the future
    "event_refs": [],
    "pubkey_refs": [],
    "limit": LIMIT, # TODO this should be a constant
}

TIMEOUT = 300

CONFIG = {
    "limit": LIMIT,
    "since": UNTIL,
    "filters": [FILTER_TEMPLATE],
    "timeout": TIMEOUT,
}

"""     
    filters = FiltersList(
        [
            # Example Filter
            Filters(
                kinds=[EventKind.TEXT_NOTE],
                limit=3
                # since=SINCE,
                # until=UNTIL,
            )
        ]
    ) 
"""

class FilterHandler:
    def __init__(
            self, 
            job_type: int, 
            relay_config: dict, 
            filter_template: dict
        ):
        self._job_type = job_type
        self.relay_config = relay_config
        self.filter_template = filter_template

    def configure_template(self) -> Filters:
        """ STEP ONE
            Apply Relay preferences from RelayConfig
        """
        pass

    def _get_date_range_for_job(self) -> list:
        """ STEP TWO
            Depending on the job_type, derive a list of subject
            datetime objects that are subject for scraping, for a given relay
        """
        pass

    def derive_daily_filters(self) -> FiltersList:
        """ STEP THREE
            Given a template configured for individual relay configs and
            a single date, derive a FiltersList that use the `since` and 
            `until` params on the filter to walk the Relay's history for the
            date
        """
        pass



