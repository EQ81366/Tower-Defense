import pygame
from typing import TYPE_CHECKING, Any
from image_loader import load_images, UpgradeType, TowerType
from upgrade_loader import load_upgrades
from money import money_script
from mouse import mouse_info
from fonts import font_30, font_25

tower_images, upgrade_images = load_images(["tower", "upgrade"])

upgrade_text = load_upgrades()

screen = pygame.display.set_mode((0, 0)) # in pixels

class Upgrades(pygame.sprite.Sprite):
    def __init__(self, *groups : Any):
        super().__init__()

        self.upgrade : UpgradeType = groups[0]

        self.x : int = groups[1]
        self.y : int = groups[2]

        self.clicked = False
        
        self.image : pygame.Surface = upgrade_images[self.upgrade][0]

        self.rect = self.image.get_rect(center=(self.x, self.y))      

    def hovering(self, open : bool, right_side : bool):
        if open:
            # makes the upgrades open on the opposite side of the selected tower
            if right_side:
                self.rect.centerx = self.x
            else:
                self.rect.centerx = (self.x-640)*-1+640

            self.open = True
            screen.blit(self.image, self.rect)
        else:
            self.open = False
        
        #return self.open
    
    def upgrades(self, open : bool, tower : TowerType, tower_tier : int, right_side : bool, upgraded : list[bool]) -> list[int|str|float]:
        upgrade_info_placeholder : list[int|str|float] = [0, "", 0.0]
        if open:
            money = money_script(None, 0)
            
            mouse_xy, mouse_down = mouse_info()

            # makes the upgrades open on the opposite side of the selected tower
            if right_side:
                self.rect.centerx = self.x
            else:
                self.rect.centerx = (self.x-640)*-1+640
            
            # shows the tower selected in upgrade menu
            images = tower_images[tower]
            screen.blit(images[0], (self.rect.x-(images[0].get_width()-self.rect.width)/2, 80))
            screen.blit(images[1], (self.rect.x-(images[1].get_width()-self.rect.width)/2, 80-images[1].get_height()/2))

            # shows the selected tower's name and tier
            text = font_30.render(tower.name.capitalize(), True, "black")
            screen.blit(text, (self.rect.x-(text.get_width()-self.rect.width)/2, 160))
            text = font_25.render(f'Tier: {tower_tier}', True, "black")
            screen.blit(text, (self.rect.x-(text.get_width()-self.rect.width)/2, 193))

            tower_tier += 1 # for upgrade info

            # shows upgrades
            screen.blit(self.image, (self.rect.x, self.rect.y))
            screen.blit(self.image, (self.rect.x, self.rect.y+80))

            text_info, upgrade_info = upgrade_text[tower] # gets the upgrade info for the tower currently selected

            for i in range(len(text_info[tower_tier*2-2])):
                screen.blit(text_info[tower_tier*2-2][i], (self.rect.x+7, self.rect.y+8+25*i))
                
            for i in range(len(text_info[tower_tier*2-1])):            
                screen.blit(text_info[tower_tier*2-1][i], (self.rect.x+7, self.rect.y+88+25*i))

            if self.rect.collidepoint(mouse_xy) and mouse_down and money >= int(upgrade_info[tower_tier*2-2][0]) and not upgraded[0]:
                self.clicked = True
            elif self.rect.collidepoint(mouse_xy) and not mouse_down and self.clicked:
                self.clicked = False
                return upgrade_info[tower_tier*2-2]
            
            if pygame.Rect(self.rect.x, self.rect.y+80, self.rect.width, self.rect.height).collidepoint(mouse_xy) and mouse_down and money >= int(upgrade_info[tower_tier*2-1][0]) and not upgraded[1]:
                self.clicked = True
            elif pygame.Rect(self.rect.x, self.rect.y+80, self.rect.width, self.rect.height).collidepoint(mouse_xy) and not mouse_down and self.clicked:
                self.clicked = False
                return upgrade_info[tower_tier*2-1]
    
        return upgrade_info_placeholder
    

if TYPE_CHECKING:
    Type = pygame.sprite.Group[Upgrades]
else:
    Type = pygame.sprite.Group

# defines the towers group
upgrades : Type = pygame.sprite.Group()