import copy
from typing import List
from datetime import datetime
from app.services.admin import Admin
from app.repository.models import JobType, Job, Filter
from app.repository.connection import yield_db_session
from app.services.filter_manager import FilterManager
from app.utils import get_today_raw, get_last_second_of_date, \
    get_first_second_of_date
# TODO Eventually the JobManager should receive only one Job
# and the Processor and each JobManager will create its own DB Session.
class JobManager:
    def __init__(
        self,
        #db_session, # Eventually this will be passed down, but at time of development component is top of the hierarchy
        date: datetime,
        job_type_id: int,
    ):
        """
            Fetches the datetime and unix timestamp
            for yesterday at midnight. Then looks for any 
            historical or daily job that is scheduled to run
            in the past 5 minutes.

            Gathers and sets information related to running
            each job after examination.
        """
        self.job_type_id = job_type_id
        self.job_date = date
        self.job_type_id = job_type_id
        # Set DB and Lookup Parameters for jobs
        self.session = next(yield_db_session())
        self.admin = Admin(self.session)
        # Get Job Type
        self.job_type: JobType = [jt for jt in self.admin.lookup_job_types() if jt.id == self.job_type_id][0]
        # Get Batch Bounds Based on Job Type
        job_batch_datetime_bounds = self._get_datetime_batch_bounds()
        self.job_batch_start_bound: datetime = job_batch_datetime_bounds[0]
        self.job_batch_end_bound: datetime = job_batch_datetime_bounds[1]
        # Get Jobs to Process
        self.jobs_batch = self.pull_batch_jobs()
        # Operational Attrs
        self.queued_jobs = copy.deepcopy(self.jobs_batch)
        self.completed_jobs = []
        # TODO Left Off Start creating filters
        # - Create initial filter 

        # - Determine the incrementer: 60 * 60 * 24 * 6  # 1 week

        # - Generate a batch of filters based on 
        #   the initial template and the incrementer.

        # - Assist in the creation of subscriptions that
        #   align to each filter

    def _get_datetime_batch_bounds(self) -> tuple:
        """
            returns tuple where idx 0 is start datetime bound
            and idx 1 is end datetime bound

            ignoring use of match here for now
        """
        if "historical" in self.job_type.process:
            # TODO Re-evaluate this range for historical processes later
            # Get all of today's scheduled historical jobs
            return (get_first_second_of_date(), get_last_second_of_date())
        elif "daily" in self.job_type.process:
            # TODO Implement daily bounds
            pass
    
    def pull_batch_jobs(self) -> List[Job]:
        try:
            return self.session.query(Job).filter(
                # Known Job Type ID
                Job.job_type == self.job_type_id,
                # Jobs scheduled to start after the first second of today (or first second)
                Job.start_time >= self.job_batch_start_bound,
                # Jobs scheduled to start before the last second of today (or last second)
                Job.start_time <= self.job_batch_end_bound,
            ).all()
        except Exception as e:
            # TODO Logging
            # TODO Error Handling
            print(f"pull_batch_jobs failed with error: {e}.")
            raise e
    
    def pop_job_to_processor(self) -> Job:
        """
            Pass next job from self.queued_jobs to the processor.
            When this job is returned back to the component,
            it will handled as completed and appended to
            self.completed_jobs
        """
        pass

    def handle_completed_job(self, completed_job: Job) -> bool:
        """
            What the processor will use to pass a completed (or errored)
            job back to the job manager for handling its results.
        """
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
    
