from details.Detail import Detail
from machines.Machine import Machine
from staff.Worker import Worker


class DefectReport:
    def __init__(self, detail:Detail, operator:Worker, machine:Machine):
        self.detail_id = detail.detail_id
        self.detail_type = detail.name
        self.operator_id = operator.sign
        self.machine_id = machine.machine_id
        self.push_to_maintenance(operator.production_line.maintenance, machine)

    def push_to_maintenance(self, maintenance, machine:Machine):
        maintenance.add(machine)
        maintenance.reports.append(self)