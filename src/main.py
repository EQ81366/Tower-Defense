import pygame
import math

from image_loader import ImageLoader, Images
from tower_aiming import point_enemy
from map_sys import map

# TO-DO LIST
# 1. make various ui stuff
# 1. add more towers/enemies
# 2. make bosses
#
# I'll add more as I go on



# initiates pygame
pygame.init()
pygame.font.init()

# sets screen width and height
screen = pygame.display.set_mode((1280, 720)) # in pixels

clock = pygame.time.Clock()
running = True

shop_font = pygame.font.SysFont('Arial', 25)
stat_font = pygame.font.SysFont('Arial', 30)

# temporary map system
#path = pygame.image.load("path1.png")
#movements_nodes = [[178, 260], [225, 560], [505, 560], [566, 254], [758, 259], [833, 586], [1130, 590], [1200, 260], [1279, 259]] # all destinations for the enemy on a given map

# just defining variables, nothing to look at
placing_tower = False
money = 100
hp = 100



# defines the class Enemies
class Enemies(pygame.sprite.Sprite):
    def __init__(self, enemy, x, y):
        super().__init__()

        self.enemy = enemy

        self.x = x
        self.y = y

        # checks which type of enemy was spawned
        if enemy == "basic":
            self.image = ImageLoader.load(Images.ENEMY1)
            self.tier = 1
            self.speed = 1
            self.hp = 1

        if enemy == "tank":
            self.image = ImageLoader.load(Images.BULLET)
            self.tier = 1
            self.speed = 0.5
            self.hp = 100

        self.max_hp = self.hp

        self.rect = self.image.get_rect(center=(x, y))
        # sets the current destination number(refer to the map system above)
        self.current_node = 0

    # script to make enemies go to map destinations
    def pathfind(self):
        if len(movement_nodes) != self.current_node:
            # determines which destination in the destination list to go to
            destination = movement_nodes[self.current_node]

            # next 10 lines enact vector normalized movement
            dx = destination[0] - self.rect.centerx
            dy = destination[1] - self.rect.centery

            magnitude = math.sqrt(dx*dx + dy*dy)

            self.x += dx/magnitude * self.speed
            self.y += dy/magnitude * self.speed

            self.rect.centerx = self.x
            self.rect.centery = self.y

            def at_destination():
                self.current_node += 1
                self.rect.centerx = destination[0]
                self.rect.centery = destination[1]

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
        elif len(movement_nodes) == self.current_node:
            self.kill()
            # returns the amount of damage to deal
            return self.tier
        
    def damage(self, damage):
        self.hp -= damage


