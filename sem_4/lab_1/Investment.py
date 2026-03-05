class Investment:
    def __init__(self, name:str, percent:int):
        self.name = name
        self.percent = 0
        self.set_percent(percent)

    def set_percent(self, percent):
        if percent>=0:
            self.percent = percent
        else:
            print("Percent can't be under 0\n")
            percent = int(input("Input new percent:"))
            self.set_percent(percent)