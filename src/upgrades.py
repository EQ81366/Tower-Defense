import pygame
from enum import Enum

pygame.font.init()

font = pygame.font.SysFont('Arial', 16)

def render_text(input : str):
    return font.render(input, True, "black")

def upgrades(type : str):
    if type == "BASIC":
        basic : list[list[str|list[pygame.Surface]]]
        basic = [
            # first number is upgrade tier, second number determines left or right upgrade
            ["1-0", [render_text("Faster Reload:")], [render_text("shoots 20% faster")]],
            ["1-1", [render_text("Oiled Cogs:")], [render_text("turns 20% faster")]]
                ]
        return basic