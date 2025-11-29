

class WrongDefectChanceError(Exception):
    def __init__(self, chance, message="Wrong defect chance:"):
        self.direction = chance
        super().__init__(f"{message}: {chance}")