from datetime import datetime
from pynostr.event import EventKind
from app.repository.models import Filter, Relay, Job
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

class FilterManager:
    """
        Always expect to append limit, since, and until params
        to the filter template at least.
    """
    def __init__(
            self, 
            job: Job, 
            incrementer: int,
        ):
        pass

