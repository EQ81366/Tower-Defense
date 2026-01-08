import pygame
from constants import tower_constants
from image_loader import load_images, ShopType, TowerType
from map_sys import show_map, map
from money import money_script
from mouse import mouse_info
from tower import Towers, towers # type: ignore

tower_images, shop_images = load_images(False, True, True, False) # reminder: move this someplace better

pygame.font.init()

screen = pygame.display.set_mode((120, 720)) # in pixels

# fonts
tower_stat_font = pygame.font.SysFont('Arial', 16)
shop_font = pygame.font.SysFont('Arial', 25)

# defines the shop group
shop = pygame.sprite.Group() # type: ignore


class Shop(pygame.sprite.Sprite):
    def __init__(self, shop : str, x : int, y : int):
        super().__init__()

        self.path = map(show_map())[0]
        self.map_offsets = map(show_map())[2]

        self.shop = shop

        self.original_x = x
        self.original_y = y

        # defines generic things for non-panel shop items
        if not shop.upper() in ShopType.__members__:
            tower_type_number = TowerType[shop.upper()].value

            placeholder = tower_images[TowerType[shop.upper()]]
            if isinstance(placeholder, list):
                self.image : pygame.Surface = placeholder[0] # loads a tower base image

            tower_stats = tower_constants()[tower_type_number]
            self.cost = int(tower_stats[7])

            self.text = shop_font.render(f'{shop.capitalize()} ${self.cost}', True, "black")

            self.description = [
                tower_stat_font.render(f'{self.shop.capitalize()}:', True, "black"),
                tower_stat_font.render(f'Damage: {tower_stats[3]}', True, "black"),
                tower_stat_font.render(f'Cooldown: {tower_stats[4]}', True, "black"),
                tower_stat_font.render(f'Range: {tower_stats[5]}', True, "black"),
                tower_stat_font.render(f'R-Speed:  {tower_stats[6]}', True, "black")
            ]

            self.clicked = False
        else:
            placeholder = shop_images[ShopType[shop.upper()]]
            if isinstance(placeholder, pygame.Surface):
                self.image : pygame.Surface = placeholder

            self.open = False

        self.rect = self.image.get_rect(center=(x, y))

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
        
        if hovering_on_tower:
            return False, hovering_on_tower, 0, self.description
        else:
            return False, hovering_on_tower, 0
        
    # if the user bought a tower from the shop, it will follow the mouse until placed
    def place_tower(self):
        mouse_xy, mouse_down = mouse_info()

        self.rect.centerx = mouse_xy[0]
        self.rect.centery = mouse_xy[1]
        screen.blit(self.image, self.rect)

        mask1 = pygame.mask.from_surface(self.image)
        mask2 = pygame.mask.from_surface(self.path)
    
        offset_x = self.map_offsets[0] - self.rect.left # type: ignore
        offset_y = self.map_offsets[1] - self.rect.top # type: ignore

        colliding = mask1.overlap(mask2, (offset_x, offset_y))
        
        # waits to place tower until mouse down and not touching track, it then waits for mouse release to place
        if mouse_down and not colliding:
            self.clicked = True
        elif not mouse_down and self.clicked:
            self.clicked = False
            towers.add(Towers(self.shop, self.rect.centerx, self.rect.centery)) # type: ignore
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