from tests.fixtures import *
from app.services.admin import Admin
from app.utils import historical_same_day_register_cutoff, \
    get_tomorrow_raw
from app.repository.models import Relay, RelayConfig, Job, JobType

class TestAdmin:
    def test_add_relay_w_config(
        self,
        admin: Admin, 
        relay_url: str,
        relay_name: str,
        dt_epoch_start: datetime,
    ):
        relay = admin.add_relay_w_config(
            url=relay_url,
            name=relay_name,
            epoch_start=dt_epoch_start,
        )
        #Assert
        assert type(relay) == Relay
        assert type(relay.relay_config) == RelayConfig
        assert relay.id == relay.relay_config.relay_id
        admin.session.flush()

    def test_get_relay_w_config_by_id(
        self, 
        admin: Admin,
    ):
        test_id = 1
        result: Relay = admin.get_relay_w_config_by_id(relay_id=test_id)

        assert result.id == test_id == result.relay_config.relay_id
        admin.session.flush()

    def test_get_all_relay_w_config(
        self, 
        admin: Admin,
    ):
        known_threshold = 2
        results: list = admin.get_all_relay_w_config()

        assert len(results) >= known_threshold
        admin.session.flush()

    def test_update_relay(
        self, 
        admin: Admin,
    ):
        test_name = "not the orignal"
        # Update Name
        update_fields = {"name": test_name}
        updated_relay = admin.update_relay(
            relay_id=1, 
            fields=update_fields
        )
        # Assert
        assert updated_relay.name == test_name
        assert updated_relay.updated_at is not None
        admin.session.flush()

    def test_update_relay_config(
        self, 
        admin: Admin
    ):
        test_epoch_start = datetime.now()
        update_fields = {"epoch_start": test_epoch_start}
        updated_relay_w_config = admin.update_relay_config(
            relay_id=1,
            fields=update_fields,
        )
        # Assert
        assert updated_relay_w_config.relay_config.epoch_start == test_epoch_start
        assert updated_relay_w_config.relay_config.updated_at is not None
        admin.session.flush()

    def test_schedule_valid_historical_job(
        self,
        admin: Admin,
    ):
        # Relay IDs
        relay_ids = [1,]
        # Job Type
        job_type_ids = [1,]
        # Should schedule today?
        sched_today = historical_same_day_register_cutoff()
        for r_id, jt_id in zip(relay_ids, job_type_ids):
            job = admin.schedule_historical_job(
                relay_id=r_id,
                job_type_id=jt_id,
            )
            # Assert
            assert type(job) == Job
            assert type(job.job_desc) == JobType
            if sched_today:
                # Assert that the start time is tonight (today)
                assert job.start_time.date() == datetime.today().date() 
            else:
                # assert that the start time is tomorrow night (tomorrow)
                tomorrow = get_tomorrow_raw().date()
                assert job.start_time.date() == tomorrow

    def test_rollback_if_exception(
        self, 
        admin: Admin
    ):
        """
        TODO will have to early commit to test
        this functionality.
        """
        pass

