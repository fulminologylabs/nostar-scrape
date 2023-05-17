from dataclasses import dataclass

@dataclass(kw_only=True)
class RelayJob:
    """
        Populated by running a Daily process

        Intended to be main input to scrapers
    """
    relay_id: int
    filter_id: int

   
@dataclass(kw_only=True)
class RelayJobRecord(RelayJob):
    subscription_id: str
    created_at: int

