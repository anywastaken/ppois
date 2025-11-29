

class ImportDirectionError(Exception):
    def __init__(self, direction, message="Wrong direction:"):
        self.direction = direction
        super().__init__(f"{message}: {direction}")