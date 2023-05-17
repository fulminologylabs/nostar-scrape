from dateutil.parser import parse
from constants import MS_MULTIPLE, HR, DAY, MIN
from datetime import datetime, time, timedelta, timezone

def handle_date_string(date: str) -> datetime:
    """
        Handle potentially unknown date format and return datetime
    """
    return parse(date)

def init_scrape_subscription_since_param() -> int:
    """
        A new Relay scrape sets a Filter "since" param to the first second
        of the previous day.
    """
    start_bound = get_yesterday_raw()
    return convert_datetime_to_unix_ts(start_bound)

def init_scrape_subscription_until_param() -> int:
    """
        A new Relay scrape sets a Filter "until" param to the last second
        of the previous day.
    """
    yesterday = get_yesterday_raw()
    end_bound = get_last_second_of_date(yesterday)
    return convert_datetime_to_unix_ts(end_bound)

def daily_scrape_subscription_since_param() -> int:
    """
        A daily Relay scrape sets a Filter "since" param to the first second
        of the current day
    """
    start_bound = get_today_raw()
    return convert_datetime_to_unix_ts(start_bound)

def daily_scrape_subscription_until_param() -> int:
    """
        A daily Relay scrape sets a Filter "until" param to the last second of the current
        day
    """
    today = get_today_raw()
    end_bound = get_last_second_of_date(today)
    return convert_datetime_to_unix_ts(end_bound)

def adjust_since_bound(since: int, step_back_days: int = 1) -> int:
    """
        param since int
        param since the last passed since param (unix timestamp)

        param step_back_days int
        param step_back_days number of days to set the next since bound

        returns int unix timestamp of next since param
    """
    return get_unix_ts_n_hours_from_now(ts=since, days=step_back_days)

def adjust_until_bound(until: int, step_back_days: int = 1) -> int:
    """
        param until int
        param until the last passed until param (unix timestamp)

        param step_back_days int
        param step_back_days number of days to set the next until bound

        return int unix timestamp
    """
    return get_unix_ts_n_days_ago(ts=until, days=step_back_days)

def get_today_raw() -> datetime:
    raw = datetime.today()
    return datetime.combine(raw, time.min, tzinfo=timezone.utc)

def get_yesterday_raw() -> datetime:
    raw = datetime.today() - timedelta(days=1)
    return datetime.combine(raw, time.min, tzinfo=timezone.utc)

def get_last_second_of_date(dt: datetime) -> datetime:
    """
        Get last second of datetime object passed as dt param
    """
    return datetime.combine(dt, time.max, tzinfo=timezone.utc)

def get_first_second_of_date(dt: datetime) -> datetime:
    """
        Get first second of datetime object passed as dt param
    """
    return datetime.combine(dt, time.min, tzinfo=timezone.utc)

def convert_datetime_to_unix_ts(dt: datetime) -> int:
    return int(dt.timestamp() * MS_MULTIPLE)

def convert_unix_ts_to_datetime(ts: int) -> datetime:
    return datetime.fromtimestamp(ts)

def convert_date_str_to_datetime(date_str: str, fmt: str = "%m/%d/%Y") -> datetime:
    return datetime.strptime(date_str, fmt)

def convert_datetime_to_date_str(date: datetime, fmt: str = "%m/%d/%Y") -> str:
    return datetime.strftime(date, fmt)

def get_unix_ts_n_hours_from_now(ts: int, hours: int = 1) -> int:
    multiple = HR * hours
    return ts + multiple

def get_unix_ts_n_days_ago(ts: int, days: int = 1) -> int:
    diff = DAY * days
    return ts - diff

def generate_stepwise_filters_for_date(dt: datetime, step: int = 5) -> list:
    """
        Given a datetime object, generate a list of tuples where each tuple
        contains a since and until param for a filter.

        The difference between each since and until param in a given tuple
        is determined by the step.

        step param is representative of minutes

        returns list of tuples (<start Filter param>, <end Filter param>)
    """
    params = []
    step_size_seconds = step * MIN

    start_bound = get_first_second_of_date(dt)
    end_bound = get_last_second_of_date(dt)

    current_since = start_bound
    while current_since > end_bound:
        # Handle the last step gracefully
        if current_since + step_size_seconds > end_bound:
            params.append((current_since, end_bound))
        # Calculate the next upper bound
        next_bound = current_since + step_size_seconds
        params.append((current_since, next_bound))
        # Update the iterator for the step just recorded
        current_since = next_bound
    return params

def generate_date_range_from_dts(old_point: datetime, new_point: datetime) -> list:
    rng = []

    dt_start = old_point.replace(tzinfo=timezone.utc)
    dt_stop = new_point.replace(tzinfo=timezone.utc)

    current = dt_start
    while current < dt_stop:
        rng.append(get_first_second_of_date(current))
        current = current + timedelta(days=1)
    return rng 

def generate_date_range_from_ts(old_point: int, new_point: int) -> list:
    dt_start = convert_unix_ts_to_datetime(old_point)
    dt_end = convert_unix_ts_to_datetime(new_point)

    return generate_date_range_from_dts(old_point=dt_start, new_point=dt_end)

def date_str_to_datetime(date: str, format: str = "%m/%d/%Y") -> datetime:
    """
        Check formats that are valid per datetime.datetime.strftime documentation
        TODO add link to datetime documentation

        returns datetime
    """
    return datetime.strftime(date, format)
