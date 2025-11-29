

class MachineAlreadyRunningError(Exception):
    def __init__(self):
        super().__init__("Machine is already running!")