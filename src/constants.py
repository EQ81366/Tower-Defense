from enum import Enum

def stat_constants():
    money = 100
    hp = 100

    return [
        money,
        hp
    ]

def enemy_constants() -> list[list[str|int|float]]:
    # [A, B, C, D, (E)]
    # replace A with type, B with tier, C with speed, D with hp, (E with custom money drop)
    basic : list[str|int|float] = ["basic", 1, 3.0, 1]
    tank : list[str|int|float] = ["tank", 1, 0.5, 100]

    return [
        basic, 
        tank
    ]

def tower_constants() -> list[list[str|int]]:
    # [A, B, C, D, E, F]
    # replace A with type, B with tier, C with dmg, D with cd, E with range, F with rotation speed, G with cost
    basic : list[str|int] = ["basic", 1, 1, 60, 400, 100, 100]

    return [
        basic
    ]

class TargetingStates(Enum):
    EFFICIENT = 0
    CLOSE = 1
    FIRST = 2
    LAST = 3
    STRONG = 4