# defines the class Towers
class Towers(pygame.sprite.Sprite):
    def __init__(self, tower : str, x : int, y : int):
        super().__init__()

        self.tower = tower

        self.x = x
        self.y = y

        self.current_angle = 0

        self.rotation_angle = 0
        self.exported_angle = 0

        self.base_image, self.image, self.firing_image = ImageLoader.load_tower(tower)

        # towers damage
        self.dmg = 0
        # towers cooldown
        self.cd = 0
        # towers rotational speed
        self.r_speed = 0
        # enemy to target
        self.targeting_mode = ""

        # checks which type of tower was spawned
        # you can add more towers using these variables
        if tower == "basic":
            self.dmg = 1
            self.cd = 60
            self.r_speed = 1000000
            self.targeting_mode = "strong"

        # makes sure there is no firing cooldown on placement
        self.wait = self.cd

        # if you don't understand what this line of code means...
        self.firing = False
        self.shoot_enemy = False
        
        self.rect = self.image.get_rect(center=(x, y))

        self.b_rect = self.base_image.get_rect(center=(x, y))

        self.height = self.image.get_height()
    
    # defines the rotation and firing animation of the tower
    def rotate(self):
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
            self.r_image = pygame.transform.rotate(self.firing_image, self.current_angle)
            self.rect = self.r_image.get_rect(center=(xy[0], xy[1]))
        
        x = math.cos(math.radians(90+self.current_angle))*self.height/2
        y = math.sin(math.radians(90+self.current_angle))*self.height/2

        screen.blit(self.base_image, self.b_rect)
        screen.blit(self.r_image, (self.rect.x+x, self.rect.y-y))

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
            print("hi")

    # determines when to switch back to the original tower state
    def unfire(self):
        if self.wait > self.cd/5:
            self.firing = False

    # finds the closest enemy
    def find_closest_enemy(self):
        # high default distance so as to not interfere with anythin
        if self.wait > self.cd/5 or self.wait == 0:
            x = 0
            closest_id = 0

            # targets closest enemy
            if self.targeting_mode == "closest":
                distance = 99999
                closest_distance = distance
                for sprite in enemies:
                    dx = sprite.rect.centerx - self.rect.centerx
                    dy = sprite.rect.centery - self.rect.centery
                    distance = math.sqrt(dx*dx + dy*dy)

                    x += 1

                    if distance < closest_distance:
                        closest_distance = distance
                        closest_id = x

            # targets the most "efficient" enemy; whichever enemy is fastest to shoot
            elif self.targeting_mode == "efficiency":
                dr = 99999
                lowest_dr = dr
                for sprite in enemies:
                    self.rotation_angle = point_enemy(self.rect.centerx, self.rect.centery, sprite.rect.centerx, sprite.rect.centery)
                    dr = self.rotation_angle - self.current_angle
            
                    x += 1

                    if abs(dr) < abs(lowest_dr):
                        lowest_dr = dr
                        closest_id = x

            # targets the furthest most enemy in range
            elif self.targeting_mode == "first":
                if len(enemies) > 0:
                    closest_id = 1

            # targets the furthest back enemy in range
            elif self.targeting_mode == "last":
                closest_id = len(enemies)

            # targets the enemy with the most hp
            elif self.targeting_mode == "strong":
                e_hp = 0
                highest_e_hp = e_hp
                for sprite in enemies:
                    x += 1
                    e_hp = sprite.max_hp
                    if e_hp > highest_e_hp:
                        highest_e_hp = e_hp
                        closest_id = x

            # makes sure there are enemies within tower range
            if closest_id != 0:
                # gets a list format of the enemies group
                enemy_list = enemies.sprites()
                # finds the angle to targeted enemy
                self.rotation_angle = point_enemy(self.rect.centerx, self.rect.centery, enemy_list[closest_id-1].rect.centerx, enemy_list[closest_id-1].rect.centery)
                # checks if firing cooldown is over and that the tower is rotated within 4 degrees of the enemy
                if self.wait >= self.cd and self.current_angle >= self.rotation_angle-2 and self.current_angle <= self.rotation_angle+2:
                    # kills the targeted enemy
                    enemy_list[closest_id-1].damage(self.dmg)
                    self.shoot_enemy = False
                    self.firing = True
                    self.wait = 0



# defines the Tower_Projectiles class
# CURRENTLY OBSOLETE(most likely will not be added again)
class Tower_Projectiles(pygame.sprite.Sprite):
    def __init__(self, projectile, x, y, angle):    
        super().__init__()

        self.projectile = projectile

        self.x = x
        self.y = y

        self.angle = angle

        # checks which projectile was spawned
        if projectile == "basic":
            self.image = ImageLoader.Load(Images.BULLET)
            self.speed = 300
            # think of pierce as bullet hp
            self.pierce = 1

        self.rect = self.image.get_rect(center=(x, y))

        self.height = self.image.get_height()

    # this moves the bullet
    def move(self):
        self.r_image = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.r_image.get_rect(center=(self.x, self.y))

        x_offset = math.cos(math.radians(90+self.angle))*self.height/2
        y_offset = math.sin(math.radians(90+self.angle))*self.height/2


        # vector normalized movement
        dx = math.cos(math.radians(90+self.angle))
        dy = math.sin(math.radians(-90+self.angle))

        magnitude = math.sqrt(dx*dx + dy*dy)

        self.x += dx/magnitude * self.speed
        self.y += dy/magnitude * self.speed

        self.rect.centerx = self.x
        self.rect.centery = self.y

        screen.blit(self.r_image, (self.rect.x+x_offset, self.rect.y-y_offset))

        for sprite in enemies:
            if self.rect.colliderect(sprite.rect):
                sprite.kill()

