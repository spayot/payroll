import argparse

from src import payroll as pr

DEFAULT_CONFIGPATH = "config/example.yml"
RECORDS_PATH = "data/service_records.jsonl"


def main(config_path: str, path_to_records: str):
    registry = pr.ServiceTypeRegistry.from_yaml(config_path)

    current_week_dates = pr.generate_current_week_dates()

    gui = pr.PayPeriodGUI(
        dates=current_week_dates,
        registry=registry,
        path_to_records=path_to_records,
    )

    root = gui.create_layout()
    root.mainloop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--config",
        default=DEFAULT_CONFIGPATH,
        help="path to the services config YAML file",
        type=str,
    )

    args = parser.parse_args()

    main(args.config, RECORDS_PATH)
