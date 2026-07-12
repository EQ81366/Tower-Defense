import pygame
from typing import TYPE_CHECKING, Any
from image_loader import load_images
from upgrade_loader import get_upgrades, get_tier_ups
from money import money_script
from mouse import mouse_info, clicked_and_released
from fonts import font_30, font_25
from constants import UpgradeType, TowerStats
from tower import towers

tower_images, upgrade_images = load_images(["tower", "upgrade"])


class Upgrades(pygame.sprite.Sprite):
    def __init__(self, *groups: Any):
        super().__init__()

        self.upgrade: UpgradeType = groups[0]

        self.x: int = groups[1]
        self.y: int = groups[2]

        self.clicked = False

        self.image: pygame.Surface = upgrade_images[self.upgrade][0].convert_alpha()

        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.rect_two = self.image.get_rect(center=(self.x, self.y + 80))

    def hovering(self, open: bool, right_side: bool, screen: pygame.Surface):
        if open:
            # makes the upgrades open on the opposite side of the selected tower
            if right_side:
                self.rect.centerx = self.x
            else:
                self.rect.centerx = (self.x - 640) * -1 + 640

            self.open = True
            screen.blit(self.image, self.rect)
        else:
            self.open = False

        # return self.open

    def upgrades(self, tower_number: int, screen: pygame.Surface):
        tower = towers.sprites()[tower_number]
        tower_enum = tower.tower
        tower_tier = tower.stats[TowerStats.TIER]
        upgraded_upgrades = tower.upgrades_bought[tower_tier]

        money = money_script(None, 0)

        mouse_xy, mouse_down = mouse_info()

        # makes the upgrades open on the opposite side of the selected tower
        if tower.right_side:
            self.rect.centerx = self.x
            self.rect_two.centerx = self.x
        else:
            self.rect.centerx = (self.x - 640) * -1 + 640
            self.rect_two.centerx = (self.x - 640) * -1 + 640

        # shows the tower selected in upgrade menu
        images = tower_images[tower_enum]
        screen.blit(
            images[0],
            (self.rect.x - (images[0].get_width() - self.rect.width) / 2, 80),
        )
        screen.blit(
            images[1],
            (
                self.rect.x - (images[1].get_width() - self.rect.width) / 2,
                80 - images[1].get_height() / 2,
            ),
        )

        # shows the selected tower's name and tier
        text = font_30.render(tower_enum.name.capitalize(), True, "black")
        screen.blit(text, (self.rect.x - (text.get_width() - self.rect.width) / 2, 160))
        text = font_25.render(f"Tier: {tower_tier}", True, "black")
        screen.blit(text, (self.rect.x - (text.get_width() - self.rect.width) / 2, 193))

        # shows upgrade tiles
        screen.blit(self.image, (self.rect.x, self.rect.y))
        screen.blit(self.image, (self.rect.x, self.rect_two.y))

        if tower_tier < 3:  # makes sure no issues occur with towers you cannot buy upgrades for anymore
            fully_upgraded = upgraded_upgrades[0] and upgraded_upgrades[1]
            if fully_upgraded:
                upgrade_one, upgrade_two = get_tier_ups(tower_enum, tower_tier, tower.upgrade_path)
            else:
                upgrade_one, upgrade_two = get_upgrades(
                    tower_enum, tower_tier, tower.upgrade_path
                )  # gets the upgrade info for the tower currently selected

            upgrade_one_info, *upgrade_one_text = upgrade_one
            upgrade_two_info, *upgrade_two_text = upgrade_two

            x = self.rect.x + 7
            for i, text in enumerate(upgrade_one_text):
                if i == 1:
                    y = self.rect.y + 6 + 20 * i
                else:
                    y = self.rect.y + 6 + 18 * i
                screen.blit(
                    text,
                    (x, y),
                )

            for i, text in enumerate(upgrade_two_text):
                if i == 1:
                    y = self.rect_two.y + 6 + 20 * i
                else:
                    y = self.rect_two.y + 6 + 18 * i
                screen.blit(
                    text,
                    (x, y),
                )

            pressed, self.clicked = clicked_and_released(mouse_down, self.clicked)

            if pressed:
                if fully_upgraded:
                    if self.rect.collidepoint(mouse_xy):
                        return upgrade_one_info, 0
                    if self.rect_two.collidepoint(mouse_xy):
                        return upgrade_two_info, 1
                else:
                    if isinstance(upgrade_one_info[0], int) and isinstance(upgrade_two_info[0], int):
                        if not upgraded_upgrades[0] and self.rect.collidepoint(mouse_xy) and money >= int(upgrade_one_info[0]):
                            return upgrade_one_info, 0

                        if not upgraded_upgrades[1] and self.rect_two.collidepoint(mouse_xy) and money >= int(upgrade_two_info[0]):
                            return upgrade_two_info, 1


if TYPE_CHECKING:
    Type = pygame.sprite.Group[Upgrades]
else:
    Type = pygame.sprite.Group

# defines the towers group
upgrades: Type = pygame.sprite.Group()
