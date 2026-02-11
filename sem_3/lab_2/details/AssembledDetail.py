from details.Detail import Detail


class AssembledDetail(Detail):
    def __init__(self, defect_chance):
        super().__init__(defect_chance)
        self.components:list[Detail] = []