from constants import stat_constants

money = stat_constants()[0]

def money_script(add : bool|None, amount : int):
    global money
    if add:
        money += amount
    elif not add:
        money -= amount
    else:
        pass

    return money