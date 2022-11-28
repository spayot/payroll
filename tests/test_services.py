import pytest

import payroll as pr

YAML_CONTENT = """services:
- hourly_rate: 22
  name: one_child\n"""


@pytest.fixture(scope="module")
def date():
    return pr.Date(2022, 10, 23)


@pytest.fixture(scope="module")
def employee():
    return pr.Employee(name="Jane Doe")


@pytest.fixture(scope="module")
def service_type():
    return pr.ServiceType(name="one_child", hourly_rate=22)


def test_date(date):
    assert str(date) == "2022-10-23"


class TestService:
    def test_base_cost(self, date, employee, service_type):
        service = pr.Service(date, employee, service_type, duration_hrs=8)
        assert service.base_cost == 176


class TestRegistry:
    def test_register(self, service_type):
        registry = pr.ServiceTypeRegistry()
        registry.register(service_type)
        assert len(registry.types) == 1

    def test_getitem(self, service_type):
        registry = pr.ServiceTypeRegistry()
        registry.register(service_type)
        assert registry["one_child"].hourly_rate == 22

    def test_get_rate_from_type(self, service_type):
        registry = pr.ServiceTypeRegistry()
        registry.register(service_type)
        assert registry.get_rate_from_type("one_child") == 22
        assert (
            registry.get_rate_from_type("one_child_OT")
            == 22 * pr.services.OVERTIME_MULTIPLIER
        )

    def test_from_yaml(self):
        registry = pr.ServiceTypeRegistry.from_yaml("data/service_types.yaml")
        assert registry.get_rate_from_type("two_children") == 24

    def test_to_yaml(self, tmpdir, service_type):
        p = tmpdir.join("tmp.yml")
        registry = pr.ServiceTypeRegistry()
        registry.register(service_type)
        registry.to_yaml(p)
        assert p.read() == YAML_CONTENT
        assert len(tmpdir.listdir()) == 1
