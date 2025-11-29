from machines.Machine import Machine
from exceptions.MachineAlreadyRunningError import MachineAlreadyRunningError
from exceptions.MachineNotRunningError import MachineNotRunningError
from details.AssembledDetail import AssembledDetail
from details.Assembly import Assembly

class AssemblyMachine(Machine):
    def __init__(self):
        super().__init__()
        self.instruction:Assembly | None = None

    def run(self):
        if self.is_running:
            raise MachineAlreadyRunningError
        self.is_running = True

    def stop(self):
        if not self.is_running:
            raise MachineNotRunningError
        self.is_running = False

    def make_detail(self)->AssembledDetail:
        if not self.is_running:
            raise MachineNotRunningError
        detail = AssembledDetail(self.defect_chance)
        if detail.defect:
            self.defect_chance += 0.1
        detail.name = self.instruction.result
        detail.mass = self.instruction.mass
        detail.price = self.instruction.price
        return detail