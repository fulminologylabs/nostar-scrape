"""
    Handles Relay entries, RelayConfig entries, JobType entries, Eventkind entries, and Filter entries
"""
import copy
from typing import List
from datetime import datetime
from app.repository.models import Relay, RelayConfig, \
    Job, Status, EventKind, JobType
from app.constants import JOB_STATUS
from app.utils import historical_same_day_register_cutoff, \
    get_last_second_of_date, get_today_raw, get_tomorrow_raw

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
            self.session.flush() # TODO is this required prior to inserting RelayConfig?
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
            self.session.commit()
            return relay
        except Exception as e:
            # TODO logging
            # TODO error handling
            print(f"add_relay_w_config failed with error: {e}.")
            self.session.rollback()

    def update_relay(
        self, 
        relay_id: int,
        fields: dict,
    ) -> Relay:
        """
            keys on fields must be attributes of
            Relay
        """
        try:
            relay = self.get_relay_w_config_by_id(relay_id)
            relay_raw = copy.deepcopy(relay.__dict__)
            # TODO not sure why this is attached
            del relay_raw["_sa_instance_state"]
            # Update
            update_raw = {**relay_raw, **fields}
            update_raw = Relay(**update_raw)
            # Merge and Refresh
            val = self.session.merge(update_raw)
            # Commit
            self.session.commit()
            self.session.refresh(val)
            #return updated
            return val
        except Exception as e:
            # TODO Logging
            # TODO Error Handling
            print(f"update_relay failed with error: {e}.")
            self.session.rollback()

    def update_relay_config(
        self, 
        relay_id: int,
        fields: dict,
    ) -> Relay:
        """
            keys on fields must be attributes of
            RelayConfig
        """
        try:
            relay = self.get_relay_w_config_by_id(relay_id)
            config = relay.relay_config
            config_raw = copy.deepcopy(config.__dict__)
            # TODO not sure why this is attached
            del config_raw["_sa_instance_state"]
            # Update
            update_raw = {**config_raw, **fields}
            update_raw = RelayConfig(**update_raw)
            # Merge and Refresh
            val = self.session.merge(update_raw)
            # Commit
            self.session.commit()
            self.session.refresh(val)
            self.session.refresh(relay) # Refresh relay as well
            #return relay
            return relay
        except Exception as e:
            # TODO Logging
            # TODO Error Handling
            print(f"update_relay_config failed with error: {e}.")
            self.session.rollback()
        

    def get_relay_w_config_by_id(
        self,
        relay_id: int,
    ) -> Relay | None:
        result = None
        try:
            result = self.session.query(Relay).filter(Relay.id == relay_id).one()
            return result
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
    
    def schedule_historical_job(
        self,
        relay_id: int,
        job_type_id: int,
    ):
        try:
            pending_status = [
                status for status in self.lookup_statuses() \
                if status.status == JOB_STATUS.PENDING.value
            ][0].id

            start = Admin.register_start_time_for_historical_job()
            job: Job = Admin.create_job(
                relay_id=relay_id, 
                job_type_id=job_type_id,
                start_time=start,
                status_id=pending_status,
            )
            # add
            self.session.add(job)
            # commit
            self.session.commit()
            self.session.refresh(job)
            print()
            return job
        except Exception as e:
            # TODO Error Handling
            # TODO Logging
            print(f"schedule_historical_job failed with error: {e}.")
            self.session.rollback()

    @staticmethod
    def register_start_time_for_historical_job() -> int:
        """
            A new historical job for a loader is scheduled
            for the current day at midnight if earlier than 5 PM EST
            or, tomorrow at midnight. The value returned is a unix timestamp.

            When many historical jobs are scheduled for the same night,
            additional prioritization or spacing-in-scedule logic will 
            need to be added.
        """
        try:
            schedule_tonight = historical_same_day_register_cutoff()
            if schedule_tonight:
                today = get_today_raw()
                midnight = get_last_second_of_date(today)
                # schedule today
                return midnight
            tomorrow = get_tomorrow_raw()
            midnight = get_last_second_of_date(tomorrow)
            # schedule tomorrow
            return midnight
        except TypeError as e:
            print(f"register_start_time failed with error: {e}.")
            raise e

    
    def lookup_event_kinds(self) -> List[EventKind]:
        results = []
        try:
            res = self.session.query(EventKind).all()
            results.extend(res)
        except Exception as e:
            # TODO error handling
            # TODO logging
            print(f"get_all_relay_w_config failed with exception: {e}.")
        return results
    
    def lookup_job_types(self) -> List[JobType]:
        results = []
        try:
            res = self.session.query(JobType).all()
            results.extend(res)
        except Exception as e:
            # TODO error handling
            # TODO logging
            print(f"get_all_relay_w_config failed with exception: {e}.")
        return results

    def lookup_statuses(self) -> List[Status]:
        results = []
        try:
            res = self.session.query(Status).all()
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
    
    @staticmethod
    def create_job(
        relay_id: int,
        job_type_id: int,
        start_time: int,
        status_id: int,
    ) -> Job:
        return Job(
            relay_id=relay_id,
            job_type=job_type_id,
            status_id=status_id,
            start_time=start_time,
        )

