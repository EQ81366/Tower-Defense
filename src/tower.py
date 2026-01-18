import pygame, math, constants
from image_loader import load_images, TowerType
from tower_aiming import point_enemy
from mouse import mouse_info
from enemy import enemies #type: ignore

tower_images = load_images(["tower"])[0]

# defines the towers group
towers = pygame.sprite.Group() # type: ignore

screen = pygame.display.set_mode((0, 0)) # in pixels

class Towers(pygame.sprite.Sprite):
    def __init__(self, tower : str, x : int, y : int):
        super().__init__()

        self.tower = tower

        self.x = x
        self.y = y

        self.current_angle = 0

        self.rotation_angle = 0
        self.exported_angle = 0

        self.firing_pose = 0

        tower_image_bundle = tower_images[TowerType[tower.upper()]]
        tower_type_number = TowerType[tower.upper()].value
        
        info = constants.tower_constants()[tower_type_number]

        if isinstance(tower_image_bundle, list):
            # base image
            self.b_image = tower_image_bundle[0]
            # turret image
            self.image = tower_image_bundle[1]
            # firing turret image
            self.f_image = tower_image_bundle[2]

        # tower info
        self.tier = int(info[1])
        self.turrets = int(info[2])
        self.dmg = int(info[3])
        self.cd = int(info[4])
        self.range = int(info[5])
        self.r_speed = int(info[6])

        if isinstance(tower_image_bundle, list) and self.turrets > 1:
            self.f2_image = tower_image_bundle[3]

        # list of upgrades(bought and non-bought)
        self.upgrades_bought = {1:[False, False], 2:[False, False]}

        # amount of each enemy tier killed
        # first number enemy tier, second number amount
        self.enemies_killed : dict[int, int] = {}
        for i in range(5):
            self.enemies_killed[i+1] = 0

        # makes the physical circle of range
        self.range_circle = pygame.image.load("assets/circle.png")
        self.range_circle_scaled = pygame.transform.scale(self.range_circle, (self.range*2, self.range*2))

        # targeting mode(default is rotationaly efficient)
        self.targeting_mode = constants.TargetingStates.EFFICIENT
        self.targeting_mode = constants.TargetingStates.FIRST

        # makes sure there is no firing cooldown on placement
        self.wait = self.cd
        self.shots_left = self.turrets

        # if you don't understand what this line of code means...
        self.firing = False
        self.shoot_enemy = False
        self.clicked = False
        self.upgrades_open = False
        
        self.rect = self.image.get_rect(center=(x, y))

        self.b_rect = self.b_image.get_rect(center=(x, y))

        self.height = self.image.get_height()
    
    # defines the rotation and firing animation of the tower
    def rotate(self):
        print(self.tier, self.upgrades_bought, self.enemies_killed)

        dr = self.rotation_angle - self.current_angle
    
        if abs(dr) > 1:
            self.current_angle += self.r_speed/60 * dr/abs(dr)
            dr = self.rotation_angle - self.current_angle
            if abs(dr) <= 2*(self.r_speed/100):
                self.current_angle = self.rotation_angle
            if self.current_angle >= 360:
                self.current_angle = 0

        self.r_image = pygame.transform.rotate(self.image, self.current_angle)
        self.rect = self.r_image.get_rect(center=(self.x, self.y))
        xy = [self.rect.centerx, self.rect.centery]

        # if shooting, switches image to shooting image
        if self.firing:
            if self.wait < self.cd/10 and self.turrets-1 == self.shots_left:
                self.r_image = pygame.transform.rotate(self.f_image, self.current_angle)
            
            elif self.wait < self.cd/5 and self.turrets-2 == self.shots_left:
                self.r_image = pygame.transform.rotate(self.f2_image, self.current_angle)

            self.rect = self.r_image.get_rect(center=(xy[0], xy[1]))
        
        self.dx = math.cos(math.radians(90+self.current_angle))*self.height/2
        self.dy = math.sin(math.radians(90+self.current_angle))*self.height/2

        screen.blit(self.b_image, self.b_rect)
        screen.blit(self.r_image, (self.rect.x+self.dx, self.rect.y-self.dy))

    # determines whether the tower can shoot yet
    # CURRENTLY OBSOLETE(most likely will not be added again)
    def shoot(self):
        self.shoot_enemy = False
        if self.wait >= self.cd and self.current_angle >= self.rotation_angle-2 and self.current_angle <= self.rotation_angle+2:
            #  ⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄uncomment this for bullets⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄⌄
            #tower_projectiles.add(Tower_Projectiles("basic", self.rect.centerx, self.rect.centery, self.exported_angle))
            self.shoot_enemy = True
            self.firing = True
            self.wait = 0

    # determines when to switch back to the original tower state
    def unfire(self):
        if self.wait > self.cd/5 and self.shots_left != self.turrets-1:
            self.firing = False
            
    # finds the closest enemy
    def find_closest_enemy(self) -> list[int]:
        enemy_death_info : list[int] = [0, 0]

        x = 0
        self.closest_id = 0

        # targets the most "efficient" enemy; whichever enemy is fastest to shoot
        if self.targeting_mode == constants.TargetingStates.EFFICIENT:
            dr = 99999
            lowest_dr = dr
            for sprite in enemies: # type: ignore
                dx : int = int(sprite.rect.centerx) - self.rect.centerx # type: ignore
                dy : int = int(sprite.rect.centery) - self.rect.centery # type: ignore
                distance = math.hypot(dx, dy)

                angle = point_enemy(self.rect.centerx, self.rect.centery, sprite.rect.centerx, sprite.rect.centery) # type: ignore
                dr = angle - self.current_angle
        
                x += 1

                if abs(dr) < abs(lowest_dr) and distance <= self.range:
                    lowest_dr = dr
                    self.closest_id = x

        # targets closest enemy
        elif self.targeting_mode == constants.TargetingStates.CLOSE:
            distance = 99999
            closest_distance = distance
            
            for sprite in enemies: # type: ignore
                dx : int = int(sprite.rect.centerx) - self.rect.centerx # type: ignore
                dy : int = int(sprite.rect.centery) - self.rect.centery # type: ignore
                distance = math.hypot(dx, dy)

                x += 1

                if distance < closest_distance and distance <= self.range:
                    closest_distance = distance
                    self.closest_id = x

        # targets the furthest most enemy in range
        elif self.targeting_mode == constants.TargetingStates.FIRST:
            for sprite in enemies: # type: ignore
                dx : int = int(sprite.rect.centerx) - self.rect.centerx # type: ignore
                dy : int = int(sprite.rect.centery) - self.rect.centery # type: ignore
                distance = math.hypot(dx, dy)

                x += 1

                if distance <= self.range:
                    self.closest_id = x
                    break

        # targets the furthest back enemy in range
        elif self.targeting_mode == constants.TargetingStates.LAST:
            for sprite in enemies: # type: ignore
                dx : int = int(sprite.rect.centerx) - self.rect.centerx # type: ignore
                dy : int = int(sprite.rect.centery) - self.rect.centery # type: ignore
                distance = math.hypot(dx, dy)

                x += 1

                if distance <= self.range:
                    self.closest_id = x

        # targets the enemy with the most hp
        elif self.targeting_mode == constants.TargetingStates.STRONG:
            e_hp = 0
            highest_e_hp = e_hp
            for sprite in enemies: # type: ignore
                dx : int = int(sprite.rect.centerx) - self.rect.centerx # type: ignore
                dy : int = int(sprite.rect.centery) - self.rect.centery # type: ignore
                distance = math.hypot(dx, dy)

                x += 1
                e_hp = float(sprite.max_hp) # type: ignore

                if e_hp > highest_e_hp and distance <= self.range:
                    highest_e_hp = e_hp
                    self.closest_id = x

        # makes sure there are enemies within tower range
        if self.closest_id != 0:
            # gets a list format of the enemies group
            enemy_list = enemies.sprites() # type: ignore

            # finds the angle to targeted enemy
            self.rotation_angle = point_enemy(self.rect.centerx, self.rect.centery, int(enemy_list[self.closest_id-1].rect.centerx), int(enemy_list[self.closest_id-1].rect.centery)) # type: ignore
            
            # checks if firing cooldown is over and that the tower is rotated within 4 degrees of the enemy
            if self.current_angle >= self.rotation_angle-2 and self.current_angle <= self.rotation_angle+2:
                if (self.wait >= self.cd):
                    self.shots_left = self.turrets
                    enemy_death_info = self.shoot_target(True)

                elif self.shots_left == self.turrets-1 and self.wait >= self.cd/10:
                    enemy_death_info = self.shoot_target(True)

        return enemy_death_info # type: ignore
    
    def shoot_target(self, shoot : bool) -> list[int]:
        enemy_death_info = [0, 0]
        if shoot and self.shots_left > 0:
            enemy_list = enemies.sprites() # type: ignore
            # damages the target
            if self.closest_id != 0:
                enemy_death_info : list[int] = enemy_list[self.closest_id-1].damage(self.dmg) # type: ignore

                # updates amount of enemies killed
                if enemy_death_info != [0, 0]:
                    self.enemies_killed[enemy_death_info[0]] += 1

            self.shoot_enemy = False
            self.firing = True
            self.shots_left -= 1
            self.wait = 0

            if enemy_death_info != [0, 0]:
                return enemy_death_info # type: ignore
            
        return [0, 0]

    def open_upgrades(self, upgrade_rect : pygame.Rect):
        mouse_xy, mouse_down = mouse_info()

        if self.rect.collidepoint(mouse_xy):
            if mouse_down:
                self.clicked = True
            elif not mouse_down and self.clicked:
                self.clicked = False
                self.upgrades_open = not self.upgrades_open
        else:
            if mouse_down and not upgrade_rect.collidepoint(mouse_xy):
                self.clicked = True
            elif not mouse_down and self.clicked:
                self.clicked = False
                self.upgrades_open = False
            
        return self.upgrades_open
    
    def show_range(self):
        if self.upgrades_open:
            self.range_circle_scaled = pygame.transform.scale(self.range_circle, (self.range*2, self.range*2))
            return self.range_circle_scaled, (self.x-self.range_circle_scaled.get_width()/2, self.y-self.range_circle_scaled.get_height()/2)
        return None