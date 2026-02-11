import random


from details.Detail import Detail
from machines.Machine import Machine

from staff.Employee import Employee


class Worker(Employee):
    def __init__(self):
        super().__init__()
        self.machine_type:str = ''
        self.machine:Machine | None = None
        self.fingers = 10
        self.attentiveness:bool | None= None
        from manufactoring.ProductionLine import ProductionLine
        self.production_line:ProductionLine|None = None

    def run_machine(self):
        self.machine.run()

    def make_detail(self)->Detail:
        detail = self.machine.make_detail()
        if detail.defect:
            if self.attentiveness:
                self.make_report(detail)
            else:
                if random.random()<0.5:
                    self.fingers -= 1

        return detail


    def make_report(self, detail):
        from manufactoring.DefectReport import DefectReport
        return DefectReport(detail, self, self.machine)

    def send_to_storage(self, detail:Detail):
        self.production_line.get_detail(detail)

    def smoke(self):
        print('Worker is relaxed now!')
        self.attentiveness = False