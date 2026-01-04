import pygame, math
from image_loader import load_images, EnemyType
from constants import enemy_constants
from map_sys import show_map, map

enemy_images = load_images()[0]

# defines the enemies group
enemies = pygame.sprite.Group() # type: ignore

class Enemies(pygame.sprite.Sprite):
    def __init__(self, enemy : str, x : int, y : int):
        super().__init__()

        self.movement_nodes = map(show_map())[1]

        self.enemy = enemy

        self.x = float(x)
        self.y = float(y)

        enemy_type_number = EnemyType[enemy.upper()].value

        info = enemy_constants()[enemy_type_number]

        self.image = enemy_images[EnemyType[enemy.upper()]]

        self.tier = int(info[1])
        self.speed = float(info[2])
        self.hp = int(info[3])
        self.max_hp = self.hp

        self.money_drop = round(4**self.tier)

        # allows for custom money drops
        if len(info) > 4:
            self.money_drop = int(info[4])

        self.rect = self.image.get_rect(center=(x, y))
        # sets the current destination number(refer to the map system above)
        self.current_node = 0

    # script to make enemies go to map destinations
    def pathfind(self):
        if len(self.movement_nodes) != self.current_node:
            # determines which destination in the destination list to go to
            destination = self.movement_nodes[self.current_node]

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

            return 0

        # if enemy reaches end of map
        elif len(self.movement_nodes) == self.current_node:
            self.kill()
            # returns the amount of damage to deal
            return (2**self.tier)/2
        
    def damage(self, damage : float) -> list[int]:
        self.hp -= damage
        if not self.hp > 0:
            self.kill()
            return [self.tier, self.money_drop]
        
        return [0, 0]