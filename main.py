from collections import namedtuple

import yaml

from src import payroll as pr

FILEPATH = "data/services.yml"


def main(filepath):
    registry = pr.ServiceTypeRegistry.from_yaml(filepath)

    current_week_dates = pr.generate_current_week_dates()
    gui = pr.PayPeriodGUI(
        dates=current_week_dates,
        registry=registry,
    )

    root = gui.create_layout()
    root.mainloop()


if __name__ == "__main__":
    main(FILEPATH)
