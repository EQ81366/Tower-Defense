import pygame
from typing import TYPE_CHECKING, Any
from constants import TowerConstants, ShopType, TowerStats
from image_loader import load_images
from map_sys import show_map, map
from money import money_script
from mouse import mouse_info, clicked_and_released
from tower import Towers, towers
from fonts import font_25, font_16

tower_images, shop_images = load_images(["tower", "shop"])

pygame.font.init()


class Shop(pygame.sprite.Sprite):
    shop_open = False
    tower_stats: list[pygame.Surface] = []
    placing_tower = False
    tower_being_bought: TowerConstants

    def __init__(self, *groups: Any):
        super().__init__()

        self.path = map(show_map())[0]
        self.map_offsets = map(show_map())[2]

        self.shop: ShopType | TowerConstants = groups[0]

        self.original_x: int = groups[1]
        self.original_y: int = groups[2]

        self.tower = False

        # defines generic things for non-panel shop items
        if self.shop not in ShopType:
            self.tower = True

            self.image: pygame.Surface = tower_images[TowerConstants[self.shop.name]][0]  # loads a tower base image

            info = TowerConstants[self.shop.name].constants
            tower_stats = {stat: int(info[i]) for i, stat in enumerate(TowerStats)}

            self.cost = int(info[-1])  # since cost will always be last info in constants for a tower

            self.text = font_25.render(f"{self.shop.name.capitalize()} ${self.cost}", True, "black").convert_alpha()

            self.description = [
                font_16.render(f"{self.shop.name.capitalize()}:", True, "black").convert_alpha(),
                font_16.render(f"Damage: {tower_stats[TowerStats.DAMAGE]}", True, "black").convert_alpha(),
                font_16.render(f"Cooldown: {tower_stats[TowerStats.COOLDOWN]}", True, "black").convert_alpha(),
                font_16.render(f"Range: {tower_stats[TowerStats.RANGE]}", True, "black").convert_alpha(),
                font_16.render(f"R-Speed:  {tower_stats[TowerStats.ROTATION_SPEED]}", True, "black").convert_alpha(),
            ]

            self.clicked = False
        else:
            self.image: pygame.Surface = shop_images[self.shop][0]

        self.rect = self.image.get_rect(center=(self.original_x, self.original_y))

    # checks whether the mouse is hovering over the shop panel and changes the panel accordingly
    def hovering(self, screen: pygame.Surface):
        if self.shop is ShopType.SHOPUI:
            mouse_xy = mouse_info()[0]

            if self.rect.collidepoint(mouse_xy):
                Shop.shop_open = True
                self.rect.centery = 700
            else:
                Shop.shop_open = False
                self.rect.centery = 900

            screen.blit(self.image, self.rect)

    # checks if the shop is open and if so, displays all the items in the shop
    def showing(self, screen: pygame.Surface):
        if Shop.shop_open and type(self.shop) is TowerConstants:
            money = money_script(None, 0)

            mouse_xy, mouse_down = mouse_info()

            screen.blit(self.image, self.rect)
            screen.blit(
                self.text,
                (
                    self.rect.centerx - self.text.get_width() / 2,
                    self.rect.centery + self.rect.height / 2,
                ),
            )

            # if the mouse is down when hovering over an item in the shop, it will wait until mouse not down, and attempt to buy that item
            pressed, self.clicked = clicked_and_released(mouse_down, self.clicked)
            if self.rect.collidepoint(mouse_xy):
                # hovering_on_tower used to determine whether to show tower stats
                Shop.tower_stats = self.description
                if pressed and money >= self.cost:
                    money_script(False, self.cost)
                    Shop.placing_tower = True
                    Shop.tower_being_bought = self.shop
                    return (True, self.shop)

        return False, self.shop

    # if the user bought a tower from the shop, it will follow the mouse until placed
    def place_tower(self, screen: pygame.Surface):
        if Shop.placing_tower and self.shop is Shop.tower_being_bought:
            mouse_xy, mouse_down = mouse_info()

            self.rect.centerx = mouse_xy[0]
            self.rect.centery = mouse_xy[1]
            screen.blit(self.image, self.rect)

            mask1 = pygame.mask.from_surface(self.image)
            mask2 = pygame.mask.from_surface(self.path)

            offset_x = self.map_offsets[0] - self.rect.left
            offset_y = self.map_offsets[1] - self.rect.top

            colliding = mask1.overlap(mask2, (offset_x, offset_y))
            for tower in towers:
                if self.rect.colliderect(tower.b_rect):
                    return

            # waits to place tower until mouse down and not touching track, it then waits for mouse release to place
            pressed, self.clicked = clicked_and_released(mouse_down, self.clicked)
            if pressed and not colliding:
                towers.add(Towers(self.shop, self.rect.centerx, self.rect.centery))
                self.rect.centerx = self.original_x
                self.rect.centery = self.original_y
                Shop.placing_tower = False

    def show_stats(self, screen: pygame.Surface):
        if Shop.shop_open and Shop.tower_stats != [] and self.shop is ShopType.TOWERUI:
            mouse_xy = mouse_info()[0]

            self.rect.bottomleft = mouse_xy
            screen.blit(self.image, self.rect)

            for i in range(len(Shop.tower_stats)):
                screen.blit(
                    Shop.tower_stats[i],
                    (self.rect.topleft[0] + 10, self.rect.topleft[1] + 5 + 17 * i),
                )


if TYPE_CHECKING:
    Type = pygame.sprite.Group[Shop]
else:
    Type = pygame.sprite.Group()

# defines the towers group
shop: Type = pygame.sprite.Group()
