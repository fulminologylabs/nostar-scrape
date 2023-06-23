from datetime import datetime
from app.repository.models import Job
from app.services.filter_manager import FilterManager

class JobManager:
    def __init__(
        self, 
        job_template: Job,
    ):
        """
            Fetches the datetime and unix timestamp
            for yesterday at midnight. Then looks for any 
            historical or daily job that is scheduled to run
            in the past 5 minutes.

            Gathers and sets information related to running
            each job after examination.
        """
        self.job_template = job_template
    
    def _get_batch_time_range(self) -> tuple:
        pass

    def _get_jobs_batch(self, start: datetime, stop: datetime) -> list[Job]:
        pass

    def _pull_daily_job(
        self, 
        relay_id: int
    ) -> Job:
        pass
    
    def _pull_historical_job(
            self, 
            relay_id: int
    ) -> Job:
        pass

    def pull_jobs_for_date_range(self, 
        start_bound: datetime, 
        end_bound: datetime
    ) -> list:
        pass

    def schedule_next_daily_jobs(self) -> bool:
        pass

    def schedule_historical_job(self) -> bool:
        pass

    def register_daily_job(self) -> bool:
        pass

    def mark_historical_job_complete(self) -> bool:
        pass

    def get_job_type(self, id: int) -> str:
        pass

    def init_filter_manager(self) -> FilterManager:
        pass

    def create_filters(self) -> list:
        pass

    def create_subscriptions(self) -> list:
        pass

    def register_subscription(
            self, 
            filter_id: int, 
            subscription_id: int, 
            count: int,
            status: str, 
            completed: datetime
    ) -> bool:
        pass

    def update_subscription_status(
            self, 
            status: int, 
            sub_id: int
        ) -> bool:
        pass
    
