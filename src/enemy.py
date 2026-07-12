import pygame, math, pygame.gfxdraw
from typing import TYPE_CHECKING, Any
from image_loader import load_images
from constants import EnemyConstants, EnemyShape, EnemyAbilities
from map_sys import show_map, map

# from fonts import font_30

enemy_images = load_images(["enemy"])[0]
movement_nodes = map(show_map())[1]


class Enemies(pygame.sprite.Sprite):
    id = 0
    damage_dealt = 0

    def __init__(self, *groups: Any):
        super().__init__()

        self.id = Enemies.id
        Enemies.id += 1

        enemy: EnemyConstants = groups[0]

        self.xy: list[float] = [groups[1], groups[2]]

        info = EnemyConstants[enemy.name.upper()].constants

        abilities = enemy.abilities
        self.abilities = {ability: abilities[i] for i, ability in enumerate(EnemyAbilities)}

        self.shape = info[0][0]
        self.color = info[0][1]
        self.used_color = self.color

        self.image = enemy_images[enemy][0]
        self.current_image = self.image

        self.rect = self.image.get_rect(center=(self.xy))

        if self.shape is not EnemyShape.COMPLEX:
            self.radius = int(self.image.get_width() / 2)
            del self.image
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
        self.bleed_damage = self.max_hp * 0.01
        self.weight = int(info[4])  # the more weight the less it's stunned with each hit

        self.damage_frame_length = int(30 / self.weight)
        self.damage_frame = 0

        self.bleed_timer = -1

        self.money_drop = round(4**self.tier)
        self.damage_at_end = 2**self.tier
        if self.damage_at_end > 1:
            self.damage_at_end *= 0.5

        # allows for custom money drops
        if len(info) > 5:
            self.money_drop = int(info[5])

        # sets the current destination number(refer to the map system above)
        self.current_node: int = 0

        self.dead = False

    # script to make enemies go to map destinations
    def pathfind(self, screen: pygame.Surface):
        if self.bleed_timer > 0:
            if self.bleed_timer % 60 == 0:
                self.damage(self.bleed_damage, bleeding=True)

            self.bleed_timer -= 1

        self.damage_frame -= 1
        current_node = self.current_node

        rect = self.rect

        if self.shape is EnemyShape.COMPLEX:
            screen.blit(self.current_image, rect)
        else:
            pygame.gfxdraw.filled_circle(screen, rect.centerx, rect.centery, self.radius, self.used_color)

        if len(movement_nodes) != current_node and (self.damage_frame <= 0 or self.abilities[EnemyAbilities.STUN_IMMUNITY]):
            if self.damage_frame == 0:
                if self.shape is EnemyShape.COMPLEX:
                    self.current_image = self.image
                else:
                    self.used_color = self.color

            destination = movement_nodes[current_node]  # determines which destination in the destination list to go to
            location = rect.center

            distance = math.dist(destination, location)

            speed = self.speed

            # determines if the enemy actually made it to it's destination
            if distance < speed:
                self.current_node += 1
                rect.center = destination  # type: ignore
            else:
                # vector normalized movement
                ratio = speed / distance

                movement_vector_x = (destination[0] - location[0]) * ratio
                movement_vector_y = (destination[1] - location[1]) * ratio

                self.xy[0] += movement_vector_x
                self.xy[1] += movement_vector_y

                rect.center = self.xy  # type: ignore

                # screen.blit(font_30.render(str(self.hp), True, "white"), self.rect.center) # for hp
                # screen.blit(font_30.render(str(self.id), True, "gray"), self.rect) # for id

                return (movement_vector_x, movement_vector_y), rect.centerx, rect.centery

        # if enemy reaches end of map
        elif len(movement_nodes) == current_node:
            self.kill()
            return self.damage_at_end  # returns the amount of damage to deal

        return (0, 0), rect.centerx, rect.centery

    def damage(self, damage: float, bleed: bool = False, slow: float = 0, bleeding: bool = False) -> list[int]:
        if self.damage_frame <= 0 or bleeding:
            self.hp -= damage
            Enemies.damage_dealt += damage
            self.damage_frame = self.damage_frame_length

            if self.shape is EnemyShape.COMPLEX:
                self.current_image = self.damage_image
            else:
                self.used_color = (255, 0, 0)

            if not self.hp > 0:
                # self.kill()
                return [self.tier, self.money_drop]
            else:
                if bleed:
                    self.bleed_timer = 180

                self.speed *= 1 - (slow / 100)

        return [0, 0]

    def update(self):
        if not self.hp > 0 and not self.dead:
            self.dead = True
        elif self.dead:
            self.kill()


if TYPE_CHECKING:
    Type = pygame.sprite.Group[Enemies]
else:
    Type = pygame.sprite.Group

# defines the enemies group
enemies: Type = pygame.sprite.Group()
