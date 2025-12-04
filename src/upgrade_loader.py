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
            [render_text("Oiled Cogs:"), render_text("turns 20% faster")]
        ]
        # MAKE SURE NAME OF TOWER ATTRIBUTE MATCHES EXACTLY TO TOWER VARIABLE NAMES
        upgrade_info = [
            [150, "cd", 0.8, 1.1],
            [100, "r_speed", 1.2, 1.2]
        ]

    return upgrade_images, upgrade_info

class UpgradeList(Enum):
    BASIC = 0

def load_upgrades():
    upgrade_list : dict[Enum, tuple[list[list[pygame.Surface]], list[list[int|str|float]]]] = {}

    for enum in UpgradeList:
        #print(enum.name)
        upgrade_list[enum] = upgrades(enum.name)
        #print(upgrade_list)

    return upgrade_list

#load_upgrades()