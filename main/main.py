import pygame, math, constants, image_paths

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
money, hp = constants.stat_constants()

path, movement_nodes, map_offsets = map("path1")



# defines the class Enemies
class Enemies(pygame.sprite.Sprite):
    def __init__(self, enemy : str, x : int, y : int):
        super().__init__()

        self.enemy = enemy

        self.x = float(x)
        self.y = float(y)

        # default value
        enemy_type_number = 0

        # checks which type of enemy was spawned
        if enemy == "basic":
            enemy_type_number = 0

        elif enemy == "tank":
            enemy_type_number = 1

        info = constants.enemy_constants()[enemy_type_number]

        image_path = image_paths.enemy_image_path(enemy_type_number)

        self.image = pygame.image.load(image_path)

        self.tier = str(info[1])
        self.speed = float(info[2])
        self.hp = int(info[3])
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
        elif len(movement_nodes) == self.current_node:
            self.kill()
            # returns the amount of damage to deal
            return self.tier
        
    def damage(self, damage : float):
        self.hp -= damage
        if not self.hp > 0:
            self.kill()


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

        # default value
        tower_type_number = 0

        # checks which type of tower was spawned
        if tower == "basic":
            tower_type_number = 0
        
        info = constants.tower_constants()[tower_type_number]

        image_path_list = image_paths.tower_image_path_list(tower_type_number)

        self.image = pygame.image.load(image_path_list[0])
        # f stands for firing
        self.f_image = pygame.image.load(image_path_list[1])
        # b stands for base(refers to the towers base)
        self.b_image = pygame.image.load(image_path_list[2])

        self.dmg = int(info[1])
        self.cd = int(info[2])
        self.r_speed = int(info[3])

        # targeting mode(default is rotationaly efficient)
        self.targeting_mode = "default"
        self.targeting_mode = "first"

        # makes sure there is no firing cooldown on placement
        self.wait = self.cd

        # if you don't understand what this line of code means...
        self.firing = False
        self.shoot_enemy = False
        
        self.rect = self.image.get_rect(center=(x, y))

        self.b_rect = self.b_image.get_rect(center=(x, y))

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
            self.r_image = pygame.transform.rotate(self.f_image, self.current_angle)
            self.rect = self.r_image.get_rect(center=(xy[0], xy[1]))
        
        x = math.cos(math.radians(90+self.current_angle))*self.height/2
        y = math.sin(math.radians(90+self.current_angle))*self.height/2

        screen.blit(self.b_image, self.b_rect)
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
                
                for sprite in enemies: # type: ignore
                    dx : int = int(sprite.rect.centerx) - self.rect.centerx # type: ignore
                    dy : int = int(sprite.rect.centery) - self.rect.centery # type: ignore
                    distance = math.sqrt(dx*dx + dy*dy)

                    x += 1

                    if distance < closest_distance:
                        closest_distance = distance
                        closest_id = x

            # targets the most "efficient" enemy; whichever enemy is fastest to shoot
            elif self.targeting_mode == "efficiency" or self.targeting_mode == "default":
                dr = 99999
                lowest_dr = dr
                for sprite in enemies: # type: ignore
                    self.rotation_angle = point_enemy(self.rect.centerx, self.rect.centery, sprite.rect.centerx, sprite.rect.centery) # type: ignore
                    dr = self.rotation_angle - self.current_angle
            
                    x += 1

                    if abs(dr) < abs(lowest_dr):
                        lowest_dr = dr
                        closest_id = x

            # targets the furthest most enemy in range
            elif self.targeting_mode == "first":
                if len(enemies) > 0: # type: ignore
                    closest_id = 1

            # targets the furthest back enemy in range
            elif self.targeting_mode == "last":
                closest_id = len(enemies) # type: ignore

            # targets the enemy with the most hp
            elif self.targeting_mode == "strong":
                e_hp = 0
                highest_e_hp = e_hp
                for sprite in enemies: # type: ignore
                    x += 1
                    e_hp = float(sprite.max_hp) # type: ignore
                    if e_hp > highest_e_hp:
                        highest_e_hp = e_hp
                        closest_id = x

            # makes sure there are enemies within tower range
            if closest_id != 0:
                # gets a list format of the enemies group
                enemy_list = enemies.sprites() # type: ignore
                # finds the angle to targeted enemy
                self.rotation_angle = point_enemy(self.rect.centerx, self.rect.centery, int(enemy_list[closest_id-1].rect.centerx), int(enemy_list[closest_id-1].rect.centery)) # type: ignore
                # checks if firing cooldown is over and that the tower is rotated within 4 degrees of the enemy
                if self.wait >= self.cd and self.current_angle >= self.rotation_angle-2 and self.current_angle <= self.rotation_angle+2:
                    # kills the targeted enemy
                    enemy_list[closest_id-1].damage(self.dmg) # type: ignore
                    self.shoot_enemy = False
                    self.firing = True
                    self.wait = 0



# defines the Tower_Projectiles class
# CURRENTLY OBSOLETE(most likely will not be added again)
class Tower_Projectiles(pygame.sprite.Sprite):
    def __init__(self, projectile : str, x : int, y : int, angle : float):    
        super().__init__()

        self.projectile = projectile

        self.x = x
        self.y = y

        self.angle = angle

        # checks which projectile was spawned
        if projectile == "basic":
            self.image = pygame.image.load("main/b_bullet.png")
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

        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)

        screen.blit(self.r_image, (self.rect.x+x_offset, self.rect.y-y_offset))

        for sprite in enemies: # type: ignore
            if self.rect.colliderect(sprite.rect): # type: ignore
                sprite.kill() # type: ignore

