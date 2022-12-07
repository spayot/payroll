from datetime import datetime, timedelta


class Date:
    def __init__(self, *args, **kwargs):
        self.datetime = datetime(*args, **kwargs)

    def __repr__(self):
        return self.datetime.strftime("%a %Y-%m-%d")

    @classmethod
    def today(cls):
        today = datetime.today()
        return cls.from_datetime(today)

    @classmethod
    def from_datetime(cls, dt: datetime):
        return cls(dt.year, dt.month, dt.day)

    def __add__(self, other: timedelta):
        return Date.from_datetime(self.datetime + other)


def generate_current_week_dates() -> list[Date]:
    today = datetime.today()
    dayofweek = today.weekday()
    deltas = range(-dayofweek, -dayofweek + 7)  # Monday to Sunday
    return [Date.from_datetime(today + timedelta(days=delta)) for delta in deltas]
