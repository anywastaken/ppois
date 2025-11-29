
from details.Detail import Detail
from details.Instruction import Instruction


class Assembly(Instruction):
    def __init__(self):
        super().__init__()
        self.components:list[Detail] = []