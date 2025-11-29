from abc import ABC
import uuid


class Employee(ABC):
    def __init__(self):
        self.sign = uuid.uuid4()
        self.name:str = ''
        self.salary:int = 0

