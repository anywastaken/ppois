class Product:
    def __init__(self, name, manufacturer, unp, quantity, address):
        self.name = str(name)
        self.manufacturer = str(manufacturer)
        try:
            self.unp = int(unp)
        except ValueError:
            self.unp = 0
        self.quantity = self._validate_quantity(quantity)
        
        self.address = str(address)

    def _validate_quantity(self, value):
        if str(value).lower() == "нет на складе":
            return "нет на складе"
        try:
            return int(value)
        except ValueError:
            return 0