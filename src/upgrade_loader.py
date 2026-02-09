import pygame
from enum import Enum
#from upgrades import upgrades

pygame.font.init()

font = pygame.font.SysFont('Arial', 20)

def render_text(input : str):
    return font.render(input, True, "black")

def upgrades(type : str):
    upgrade_images : list[list[pygame.Surface]] = [[]]
    upgrade_info : list[list[int|str|float]] = [[]]

    if type == "BASIC":
        upgrade_images = [
            [render_text("Faster Reload:"), render_text("shoots 20% faster")],
            [render_text("Oiled Cogs:"), render_text("turns 20% faster")],

            [render_text("Bullseye:"), render_text("deals 100% more damage")],
            [render_text("Speeeeeeeed:"), render_text("turns 35% faster")]
        ]
        # MAKE SURE NAME OF TOWER ATTRIBUTE MATCHES EXACTLY TO TOWER VARIABLE NAMES
        upgrade_info = [
            # first input is cost, second input is stat to upgrade, third input is stat multiplier, fourth input is upgrade
            [150, "cd", 0.8, 1.1],
            [100, "r_speed", 1.2, 1.2],
            
            [400, "dmg", 2, 2.1],
            [300, "r_speed", 1.35, 2.2]
        ]

    elif type == "DOUBLE":
        upgrade_images = [
            [render_text("Better Goggles:"), render_text("30% more range")],
            [render_text("Higher Caliber:"), render_text("deals 25% more damage")],

            [render_text("Double:"), render_text("shoot twice before"), render_text("reloading")],
            [render_text("Speeeeeeeed:"), render_text("turns 35% faster")]
        ]
        upgrade_info = [
            [200, "range", 1.3, 1.1],
            [250, "dmg", 1.25, 1.2],
            
            [400, "turrets", 2, 2.1],
            [300, "r_speed", 1.35, 2.2]
        ]

    return upgrade_images, upgrade_info

class UpgradeList(Enum):
    BASIC = 0
    DOUBLE = 1

def load_upgrades():
    upgrade_list : dict[Enum, tuple[list[list[pygame.Surface]], list[list[int|str|float]]]] = {}

    for enum in UpgradeList:
        #print(enum.name)
        upgrade_list[enum] = upgrades(enum.name)
        #print(upgrade_list)

    return upgrade_list

#load_upgrades()