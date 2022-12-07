from src import payroll as pr


def main():

    registry = pr.ServiceTypeRegistry()

    registry.register(pr.ServiceType(name="one_child", hourly_rate=22))
    registry.register(pr.ServiceType(name="two_children", hourly_rate=24))

    current_week_dates = pr.generate_current_week_dates()
    gui = pr.PayPeriodGUI(
        dates=current_week_dates,
        registry=registry,
    )

    root = gui.create_layout()
    root.mainloop()


if __name__ == "__main__":
    main()
