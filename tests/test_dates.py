import pytest

import payroll as pr


def test_generate_current_week_dates():
    dates = pr.generate_current_week_dates()

    assert str(dates[0]).startswith("Mon")
