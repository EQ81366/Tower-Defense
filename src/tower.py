import pygame, math
from typing import Any, TYPE_CHECKING
from constants import TowerConstants, TargetingStates
from image_loader import load_images, TowerType
from tower_aiming import point_enemy
from mouse import mouse_info, clicked_and_released
from enemy import enemies
from tower_projectiles import Tower_Projectiles, tower_projectiles

tower_images = load_images(["tower"])[0]

screen = pygame.display.set_mode((0, 0)) # in pixels

class Towers(pygame.sprite.Sprite):
    id = 0
    range_circle = pygame.image.load("assets/circle.png")

    def __init__(self, *groups : Any):
        super().__init__()

        self.id = Towers.id
        Towers.id += 1

        self.tower : TowerType = groups[0]
        self.x : int = groups[1]
        self.y : int = groups[2]

        info = TowerConstants[self.tower.name].value
        self.tier = int(info[1])
        self.turrets = int(info[2])
        self.damage = int(info[3])
        self.cooldown = int(info[4])
        self.range = int(info[5])
        self.rotation_speed = int(info[6])

        self.recoil_multiplier = 5

        self.wait = self.cooldown
        self.shots_left = self.turrets # sets shots available to the amount of turrets
        self.current_angle = 0
        self.rotation_angle = 0

        self.upgrades_bought = {i : [False, False] for i in range(2)}
        self.enemies_killed : dict[int, int] = {i : 0 for i in range(5)}

        #self.range_circle_scaled = pygame.transform.scale(self.range_circle, (self.range*2, self.range*2)) # scales the range circle accordingly to tower range

        tower_image_bundle = tower_images[self.tower]
        self.b_image = tower_image_bundle[0]
        self.image = tower_image_bundle[1]
        self.f_image = tower_image_bundle[2]
        if self.turrets > 1:
            self.f2_image = tower_image_bundle[3]

        self.height = self.image.get_height()
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.b_rect = self.b_image.get_rect(center=(self.x, self.y))  

        self.firing = False
        self.shoot_enemy = False
        self.clicked = False
        self.upgrades_open = False

        self.targeting_mode = TargetingStates.EFFICIENT # targeting mode(default is rotationaly efficient)
    
    # defines the rotation and firing animation of the tower
    def rotate(self):
        if self.current_angle >= 180:
            self.current_angle = -180
        elif self.current_angle < -180:
            self.current_angle = 179

        dr = self.rotation_angle - self.current_angle
    
        if abs(dr) > 1:
            self.current_angle += self.rotation_speed/60 * dr/abs(dr)
            dr = self.rotation_angle - self.current_angle
            if abs(dr) <= 2*(self.rotation_speed/100): # if rotation is close enough based upon rotational speed it just accepts the wanted rotation value
                self.current_angle = self.rotation_angle

        self.r_image = pygame.transform.rotate(self.image, self.current_angle)
        self.rect = self.r_image.get_rect(center=(self.x, self.y))
        xy = [self.rect.centerx, self.rect.centery]

        # if shooting, switches image to shooting image
        if self.firing:
            if self.wait < self.cooldown/((self.shots_left+1)*self.recoil_multiplier) and self.turrets-1 == self.shots_left:
                self.r_image = pygame.transform.rotate(self.f_image, self.current_angle)
            
            elif self.wait < self.cooldown/((self.shots_left+1)*self.recoil_multiplier) and self.turrets-2 == self.shots_left:
                self.r_image = pygame.transform.rotate(self.f2_image, self.current_angle)

            self.rect = self.r_image.get_rect(center=(xy[0], xy[1]))
        
        self.dx = math.cos(math.radians(90+self.current_angle))*self.height/2
        self.dy = math.sin(math.radians(90+self.current_angle))*self.height/2

        screen.blit(self.b_image, self.b_rect)
        screen.blit(self.r_image, (self.rect.x+self.dx, self.rect.y-self.dy))

    # determines when to switch back to the original tower state
    def unfire(self):
        if self.wait > self.cooldown/5 and self.shots_left != self.turrets-1:
            self.firing = False

    # creates a bullet
    def shoot(self):
        #  ⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄uncomment this for bullets⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄
        tower_projectiles.add(Tower_Projectiles(self.tower, self.rect.centerx, self.rect.centery, self.current_angle, self.damage, self.id))
            
    # finds the closest enemy
    def find_closest_enemy(self) -> list[int]:
        enemy_death_info : list[int] = [0, 0]

        x = 0
        self.closest_id = 0

        # targets the most "efficient" enemy; whichever enemy is fastest to shoot
        if self.targeting_mode == TargetingStates.EFFICIENT:
            dr = 99999
            lowest_dr = dr
            for sprite in enemies:
                dx = sprite.rect.centerx - self.rect.centerx
                dy = sprite.rect.centery - self.rect.centery
                distance = math.hypot(dx, dy)

                angle = point_enemy(self.rect.centerx, self.rect.centery, sprite.rect.centerx, sprite.rect.centery)
                dr = angle - self.current_angle
        
                x += 1

                if abs(dr) < abs(lowest_dr) and distance <= self.range:
                    lowest_dr = dr
                    self.closest_id = x

        # targets closest enemy
        elif self.targeting_mode == TargetingStates.CLOSE:
            distance = 99999
            closest_distance = distance
            
            for sprite in enemies:
                dx : int = int(sprite.rect.centerx) - self.rect.centerx
                dy : int = int(sprite.rect.centery) - self.rect.centery
                distance = math.hypot(dx, dy)

                x += 1

                if distance < closest_distance and distance <= self.range:
                    closest_distance = distance
                    self.closest_id = x

        # targets the furthest most enemy in range
        elif self.targeting_mode == TargetingStates.FIRST:
            for sprite in enemies:
                dx : int = int(sprite.rect.centerx) - self.rect.centerx
                dy : int = int(sprite.rect.centery) - self.rect.centery
                distance = math.hypot(dx, dy)

                x += 1

                if distance <= self.range:
                    self.closest_id = x
                    break

        # targets the furthest back enemy in range
        elif self.targeting_mode == TargetingStates.LAST:
            for sprite in enemies:
                dx : int = int(sprite.rect.centerx) - self.rect.centerx
                dy : int = int(sprite.rect.centery) - self.rect.centery
                distance = math.hypot(dx, dy)

                x += 1

                if distance <= self.range:
                    self.closest_id = x

        # targets the enemy with the most hp
        elif self.targeting_mode == TargetingStates.STRONG:
            e_hp = 0
            highest_e_hp = e_hp
            for sprite in enemies:
                dx : int = int(sprite.rect.centerx) - self.rect.centerx
                dy : int = int(sprite.rect.centery) - self.rect.centery
                distance = math.hypot(dx, dy)

                x += 1
                e_hp = float(sprite.max_hp)

                if e_hp > highest_e_hp and distance <= self.range:
                    highest_e_hp = e_hp
                    self.closest_id = x

        # makes sure there are enemies within tower range
        if self.closest_id != 0:
            enemy_list = enemies.sprites() # gets a list format of the enemies group

            # finds the angle to targeted enemy
            self.rotation_angle = point_enemy(self.rect.centerx, self.rect.centery, int(enemy_list[self.closest_id-1].rect.centerx), int(enemy_list[self.closest_id-1].rect.centery))
            
            # checks if firing cooldown is over and that the tower is rotated within 4 degrees of the enemy
            if self.current_angle >= self.rotation_angle-2 and self.current_angle <= self.rotation_angle+2:
                if (self.wait >= self.cooldown):
                    self.shots_left = self.turrets # resets ammo
                    enemy_death_info = self.shoot_target(True)

                elif self.shots_left == self.turrets-1 and self.wait >= self.cooldown/5:
                    enemy_death_info = self.shoot_target(True)

        return enemy_death_info
    
    def shoot_target(self, shoot : bool) -> list[int]:
        enemy_death_info = [0, 0]
        if shoot and self.shots_left > 0:
            self.shoot()
            enemy_list = enemies.sprites()
            # damages the target
            if self.closest_id != 0:
                #enemy_death_info : list[int] = enemy_list[self.closest_id-1].damage(self.damage)

                # updates amount of enemies killed
                if enemy_death_info != [0, 0]:
                    self.enemies_killed[enemy_death_info[0]] += 1

            self.shoot_enemy = False
            self.firing = True
            self.shots_left -= 1
            self.wait = 0

            return enemy_death_info
            
        return [0, 0]

    def open_upgrades(self, upgrade_rect : pygame.Rect):
        mouse_xy, mouse_down = mouse_info()
        pressed, self.clicked = clicked_and_released(mouse_down, self.clicked)

        if self.rect.collidepoint(mouse_xy) and pressed:
            self.upgrades_open = not self.upgrades_open
        elif not upgrade_rect.collidepoint(mouse_xy) and pressed:
            self.upgrades_open = False
            
        return self.upgrades_open
    
    def show_range(self):
        if self.upgrades_open:
            self.range_circle_scaled = pygame.transform.scale(self.range_circle, (self.range*2, self.range*2))
            return self.range_circle_scaled, [self.x-self.range_circle_scaled.get_width()/2, self.y-self.range_circle_scaled.get_height()/2]
        return None
    

if TYPE_CHECKING:
    Type = pygame.sprite.Group[Towers]
else:
    Type = pygame.sprite.Group

# defines the towers group
towers : Type = pygame.sprite.Group()