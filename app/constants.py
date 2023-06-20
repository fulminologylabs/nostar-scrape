from enum import Enum
# Core
# TODO Find out what a good start date is
EPOCH_START = "8/15/2022"
POSTGRESQL_TS_FORMAT_PARAM = "YYYY-MM-DD HH24:MI:SS"
RELAY_LIST = [
    #"wss://nostr-pub.wellorder.net",
    "wss://relay.damus.io",
    #"wss://relay.nostr.band/"
]
NOSTR_BAND_ALL = "wss://relay.nostr.band/all"
# Dates
MS_MULTIPLE = 1e3
SECOND      = 1
MIN         = 60
HR          = 60 * 60
DAY         = 60 * 60 * 24

class SUPPORTED_TAGS(Enum):
    EVENT  = "#e"
    PUBKEY = "#p"
  