"""
    Handles Relay entries, RelayConfig entries, JobType entries, Eventkind entries, and Filter entries
"""
from typing import List
from datetime import datetime
from app.repository.models import Relay, RelayConfig

class Admin:
    """
        Main service for the admin API for the control panel.
        Some method will also have roles in fetching relay_config
        data given, a job.
    """
    def __init__(self, db_session):
        self.session = db_session

    def add_relay_w_config(
        self,
        url: str,
        name: str = None,
        epoch_start: datetime = None
    ) -> Relay:
        try:
            relay = Admin.create_relay(name=name, url=url)
            # Add Relay
            self.session.add(relay)
            self.session.flush()
            # Refresh for ID
            self.session.refresh(relay)
            # Add RelayConfig
            config = Admin.create_relay_config(relay_id=relay.id, epoch_start=epoch_start)
            # Add Relay Config
            self.session.add(config)
            # Refresh Objects
            self.session.refresh(relay)
            self.session.refresh(config) # TODO do we need this?
            # Relay obj should now carry RelayConfig obj
            return relay
        except Exception as e:
            # TODO logging
            # TODO error handling
            print(f"add_relay_w_config failed with error: {e}.")
            self.session.rollback()
        
    def add_relay_config(
        self, 
        relay_id: int, 
        epoch_start: datetime = None
    ) -> Relay:
        return False

    def update_relay(
        self, 
        fields: dict,
    ) -> Relay:
        """
            keys on fields must be attributes of
            Relay
        """
        return False

    def update_relay_config(
        self, 
        fields: dict,
    ) -> Relay:
        """
            keys on fields must be attributes of
            RelayConfig
        """
        return False

    def get_relay_w_config_by_id(
        self,
        relay_id: int,
    ) -> Relay | None:
        result = None
        try:
            result = self.session.query(Relay).filter(Relay.id == relay_id).one()
        except Exception as e:
            # TODO error handling
            # TODO logging
            print(f"get_relay_w_config_by_id failed with exception: {e}.")
        return result

    def get_all_relay_w_config(self) -> List[Relay]:
        results = []
        try:
            res = self.session.query(Relay).all()
            results.extend(res)
        except Exception as e:
            # TODO error handling
            # TODO logging
            print(f"get_all_relay_w_config failed with exception: {e}.")
        return results

    @staticmethod
    def create_relay(
        name: str,
        url: str,
    ) -> Relay:
        return Relay(name=name, url=url)

    @staticmethod
    def create_relay_config(
        relay_id: int,
        epoch_start: datetime = None,
    ) -> RelayConfig:
        return RelayConfig(
            relay_id=relay_id,
            epoch_start=epoch_start,
        )

