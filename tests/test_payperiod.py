import pytest

import payroll as pr


@pytest.fixture(scope="module")
def registry():
    registry = pr.ServiceTypeRegistry()

    employee = pr.Employee(name="Jane Doe")
    registry.register(
        pr.ServiceType(employee=employee, name="one_child", hourly_rate=22)
    )
    registry.register(
        pr.ServiceType(employee=employee, name="two_children", hourly_rate=24)
    )
    return registry


@pytest.fixture(scope="module")
def service():
    service_type = pr.ServiceType(
        employee=pr.Employee(name="Jane Doe"), name="one_child", hourly_rate=22
    )
    date = pr.Date(2022, 10, 23)
    return pr.Service(date, service_type, duration_hrs=8)


def test_record_service(service, registry):
    payperiod = pr.PayPeriod(registry=registry)
    payperiod.record_service(service)
    assert len(payperiod.services_performed) == 1


def test_init(service, registry):
    payperiod = pr.PayPeriod(registry=registry, services_performed=[service, service])
    assert len(payperiod.services_performed) == 2


def test_total_hours(service, registry):
    payperiod = pr.PayPeriod(registry=registry, services_performed=[service, service])
    assert payperiod.total_hours == 16


def test_total_hours_by_type_with_overtime(registry):
    payperiod = pr.PayPeriod(registry=registry)
    date = pr.Date(2022, 10, 23)

    services = [
        ("one_child", 8),
        ("two_children", 9.5),
        ("two_children", 9.5),
        ("two_children", 9.5),
        ("two_children", 9),
    ]

    for type_name, duration in services:
        payperiod.record_service(
            pr.Service(date=date, type=registry[type_name], duration_hrs=duration)
        )

    assert payperiod.total_hours == 45.5
    assert payperiod.total_pay == 1142.0
    assert payperiod.total_hours_by_type_with_overtime() == {
        "one_child": 8.0,
        "two_children": 32.0,
        "two_children_OT": 5.5,
    }


def test_repr(registry, service):
    payperiod = pr.PayPeriod(registry=registry, services_performed=[service])
    assert str(payperiod).startswith("PayPeriod(\n\tService(date")
