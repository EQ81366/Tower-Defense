import pygame
from types import FunctionType
from image_loader import image_cache
from upgrade_loader import get_upgrades, get_tier_ups, render_text
from money import money_man
from mouse import mouse_info, clicked_and_released
from fonts import font_30, font_25
from constants import UpgradeType, TowerStats, BulletStats
from tower import Towers

tower_images, upgrade_images = image_cache["tower"], image_cache["upgrade"]


class Upgrade:
    def __init__(self, upgrade: UpgradeType, x: int, y: int):
        self.upgrade = upgrade

        self.x = x
        self.y = y

        self.image: pygame.Surface = upgrade_images[self.upgrade][0]

        self.rect = self.image.get_rect(center=(self.x, self.y))


class UpgradeBackground(Upgrade):
    def __init__(self, x: int, y: int):
        super().__init__(UpgradeType.UPGRADEUI, x, y)

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


class Upgrades(Upgrade):
    upgrade_info: tuple[int, list[tuple[TowerStats | BulletStats, float, FunctionType]]]
    tier_info: list[tuple[TowerStats | BulletStats, float, FunctionType]]

    def __init__(self, x: int, y: int):
        super().__init__(UpgradeType.UPGRADES, x, y)

        self.clicked = False
        self.rect_two = self.image.get_rect(center=(self.x, self.y + 80))
        self.rect_three = self.image.get_rect(center=(self.x, self.y + 160))
        self.skip_text = render_text(f"Skip for", True)

    def upgrades(self, tower: Towers, screen: pygame.Surface):
        if tower.upgrades_open:
            tower_enum = tower.tower
            tower_tier = tower.stats[TowerStats.TIER]
            upgraded_upgrades = tower.upgrades_bought[tower_tier]

            money = money_man.get_money()

            mouse_xy, mouse_down = mouse_info()

            # makes the upgrades open on the opposite side of the selected tower
            if tower.right_side:
                self.rect.centerx = self.x
                self.rect_two.centerx = self.x
                self.rect_three.centerx = self.x
            else:
                self.rect.centerx = (self.x - 640) * -1 + 640
                self.rect_two.centerx = self.rect.centerx
                self.rect_three.centerx = self.rect.centerx

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

            if tower_tier < 3:  # makes sure no issues occur with maxed towers
                fully_upgraded = upgraded_upgrades[0] and upgraded_upgrades[1]
                if fully_upgraded:
                    upgrade_one, upgrade_two = get_tier_ups(tower_enum, tower_tier, tower.upgrade_path)
                else:
                    upgrade_one, upgrade_two = get_upgrades(tower_enum, tower_tier, tower.upgrade_path)
                    cost_one = upgrade_one[0][0]
                    cost_two = upgrade_two[0][0]

                    cost_one_text = render_text(f"${cost_one}", True)
                    cost_two_text = render_text(f"${cost_two}", True)

                    offset_one_x = self.rect.right - cost_one_text.get_width() - 7
                    screen.blit(cost_one_text, (offset_one_x, self.rect.y + 6))

                    offset_two_x = self.rect_two.right - cost_two_text.get_width() - 7
                    screen.blit(cost_two_text, (offset_two_x, self.rect_two.y + 6))

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

                skip_cost = (1 + tower_tier) * 500
                if not fully_upgraded:
                    screen.blit(self.image, (self.rect.x, self.rect_three.y))
                    skip_cost_text = render_text(f"${skip_cost}", True)
                    offset_x = self.rect_three.right - skip_cost_text.get_width() - 7
                    screen.blit(skip_cost_text, (offset_x, self.rect_three.y + 6))
                    screen.blit(self.skip_text, (x, self.rect_three.y + 6))

                pressed, self.clicked = clicked_and_released(mouse_down, self.clicked)

                if pressed:
                    if self.rect_three.collidepoint(mouse_xy) and money >= skip_cost:
                        return 3

                    if fully_upgraded and type(upgrade_one_info) is list and type(upgrade_two_info) is list:
                        if self.rect.collidepoint(mouse_xy):
                            Upgrades.tier_info = upgrade_one_info
                            return 0
                        if self.rect_two.collidepoint(mouse_xy):
                            Upgrades.tier_info = upgrade_two_info
                            return 1
                    else:
                        if type(upgrade_one_info) is tuple and type(upgrade_two_info) is tuple:
                            if not upgraded_upgrades[0] and self.rect.collidepoint(mouse_xy) and money >= int(upgrade_one_info[0]):
                                Upgrades.upgrade_info = upgrade_one_info
                                return 0

                            if not upgraded_upgrades[1] and self.rect_two.collidepoint(mouse_xy) and money >= int(upgrade_two_info[0]):
                                Upgrades.upgrade_info = upgrade_two_info
                                return 1

    def buy_upgrade(self, tower: Towers, index: int):
        upgrades_bought = tower.upgrades_bought[tower.stats[TowerStats.TIER]]
        upgrade_values: list[tuple[TowerStats | BulletStats, float, FunctionType]] | None = None

        fully_upgraded = upgrades_bought[0] and upgrades_bought[1]  # variable for checking if tower's current tier is fully upgraded
        if not fully_upgraded:  # if not fully upgraded runs upgrades for basic upgrades
            upgrade_cost = Upgrades.upgrade_info[0]
            money_man.sub_money(upgrade_cost)
            upgrade_values = Upgrades.upgrade_info[1]

            tower.upgrades_bought[tower.stats[TowerStats.TIER]][index] = True  # updates upgrades_bought

        else:  # if it's fully upgraded, it'll return the type for tier-up choices
            upgrade_values = Upgrades.tier_info
            tower.stats[TowerStats.TIER] += 1
            tower.upgrade_path += [index]

        if upgrade_values:
            for upgrade in upgrade_values:
                upgrading = upgrade[0]  # the stat being upgraded
                upgrade_function = upgrade[2]  # the function used for upgrading the stat
                stat_value_mod = upgrade[1]  # the stat modifier value

                if type(upgrading) is TowerStats:
                    tower.stats[upgrading] = upgrade_function(tower.stats[upgrading], stat_value_mod)

                elif type(upgrading) is BulletStats:
                    tower.bullet_stats[upgrading] = upgrade_function(tower.bullet_stats[upgrading], stat_value_mod)

    def skip_upgrade_set(self, tower: Towers):
        tower.upgrades_bought[tower.stats[TowerStats.TIER]] = [True, True]


upgrade_manager = Upgrades(1160, 360)
upgrade_background = UpgradeBackground(1180, 360)
