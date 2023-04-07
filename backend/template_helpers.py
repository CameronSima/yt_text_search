from datetime import timedelta


def format_time(time):
    formatted = str(timedelta(seconds=time))
    # remove ms
    return formatted.split('.')[0]
