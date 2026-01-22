import datetime


def check_time_interval(check_dt: datetime.datetime, start_dt: datetime.datetime,
                        delta_dt: datetime.timedelta | None = None, end_dt: datetime.datetime | None = None) -> bool:
    ''' Если введены delta_dt и end_dt - приоритет end_dt.'''
    if not end_dt:
        end_dt = start_dt + delta_dt
    return start_dt <= check_dt <= end_dt
