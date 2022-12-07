import argparse

from src import payroll as pr

DEFAULT_CONFIGPATH = "config/example.yml"


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
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p",
        "--path",
        default=DEFAULT_CONFIGPATH,
        help="path to the services config YAML file",
        type=str,
    )

    args = parser.parse_args()

    main(args.path)
