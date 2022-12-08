from datetime import datetime

import pytest

import payroll as pr


def test_generate_current_week_dates():
    dates = pr.generate_current_week_dates()

    assert str(dates[0]).startswith("Mon")
    assert len(dates) == 7
    assert str(dates[-1]).startswith("Sun")


def test_from_datetime():
    dt = datetime(2000, 1, 1)
    date = pr.Date.from_datetime(dt)

    assert str(date) == "Sat 2000-01-01"
