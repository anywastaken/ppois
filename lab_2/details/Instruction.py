import uuid
from abc import ABC

from details.Detail import Detail
from materials.Material import Material


class Instruction(ABC):
    def __init__(self):
        self.instruction_id = uuid.uuid4()
        self.author: str = ''
        self.result: str = ''
        self.mass: float = 0

        self.components: list[Material] | list[Detail] = []
        self.price: int = 0