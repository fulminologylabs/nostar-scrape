from app.repository.connection import yield_db_session
from app.repository.models import Job, JobType
from app.constants import HISTORICAL_JOBS
from app.services.admin import Admin

RELAY_ID = 1

if __name__ == "__main__":
    session = next(yield_db_session())
    admin = Admin(db_session=session)
    # Get Job Type
    job_types = admin.lookup_job_types()
    print(job_types)
    job_type: JobType = [
        jt for jt in admin.lookup_job_types()\
        if jt.process == HISTORICAL_JOBS.HIST_BASE_1.value
    ][0] # get remaining item after comprehension filtering
    scheduled_job: Job = admin.schedule_historical_job(
        relay_id=RELAY_ID,
        job_type_id=job_type.id
    )
    print(f"JOB Scheduled for: {scheduled_job.start_time}")

