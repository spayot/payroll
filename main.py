from src import payroll as pr

registry = pr.ServiceTypeRegistry()

registry.register(pr.ServiceType(name="one_child", rate=22))
registry.register(pr.ServiceType(name="two_children", rate=24))
