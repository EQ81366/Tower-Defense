import pygame
from fonts import font_16, font_18
from constants import TowerConstants, TowerStats, BulletStats
from operator import add, mul
from typing import Any
from types import FunctionType

pygame.font.init()


def render_text(input: str, header: bool = False):
    if header:
        font = font_18
    else:
        font = font_16
    # font.set_bold(header)

    return font.render(input, True, "black").convert_alpha()


def set_equal(a: Any, b: Any):
    a = b
    return a


# T0
# Faster reload: cooldown decreased.
# Oiled cogs: increased turn speed.
#
# T1(speed): bullet speed, turn speed, and attack cooldown slightly reduced.
# Speeeeed: turn speed greatly increased.
# Grooves: projectile speed increased.
#
# T2(Gatling): Attack cooldown greatly decreased.
# Tiny bullets: bullet size and damage decreased slightly, bullet speed greatly increased.
# Needles: bullet pierce increased.
#
# T3(drill): (Ill explain this one in person it's hard to write out).
# T3(overheat): after every 5th bullet has triple damage, speed, pierce.
#
# T2(Shrapnel): bullets produce shrapnel upon hitting enemy.
# Travel: shrapnel goes farther before despawning.
# Bleeding: enemy's hit take 1% of their max health as damage every second after being hit (around 5 second total).
#
# T3(glass cannon): all pierce removed, shrapnel effectiveness and damage greatly increased.
# T3(Chain): every enemy hit by shrapnel produces 3 bullets of extra shrapnel.
#
# T1(damage): pierce, damage, range slightly increased.
# Bullseye: damage increased.
# Bigger chamber: bullet speed, damage, size slightly increased.
#
# T2(Sniper): damage, range, projectile speed increased.
# Heavy: bullet speed slightly decreased, damage increased.
# Growth: bullet size and damage increase the more the bullet travels.
#
# T3(Hitscan): instant projectile speed, pierce increased.
# T3(Lead): Bullets deal more damage and slow enemys.
#
# T2(Shotgun): range greatly decreased, shoots multiple bullets that spread out.
# Barrel: range slightly increased.
# Spread: Increased bullet count and spread.
#
# T3(slug): Projectile count and spread greatly decreased and damage greatly increased.
# T3(Shockwave): attacks knock back enemys.


