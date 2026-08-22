from constants import stat_constants

money = stat_constants()[0]


class Money:
    def __init__(self):
        self.money = money

    def get_money(self):
        return self.money

    def add_money(self, value: int):
        self.money += value

    def sub_money(self, value: int):
        self.money -= value


money_man = Money()
