import pygame, math
from image_loader import load_images, EnemyType
from constants import enemy_constants
from map_sys import show_map, map

enemy_images = load_images(["enemy"])[0]

movement_nodes = map(show_map())[1]

# defines the enemies group
enemies = pygame.sprite.Group() # type: ignore

class Enemies(pygame.sprite.Sprite):
    def __init__(self, enemy : str, x : int, y : int):
        super().__init__()

        self.enemy = enemy

        self.x = float(x)
        self.y = float(y)

        enemy_type_number = EnemyType[enemy.upper()].value

        info = enemy_constants()[enemy_type_number]

        placeholder = enemy_images[EnemyType[enemy.upper()]]
        if isinstance(placeholder, pygame.Surface):
            self.image = placeholder

        # makes a copy of the enemies image but red
        self.damage_image = self.image.copy()
        with pygame.PixelArray(self.damage_image) as pixel_array:
            pixel_array.replace(self.image.get_at((int(self.image.get_width()/2), int(self.image.get_height()/2))), (255, 0, 0))

        self.tier = int(info[1])
        self.speed = float(info[2])
        self.hp = int(info[3])
        self.max_hp = self.hp
        # the more weight the less it's stunned with each hit
        self.weight = int(info[4])

        self.damage_frame_length = int(30/self.weight)
        self.damage_frame = 0

        self.money_drop = round(4**self.tier)

        # allows for custom money drops
        if len(info) > 5:
            self.money_drop = int(info[5])

        self.rect = self.image.get_rect(center=(x, y))
        # sets the current destination number(refer to the map system above)
        self.current_node = 0

    # script to make enemies go to map destinations
    def pathfind(self):
        self.damage_frame -= 1
        if len(movement_nodes) != self.current_node and self.damage_frame <= 0:
            # determines which destination in the destination list to go to
            destination = movement_nodes[self.current_node]

            # next 10 lines enact vector normalized movement
            dx = destination[0] - self.rect.centerx
            dy = destination[1] - self.rect.centery

            magnitude = math.sqrt(dx*dx + dy*dy)

            self.x += dx/magnitude * self.speed
            self.y += dy/magnitude * self.speed

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
            # returns the amount of damage to deal
            return (2**self.tier)/2
        
        return 0
        
    def damage(self, damage : float) -> list[int]:
        if self.damage_frame <= 0:
            self.hp -= damage
            self.damage_frame = self.damage_frame_length
            if not self.hp > 0:
                self.kill()
                return [self.tier, self.money_drop]
        
        return [0, 0]