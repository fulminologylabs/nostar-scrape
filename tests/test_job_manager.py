from datetime import datetime
from pynostr.event import EventKind
from pynostr.filters import Filters, FiltersList
from app.services.job_manager import JobManager
from app.services.filter_manager import FilterManager
#from app.repository.models import Filter, Relay, Job, Base

class TestJobManager:
    def test_init_job_manager(self):
        pass

    def test_get_batch_time_range(self):
        pass

    def get_jobs_batch(self, start: datetime, stop: datetime):
        pass

    def test_pull_daily_job(self):
        pass

    def test_pull_historical_job(self):
        pass

    def test_pull_jobs_for_date_range(self):
        pass

    def test_schedule_next_daily_jobs(self):
        pass

    def test_schedule_historical_job(self):
        pass

    def test_register_daily_job(self):
        pass

    def test_mark_historical_job_complete(self):
        pass

    def test_get_job_type(self):
        pass

    def test_init_filter_manager(self):
        pass

    def test_create_filters(self):
        pass

    def test_create_subscriptions(self):
        pass

    def test_register_subscriptions(self):
        pass

    def test_update_job_status(self):
        pass

    def test_update_subscription_status(self):
        pass

