import pygame

def mouse_info():
    mouse_xy = pygame.mouse.get_pos()
    mouse_down = pygame.mouse.get_pressed()[0]
    return mouse_xy, mouse_down

def clicked_and_released(mouse_down : bool, clicked : bool):
    if mouse_down:
        clicked = True
        return False, True
    elif not mouse_down and clicked:
        return True, False
    
    return False, False