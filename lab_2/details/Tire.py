
from details.ProducedDetail import ProducedDetail


class Tire(ProducedDetail):
    def __init__(self, defect_chance: float):
        super().__init__(defect_chance)

        self.name = "Tire"
        self.radius:float = 0
        self.width:float = 0
        self.profile:int = 0
        self.mass = self.calculate_mass()
        self.price = self.calculate_price()

    def calculate_mass(self):
        base_density = 1.1
        volume = self.radius * self.width * (self.profile / 100)
        return volume * base_density

    def calculate_price(self):
        return int(self.mass * 10)