import uuid

import random


class Detail:
    def __init__(self, defect_chance):
        self.detail_id = uuid.uuid4()
        self.operator = None
        self.name:str = ''
        self.mass:float = 0
        self.price:int = 0
        self.defect = random.random() < defect_chance

