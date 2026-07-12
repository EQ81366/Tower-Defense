import numpy
import pygame, math
from random import randint
from typing import Any, TYPE_CHECKING
from constants import TowerConstants, TargetingStates, TowerStats, BulletStats
from image_loader import load_images, get_resource_path
from tower_aiming import point_enemy
from mouse import mouse_info, clicked_and_released
from enemy import enemies
from tower_projectiles import Tower_Projectiles, tower_projectiles
from pathlib import Path
from scipy.spatial.distance import cdist

tower_images = load_images(["tower"])[0]


class Towers(pygame.sprite.Sprite):
    id = 0
    range_circle = pygame.image.load(get_resource_path(Path("assets/circle.png"))).convert_alpha()

    def __init__(self, *groups: Any):
        super().__init__()

        self.id = Towers.id
        Towers.id += 1

        self.tower: TowerConstants = groups[0]
        self.x: int = groups[1]
        self.y: int = groups[2]

        info = self.tower.constants

        self.stats = {stat: int(info[i]) for i, stat in enumerate(TowerStats)}

        bullet_info = self.tower.bullet_info

        self.bullet_stats = {stat: bullet_info[i] for i, stat in enumerate(BulletStats)}

        self.recoil_time = 5

        self.wait = self.stats[TowerStats.COOLDOWN]

        self.shots_left = self.stats[TowerStats.BULLET_CAPACITY]
        self.current_angle = 0
        self.dr: float = 0

        self.upgrades_bought = {i: [False, False] for i in range(4)}
        self.upgrade_path = [0]

        self.enemies_killed: dict[int, int] = {i: 0 for i in range(5)}

        tower_image_bundle = tower_images[self.tower]
        self.b_image = tower_image_bundle[0]
        self.image = tower_image_bundle[1]
        self.f_image = tower_image_bundle[2]
        if self.stats[TowerStats.TURRETS] > 1:
            self.f2_image = tower_image_bundle[3]

        self.height = self.image.get_height()
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.b_rect = self.b_image.get_rect(center=(self.x, self.y))

        self.firing = False
        self.clicked = False
        self.upgrades_open = False

        # this is for upgrade side
        if self.x > 640:
            self.right_side = False
        else:
            self.right_side = True

        self.targeting_mode = TargetingStates.LAST  # targeting mode(default is rotationally efficient)

    # defines the rotation and firing animation of the tower
    def rotate(self, screen: pygame.Surface):
        if self.firing:
            f_image = self.f_image
            if self.stats[TowerStats.TURRETS] == 2:
                if self.shots_left % 2 == 0:
                    f_image = self.f2_image

            current_image = f_image
            self.recoil_time -= 1
        else:
            current_image = self.image

        if self.recoil_time <= 0:
            self.firing = False
            self.recoil_time = 5

        r_image = pygame.transform.rotate(current_image, self.current_angle)
        self.rect = r_image.get_rect(center=(self.x, self.y))

        dx = math.cos(math.radians(90 + self.current_angle)) * self.height / 2
        dy = math.sin(math.radians(90 + self.current_angle)) * self.height / 2

        screen.blit(self.b_image, self.b_rect)
        screen.blit(r_image, (self.rect.x + dx, self.rect.y - dy))

    # creates a bullet
    def shoot(self):
        spread = self.bullet_stats[BulletStats.BULLET_SPREAD]
        for i in range(self.bullet_stats[BulletStats.BULLET_AMOUNT]):  # type: ignore
            tower_projectiles.add(
                Tower_Projectiles(
                    self.tower,
                    self.rect.centerx,
                    self.rect.centery,
                    self.current_angle + randint(int(spread * -1), int(spread)),
                    self.stats[TowerStats.DAMAGE],
                    self.id,
                    self.bullet_stats,
                    False,
                )
            )

    # finds the closest enemy
    def find_closest_enemy(self, enemy_xy: numpy.ndarray):
        if len(enemies) > 0:
            closest_id = -1

            xy = self.rect.center

            targeting_mode = self.targeting_mode

            distance = cdist(enemy_xy, [xy], "euclidean")
            valid = distance <= self.stats[TowerStats.RANGE]

            if len(numpy.where(valid)[0]) < 1:
                return

            # targets the most "efficient" enemy; whichever enemy is fastest to shoot
            if targeting_mode is TargetingStates.EFFICIENT:
                dr = numpy.array(
                    [
                        point_enemy(
                            xy[0],
                            xy[1],
                            sprite.rect.centerx,
                            sprite.rect.centery,
                        )
                        % 360
                        for sprite in enemies
                    ]
                )
                dr = abs(dr - self.current_angle)

                closest_id = int(valid[numpy.argmin(dr[valid])])

            # targets closest enemy
            elif targeting_mode is TargetingStates.CLOSE:
                closest_id = numpy.argmin(distance)

            # targets the furthest most enemy in range
            elif targeting_mode is TargetingStates.FIRST:
                closest_id = numpy.min(numpy.where(valid)[0])

            # targets the furthest back enemy in range
            elif targeting_mode is TargetingStates.LAST:
                closest_id = numpy.max(numpy.where(valid)[0])

            # targets the enemy with the most hp
            elif targeting_mode is TargetingStates.STRONG:
                e_hp = 0
                highest_e_hp = 0
                for i, sprite in enumerate(enemies):
                    e_hp = sprite.max_hp

                    if e_hp > highest_e_hp and i in valid:
                        highest_e_hp = e_hp
                        closest_id = i

            # makes sure there are enemies within tower range
            if closest_id != -1:
                current_enemy_xy = enemy_xy[closest_id]
                # finds the angle to targeted enemy
                rotation_angle = point_enemy(xy[0], xy[1], current_enemy_xy[0], current_enemy_xy[1])

                # calculate the difference and wrap it to [-180, 180]
                self.dr = (rotation_angle - self.current_angle) % 360
                if self.dr > 180:
                    self.dr -= 360

                if abs(self.dr) > 1:
                    self.current_angle += self.stats[TowerStats.ROTATION_SPEED] / 60 * (self.dr / abs(self.dr))
                    if abs(self.dr) <= 2 * (
                        self.stats[TowerStats.ROTATION_SPEED] / 100
                    ):  # based on rotation speed, if delta rotation is low enough it sets current to wanted rotation
                        self.current_angle = rotation_angle

                # checks if firing cooldown is over and that the tower is rotated within 1 degree(s) of the enemy
                if abs(int(self.dr)) < 1:
                    if self.wait >= int(self.stats[TowerStats.COOLDOWN]):
                        if self.shots_left <= 0:
                            self.shots_left = self.stats[TowerStats.BULLET_CAPACITY]  # resets ammo
                            self.wait = 0
                        else:
                            self.wait = int(
                                self.stats[TowerStats.COOLDOWN] * 0.9
                            )  # if shots left is greater than 0, wait time is drastically reduced
                            self.shoot_target(True)

    def shoot_target(self, shoot: bool):
        if shoot and self.shots_left > 0:
            self.shoot()
            self.firing = True
            self.shots_left -= 1

    def open_upgrades(self, upgrade_rect: pygame.Rect):
        mouse_xy, mouse_down = mouse_info()
        pressed, self.clicked = clicked_and_released(mouse_down, self.clicked)

        if self.rect.collidepoint(mouse_xy) and pressed:
            self.upgrades_open = not self.upgrades_open
        elif not upgrade_rect.collidepoint(mouse_xy) and pressed:
            self.upgrades_open = False

        return self.upgrades_open

    def show_range(self, screen: pygame.Surface):
        if self.upgrades_open:
            range = self.stats[TowerStats.RANGE]
            range_circle_scaled = pygame.transform.scale(self.range_circle, (range * 2, range * 2))
            screen.blit(range_circle_scaled, (self.x - range_circle_scaled.get_width() / 2, self.y - range_circle_scaled.get_height() / 2))


if TYPE_CHECKING:
    Type = pygame.sprite.Group[Towers]
else:
    Type = pygame.sprite.Group

# defines the towers group
towers: Type = pygame.sprite.Group()
