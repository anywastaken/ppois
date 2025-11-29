from other.SocialNetwork import SocialNetwork
from staff.Employee import Employee


class Smm(Employee):
    def __init__(self):
        super().__init__()
        self.social_networks:list[SocialNetwork]
        self.raw_content:bool = False
        self.edited_content:bool = False

    def film_content(self):
        self.raw_content = True
        print('Content is filmed!')

    def edit_content(self):
        if self.raw_content:
            self.raw_content = False
            self.edited_content = True
            print('Content is edited!')
        else:
            print('Film content at first!')

    def post_content(self):
        if self.edited_content:
            self.edited_content = False
            print('Content is posted!')
        else:
            print('Edit content at first!')