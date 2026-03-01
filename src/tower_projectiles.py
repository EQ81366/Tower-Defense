import pygame, math, numpy
from typing import Any, TYPE_CHECKING
from enemy import enemies
from money import money_script
from image_loader import TowerType

screen = pygame.display.set_mode((0, 0)) # in pixels


# defines the Tower_Projectiles class
class Tower_Projectiles(pygame.sprite.Sprite):
    image = pygame.image.load("assets/b.png")
    def __init__(self, *groups : Any):    
        super().__init__()

        self.tower_id = groups[5]

        self.projectile : TowerType = groups[0]

        self.x = groups[1]
        self.y = groups[2]

        self.angle = groups[3]

        self.damage = groups[4]

        # checks which projectile was spawned
        if self.projectile == TowerType.BASIC:
            #self.image = pygame.image.load("assets/b.png")
            self.speed = 100
            self.pierce = 2 # pierce = hp
        elif self.projectile == TowerType.DOUBLE:
            #self.image = pygame.image.load("assets/b.png")
            self.speed = 200
            self.pierce = 2 # pierce = hp

        if self.speed > 10000:
           self.speed = 10000
        elif self.speed < 0:
            self.speed = 1

        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.original_rect = self.rect

        self.height = self.image.get_height()

    # this moves the bullet
    def move(self):
        if self.alive():
            self.r_image = pygame.transform.rotate(self.image, self.angle)
            self.rect = self.r_image.get_rect(center=(self.x, self.y))

            x_offset = math.cos(math.radians(90+self.angle))*self.height/2
            y_offset = math.sin(math.radians(90+self.angle))*self.height/2


            # vector normalized movement
            dx = math.cos(math.radians(90+self.angle))
            dy = math.sin(math.radians(-90+self.angle))

            magnitude = math.hypot(dx, dy)

            movement_vector = pygame.math.Vector2(dx/magnitude * self.speed, dy/magnitude * self.speed)

            self.x += movement_vector.x
            self.y += movement_vector.y

            self.rect.centerx = int(self.x)
            self.rect.centery = int(self.y)

            if abs(self.x) > 10000 or abs(self.y) > 10000:
                self.kill()

            screen.blit(self.r_image, (self.rect.x+x_offset, self.rect.y-y_offset))

            start = pygame.math.Vector2(self.original_rect.width/2, self.original_rect.height/2)
            end = pygame.math.Vector2(self.original_rect.width/2, self.original_rect.height*1.5)
            offset = start-end
            tip = pygame.math.Vector2(self.x, self.y) + offset.rotate(-self.angle)        

            for sprite in enemies:
                if not self.alive(): # makes sure the bullet is still alive
                    break
                relative_position = pygame.math.Vector2(tip.x, tip.y) - pygame.math.Vector2(sprite.x, sprite.y)
                distance = math.hypot(sprite.x-tip.x, sprite.y-tip.y)
                
                relative_velocity = movement_vector - sprite.movement_vector

                a = relative_velocity.dot(relative_velocity)
                b = 2*(relative_position.dot(relative_velocity))
                c = relative_position.dot(relative_position) - (sprite.rect.width/2)*(sprite.rect.width/2)
                d = b*b-4*a*c
                if d >= 0 and distance <= self.speed + sprite.rect.width + 5:
                    time_to_impact = numpy.roots([a, b, c])[1]
                    if time_to_impact <= 0:
                        enemy_death_info = sprite.damage(self.damage)
                        self.pierce -= 1
                        if enemy_death_info != [0, 0]:
                            money_script(True, enemy_death_info[1])

                        return enemy_death_info, self.tower_id

                if self.pierce <= 0:
                    self.kill()
        
        return [0, 0], self.tower_id


if TYPE_CHECKING:
    Type = pygame.sprite.Group[Tower_Projectiles]
else:
    Type = pygame.sprite.Group

tower_projectiles : Type = pygame.sprite.Group()