# defines the class Shop
class Shop(pygame.sprite.Sprite):
    def __init__(self, shop : str, x : int, y : int):
        super().__init__()

        self.shop = shop

        self.original_x = x
        self.original_y = y

        # default value for non-panel shop items
        tower_number = 0

        # checks which shop item was initiated
        if shop == "panel":
            self.image = pygame.image.load(image_paths.shop_image_path(shop))
            self.open = False

        # to add more towers copy and paste the code below and continue to elif
        elif shop == "basic": # change the string to relating tower name defined in the Tower class
            tower_number = 0
            # the cost of the tower
            self.cost = 100

        # defines generic things for non-panel shop items
        if shop != "panel":
            self.image = pygame.image.load(image_paths.tower_image_path_list(tower_number)[2])
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
    def showing(self, open : bool):
        if open:
            screen.blit(self.image, self.rect)
            screen.blit(self.text, (self.rect.centerx-self.text.get_width()/2, self.rect.centery+self.rect.height/2))

            # if the mouse is down when hovering over an item in the shop, it will wait until mouse not down, and attempt to buy that item
            if money >= self.cost:
                if mouse_xy[0] >= self.rect.x and mouse_xy[0] < self.rect.x+self.rect.width and mouse_xy[1] >= self.rect.y and mouse_xy[1] < self.rect.y+self.rect.height:
                    # hovering_on_tower used to determine whether to show tower stats
                    self.hovering_on_tower = True
                    if pygame.mouse.get_pressed()[0] and not self.clicked:
                        self.clicked = True
                    elif not pygame.mouse.get_pressed()[0] and self.clicked:
                        self.clicked = False
                        return True, self.cost
                else:
                    self.hovering_on_tower = False
        return False, 0
    
    # if the user bought a tower from the shop, it will follow the mouse until placed
    def place_tower(self):
        self.rect.centerx = mouse_xy[0]
        self.rect.centery = mouse_xy[1]
        screen.blit(self.image, self.rect)

        mask1 = pygame.mask.from_surface(self.image)
        mask2 = pygame.mask.from_surface(path)
    
        offset_x = map_offsets[0] - self.rect.left # type: ignore
        offset_y = map_offsets[1] - self.rect.top # type: ignore

        colliding = mask1.overlap(mask2, (offset_x, offset_y))
        
        # waits to place tower until mouse down and not touching track, it then waits for mouse release to place
        if pygame.mouse.get_pressed()[0] and not colliding:
            self.clicked = True
        elif not pygame.mouse.get_pressed()[0] and self.clicked:
            self.clicked = False
            towers.add(Towers(self.shop, self.rect.centerx, self.rect.centery)) # type: ignore
            self.rect.centerx = self.original_x
            self.rect.centery = self.original_y
            return False
        
        return True
    
    def show_stats(self):
        if self.hovering_on_tower:
            pass
            

    
def stats(money : int, hp : int):
    text = stat_font.render(f'Money: ${money}', True, "black")
    screen.blit(text, (5, 0))
    text = stat_font.render(f'Health: {hp}', True, "black")
    screen.blit(text, (5, 35))

# defines the towers group
towers = pygame.sprite.Group() # type: ignore

towers.add(Towers("basic", 640, 360)) # type: ignore

tower_projectiles = pygame.sprite.Group() # type: ignore

# defines the enemies group
enemies = pygame.sprite.Group() # type: ignore

#enemies.add(Enemies("basic", 8, 280))

# defines the shop group
shop = pygame.sprite.Group() # type: ignore

shop.add(Shop("panel", 640, 900)) # type: ignore
shop.add(Shop("basic", 100, 540)) # type: ignore
 
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

    for sprite in tower_projectiles: # type: ignore
        sprite.move() # type: ignore

    # cycles through all the necessary commands for the towers group
    for sprite in towers: # type: ignore
        sprite.wait += 1 # type: ignore
        sprite.find_closest_enemy() # type: ignore
        #sprite.shoot()
        sprite.unfire() # type: ignore
        sprite.rotate() # type: ignore

    # cycles through all the necessary commands for the enemies group
    for sprite in enemies: # type: ignore
        hp -= int(sprite.pathfind()) # type: ignore

    # cycles through all the necessary commands for the shop group
    for sprite in shop: # type: ignore
        # only runs hovering function for the panel type in the shop group
        if sprite.shop == "panel": # type: ignore
            open = bool(sprite.hovering()) # type: ignore
        # runs normally for all other types in the shop group
        else:
            if not placing_tower:
                temp_pkg : list[bool|int] = sprite.showing(open) # type: ignore
                placing_tower = bool(temp_pkg[0]) # type: ignore
                money -= int(temp_pkg[1]) # type: ignore
            else:
                placing_tower = bool(sprite.place_tower()) # type: ignore

    # draws the enemies on the screen
    enemies.draw(screen)

    stats(money, hp)

    x += 1
    if x > 100:
        enemies.add(Enemies("basic", 8, 280)) # type: ignore
        x = 80

    pygame.display.flip()
    clock.tick(60)