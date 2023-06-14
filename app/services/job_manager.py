from datetime import datetime
from repository.models import Job

class JobManager:
    def __init__(self, job_template: Job):
        self.job_template = job_template

    def pull_one_job(self, relay_id: int) -> Job:
        pass

    def pull_jobs_for_date_range(self, start_bound: datetime, end_bound: datetime) -> list:
        pass

    def schedule_next_daily_jobs(self) -> bool:
        pass

    def schedule_historical_job(self) -> bool:
        pass

    def register_daily_job(self) -> bool:
        pass

    def mark_historical_job_complete(self) -> bool:
        pass

    def get_job_type_by_id(self, id: int) -> str:
        pass

    def register_batch(
            self, 
            filter_id: int, 
            subscription_id: int, 
            count: int,
            status: str, 
            completed: datetime
    ) -> bool:
        pass
    
