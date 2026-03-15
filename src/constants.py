from enum import Enum


def stat_constants():
    starting_money = 1000
    hp = 100

    return [starting_money, hp]


class EnemyShape(Enum):
    COMPLEX = None
    CIRCLE = "circle"

class EnemyConstants(Enum):
    # [A, B, C, D, E, (F)]
    # replace A with (image type, color), B with tier, C with speed, D with hp, E with weight, (F with custom money drop)
    BASIC = (EnemyShape.CIRCLE, (0, 0, 0)), 0, 2.0, 1, 10
    TANK = (EnemyShape.CIRCLE, (0, 255, 0)), 0, 0.5, 100, 4


class TowerConstants(Enum):
    # [A, B, C, D, E, F]
    # replace A with type, B with tier, C with turrets, D with dmg, E with cd, F with range, G with rotation speed, H with cost
    BASIC = "basic", 0, 1, 1, 1, 200, 300, 100
    DOUBLE = "double", 0, 2, 4, 140, 1000, 60, 300


class TargetingStates(Enum):
    EFFICIENT = 0
    CLOSE = 1
    FIRST = 2
    LAST = 3
    STRONG = 4
