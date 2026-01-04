import pygame
from constants import tower_constants
from image_loader import load_images, ShopType, TowerType
from tower import Towers, towers # type: ignore

enemy_images, tower_images, shop_images, upgrade_images = load_images() # reminder: move this someplace better


pygame.font.init()

class Shop(pygame.sprite.Sprite):
    def __init__(self, shop : str, x : int, y : int):
        super().__init__()

        from main import tower_stat_font, shop_font

        self.shop = shop

        self.original_x = x
        self.original_y = y

        # defines generic things for non-panel shop items
        if not shop.upper() in ShopType.__members__:
            tower_type_number = TowerType[shop.upper()].value

            self.image = tower_images[TowerType[shop.upper()]][0] # loads a tower base image

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
            self.image = shop_images[ShopType[shop.upper()]]
            self.open = False

        self.rect = self.image.get_rect(center=(x, y))

    # checks whether the mouse is hovering over the shop panel and changes the panel accordingly
    def hovering(self):
        from main import mouse_xy, screen

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
        from main import mouse_xy, mouse_down, money, screen

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
        from main import mouse_xy, mouse_down, screen, path, map_offsets

        self.rect.centerx = mouse_xy[0]
        self.rect.centery = mouse_xy[1]
        screen.blit(self.image, self.rect)

        mask1 = pygame.mask.from_surface(self.image)
        mask2 = pygame.mask.from_surface(path)
    
        offset_x = map_offsets[0] - self.rect.left # type: ignore
        offset_y = map_offsets[1] - self.rect.top # type: ignore

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
            from main import mouse_xy, screen

            self.rect.bottomleft = mouse_xy
            screen.blit(self.image, self.rect)
            if tower_stats != None:
                for i in range(len(tower_stats)):
                    screen.blit(tower_stats[i], (self.rect.topleft[0]+10, self.rect.topleft[1]+5+17*i))