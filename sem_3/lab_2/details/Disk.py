
from details.ProducedDetail import ProducedDetail


class Disk(ProducedDetail):
    def __init__(self, defect_chance: float):
        super().__init__(defect_chance)

        self.name = "Disk"
        self.radius:float = 0
        self.thickness:float = 0

        self.mass = self.calculate_mass()
        self.price = self.calculate_price()

    def calculate_mass(self):
        volume = 3.1415 * (self.radius ** 2) * self.thickness
        density = 7.8
        return volume * density

    def calculate_price(self):
        return int(self.mass * 0.5)