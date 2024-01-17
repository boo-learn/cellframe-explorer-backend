from datetime import datetime


def date_format(date: datetime) -> str:
    return str(int(date.timestamp()))
