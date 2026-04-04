import pygame, math, numpy
from typing import Any, TYPE_CHECKING
from enemy import enemies
from money import money_script
from image_loader import get_resource_path
from pathlib import Path
from constants import TowerConstants

screen = pygame.display.set_mode((0, 0))  # in pixels


# defines the Tower_Projectiles class
class Tower_Projectiles(pygame.sprite.Sprite):
    image = pygame.image.load(get_resource_path(Path("assets/b.png"))).convert_alpha()

    def __init__(self, *groups: Any):
        super().__init__()

        self.tower_id = groups[5]

        self.projectile: TowerConstants = groups[0]

        self.x = groups[1]
        self.y = groups[2]

        self.angle = groups[3]

        self.damage = groups[4]

        # checks which projectile was spawned
        if self.projectile is TowerConstants.BASIC:
            self.speed = 100
            self.pierce = 99999  # pierce = hp
        elif self.projectile is TowerConstants.DOUBLE:
            self.speed = 200
            self.pierce = 2

        if self.speed > 10000:
            self.speed = 10000
        elif self.speed < 0:
            self.speed = 1

        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.original_rect = self.rect

        self.height = self.image.get_height()

        self.dx = math.cos(math.radians(90 + self.angle)) * self.speed
        self.dy = math.sin(math.radians(-90 + self.angle)) * self.speed
        self.movement_vector = [self.dx, self.dy]

        self.x_offset = math.cos(math.radians(90 + self.angle)) * self.height / 2
        self.y_offset = math.sin(math.radians(90 + self.angle)) * self.height / 2

        start = pygame.math.Vector2(self.original_rect.width / 2, self.original_rect.height / 2)
        end = pygame.math.Vector2(self.original_rect.width / 2, self.original_rect.height * 1.5)
        self.offset = (start - end).rotate(-self.angle)

        self.r_image = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.r_image.get_rect(center=(self.x, self.y))

    # this moves the bullet
    def move(self, enemy_x : numpy.ndarray, enemy_y : numpy.ndarray, enemy_movement_vector : numpy.ndarray):
        if self.alive():
            self.x += self.dx
            self.y += self.dy

            self.rect.centerx = int(self.x)
            self.rect.centery = int(self.y)

            if abs(self.x) > 1500 or abs(self.y) > 1500:
                self.kill()
            else:
                screen.blit(self.r_image, (self.rect.x + self.x_offset, self.rect.y - self.y_offset))

                total_enemies = len(enemies)

                tip = pygame.math.Vector2(self.x, self.y) + self.offset

                distance = ((enemy_x - tip.x)**2 + (enemy_y - tip.y)**2)[:total_enemies]

                if (distance <= 30**2 + self.speed**2).any():
                    relative_x = numpy.subtract(enemy_x, tip.x)[:total_enemies]
                    relative_y = numpy.subtract(enemy_y, tip.y)[:total_enemies]
                    relative_position = numpy.column_stack((relative_x, relative_y))

                    relative_velocity = self.movement_vector - enemy_movement_vector[:total_enemies]
                    a = numpy.sum(relative_velocity**2, axis=1)
                    b = 2 * numpy.sum(relative_position * relative_velocity, axis=1)

                    #radius = numpy.array([sprite.rect.width / 2 for sprite in enemies])
                    c = numpy.sum(relative_position**2, axis=1) - 30**2

                    d = (b**2) - 4 * a * c

                    sqrt_d = numpy.sqrt(numpy.maximum(d, 0))
                    t = numpy.array((-b - sqrt_d) / (2 * a))

                    hit_list = (d >= 0) & (t >= 0)
                    hit_indices = numpy.where(hit_list)[0]

                    enemy_group = enemies.sprites()
                    
                    for indice in hit_indices:
                        indice : int
                        enemy_death_info = [0, 0]

                        enemy_death_info = enemy_group[indice].damage(self.damage)
                        self.pierce -= 1

                        if enemy_death_info != [0, 0]:
                            money_script(True, enemy_death_info[1])

                        if self.pierce <= 0:
                            self.kill()
                            break
                        
                        return enemy_death_info, self.tower_id

        return [0, 0], self.tower_id


if TYPE_CHECKING:
    Type = pygame.sprite.Group[Tower_Projectiles]
else:
    Type = pygame.sprite.Group

tower_projectiles: Type = pygame.sprite.Group()
