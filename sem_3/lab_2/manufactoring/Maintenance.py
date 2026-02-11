from machines.Machine import Machine

from exceptions.WrongDefectChanceValue import WrongDefectChanceError

class Maintenance:

    def __init__(self):
        self.broken_machines:list[Machine] = []
        from manufactoring.DefectReport import DefectReport
        self.reports:list[DefectReport] = []

    def add(self, machine:Machine):
        self.broken_machines.append(machine)

    def repair(self, machine:Machine):
        if machine.defect_chance<0 or machine.defect_chance>1:
            raise WrongDefectChanceError(machine.defect_chance)
        machine.defect_chance = 0.1

    def repair_all(self):
        for item in self.broken_machines:
            self.repair(item)