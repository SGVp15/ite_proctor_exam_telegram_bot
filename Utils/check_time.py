import datetime


def check_time_interval(check_dt: datetime.datetime, start_dt: datetime.datetime, delta_dt: datetime.timedelta) -> bool:
    end_dt = start_dt + delta_dt
    return start_dt <= check_dt <= end_dt
