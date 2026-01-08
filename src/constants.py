from enum import Enum

def stat_constants():
    starting_money = 100
    hp = 100

    return [
        starting_money,
        hp
    ]

def enemy_constants() -> list[list[str|int|float]]:
    # [A, B, C, D, (E)]
    # replace A with type, B with tier, C with speed, D with hp, E with weight, (F with custom money drop)
    basic : list[str|int|float] = ["basic", 1, 3.0, 5, 1]
    tank : list[str|int|float] = ["tank", 1, 0.5, 100, 4]

    return [
        basic, 
        tank
    ]

def tower_constants() -> list[list[str|int]]:
    # [A, B, C, D, E, F]
    # replace A with type, B with tier, C with turrets, D with dmg, E with cd, F with range, G with rotation speed, H with cost
    basic : list[str|int] = ["basic", 1, 1, 1, 60, 400, 100, 100]
    double : list[str|int] = ["double", 1, 2, 4, 140, 200, 60, 300]

    return [
        basic,
        double
    ]

class TargetingStates(Enum):
    EFFICIENT = 0
    CLOSE = 1
    FIRST = 2
    LAST = 3
    STRONG = 4