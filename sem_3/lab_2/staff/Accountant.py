from staff.Employee import Employee


class Accountant(Employee):
    def __init__(self):
        super().__init__()

    def issue_salaries(self):
        print('Salary has been paid!')

    def generate_salary_report(self):
        print('Report has been generated!')
