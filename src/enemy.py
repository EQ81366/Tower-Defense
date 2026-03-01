import pygame, math
from typing import TYPE_CHECKING, Any
from image_loader import load_images, EnemyType
from constants import EnemyConstants
from map_sys import show_map, map

enemy_images = load_images(["enemy"])[0]

movement_nodes = map(show_map())[1]

screen = pygame.display.set_mode((0, 0)) # in pixels

class Enemies(pygame.sprite.Sprite):
    def __init__(self, *groups : Any):
        super().__init__()

        self.enemy : EnemyType = groups[0]

        self.x : float = groups[1]
        self.y : float = groups[2]

        self.movement_vector = pygame.math.Vector2(0, 0)

        info = EnemyConstants[self.enemy.name.upper()].value

        self.image = enemy_images[self.enemy][0]
        self.current_image = self.image

        # makes a copy of the enemies image but red
        self.damage_image = self.image.copy()
        with pygame.PixelArray(self.damage_image) as pixel_array:
            pixel_array.replace(self.damage_image.get_at((int(self.damage_image.get_width()/2), int(self.damage_image.get_height()/2))), (255, 0, 0))

        self.tier = int(info[1])
        self.speed = float(info[2])
        self.hp = int(info[3])
        self.max_hp = self.hp
        self.weight = int(info[4]) # the more weight the less it's stunned with each hit

        self.damage_frame_length = int(30/self.weight)
        self.damage_frame = 0

        self.money_drop = round(4**self.tier)
        self.damage_at_end = (2**self.tier)
        if self.damage_at_end > 1:
            self.damage_at_end /= 2

        # allows for custom money drops
        if len(info) > 5:
            self.money_drop = int(info[5])

        self.rect = self.image.get_rect(center=(self.x, self.y))
        # sets the current destination number(refer to the map system above)
        self.current_node = 0

    # script to make enemies go to map destinations
    def pathfind(self):
        self.damage_frame -= 1
        if len(movement_nodes) != self.current_node and self.damage_frame <= 0:
            self.current_image = self.image
            # determines which destination in the destination list to go to
            destination = movement_nodes[self.current_node]

            # next 10 lines enact vector normalized movement
            dx = destination[0] - self.rect.centerx
            dy = destination[1] - self.rect.centery

            magnitude = math.hypot(dx, dy)

            self.movement_vector = pygame.math.Vector2(dx/magnitude * self.speed, dy/magnitude * self.speed)

            self.x += self.movement_vector.x
            self.y += self.movement_vector.y

            self.rect.centerx = int(self.x)
            self.rect.centery = int(self.y)

            def at_destination():
                self.current_node += 1
                self.rect.centerx = destination[0]
                self.rect.centery = destination[1]

            # determines if the enemy actually made it to it's destination
            if (dx >= 0 and self.rect.centerx >= destination[0]) and (dy >= 0 and self.rect.centery >= destination[1]):
                at_destination()
            elif (dx >= 0 and self.rect.centerx >= destination[0]) and (dy <= 0 and self.rect.centery <= destination[1]):
                at_destination()
            elif (dx <= 0 and self.rect.centerx <= destination[0]) and (dy >= 0 and self.rect.centery >= destination[1]):
                at_destination()
            elif (dx <= 0 and self.rect.centerx <= destination[0]) and (dy <= 0 and self.rect.centery <= destination[1]):
                at_destination()


        # if enemy reaches end of map
        elif len(movement_nodes) == self.current_node:
            self.kill()
            return self.damage_at_end # returns the amount of damage to deal
        
        screen.blit(self.current_image, self.rect) # draws the enemies
        
        return 0
        
    def damage(self, damage : float) -> list[int]:
        if self.damage_frame <= 0:
            self.hp -= damage
            self.damage_frame = self.damage_frame_length
            self.current_image = self.damage_image
            if not self.hp > 0:
                self.kill()
                return [self.tier, self.money_drop]
        
        return [0, 0]
    
    
if TYPE_CHECKING:
    Type = pygame.sprite.Group[Enemies]
else:
    Type = pygame.sprite.Group

# defines the enemies group
enemies : Type = pygame.sprite.Group()