# each line with render_text is one set of 2 upgrades
# tier 0: 2 upgrades per branch, 1 branch
# tier 1: 2 upgrades per branch, 2 branches
# tier 2: 2 upgrades per branch, 4 branches
upgrade_dict: dict[
    int,
    dict[
        int,
        list[
            list[
                list[
                    tuple[
                        tuple[
                            int,
                            list[tuple[TowerStats | BulletStats, float, FunctionType]],
                        ],
                        *tuple[pygame.Surface, ...],
                    ]
                ]
            ]
        ],
    ],
] = {
    0: {
        0: [
            [
                [
                    (
                        (100, [(TowerStats.COOLDOWN, 0.8, mul)]),
                        render_text("Faster Reload:", True),
                        render_text("cooldown decreased"),
                    ),
                    (
                        (100, [(TowerStats.ROTATION_SPEED, 1.4, mul)]),
                        render_text("Oiled Cogs:", True),
                        render_text("increased turn speed"),
                    ),
                ]  # T0
            ]
        ],
        1: [
            [
                [
                    (
                        (500, [(TowerStats.ROTATION_SPEED, 2.0, mul)]),
                        render_text("Speeeeed:", True),
                        render_text("turn speed greatly"),
                        render_text("increased"),
                    ),
                    (
                        (400, [(BulletStats.SPEED, 1.5, mul)]),
                        render_text("Grooves:", True),
                        render_text("projectile speed increased"),
                    ),
                ],  # T1(speed)
                [
                    (
                        (550, [(TowerStats.DAMAGE, 1.6, mul)]),
                        render_text("Bullseye:", True),
                        render_text("damage increased"),
                    ),
                    (
                        (
                            600,
                            [
                                (BulletStats.SPEED, 1.2, mul),
                                (TowerStats.DAMAGE, 1.2, mul),
                                (BulletStats.SIZE, 1.2, mul),
                            ],
                        ),
                        render_text("Bigger chamber:", True),
                        render_text("bullet speed, damage, size"),
                        render_text("slightly increased"),
                    ),
                ],  # T1(damage)
            ]
        ],
        2: [
            [  # comes after T1(speed)
                [
                    (
                        (
                            1200,
                            [
                                (BulletStats.SIZE, 0.8, mul),
                                (TowerStats.DAMAGE, 0.8, mul),
                                (BulletStats.SPEED, 2.0, mul),
                            ],
                        ),
                        render_text("Tiny Bullets:", True),
                        render_text("bullet size/damage lowered"),
                        render_text("bullet speed increased"),
                    ),
                    (
                        (900, [(BulletStats.PIERCE, 3, add)]),
                        render_text("Needles:", True),
                        render_text("bullet pierce increased"),
                    ),
                ],  # T2(Gatling)
                [
                    (
                        (700, [(BulletStats.SHRAPNEL_DISTANCE, 2.2, mul)]),
                        render_text("Travel:", True),
                        render_text("shrapnel goes farther before"),
                        render_text("despawning"),
                    ),
                    (
                        (1500, [(BulletStats.BLEEDING, True, set_equal)]),
                        render_text("Bleeding:", True),
                        render_text("enemies hit take max hp"),
                        render_text("damage for 3 seconds"),
                    ),
                ],  # T2(Shrapnel)
            ],
            [  # comes after T1(damage)
                [
                    (
                        (
                            1100,
                            [
                                (BulletStats.SPEED, 0.8, mul),
                                (TowerStats.DAMAGE, 2.0, mul),
                            ],
                        ),
                        render_text("Heavy:", True),
                        render_text("bullet speed slightly lowered"),
                        render_text("damage increased"),
                    ),
                    (
                        (1300, [(BulletStats.GROWTH, 1.0, set_equal)]),
                        render_text("Growth:", True),
                        render_text("bullet size and damage"),
                        render_text("increase as the bullet travels"),
                    ),
                ],  # T2(Sniper)
                [
                    (
                        (600, [(TowerStats.RANGE, 1.4, mul)]),
                        render_text("Barrel:", True),
                        render_text("range slightly increased"),
                    ),
                    (
                        (
                            1200,
                            [
                                (BulletStats.BULLET_AMOUNT, 4, add),
                                (BulletStats.BULLET_SPREAD, 30, add),
                            ],
                        ),
                        render_text("Spread:", True),
                        render_text("increased bullet count and"),
                        render_text("spread"),
                    ),
                ],  # T2(Shotgun)
            ],
        ],
    },
    1: {
        0: [
            [
                [
                    (
                        (150, [(TowerStats.RANGE, 40, add)]),
                        render_text("Glasses:", True),
                        render_text("slightly increases range, you"),
                        render_text("had vision issues"),
                    ),
                    (
                        (200, [(TowerStats.COOLDOWN, 0.9, mul)]),
                        render_text("Sugary Drink:", True),
                        render_text("somehow lowers cooldown"),
                    ),
                ]
            ]
        ],
        1: [
            [
                [
                    (
                        (700, [(BulletStats.GROWTH, 1.0, set_equal)]),
                        render_text("Growing:", True),
                        render_text("bullet minorly increases"),
                        render_text("damage and size moving"),
                    ),
                    (
                        (
                            500,
                            [
                                (BulletStats.SPEED, 0.6, mul),
                                (BulletStats.SIZE, 1.2, mul),
                            ],
                        ),
                        render_text("Big Shot:", True),
                        render_text("increases bullet size"),
                        render_text("reduces bullet speed"),
                    ),
                ],
                [
                    (
                        (650, [(BulletStats.BLEEDING, True, set_equal)]),
                        render_text("Hollow-point Bullets:", True),
                        render_text("makes enemies bleed upon"),
                        render_text("impact"),
                    ),
                    (
                        (800, [(TowerStats.DAMAGE, 2.0, mul)]),
                        render_text("Titanium Tips:", True),
                        render_text("massively increases damage"),
                    ),
                ],
            ]
        ],
        2: [
            [
                [
                    (
                        (1200, [(TowerStats.DAMAGE, 1.9, mul)]),
                        render_text("Milk:", True),
                        render_text("increases damage by"),
                        render_text("strengthening your bones"),
                    ),
                    (
                        (1000, [(TowerStats.RANGE, 1.5, mul)]),
                        render_text("Scope:", True),
                        render_text("increases range"),
                    ),
                ],
                [
                    (
                        (
                            1400,
                            [
                                (TowerStats.BULLET_CAPACITY, 2, add),
                                (BulletStats.SIZE, 0.5, mul),
                            ],
                        ),
                        render_text("Smaller Bullets:", True),
                        render_text("increases bullet capacity"),
                        render_text("by 2 with smaller bullets"),
                    ),
                    (
                        (
                            1000,
                            [
                                (BulletStats.PIERCE, 2, add),
                                (BulletStats.SPEED, 1.4, mul),
                            ],
                        ),
                        render_text("Extra Gunpowder:", True),
                        render_text("increases bullet speed"),
                        render_text("and pierce"),
                    ),
                ],
            ],
            [
                [
                    (
                        (1100, [(TowerStats.COOLDOWN, 0.6, mul)]),
                        render_text("Gear Ratios:", True),
                        render_text("reduces cooldown through"),
                        render_text("better gear ratios"),
                    ),
                    (
                        (900, [(TowerStats.ROTATION_SPEED, 1.6, mul)]),
                        render_text("Lubrication:", True),
                        render_text("increases tower rotation"),
                        render_text("speed with lube"),
                    ),
                ],
                [
                    (
                        (800, [(BulletStats.SIZE, 1.5, mul)]),
                        render_text("Chunky:", True),
                        render_text("bullet size increase"),
                        render_text("it ate some chunkies"),
                    ),
                    (
                        (1200, [(BulletStats.SLOWING, 1.0, add)]),
                        render_text("Cold Shot:", True),
                        render_text("bullets slow enemies"),
                        render_text("(it got refrigerated)"),
                    ),
                ],
            ],
        ],
    },
}

