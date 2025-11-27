def stat_constants():
    money = 100
    hp = 100

    return [
        money,
        hp
    ]

def enemy_constants() -> list[list[str|int|float]]:
    # [A, B, C, D]
    # replace A with type, B with tier, C with speed, D with hp
    basic : list[str|int|float] = ["basic", 1, 1.0, 1]
    tank : list[str|int|float] = ["tank", 1, 0.5, 100]

    return [
        basic, 
        tank
    ]

def tower_constants() -> list[list[str|int]]:
    # [A, B, C, D, E, F]
    # replace A with type, B with dmg, C with cd, D with range, E with rotation speed, F with cost
    basic : list[str|int] = ["basic", 1, 60, 400, 100, 100]

    return [
        basic
    ]    

from image_loader import load_images

load_images()