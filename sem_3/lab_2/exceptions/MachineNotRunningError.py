

class MachineNotRunningError(Exception):
    def __init__(self):
        super().__init__("Machine is not running!")