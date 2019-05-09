import datetime


# 2019-05-08T23:22:02+00:00

def timestamp():
    year, month, day, hour, minute, second, wday, yday, tz = datetime.datetime.now().timetuple()
    timestamp = f"{year}-{month}-{day}T{hour}:{minute}:{second}"
    return timestamp
