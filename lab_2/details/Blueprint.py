

from materials.Material import Material
from details.Instruction import Instruction


class BluePrint(Instruction):
    def __init__(self):
        super().__init__()
        self.components: list[Material] = []