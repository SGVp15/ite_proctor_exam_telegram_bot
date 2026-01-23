import datetime


def time_to_seconds(t: datetime.time) -> int:
    return t.hour * 3600 + t.minute * 60 + t.second


def check_time(check_t, start_t, delta_dt=None, end_t=None):
    start_sec = time_to_seconds(start_t)
    check_sec = time_to_seconds(check_t)

    if end_t:
        end_sec = time_to_seconds(end_t)
    else:
        end_sec = start_sec + int(delta_dt.total_seconds())

    end_sec = end_sec % 86400

    return start_sec <= check_sec <= end_sec


def check_time_interval(check_dt: datetime.datetime,
                        start_dt: datetime.datetime,
                        delta_dt: datetime.timedelta | None = None,
                        end_dt: datetime.datetime | None = None) -> bool:
    ''' Если введены delta_dt и end_dt - приоритет end_dt. '''
    if type(start_dt) is datetime.time:
        return check_time(check_dt, start_dt, delta_dt, end_dt)

    if end_dt is None:
        if delta_dt is not None:
            end_dt = start_dt + delta_dt
        else:
            end_dt = start_dt
    return start_dt <= check_dt <= end_dt

#
# if __name__ == '__main__':
#     a = check_time_interval(
#         check_dt=datetime.datetime.now().time(),
#         start_dt=datetime.time(hour=9, minute=0),
#         delta_dt=datetime.timedelta(minutes=10))
#     print(a)
#
#     a = check_time_interval(
#         check_dt=datetime.datetime.now(),
#         start_dt=datetime.datetime(2026, 1, 23, hour=9, minute=0),
#         end_dt=datetime.datetime(2026, 1, 23, hour=10, minute=20),
#
#     )
#     print(a)
