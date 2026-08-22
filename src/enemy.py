import pygame, math, pygame.gfxdraw, numpy
from numpy import zeros, int8, sum
from typing import TYPE_CHECKING, Any
from image_loader import image_cache
from constants import EnemyConstants, EnemyShape, EnemyAbilities
from map.map_sys import map_system
from fonts import font_30

enemy_images = image_cache["enemy"]

movement_nodes: list[tuple[int, int]] = map_system.get_nodes()

points = map_system.get_all_nodes()

enemy_cap = 10000
enemy_xy = zeros((enemy_cap, 2), dtype=float)
enemy_movement_vector = zeros((enemy_cap, 2), dtype=float)
enemy_progress = zeros(enemy_cap, float)
enemy_alive = zeros(enemy_cap, dtype=bool)
enemy_alive.fill(False)
enemy_camo = zeros(enemy_cap, dtype=int8)
slots_available = list(range(enemy_cap))
enemy_mhp = zeros(enemy_cap, dtype=int8)


class Enemies(pygame.sprite.Sprite):
    # id = 0
    damage_dealt = 0
    c_frame_dmg = 0.0
    enemies_killed = 0

    def __init__(self, *groups: Any):
        super().__init__()

        if not slots_available:
            self.kill()
            return

        self.id = slots_available.pop()

        enemy: EnemyConstants = groups[0]

        self.current_node: int = 0
        enemy_xy[self.id] = movement_nodes[self.current_node]
        enemy_objects[self.id] = self

        info = EnemyConstants[enemy.name.upper()].constants

        abilities = enemy.abilities
        self.abilities = {ability: abilities[i] for i, ability in enumerate(EnemyAbilities)}

        self.shape = info[0][0]
        self.color = info[0][1]
        self.used_color = self.color

        self.image = enemy_images[enemy][0]
        self.current_image = self.image

        self.rect = self.image.get_rect(center=(movement_nodes[self.current_node]))

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
        self.realtime_speed = self.speed
        self.hp = int(info[3])
        self.max_hp = self.hp
        self.bleed_damage = self.max_hp * 0.01
        self.weight = int(info[4])  # the more weight the less it's stunned with each hit

        self.damage_frame_length = int(30 / self.weight)
        self.damage_frame = 0

        self.bleed_timer = -1

        self.money_drop = round(4**self.tier)
        self.damage_at_end: float = 2**self.tier
        if self.damage_at_end > 1:
            self.damage_at_end *= 0.5

        # allows for custom money drops
        if len(info) > 5:
            self.money_drop = int(info[5])

        # sets the current destination number(refer to the map system above)
        self.current_node += 1

        self.dead = False

        self.point = 0

        map_system.set_enemy_pos(int(self.point), self.id)

        self.update_movement_vector()
        self.update_mhp_list()

    def update_movement_vector(self):
        destination = movement_nodes[self.current_node]
        location = enemy_xy[self.id]
        distance = math.dist(destination, location)

        ratio = self.realtime_speed / distance

        movement_vector_x = (destination[0] - location[0]) * ratio
        movement_vector_y = (destination[1] - location[1]) * ratio

        enemy_movement_vector[self.id] = (movement_vector_x, movement_vector_y)

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
                self.realtime_speed = self.speed
                self.update_movement_vector()
                if self.shape is EnemyShape.COMPLEX:
                    self.current_image = self.image
                else:
                    self.used_color = self.color

            point = self.point
            dbpoints = map_system.get_d_b_points()
            self.point = enemy_progress[self.id] // (dbpoints)
            if point != self.point:
                map_system.remove_enemy_pos(int(point), self.id)
                map_system.set_enemy_pos(int(self.point), self.id)

            destination = movement_nodes[current_node]  # determines which destination in the destination list to go to
            location = rect.center

            distance = math.dist(destination, location)

            speed = self.realtime_speed

            # determines if the enemy actually made it to it's destination
            if distance < speed:
                self.current_node += 1
                current_node = self.current_node
                if current_node < len(movement_nodes):
                    enemy_xy[self.id] = destination
                    destination = movement_nodes[current_node]
                    distance = math.dist(destination, enemy_xy[self.id])
                    self.update_movement_vector()
            else:
                rect.center = enemy_xy[self.id]
                # screen.blit(font_30.render(str(self.hp), True, "white"), self.rect.center)  # for hp
                # screen.blit(font_30.render(str(self.id), True, "gray"), self.rect)  # for id

        # if enemy reaches end of map
        elif len(movement_nodes) == current_node:
            self.kill()
            Enemies.c_frame_dmg += self.damage_at_end

        else:
            self.realtime_speed = 0
            self.update_movement_vector()

    def damage(
        self,
        damage: float,
        bleed: bool = False,
        slow: float = 0,
        bleeding: bool = False,
    ) -> list[int]:
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

                self.speed *= 1 - (slow * 0.01)
                # self.realtime_speed = self.speed

            self.update_mhp_list()

        return [0, 0]

    def knockback(self, knockback: float):
        enemy_xy[self.id] -= knockback

    def update(self, screen: pygame.Surface):
        enemy_alive[self.id] = True
        enemy_camo[self.id] = self.abilities[EnemyAbilities.CAMOUFLAGE]

        if not self.hp > 0 and not self.dead:
            self.dead = True
        elif self.dead:
            self.kill()
            Enemies.enemies_killed += 1
            slots_available.append(self.id)
            enemy_alive[self.id] = False
            enemy_objects[self.id] = None
            map_system.remove_enemy_pos(int(self.point), self.id)
            return

        self.pathfind(screen)

    def update_mhp_list(self):
        enemy_mhp[self.id] = self.max_hp

    @classmethod
    def update_xy(cls):
        movement_vectors = enemy_movement_vector[enemy_alive]
        enemy_xy[enemy_alive] += movement_vectors
        enemy_progress[enemy_alive] += numpy.sqrt(sum(movement_vectors * movement_vectors, axis=1))


if TYPE_CHECKING:
    Type = pygame.sprite.Group[Enemies]
else:
    Type = pygame.sprite.Group

# defines the enemies group
enemies: Type = pygame.sprite.Group()
enemy_objects: list[Any] = [None] * enemy_cap


def spawn_enemy(type: EnemyConstants):
    if not slots_available:
        return
    enemies.add(Enemies(type))
