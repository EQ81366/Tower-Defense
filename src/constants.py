from enum import Enum


def stat_constants():
    starting_money = 100000
    hp = 100

    return [starting_money, hp]


class EnemyShape(Enum):
    COMPLEX = None
    CIRCLE = "circle"


class EnemyConstants(Enum):
    # [A, B, C, D, E, (F)]
    # replace A with (image type, color), B with tier, C with speed, D with hp, E with weight, (F with custom money drop)
    BASIC = (((EnemyShape.CIRCLE, (0, 0, 0)), 0, 2.0, 100, 2), 0, (False, 0))
    TANK = (((EnemyShape.CIRCLE, (0, 255, 0)), 0, 0.5, 100, 4), 1, (False, 0))

    def __init__(
        self,
        constants: tuple[tuple[EnemyShape, tuple[int, int, int]], int, float, int, int],
        number: int,
        abilities: tuple[bool, int],
    ):
        self.constants = constants
        self.number = number
        self.abilities = abilities


class EnemyAbilities(Enum):
    STUN_IMMUNITY = 0  # enemy will be able to move when shot
    CAMOUFLAGE = 1  # makes the enemy invisible


class TowerConstants(Enum):
    # last number is constants is always cost
    BASIC = (
        (0, 1, 1, 60, 200, 120, 1, 0, 100),
        0,
        (100, 1, 1, 1, 0, False, 200, 5, 0.5, False, False, 0.0, 0, 0),
    )
    DOUBLE = (
        (0, 2, 4, 140, 150, 60, 2, 0, 300),
        1,
        (150, 1, 1, 1, 0, False, 150, 5, 0.5, False, False, 0.0, 0, 0),
    )

    def __init__(
        self,
        constants: tuple[int, int, int, int, int, int, int, int, int],
        number: int,
        bullet_info: tuple[int, int, int, int, int, bool, int, int, float, bool, bool, float, int, int],
    ):
        self.constants = constants
        self.number = number
        self.bullet_info = bullet_info


class TowerStats(Enum):
    TIER = 0
    TURRETS = 1
    DAMAGE = 2
    COOLDOWN = 3
    RANGE = 4
    ROTATION_SPEED = 5
    BULLET_CAPACITY = 6
    CAMO_DETECTION = 7


class BulletStats(Enum):
    SPEED = 0
    PIERCE = 1
    SIZE = 2
    BULLET_AMOUNT = 3
    BULLET_SPREAD = 4
    SHRAPNEL = 5
    SHRAPNEL_DISTANCE = 6
    SHRAPNEL_AMOUNT = 7
    SHRAPNEL_DAMAGE = 8
    SHRAPNEL_CHAINING = 9
    BLEEDING = 10
    GROWTH = 11
    SLOWING = 12
    KNOCKBACK = 13


class TargetingStates(Enum):
    EFFICIENT = 0
    CLOSE = 1
    FIRST = 2
    LAST = 3
    STRONG = 4


# enum of all shop items
class ShopType(Enum):
    SHOPUI = 0
    TOWERUI = 1


# enum of all upgrades
class UpgradeType(Enum):
    UPGRADEUI = 0
    UPGRADES = 1


class GameScreen(Enum):
    MAIN_MENU = 0
    IN_GAME = 1
    SETTINGS = 2


class MapInfo(Enum):
    path1 = ((-4, 200), 0)

    def __init__(self, offset: tuple[int, int], number: int):
        self.offset = offset
        self.number = number
