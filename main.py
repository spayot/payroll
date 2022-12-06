from src import payroll as pr


def main():

    registry = pr.ServiceTypeRegistry()

    registry.register(pr.ServiceType(name="one_child", hourly_rate=22))
    registry.register(pr.ServiceType(name="two_children", hourly_rate=24))

    gui = pr.PayPeriodGUI(
        dates=[pr.Date.today(), pr.Date(2022, 12, 7)],
        registry=registry,
    )

    root = gui.create_layout()
    root.mainloop()


if __name__ == "__main__":
    main()
