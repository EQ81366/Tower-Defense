import pygame, constants, math

from enum import Enum
from tower_aiming import point_enemy
from map_sys import map
from image_loader import load_images, EnemyType, TowerType, ShopType, UpgradeType

# TO-DO LIST
# 1. add tower upgrading
# 1. add more towers/enemies
# 2. make bosses
#
# I'll add more as I go on


# tower upgrading ideas:
# 1. rpg like system; gain points, upgrade different stats
# 2. system like btd6
# 3. branching tree system(pros: lots of variability, cons: a LOT of upgrades to make)
# 4. place tier 1 towers and unlock it's upgrades based on it's tier; tier 1: tier 1 upgrades, tier 2: tier 2 upgrades, etc. you upgrade the tower by merging towers of the same type together


# initiates pygame
pygame.init()
pygame.font.init()

# sets screen width and height
screen = pygame.display.set_mode((1280, 720)) # in pixels

clock = pygame.time.Clock()
running = True



# loads all game images
enemy_images, tower_images, shop_images, upgrade_images = load_images()
print(shop_images)


tower_stat_font = pygame.font.SysFont('Arial', 16)
shop_font = pygame.font.SysFont('Arial', 25)
stat_font = pygame.font.SysFont('Arial', 30)

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

        enemy_type_number = EnemyType[enemy.upper()].value

        info = constants.enemy_constants()[enemy_type_number]

        self.image = enemy_images[EnemyType[enemy.upper()]]

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


        tower_image_bundle = tower_images[TowerType[tower.upper()]]
        tower_type_number = TowerType[tower.upper()].value

        
        info = constants.tower_constants()[tower_type_number]

        # base image
        self.b_image = tower_image_bundle[0]
        # turret image
        self.image = tower_image_bundle[1]
        # firing turret image
        self.f_image = tower_image_bundle[2]

        self.dmg = int(info[2])
        self.cd = int(info[3])
        self.range = int(info[4])
        self.r_speed = int(info[5])

        # makes the physical circle of range
        self.range_circle = pygame.image.load("assets/circle.png")
        self.range_circle = pygame.transform.scale(self.range_circle, (self.range*2, self.range*2))

        # targeting mode(default is rotationaly efficient)
        self.targeting_mode = constants.TargetingStates.EFFICIENT
        self.targeting_mode = constants.TargetingStates.STRONG

        # makes sure there is no firing cooldown on placement
        self.wait = self.cd

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

            # targets the most "efficient" enemy; whichever enemy is fastest to shoot
            if self.targeting_mode == constants.TargetingStates.EFFICIENT:
                dr = 99999
                lowest_dr = dr
                for sprite in enemies: # type: ignore
                    dx : int = int(sprite.rect.centerx) - self.rect.centerx # type: ignore
                    dy : int = int(sprite.rect.centery) - self.rect.centery # type: ignore
                    distance = math.hypot(dx, dy)

                    self.rotation_angle = point_enemy(self.rect.centerx, self.rect.centery, sprite.rect.centerx, sprite.rect.centery) # type: ignore
                    dr = self.rotation_angle - self.current_angle
            
                    x += 1

                    if abs(dr) < abs(lowest_dr) and distance <= self.range:
                        lowest_dr = dr
                        closest_id = x

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
                        closest_id = x

            # targets the furthest most enemy in range
            elif self.targeting_mode == constants.TargetingStates.FIRST:
                for sprite in enemies: # type: ignore
                    dx : int = int(sprite.rect.centerx) - self.rect.centerx # type: ignore
                    dy : int = int(sprite.rect.centery) - self.rect.centery # type: ignore
                    distance = math.hypot(dx, dy)
                    #print(distance)

                    x += 1

                    if distance <= self.range:
                        closest_id = x
                        break

            # targets the furthest back enemy in range
            elif self.targeting_mode == constants.TargetingStates.LAST:
                for sprite in enemies: # type: ignore
                    dx : int = int(sprite.rect.centerx) - self.rect.centerx # type: ignore
                    dy : int = int(sprite.rect.centery) - self.rect.centery # type: ignore
                    distance = math.hypot(dx, dy)

                    x += 1

                    if distance <= self.range:
                        closest_id = x

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

    def open_upgrades(self):
        self.mouse_down = pygame.mouse.get_pressed()[0]
        if self.rect.collidepoint(mouse_xy):
            if self.mouse_down:
                self.clicked = True
            elif not self.mouse_down and self.clicked:
                self.clicked = False
                self.upgrades_open = not self.upgrades_open
        else:
            if self.mouse_down:
                self.clicked = True
            elif not self.mouse_down and self.clicked:
                self.clicked = False
                self.upgrades_open = False
            
        return self.upgrades_open
    
    def show_range(self):
        if self.upgrades_open:
            return self.range_circle, (self.x-self.range_circle.get_width()/2, self.y-self.range_circle.get_height()/2)
        return None



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
            self.image = pygame.image.load("assets/b_bullet.png")
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

        # defines generic things for non-panel shop items
        if not shop.upper() in ShopType.__members__:
            tower_type_number = TowerType[shop.upper()].value

            self.image = tower_images[TowerType[shop.upper()]][0] # loads a tower base image

            tower_stats = constants.tower_constants()[tower_type_number]
            self.cost = int(tower_stats[6])

            self.text = shop_font.render(f'{shop.capitalize()} ${self.cost}', True, "black")

            self.description = [
                tower_stat_font.render(f'{self.shop.capitalize()}:', True, "black"),
                tower_stat_font.render(f'Damage: {tower_stats[2]}', True, "black"),
                tower_stat_font.render(f'Cooldown: {tower_stats[3]}', True, "black"),
                tower_stat_font.render(f'Range: {tower_stats[4]}', True, "black"),
                tower_stat_font.render(f'R-Speed:  {tower_stats[5]}', True, "black")
            ]

            self.clicked = False
        else:
            self.image = shop_images[ShopType[shop.upper()]]
            self.open = False

        self.rect = self.image.get_rect(center=(x, y))

    # checks whether the mouse is hovering over the shop panel and changes the panel accordingly
    def hovering(self):
        if self.rect.collidepoint(mouse_xy):
            self.open = True
            self.rect.centery = 700
        else:
            self.open = False
            self.rect.centery = 900

        screen.blit(self.image, self.rect)
        
        return self.open

    # checks if the shop is open and if so, displays all the items in the shop
    def showing(self, open : bool):
        hovering_on_tower = False
        if open:
            screen.blit(self.image, self.rect)
            screen.blit(self.text, (self.rect.centerx-self.text.get_width()/2, self.rect.centery+self.rect.height/2))

            # if the mouse is down when hovering over an item in the shop, it will wait until mouse not down, and attempt to buy that item
            if self.rect.collidepoint(mouse_xy):
                # hovering_on_tower used to determine whether to show tower stats
                hovering_on_tower = True
                if money >= self.cost:
                    if pygame.mouse.get_pressed()[0] and not self.clicked:
                        self.clicked = True
                    elif not pygame.mouse.get_pressed()[0] and self.clicked:
                        self.clicked = False
                        return True, hovering_on_tower, self.cost, self.description
            else:
                hovering_on_tower = False
        
        if hovering_on_tower:
            return False, hovering_on_tower, 0, self.description
        else:
            return False, hovering_on_tower, 0
        
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
    
    def show_stats(self, open : bool, hovering_on_tower : bool, tower_stats : list[pygame.Surface]|None):
        if open:
            if hovering_on_tower:
                self.rect.bottomleft = mouse_xy
                screen.blit(self.image, self.rect)
                if tower_stats != None:
                    for i in range(len(tower_stats)):
                        screen.blit(tower_stats[i], (self.rect.topleft[0]+10, self.rect.topleft[1]+5+17*i))


