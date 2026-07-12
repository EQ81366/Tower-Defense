from constants import stat_constants

money = stat_constants()[0]


def money_script(add: bool | None = None, amount: int = 0):
    global money
    if add is None:
        return money

    if add:
        money += amount
    elif not add:
        money -= amount

    return money
