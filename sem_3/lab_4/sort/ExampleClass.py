

class ExampleClass:
    def __init__(self, value):
        self.value = value

    def __lt__(self, other: "ExampleClass"):
        return self.value < other.value

    def __gt__(self, other: "ExampleClass"):
        return self.value > other.value

    def __eq__(self, other: "ExampleClass"):
        return self.value == other.value
    
    def __repr__(self) -> str:
        return f"ExampleClass({self.value})"