class Upgrades(pygame.sprite.Sprite):
    def __init__(self, upgrade : str, x : int, y : int):
        super().__init__()

        self.upgrade = upgrade

        self.x = x
        self.y = y

        upgrade_type_number = UpgradeType[upgrade.upper()].value # type: ignore
        
        self.image = upgrade_images[UpgradeType[upgrade.upper()]]

        self.rect = self.image.get_rect(center=(x, y))      

    def hovering(self, open : bool, right_side : bool):
        if open:
            if right_side:
                self.rect.centerx = self.x
            else:
                self.rect.centerx = (self.x-640)*-1+640

            self.open = True
            screen.blit(self.image, self.rect)
        else:
            self.open = False
        
        return self.open
    
    def show_tower(self, open : bool, tower : str, right_side : bool):
        if open:
            if right_side:
                self.rect.centerx = self.x
            else:
                self.rect.centerx = (self.x-640)*-1+640
            
            screen.blit(tower_images[TowerType[tower.upper()]][0], (self.rect.x-(tower_images[TowerType[tower.upper()]][0].get_width()-self.rect.width)/2, 80))
            screen.blit(tower_images[TowerType[tower.upper()]][1], (self.rect.x-(tower_images[TowerType[tower.upper()]][1].get_width()-self.rect.width)/2, 80-tower_images[TowerType[tower.upper()]][1].get_height()/2))
            text = stat_font.render(tower.capitalize(), True, "black")
            screen.blit(text, (self.rect.x-(text.get_width()-self.rect.width)/2, 160))
            text = shop_font.render(f'Tier: {constants.tower_constants()[TowerType[tower.upper()].value][1]}', True, "black")
            screen.blit(text, (self.rect.x-(text.get_width()-self.rect.width)/2, 193))
            screen.blit(self.image, (self.rect.x-50, self.rect.y))
            screen.blit(self.image, (self.rect.x+50, self.rect.y))
            pygame.draw.rect(screen, "red", (self.rect.centerx, 100, 5, 5))


    
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

