from enum import Enum

STARTING_MONEY = 10000000
HIT_POINTS = 100

def stat_constants():
    global STARTING_MONEY, HIT_POINTS

    return [
        STARTING_MONEY,
        HIT_POINTS
    ]

class EnemyConstants(Enum):
    # [A, B, C, D, E, (F)]
    # replace A with type, B with tier, C with speed, D with hp, E with weight, (F with custom money drop)
    BASIC = "basic", 0, 3.0, 100, 10
    TANK = "tank", 0, 0.5, 100, 4

class TowerConstants(Enum):
    # [A, B, C, D, E, F]
    # replace A with type, B with tier, C with turrets, D with dmg, E with cd, F with range, G with rotation speed, H with cost
    BASIC = "basic", 0, 1, 1, 60, 1000, 100, 100
    DOUBLE = "double", 0, 2, 4, 140, 1000, 60, 300

class TargetingStates(Enum):
    EFFICIENT = 0
    CLOSE = 1
    FIRST = 2
    LAST = 3
    STRONG = 4