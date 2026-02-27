import pygame
from typing import TYPE_CHECKING, Any
from constants import TowerConstants
from image_loader import load_images, ShopType, TowerType
from map_sys import show_map, map
from money import money_script
from mouse import mouse_info
from tower import Towers, towers
from fonts import font_25, font_16

tower_images, shop_images = load_images(["tower", "shop"])

pygame.font.init()

screen = pygame.display.set_mode((120, 720)) # in pixels

class Shop(pygame.sprite.Sprite):
    def __init__(self, *groups : Any):
        super().__init__()

        self.path = map(show_map())[0]
        self.map_offsets = map(show_map())[2]

        self.shop : str = groups[0]

        self.original_x : int = groups[1]
        self.original_y : int = groups[2]

        # defines generic things for non-panel shop items
        if not self.shop.upper() in ShopType.__members__:
            #tower_type_number = TowerType[self.shop.upper()].value

            self.image : pygame.Surface = tower_images[TowerType[self.shop.upper()]][0] # loads a tower base image

            tower_stats = TowerConstants[self.shop.upper()].value
            self.cost = int(tower_stats[7])

            self.text = font_25.render(f'{self.shop.capitalize()} ${self.cost}', True, "black")

            self.description = [
                font_16.render(f'{self.shop.capitalize()}:', True, "black"),
                font_16.render(f'Damage: {tower_stats[3]}', True, "black"),
                font_16.render(f'Cooldown: {tower_stats[4]}', True, "black"),
                font_16.render(f'Range: {tower_stats[5]}', True, "black"),
                font_16.render(f'R-Speed:  {tower_stats[6]}', True, "black")
            ]

            self.clicked = False
        else:
            self.image : pygame.Surface = shop_images[ShopType[self.shop.upper()]][0]

            self.open = False

        self.rect = self.image.get_rect(center=(self.original_x, self.original_y))

    # checks whether the mouse is hovering over the shop panel and changes the panel accordingly
    def hovering(self):
        mouse_xy = mouse_info()[0]

        if self.rect.collidepoint(mouse_xy):
            self.open = True
            self.rect.centery = 700
        else:
            self.open = False
            self.rect.centery = 900

        screen.blit(self.image, self.rect)
        
        return self.open

    # checks if the shop is open and if so, displays all the items in the shop
    def showing(self, open : bool):
        money = money_script(None, 0)

        mouse_xy, mouse_down = mouse_info()

        hovering_on_tower = False

        if open:
            screen.blit(self.image, self.rect)
            screen.blit(self.text, (self.rect.centerx-self.text.get_width()/2, self.rect.centery+self.rect.height/2))

            # if the mouse is down when hovering over an item in the shop, it will wait until mouse not down, and attempt to buy that item
            if self.rect.collidepoint(mouse_xy):
                # hovering_on_tower used to determine whether to show tower stats
                hovering_on_tower = True
                if money >= self.cost:
                    if mouse_down and not self.clicked:
                        self.clicked = True
                    elif not mouse_down and self.clicked:
                        self.clicked = False
                        return True, hovering_on_tower, self.cost, self.description, self.shop
            else:
                hovering_on_tower = False
        
        return False, hovering_on_tower, 0, self.description, "s"
        
    # if the user bought a tower from the shop, it will follow the mouse until placed
    def place_tower(self):
        mouse_xy, mouse_down = mouse_info()

        self.rect.centerx = mouse_xy[0]
        self.rect.centery = mouse_xy[1]
        screen.blit(self.image, self.rect)

        mask1 = pygame.mask.from_surface(self.image)
        mask2 = pygame.mask.from_surface(self.path)
    
        offset_x = self.map_offsets[0] - self.rect.left
        offset_y = self.map_offsets[1] - self.rect.top

        colliding = mask1.overlap(mask2, (offset_x, offset_y))
        
        # waits to place tower until mouse down and not touching track, it then waits for mouse release to place
        if mouse_down and not colliding:
            self.clicked = True
        elif not mouse_down and self.clicked:
            self.clicked = False
            towers.add(Towers(self.shop, self.rect.centerx, self.rect.centery))
            self.rect.centerx = self.original_x
            self.rect.centery = self.original_y
            return False
        
        return True
    
    def show_stats(self, open : bool, hovering_on_tower : bool, tower_stats : list[pygame.Surface]|None):
        if open and hovering_on_tower:
            mouse_xy = mouse_info()[0]

            self.rect.bottomleft = mouse_xy
            screen.blit(self.image, self.rect)
            if tower_stats != None:
                for i in range(len(tower_stats)):
                    screen.blit(tower_stats[i], (self.rect.topleft[0]+10, self.rect.topleft[1]+5+17*i))


if TYPE_CHECKING:
    Type = pygame.sprite.Group[Shop]
else:
    Type = pygame.sprite.Group

# defines the towers group
shop : Type = pygame.sprite.Group()