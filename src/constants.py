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
    BASIC = (((EnemyShape.CIRCLE, (0, 0, 0)), 0, 2.0, 1, 10), 0)
    TANK = (((EnemyShape.CIRCLE, (0, 255, 0)), 0, 0.5, 100, 4), 1)

    def __init__(self, constants: tuple[tuple[EnemyShape, tuple[int, int, int]], int, float, int, int], number: int):
        self.constants = constants
        self.number = number


class TowerConstants(Enum):
    # [A, B, C, D, E, F]
    # replace A with type, B with tier, C with turrets, D with dmg, E with cd, F with range, G with rotation speed, H with cost
    BASIC = (("basic", 0, 1, 1, 60, 200, 300, 100), 0)
    DOUBLE = (("double", 0, 2, 4, 140, 1000, 60, 300), 0)

    def __init__(self, constants: tuple[str, int, int, int, int, int, int, int], number: int):
        self.constants = constants
        self.number = number


class TargetingStates(Enum):
    EFFICIENT = 0
    CLOSE = 1
    FIRST = 2
    LAST = 3
    STRONG = 4


# enum of all enemies
class EnemyType(Enum):
    BASIC = 0


# enum of all shop items
class ShopType(Enum):
    SHOPUI = 0
    TOWERUI = 1


# enum of all upgrades
class UpgradeType(Enum):
    UPGRADEUI = 0
    UPGRADES = 1
