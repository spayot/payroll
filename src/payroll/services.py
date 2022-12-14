import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path

import yaml

from .dates import Date

OVERTIME_MULTIPLIER = 1.5
OVERTIME_SUFFIX = "_OT"


@dataclass
class Employee:
    name: str


@dataclass
class ServiceType:
    employee: Employee
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
            registry.register(
                ServiceType(
                    employee=Employee(info["employee_name"]),
                    name=info["name"],
                    hourly_rate=info["hourly_rate"],
                )
            )

        return registry

    def get_employees(self) -> set[str]:
        return {service.employee.name for service in self.types.values()}

    def to_yaml(self, filepath: str) -> None:
        registry_data = {"services": [asdict(t) for t in self.types.values()]}
        with open(filepath, "w") as f:
            yaml.dump(registry_data, f)

    def __repr__(self) -> str:
        return f"ServiceTypeRegistry(types=[{', '.join(list(self.types.keys()))}])"


@dataclass
class Service:
    date: Date
    type: ServiceType
    duration_hrs: float

    @property
    def base_cost(self) -> float:
        return self.duration_hrs * self.type.hourly_rate

    def to_json(self) -> dict:
        service_dict = {
            "date": str(self.date),
            "duration_hrs": self.duration_hrs,
            "type": self.type.name,
            "employee": self.type.employee.name,
            "hourly_rate": self.type.hourly_rate,
        }
        return json.dumps(service_dict)

    def record_to(self, filepath: Path) -> None:
        with filepath.open("a") as fp:
            fp.write(self.to_json() + "\n")
