from staff.Employee import Employee


class Driver(Employee):
    def __init__(self):
        super().__init__()
        self.attentiveness:bool | None = None

    def concentrate(self):
        self.attentiveness = True

    def drive(self):
        if not self.attentiveness:
            print('SSSHHHIIIIIIUUUUASDJFVNSLKFJVNLKSDJFNVLKJS')
            print('Driver just got into an accident!')