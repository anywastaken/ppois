from Employee import Employee
from machines.Machine import Machine
from manufactoring.Maintenance import Maintenance


class Engineer(Employee):
    def __init__(self):
        super().__init__()
        self.maintenance:Maintenance | None = None

    def chek_machine(self, machine:Machine):
        if machine.defect_chance>0.1:
            self.maintenance.add(machine)

    def repair(self, machine:Machine):
        machine.defect_chance = 0.1

    def repair_all(self):
        for item in self.maintenance.broken_machines:
            self.repair(item)