tier_upgrade_dict: dict[
    int,
    dict[
        int,
        list[
            list[
                list[
                    tuple[
                        list[tuple[TowerStats | BulletStats, float, FunctionType]],
                        *tuple[pygame.Surface, ...],
                    ]
                ]
            ]
        ],
    ],
] = {
    0: {
        0: [
            [
                [
                    (
                        [
                            (BulletStats.SPEED, 1.4, mul),
                            (TowerStats.ROTATION_SPEED, 1.4, mul),
                            (TowerStats.COOLDOWN, 0.7, mul),
                        ],
                        render_text("Speed:", True),
                        render_text("bullet/turn speed increased"),
                        render_text("cooldown slightly reduced"),
                    ),  # T1 path-0
                    (
                        [
                            (BulletStats.PIERCE, 3, add),
                            (TowerStats.DAMAGE, 1.5, mul),
                            (TowerStats.RANGE, 1.4, mul),
                        ],
                        render_text("Damage:", True),
                        render_text("pierce, damage, range"),
                        render_text("slightly increased"),
                    ),  # T1 path-1
                ]
            ]
        ],
        1: [
            [
                [
                    (
                        [(TowerStats.COOLDOWN, 0.15, mul)],
                        render_text("Gatling:", True),
                        render_text("attack cooldown greatly"),
                        render_text("decreased"),
                    ),  # T2 path-0-0
                    (
                        [(BulletStats.SHRAPNEL, True, set_equal)],
                        render_text("Shrapnel:", True),
                        render_text("bullets produce shrapnel"),
                        render_text("upon hitting enemy"),
                    ),  # T2 path-0-1
                ],
                [
                    (
                        [
                            (TowerStats.DAMAGE, 1.6, mul),
                            (TowerStats.RANGE, 1.8, mul),
                            (BulletStats.SPEED, 2.0, mul),
                            (TowerStats.COOLDOWN, 1.5, mul),
                        ],
                        render_text("Sniper:", True),
                        render_text("damage, range, projectile"),
                        render_text("speed & cooldown raised"),
                    ),  # T2 path-1-0
                    (
                        [
                            (TowerStats.RANGE, 0.5, mul),
                            (BulletStats.BULLET_AMOUNT, 2, add),
                            (BulletStats.BULLET_SPREAD, 5, add),
                            (BulletStats.SIZE, 0.6, mul),
                        ],
                        render_text("Shotgun:", True),
                        render_text("range greatly decreased"),
                        render_text("multi-shot with spread"),
                    ),  # T2 path-1-1
                ],
            ]
        ],
        2: [
            [
                [
                    (
                        [(BulletStats.PIERCE, 2000, set_equal)],
                        render_text("Drill:", True),
                        render_text("gains EXTREMELY high"),
                        render_text("pierce"),
                    ),  # T3 path-0-0-0
                    (
                        [(TowerStats.COOLDOWN, 1, set_equal)],
                        render_text("Full Auto:", True),
                        render_text("even shorter cooldown"),
                    ),  # T3 path-0-0-1
                ],
                [
                    (
                        [
                            (BulletStats.PIERCE, 1, set_equal),
                            (BulletStats.SHRAPNEL_DAMAGE, 4.0, mul),
                        ],
                        render_text("Glass Cannon:", True),
                        render_text("all pierce removed, shrapnel"),
                        render_text("damage greatly increased"),
                    ),  # T3 path-0-1-0
                    (
                        [(BulletStats.SHRAPNEL_CHAINING, True, set_equal)],
                        render_text("Chain:", True),
                        render_text("every enemy hit by shrapnel "),
                        render_text("produces more shrapnel"),
                    ),  # T3 path-0-1-1
                ],
            ],
            [
                [
                    (
                        [
                            (BulletStats.SPEED, 2000, set_equal),
                            (BulletStats.PIERCE, 4, add),
                        ],
                        render_text("Hitscan:", True),
                        render_text("instant projectile speed"),
                        render_text("pierce increased"),
                    ),  # T3 path-1-0-0
                    (
                        [
                            (TowerStats.DAMAGE, 1.8, mul),
                            (BulletStats.SLOWING, 1.0, add),
                        ],
                        render_text("Lead:", True),
                        render_text("bullets deal more damage"),
                        render_text("and slow enemies"),
                    ),  # T3 path-1-0-1
                ],
                [
                    (
                        [
                            (BulletStats.BULLET_AMOUNT, 3, set_equal),
                            (TowerStats.DAMAGE, 4.0, mul),
                            (BulletStats.BULLET_SPREAD, 10, set_equal),
                            (BulletStats.SIZE, 2, mul),
                        ],
                        render_text("Slug:", True),
                        render_text("projectile count and spread"),
                        render_text("lowered, damage increased"),
                    ),  # T3 path-1-1-0
                    (
                        [(BulletStats.KNOCKBACK, 10, add)],
                        render_text("Shockwave:", True),
                        render_text("attacks knock back enemies"),
                    ),  # T3 path-1-1-1
                ],
            ],
        ],
    },
    1: {
        0: [
            [
                [
                    (
                        [
                            (TowerStats.CAMO_DETECTION, 1, add),
                            (TowerStats.RANGE, 1.2, mul),
                        ],
                        render_text("Microfiber Cloth:", True),
                        render_text("by cleaning your glasses"),
                        render_text("you gain camo detection"),
                    ),
                    (
                        [(TowerStats.DAMAGE, 1.3, mul)],
                        render_text("Pointy Tips:", True),
                        render_text("damage increased through"),
                        render_text("pointier tips"),
                    ),
                ]
            ]
        ],
        1: [
            [
                [
                    (
                        [(BulletStats.GROWTH, 0.4, add)],
                        render_text("Growth Spurt:", True),
                        render_text("increases rate of growth"),
                    ),
                    (
                        [(TowerStats.DAMAGE, 1.5, mul), (BulletStats.SPEED, 0.5, mul)],
                        render_text("Lead Bullets:", True),
                        render_text("halves speed and"),
                        render_text("increases damage"),
                    ),
                ],
                [
                    (
                        [(BulletStats.SPEED, 2.5, mul)],
                        render_text("Aerodynamic:", True),
                        render_text("massively increases"),
                        render_text("bullet speed"),
                    ),
                    (
                        [
                            (TowerStats.DAMAGE, 1.2, mul),
                            (TowerStats.ROTATION_SPEED, 1.3, mul),
                            (TowerStats.COOLDOWN, 0.8, mul),
                            (TowerStats.CAMO_DETECTION, 1, add),
                            (TowerStats.RANGE, 1.2, mul),
                        ],
                        render_text("Jack:", True),
                        render_text("improves all base"),
                        render_text("stats"),
                    ),
                ],
            ]
        ],
        2: [
            [
                [
                    (
                        [
                            (TowerStats.COOLDOWN, 0.3, mul),
                            (BulletStats.SPEED, 0.2, mul),
                        ],
                        render_text("Slowest O.A.T.:", True),
                        render_text("bullet speed and cd"),
                        render_text("majorly decreased"),
                    ),
                    (
                        [(TowerStats.DAMAGE, 3, mul)],
                        render_text("Hardcore:", True),
                        render_text("boosts damage"),
                    ),
                ],
                [
                    (
                        [(BulletStats.BLEEDING, True, set_equal)],
                        render_text("Spreading:", True),
                        render_text("bullets cause bleeding"),
                        render_text("on impact"),
                    ),
                    (
                        [(BulletStats.KNOCKBACK, 7, add)],
                        render_text("Heavy Bullets:", True),
                        render_text("bullets have knockback"),
                    ),
                ],
            ],
            [[([()], render_text("", True)), ([()], render_text("", True))], [([()], render_text("", True)), ([()], render_text("", True))]],
        ],
    },
}


