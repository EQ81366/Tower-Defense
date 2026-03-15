import numpy
import pygame, math, pygame.gfxdraw
from typing import TYPE_CHECKING, Any
from image_loader import load_images, EnemyType
from constants import EnemyConstants, EnemyShape
from map_sys import show_map, map
from fonts import font_30

enemy_images = load_images(["enemy"])[0]

movement_nodes = map(show_map())[1]

screen = pygame.display.set_mode((0, 0))  # in pixels


class Enemies(pygame.sprite.Sprite):
    id = 0
    def __init__(self, *groups: Any):
        super().__init__()

        self.id = Enemies.id
        Enemies.id += 1

        self.enemy: EnemyType = groups[0]

        self.xy: pygame.Vector2 = pygame.Vector2(groups[1], groups[2])

        info = EnemyConstants[self.enemy.name.upper()].value

        self.shape = info[0][0]
        self.color = info[0][1]
        self.used_color = self.color

        self.image = enemy_images[self.enemy][0].convert_alpha()
        self.current_image = self.image

        if self.shape is not EnemyShape.COMPLEX:
            self.radius = int(self.image.get_width()/2)
        else:
            # makes a copy of the enemies image but red
            self.damage_image = self.image.copy()
            with pygame.PixelArray(self.damage_image) as pixel_array:
                pixel_array.replace(
                    self.damage_image.get_at(
                        (
                            int(self.damage_image.get_width() / 2),
                            int(self.damage_image.get_height() / 2),
                        )
                    ),
                    (255, 0, 0),
                )

        self.tier = int(info[1])
        self.speed = float(info[2])
        self.hp = int(info[3])
        self.max_hp = self.hp
        self.weight = int(info[4])  # the more weight the less it's stunned with each hit

        self.damage_frame_length = int(30 / self.weight)
        self.damage_frame = 0

        self.money_drop = round(4**self.tier)
        self.damage_at_end = 2**self.tier
        if self.damage_at_end > 1:
            self.damage_at_end /= 2

        # allows for custom money drops
        if len(info) > 5:
            self.money_drop = int(info[5])

        self.rect = self.image.get_rect(center=(self.xy))
        # sets the current destination number(refer to the map system above)
        self.current_node : int = 0
        self.amount_of_nodes = len(movement_nodes)

        self.frame = 0

    # script to make enemies go to map destinations
    def pathfind(self):
        self.damage_frame -= 1
        if self.damage_frame == 0:
            self.used_color = self.color

        if self.amount_of_nodes != self.current_node and self.damage_frame <= 0:
            #if self.damage_frame == 0:
            #    self.used_color = self.color
            # determines which destination in the destination list to go to
            destination = movement_nodes[self.current_node]
            location = self.rect.center

            distance = math.dist(destination, location)
            
            # determines if the enemy actually made it to it's destination
            if distance < self.speed:
                self.current_node += 1
                self.rect.center = destination # type: ignore
                pygame.gfxdraw.filled_circle(screen, self.rect.centerx, self.rect.centery, self.radius, self.used_color)
            else:
                #vector normalized movement
                dx = destination[0] - location[0]
                dy = destination[1] - location[1]

                movement_vector_x = dx / distance * self.speed
                movement_vector_y = dy / distance * self.speed 

                self.xy[0] += movement_vector_x
                self.xy[1] += movement_vector_y

                self.rect.centerx = int(self.xy.x)
                self.rect.centery = int(self.xy.y)

                pygame.gfxdraw.filled_circle(screen, self.rect.centerx, self.rect.centery, self.radius, self.used_color)
                #screen.blit(font_30.render(str(self.hp), True, "white"), self.rect.center)
                #screen.blit(font_30.render(str(self.id), True, "gray"), self.rect)

                return movement_vector_x, movement_vector_y

        # if enemy reaches end of map
        elif len(movement_nodes) == self.current_node:
            self.kill()
            return self.damage_at_end # returns the amount of damage to deal

        #if self.shape is EnemyShape.COMPLEX:
        #    screen.blit(self.current_image, self.rect)  # draws the enemies
        #else:

        return 0

    def damage(self, damage: float) -> list[int]:
        if self.damage_frame <= 0:
            self.hp -= damage
            self.damage_frame = self.damage_frame_length
            if self.shape is EnemyShape.COMPLEX:
                self.current_image = self.damage_image
            else:
                self.used_color = (255, 0, 0)

            if not self.hp > 0:
                self.kill()
                return [self.tier, self.money_drop]
        elif self.shape is EnemyShape.COMPLEX:
            self.current_image = self.image
        else:
            self.used_color = self.color

        return [0, 0]


if TYPE_CHECKING:
    Type = pygame.sprite.Group[Enemies]
else:
    Type = pygame.sprite.Group

# defines the enemies group
enemies: Type = pygame.sprite.Group()
