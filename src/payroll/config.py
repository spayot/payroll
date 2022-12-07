from dataclasses import dataclass

import yaml


@dataclass
class ServiceTypeConfig:
    name: str
    hourly_rate: float
    employee_name: str


@dataclass
class Config:
    services: list[ServiceTypeConfig]

    @classmethod
    def from_yaml(cls, filepath: str):
        with open(filepath, "r") as f:
            data = yaml.safe_load(f)

        return cls(services=[ServiceTypeConfig(**c) for c in data["services"]])