shop.add(Shop("shopui", 640, 900)) # type: ignore
shop.add(Shop("basic", 100, 540)) # type: ignore

# KEEP THIS AT END OF SHOP ITEMS
shop.add(Shop("towerui", 0, 0)) # type: ignore

upgrades = pygame.sprite.Group() # type: ignore
upgrades.add(Upgrades("upgradeui", 1180, 360)) # type: ignore
upgrades.add(Upgrades("basicupgrades", 1160, 360)) # type: ignore
 
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
    open_list = []
    range_circle = None
    tower_selected = None
    right_side = True
    for sprite in towers: # type: ignore
        sprite.wait += 1 # type: ignore
        sprite.find_closest_enemy() # type: ignore
        #sprite.shoot()
        sprite.unfire() # type: ignore
        sprite.rotate() # type: ignore
        open_list += [sprite.open_upgrades()] # type: ignore
        range_circle_test = sprite.show_range() # type: ignore
        if range_circle_test != None:
            range_circle = range_circle_test # type: ignore
            tower_selected = sprite.tower # type: ignore

            if sprite.x > 640: # type: ignore
                right_side = False

    if range_circle != None:
        screen.blit(range_circle[0], range_circle[1]) # type: ignore

    # cycles through all the necessary commands for the enemies group
    for sprite in enemies: # type: ignore
        hp -= int(sprite.pathfind()) # type: ignore

    # draws the enemies on the screen
    enemies.draw(screen)

    open = False
    if True in open_list:
        open = True

    # cycles through all the necessary commands for the upgrades group
    for sprite in upgrades: # type: ignore
        if sprite.upgrade == "upgradeui": # type: ignore
            sprite.hovering(open, right_side) # type: ignore
        else:
            sprite.show_tower(open, tower_selected, right_side) # type: ignore

    # cycles through all the necessary commands for the shop group
    hovering_on_tower = False
    tower_stats = None
    for sprite in shop: # type: ignore
        # only runs hovering function for the panel type in the shop group
        if sprite.shop == "shopui": # type: ignore
            open = bool(sprite.hovering()) # type: ignore
        # runs normally for all other types in the shop group
        elif sprite.shop != "shopui" and sprite.shop != "towerui": # type: ignore
            if not placing_tower:
                temp_pkg = sprite.showing(open) # type: ignore
                placing_tower = bool(temp_pkg[0]) # type: ignore
                hovering_on_tower = bool(temp_pkg[1]) # type: ignore
                if hovering_on_tower:
                    tower_stats = temp_pkg[3] # type: ignore
                money -= int(temp_pkg[2]) # type: ignore
            else:
                placing_tower = bool(sprite.place_tower()) # type: ignore
        else:
            sprite.show_stats(open, hovering_on_tower, tower_stats) # type: ignore

    stats(money, hp)

    x += 1
    if x > 100:
        enemies.add(Enemies("basic", 8, 280)) # type: ignore
        x = 0

    #print(len(enemies))

    pygame.display.flip()
    clock.tick(60)
    #print(clock.get_fps())