from datetime import datetime
from pynostr.event import EventKind

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