def get_upgrades(tower: TowerConstants, tier: int, upgrade_path: list[int]) -> list[
    tuple[
        tuple[int, list[tuple[TowerStats | BulletStats, float, FunctionType]]],
        *tuple[pygame.Surface, ...],
    ]
]:
    tower_number = tower.number
    upgrade_info = upgrade_dict[tower_number][tier]

    # indexes to get rid of un-needed lists
    for i in range(2 - (tier % 3)):
        upgrade_info = upgrade_info[0]

    for i in range(tier % 3):
        if isinstance(upgrade_info, list):
            upgrade_info = upgrade_info[upgrade_path[i + 1]]

    upgrades: list[tuple[tuple[int, list[tuple[TowerStats | BulletStats, float, FunctionType]]], *tuple[pygame.Surface, ...]]] = upgrade_info  # type: ignore

    return upgrades


def get_tier_ups(
    tower: TowerConstants, tier: int, upgrade_path: list[int]
) -> list[tuple[list[tuple[TowerStats | BulletStats, float, Any]], *tuple[pygame.Surface, ...]]]:
    tower_number = tower.number
    upgrade_info = tier_upgrade_dict[tower_number][tier]

    for i in range(2 - (tier % 3)):
        upgrade_info = upgrade_info[0]

    for i in range(tier % 3):
        if isinstance(upgrade_info, list):
            upgrade_info = upgrade_info[upgrade_path[i + 1]]

    tier_ups: list[tuple[list[tuple[TowerStats | BulletStats, float, Any]], *tuple[pygame.Surface, ...]]] = upgrade_info  # type: ignore

    return tier_ups
