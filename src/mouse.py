import pygame

def mouse_info():
    mouse_xy = pygame.mouse.get_pos()
    mouse_down = pygame.mouse.get_pressed()[0]
    return mouse_xy, mouse_down