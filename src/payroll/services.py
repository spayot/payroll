from dataclasses import asdict, dataclass
from datetime import datetime

import yaml

from .dates import Date

OVERTIME_MULTIPLIER = 1.5
OVERTIME_SUFFIX = "_OT"


@dataclass
class Employee:
    name: str


@dataclass
class ServiceType:
    name: str
    hourly_rate: float


class ServiceTypeRegistry:
    def __init__(self):
        self.types = {}

    def register(self, service_type: ServiceType) -> None:
        self.types[service_type.name] = service_type

    def __getitem__(self, key: str) -> ServiceType:
        return self.types.get(key)

    def get_rate_from_type(self, type_name: str) -> float:
        """If overtime suffix is present, hourly rate is mutliplied
        by OVERTIME_MULTIPLIER"""
        if type_name.endswith(OVERTIME_SUFFIX):
            type_name = type_name[: -len(OVERTIME_SUFFIX)]
            return self.types[type_name].hourly_rate * OVERTIME_MULTIPLIER

        return self.types[type_name].hourly_rate

    @classmethod
    def from_yaml(cls, filepath: str):
        registry = cls()
        with open(filepath, "r") as f:
            data = yaml.safe_load(f)
        for info in data.get("services"):
            registry.register(ServiceType(**info))

        return registry

    def to_yaml(self, filepath: str) -> None:
        registry_data = {"services": [asdict(t) for t in self.types.values()]}
        with open(filepath, "w") as f:
            yaml.dump(registry_data, f)

    def __repr__(self) -> str:
        return f"ServiceTypeRegistry(types=[{', '.join(list(self.types.keys()))}])"


@dataclass
class Service:
    date: Date
    employee: Employee
    type: ServiceType
    duration_hrs: float

    @property
    def base_cost(self) -> float:
        return self.duration_hrs * self.type.hourly_rate

    def record(self, filepath: str) -> None:
        pass
