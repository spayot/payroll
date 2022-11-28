from collections import defaultdict

from .services import OVERTIME_SUFFIX, Service, ServiceType, ServiceTypeRegistry

OVERTIME_CUTOFF_HOURS = 40


class PayPeriod:
    def __init__(
        self,
        registry: ServiceTypeRegistry,
        services_performed: list[Service] = None,
    ):
        self.services_performed = services_performed if services_performed else []
        self.registry = registry

    def record_service(self, service: Service) -> None:
        self.services_performed.append(service)

    @property
    def total_hours(self) -> float:
        return sum([service.duration_hrs for service in self.services_performed])

    def total_hours_by_type_with_overtime(self) -> dict[str, float]:
        """calculates total hours and assigns overtime hours"""
        hours = self._raw_total_hours_by_type()
        overtime_hours: float = self._overtime_hours()
        overtime_type: str = self._define_overtime_servicetype()
        hours[overtime_type] -= overtime_hours
        hours[overtime_type + OVERTIME_SUFFIX] = overtime_hours

        return dict(hours)

    def _raw_total_hours_by_type(self) -> dict[str, float]:
        """does not compute overtime"""
        hours = defaultdict(float)
        for service in self.services_performed:
            hours[service.type.name] += service.duration_hrs

        return hours

    def _overtime_hours(self) -> float:
        return max(0, self.total_hours - OVERTIME_CUTOFF_HOURS)

    def _define_overtime_servicetype(self) -> ServiceType:
        hours = self._raw_total_hours_by_type()
        return max(hours, key=hours.get)

    @property
    def total_pay(self) -> float:
        hours_counts = self.total_hours_by_type_with_overtime()
        return sum(
            [
                hours * self.registry.get_rate_from_type(type_name)
                for type_name, hours in hours_counts.items()
            ]
        )

    def __repr__(self) -> str:
        repr = """PayPeriod(\n"""
        for service in self.services_performed:
            repr += f"\t{service}\n"
        return repr + ")"
