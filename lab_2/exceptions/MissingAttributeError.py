


class MissingAttributeError(Exception):
    def __init__(self, attr, obj):
        super().__init__(f"Object {type(obj).__name__} does not have attribute '{attr}'")
