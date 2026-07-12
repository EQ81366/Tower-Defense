import pygame, math, numpy
from typing import Any, TYPE_CHECKING
from enemy import enemies
from money import money_script
from image_loader import get_resource_path
from pathlib import Path
from constants import TowerConstants, BulletStats
from random import randint
from copy import deepcopy


# defines the Tower_Projectiles class
class Tower_Projectiles(pygame.sprite.Sprite):
    image = pygame.image.load(get_resource_path(Path("assets/b.png"))).convert_alpha()

    def __init__(self, *groups: Any):
        super().__init__()

        self.projectile: TowerConstants = groups[0]
        self.x: float = groups[1]
        self.y: float = groups[2]
        self.angle: float = groups[3]
        self.damage: float = groups[4]
        self.tower_id: int = groups[5]
        self.stats: dict[BulletStats, int | bool] = deepcopy(groups[6])
        self.is_shrapnel: bool = groups[7]

        # self.stats[BulletStats.PIERCE] = 2
        self.pierce = self.stats[BulletStats.PIERCE]

        self.enemies_killed: dict[int, int] = {i: 0 for i in range(5)}

        if self.stats[BulletStats.SIZE] != 1:
            self.image = pygame.transform.scale_by(self.image, self.stats[BulletStats.SIZE])

        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.original_rect = self.rect

        speed = self.stats[BulletStats.SPEED]
        self.dx = math.cos(math.radians(90 + self.angle)) * speed
        self.dy = math.sin(math.radians(-90 + self.angle)) * speed
        self.movement_vector = [self.dx, self.dy]
        if self.is_shrapnel:
            self.speed = speed
            self.stats[BulletStats.PIERCE] = 1
            self.stats[BulletStats.SHRAPNEL_AMOUNT] -= 1

        height = self.image.get_height()
        self.x_offset = math.cos(math.radians(90 + self.angle)) * height / 2
        self.y_offset = math.sin(math.radians(90 + self.angle)) * height / 2

        start = pygame.math.Vector2(self.original_rect.width / 2, self.original_rect.height / 2)
        end = pygame.math.Vector2(self.original_rect.width / 2, self.original_rect.height * 1.5)
        self.offset = (start - end).rotate(-self.angle)

        self.r_image = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.r_image.get_rect(center=(self.x, self.y))

    # this moves the bullet
    def move(self, enemy_xy: numpy.ndarray, enemy_movement_vector: numpy.ndarray, enemy_alive: numpy.ndarray, screen: pygame.Surface):
        if self.alive():
            if self.stats[BulletStats.GROWTH]:
                self.image = pygame.transform.scale_by(self.image, 1.2)
                self.rect = self.image.get_rect(center=(self.x, self.y))
                self.original_rect = self.rect

                height = self.image.get_height()
                self.x_offset = math.cos(math.radians(90 + self.angle)) * height / 2
                self.y_offset = math.sin(math.radians(90 + self.angle)) * height / 2

                start = pygame.math.Vector2(self.original_rect.width / 2, self.original_rect.height / 2)
                end = pygame.math.Vector2(self.original_rect.width / 2, self.original_rect.height * 1.5)
                self.offset = (start - end).rotate(-self.angle)

                self.r_image = pygame.transform.rotate(self.image, self.angle)
                self.rect = self.r_image.get_rect(center=(self.x, self.y))

                self.damage *= 1.1

            x = self.x
            y = self.y

            self.rect.centerx = int(x)
            self.rect.centery = int(y)

            self.x += self.dx
            self.y += self.dy

            if abs(x) > 1500 or abs(y) > 1500 or self.pierce <= 0:
                self.kill()
            else:
                screen.blit(self.r_image, (self.rect.x + self.x_offset, self.rect.y - self.y_offset))

                tip = pygame.math.Vector2(x, y) + self.offset

                distance: numpy.ndarray = numpy.sum((enemy_xy - tip) ** 2, axis=1)

                pygame.draw.rect(screen, "red", pygame.Rect(tip.x, tip.y, 10, 10))

                # + self.stats[BulletStats.SPEED]**2
                # numpy.where()
                if (distance <= (35**2 + self.stats[BulletStats.SPEED] ** 2)).any() or self.stats[BulletStats.SPEED] > 1000:
                    relative_position = enemy_xy - tip

                    relative_velocity = self.movement_vector - enemy_movement_vector
                    a = numpy.sum(relative_velocity**2, axis=1)
                    b = 2 * numpy.sum(relative_position * relative_velocity, axis=1)

                    c = numpy.sum(relative_position**2, axis=1) - 35**2

                    d = (b**2) - 4 * a * c

                    sqrt_d = numpy.sqrt(numpy.maximum(d, 0))
                    t = numpy.array((-b - sqrt_d) / (2 * a))  # time after impact(negative numbers mean time to impact)

                    if self.stats[BulletStats.SPEED] > 1000:
                        hit_list = (d >= 0) & (t <= 0.0) & enemy_alive
                    else:
                        hit_list = (d >= 0) & (t <= 0.2) & (t >= -1.2) & enemy_alive
                    hit_indices = numpy.where(hit_list)[0]

                    # print(hit_indices)
                    for indice in hit_indices:
                        indice: int

                        enemy_group = enemies.sprites()

                        # print(t[indice])

                        if enemy_group[indice].id == indice:
                            enemy_death_info = enemy_group[indice].damage(
                                self.damage, bool(self.stats[BulletStats.BLEEDING]), self.stats[BulletStats.SLOWING]
                            )
                            if self.stats[BulletStats.KNOCKBACK] > 0:
                                enemy_group[indice].xy[0] += self.dx * (self.stats[BulletStats.KNOCKBACK] * 0.01)
                                enemy_group[indice].xy[1] += self.dy * (self.stats[BulletStats.KNOCKBACK] * 0.01)
                                enemy_group[indice].rect.center = enemy_group[indice].xy  # type: ignore

                            self.pierce -= 1

                            if enemy_death_info != [0, 0]:
                                self.enemies_killed[enemy_death_info[0]] += 1
                                money_script(True, enemy_death_info[1])
                                enemy_alive[indice] = False

                            if self.pierce <= 0:
                                if (not self.is_shrapnel or self.stats[BulletStats.SHRAPNEL_CHAINING]) and self.stats[BulletStats.SHRAPNEL]:
                                    for i in range(self.stats[BulletStats.SHRAPNEL_AMOUNT]):  # type: ignore
                                        tower_projectiles.add(
                                            Tower_Projectiles(
                                                self.projectile,
                                                self.x,
                                                self.y,
                                                self.angle + (randint(-40, 40)),  # shrapnel uses its own spread value
                                                self.damage * self.stats[BulletStats.SHRAPNEL_DAMAGE],
                                                self.tower_id,
                                                self.stats,
                                                True,
                                            )
                                        )

                                self.kill()
                                return self.tower_id, self.enemies_killed

            if self.is_shrapnel:
                self.stats[BulletStats.SHRAPNEL_DISTANCE] -= self.speed
                if self.stats[BulletStats.SHRAPNEL_DISTANCE] <= 0:
                    self.kill()

        return None


if TYPE_CHECKING:
    Type = pygame.sprite.Group[Tower_Projectiles]
else:
    Type = pygame.sprite.Group

tower_projectiles: Type = pygame.sprite.Group()