# defines the class Shop
class Shop(pygame.sprite.Sprite):
    def __init__(self, shop, x, y):
        super().__init__()

        self.shop = shop

        self.original_x = x
        self.original_y = y

        # checks which shop item was initiated
        if shop == "panel":
            self.image = ImageLoader.load(Images.SHOP_UI)
            self.open = False

        # to add more towers copy and paste the code below and continue to elif
        elif shop == "basic": # change the string to relating tower name defined in the Tower class
            self.image = ImageLoader.load(Images.BASIC_TOWER)
            # the cost of the tower
            self.cost = 100

        # defines generic things for non-panel shop items
        if shop != "panel":
            self.text = shop_font.render(f'{shop.capitalize()} ${self.cost}', True, "black")
            self.clicked = False

        self.rect = self.image.get_rect(center=(x, y))

    # checks whether the mouse is hovering over the shop panel and changes the panel accordingly
    def hovering(self):
        if mouse_xy[1] >= 690 and not self.open or mouse_xy[1] >= 490 and self.open:
            self.open = True
            self.rect.centery = 700
        else:
            self.open = False
            self.rect.centery = 900

        screen.blit(self.image, self.rect)

        return self.open

    # checks if the shop is open and if so, displays all the items in the shop
    def showing(self, open):
        if open:
            screen.blit(self.image, self.rect)
            screen.blit(self.text, (self.rect.centerx-self.text.get_width()/2, self.rect.centery+self.rect.height/2))

            # if the mouse is down when hovering over an item in the shop, it will wait until mouse not down, and attempt to buy that item
            if money >= self.cost:
                if mouse_xy[0] >= self.rect.x and mouse_xy[0] < self.rect.x+self.rect.width and mouse_xy[1] >= self.rect.y and mouse_xy[1] < self.rect.y+self.rect.height:
                    if pygame.mouse.get_pressed()[0] and not self.clicked:
                        self.clicked = True
                    elif not pygame.mouse.get_pressed()[0] and self.clicked:
                        self.clicked = False
                        return True, self.cost
        return False, 0
    
    # if the user bought a tower from the shop, it will follow the mouse until placed
    def place_tower(self):
        self.rect.centerx = mouse_xy[0]
        self.rect.centery = mouse_xy[1]
        screen.blit(self.image, self.rect)

        mask1 = pygame.mask.from_surface(self.image)
        mask2 = pygame.mask.from_surface(path)
    
        offset_x = map_offsets[0] - self.rect.left
        offset_y = map_offsets[1] - self.rect.top

        colliding = mask1.overlap(mask2, (offset_x, offset_y))
        
        # waits to place tower until mouse down and not touching track, it then waits for mouse release to place
        if pygame.mouse.get_pressed()[0] and not colliding:
            self.clicked = True
        elif not pygame.mouse.get_pressed()[0] and self.clicked:
            self.clicked = False
            towers.add(Towers(self.shop, self.rect.centerx, self.rect.centery))
            self.rect.centerx = self.original_x
            self.rect.centery = self.original_y
            return False
        
        return True
    
def stats(money, hp):
    text = stat_font.render(f'Money: ${money}', True, "black")
    screen.blit(text, (5, 0))
    text = stat_font.render(f'Health: {hp}', True, "black")
    screen.blit(text, (5, 35))

# --------------------------------------------------- #
# Main                                                #
# --------------------------------------------------- #
path, movement_nodes, map_offsets = map("map1")


# defines the towers group
towers = pygame.sprite.Group()

towers.add(Towers("basic", 640, 360))

tower_projectiles = pygame.sprite.Group()

# defines the enemies group
enemies = pygame.sprite.Group()

#enemies.add(Enemies("basic", 8, 280))

# defines the shop group
shop = pygame.sprite.Group()

shop.add(Shop("panel", 640, 900))
shop.add(Shop("basic", 100, 540))
 
# and so begins the main script
x = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # background
    screen.fill((50, 200, 20))
    # map
    screen.blit(path, (-4, 200))

    mouse_xy = pygame.mouse.get_pos()

    for sprite in tower_projectiles:
        sprite.move()

    # cycles through all the necessary commands for the towers group
    for sprite in towers:
        sprite.wait += 1
        sprite.find_closest_enemy()
        #sprite.shoot()
        sprite.unfire()
        sprite.rotate()

    # cycles through all the necessary commands for the enemies group
    for sprite in enemies:
        hp -= sprite.pathfind()

    # cycles through all the necessary commands for the shop group
    for sprite in shop:
        # only runs hovering function for the panel type in the shop group
        if sprite.shop == "panel":
            open = sprite.hovering()
        # runs normally for all other types in the shop group
        else:
            if not placing_tower:
                temp_pkg = sprite.showing(open)
                placing_tower = temp_pkg[0]
                money -= temp_pkg[1]
            else:
                placing_tower = sprite.place_tower()

    # draws the enemies on the screen
    enemies.draw(screen)

    stats(money, hp)

    x += 1
    if x > 100:
        #enemies.add(Enemies("basic", 8, 280))
        enemies.add(Enemies("tank", 8, 280))
        x = 0

    #print(len(enemies))

    pygame.display.flip()
    clock.tick(60)