import pygame
from enum import Enum
#from upgrades import upgrades

pygame.font.init()

font = pygame.font.SysFont('Arial', 20)

def render_text(input : str):
    return font.render(input, True, "black")

def upgrades(type : str) -> list[list[pygame.Surface]]:
    upgrades : list[list[pygame.Surface]]
    upgrades = [[]]

    if type == "BASIC":
        upgrades = [
            [render_text("Faster Reload:"), render_text("shoots 20% faster")],
            [render_text("Oiled Cogs:"), render_text("turns 20% faster")]
                ]
        
    return upgrades

class UpgradeList(Enum):
    BASIC = 0

def load_upgrades():
    upgrade_list : dict[Enum, list[list[pygame.Surface]]] = {}

    for enum in UpgradeList:
        #print(enum.name)
        upgrade_list[enum] = upgrades(enum.name)
        #print(upgrade_list)

    return upgrade_list

#load_upgrades()