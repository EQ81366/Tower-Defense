from typing import Tuple
import pygame

class MouseInfo():
    @staticmethod
    def clicked_and_released(mouse_down : bool, clicked : bool):
        if mouse_down:
            clicked = True
            return False, True
        elif not mouse_down and clicked:
            return True, False
        else:
            return False, False
    
    @staticmethod
    def get_left_click() -> bool:
        return pygame.mouse.get_pressed()[0]
    @staticmethod
    def get_right_click() -> bool:
        return pygame.mouse.get_pressed()[1]

    @staticmethod
    def get_mouse_xy() -> Tuple[int, int]:
        return pygame.mouse.get_pos()

    @staticmethod
    def get_mouse_x() -> int:
        return pygame.mouse.get_pos()[0]

    @staticmethod
    def get_mouse_y() -> int:
        return pygame.mouse.get_pos()[1]