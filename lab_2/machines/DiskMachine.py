from details.Disk import Disk
from exceptions.MachineAlreadyRunningError import MachineAlreadyRunningError
from exceptions.MachineNotRunningError import MachineNotRunningError
from machines.ProductionMachine import ProductionMachine


class DiskMachine(ProductionMachine):
    def __init__(self):
        super().__init__()

    def run(self):
        if self.is_running:
            raise MachineAlreadyRunningError
        self.is_running = True

    def stop(self):
        if not self.is_running:
            raise MachineNotRunningError
        self.is_running = False

    def make_detail(self)->Disk:
        if not self.is_running:
            raise MachineNotRunningError
        detail = Disk(self.defect_chance)
        if detail.defect:
            self.defect_chance += 0.1
        detail.name = self.instruction.result
        detail.mass = self.instruction.mass
        detail.price = self.instruction.price
        return detail