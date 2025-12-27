from datetime import datetime
from src.app.adapters.date_clock import DatetimeClock


def test_clock_returns_increasing_time():
    clock = DatetimeClock()
    a = clock.get_current()
    b = clock.get_current()
    assert b > a
    assert isinstance(a, datetime)
    assert isinstance(b, datetime)