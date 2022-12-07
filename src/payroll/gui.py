import tkinter as tk

from .dates import Date
from .payperiod import PayPeriod
from .services import Employee, Service, ServiceType, ServiceTypeRegistry

TITLE = "Payroll Management System"


class ServiceEntry:
    def __init__(
        self,
        date: Date,
        svc_type: ServiceType,
        layout_row: int,
        layout_col: int,
        root: tk.Tk,
    ):
        self.date = date
        self.svc_type = svc_type
        self.gui_entry = tk.Entry(root, background="darkgrey")
        self.gui_entry.insert(0, 0)
        self.gui_entry.grid(row=layout_row, column=layout_col)

    def read(self, employee: Employee):
        duration_hrs = float(self.gui_entry.get())
        return Service(
            date=self.date,
            employee=employee,
            type=self.svc_type,
            duration_hrs=duration_hrs,
        )


class EmployeeEntry:
    def __init__(self, root, row: int, col: int, default: str):
        self.entry = tk.Entry(root, background="darkgrey")
        self.entry.insert(50, default)
        self.entry.grid(row=row, column=col)

    def read(self) -> Employee:
        return Employee(self.entry.get())


class PayPeriodGUI:
    def __init__(self, dates: list[Date], registry: ServiceTypeRegistry):
        self.dates = dates
        self.registry = registry
        self.root = tk.Tk()
        self.root.title(TITLE)

    def create_layout(self) -> tk.Tk:
        self.employee_entry = self.create_employee_entry(row=0)
        column_labels = self.create_column_labels(row=1, starting_col=1)
        date_labels = self.create_row_labels(starting_row=2, col=0)
        self.service_entries = self.create_service_entries(starting_row=2)
        buttons_row = 2 + len(self.dates) + 1
        buttons = self.create_bottom_buttons(row=buttons_row)
        return self.root

    def create_employee_entry(self, row: int = 0):
        employee_name_label = tk.Label(self.root, text="Employee Name")
        default_employee = self.registry.get_employees().pop()
        employee_entry = EmployeeEntry(
            self.root, row=row, col=1, default=default_employee
        )

        employee_name_label.grid(row=row, column=0)

        return employee_entry

    def create_column_labels(self, row: int, starting_col: int) -> dict:
        labels = {}
        for i, svc_type in enumerate(self.registry.types):
            labels[svc_type] = tk.Label(self.root, text=svc_type)
            labels[svc_type].grid(row=row, column=i + starting_col)

        return labels

    def create_row_labels(self, starting_row: int, col: int = 0) -> dict:
        labels = {}
        for i, date in enumerate(self.dates):
            labels[date] = tk.Label(self.root, text=date)
            labels[date].grid(row=starting_row + i, column=col)

        return labels

    def create_service_entries(self, starting_row: int = 1, starting_col: int = 1):
        service_entries = []

        for i, date in enumerate(self.dates):
            for j, service_name in enumerate(self.registry.types):
                service_entries.append(
                    ServiceEntry(
                        date=date,
                        svc_type=self.registry[service_name],
                        layout_row=starting_row + i,
                        layout_col=starting_col + j,
                        root=self.root,
                    )
                )

        return service_entries

    def create_bottom_buttons(self, row: int):
        button_calculate = tk.Button(
            self.root, text="Calculate Payroll", padx=50, command=self.calculate_payroll
        )
        button_save = tk.Button(self.root, text="Record Payroll", padx=50)

        button_calculate.grid(row=row, column=1)
        button_save.grid(row=row, column=2)
        return button_calculate, button_save

    def calculate_payroll(self) -> None:
        self.payperiod = PayPeriod(registry=self.registry)
        employee = self.employee_entry.read()

        for entry in self.service_entries:
            service = entry.read(employee=employee)
            self.payperiod.record_service(service)
        print(self.payperiod.total_hours_by_type_with_overtime())

    def _parse_entry(
        self,
        entry: tk.Entry,
        date: Date,
    ):
        pass
