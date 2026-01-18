if __name__ == "__main__":

    import pygame, constants, math, map_sys

    from enemy import Enemies, enemies # type: ignore
    from tower import Towers, towers # type: ignore
    from shop import Shop, shop # type: ignore
    from upgrade import Upgrades, stat_font
    from money import money_script

    # TO-DO LIST
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

    # just defining variables, nothing to look at
    placing_tower = False
    hp = constants.stat_constants()[1]

    # loads map info
    current_map = map_sys.select_map()
    path, movement_nodes, map_offsets = map_sys.map(current_map)



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


        
    def stats(money : int, hp : int):
        text = stat_font.render(f'Money: ${money}', True, "black")
        screen.blit(text, (5, 0))
        text = stat_font.render(f'Health: {hp}', True, "black")
        screen.blit(text, (5, 35))

    def draw_towers(image : pygame.Surface, rect : tuple[int]):
        screen.blit(image, rect)



    towers.add(Towers("basic", 640, 360)) # type: ignore

    tower_projectiles = pygame.sprite.Group() # type: ignore


    shop.add(Shop("shopui", 640, 900)) # type: ignore
    shop.add(Shop("basic", 100, 540)) # type: ignore
    shop.add(Shop("double", 250, 540)) # type: ignore
    # KEEP THIS AT END OF SHOP ITEMS
    shop.add(Shop("towerui", 0, 0)) # type: ignore

    upgrades = pygame.sprite.Group() # type: ignore
    upgrades.add(Upgrades("upgradeui", 1180, 360)) # type: ignore
    upgrades.add(Upgrades("basicupgrades", 1160, 360)) # type: ignore
    
    # and so begins the main script
    x = 0
    upgrade_info : list[int|str|float] = [0, "", 0.0]
    upgrading : str = ""
    upgrade_rect = pygame.Rect(0, 0, 0, 0)

    hovering_on_tower = False
    tower_stats = None
    found = False
    temp_pkg = []





    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # background
        screen.fill((50, 200, 20))
        # map
        screen.blit(path, (-4, 200))

        for sprite in tower_projectiles: # type: ignore
            sprite.move() # type: ignore





        # cycles through all the necessary commands for the towers group
        open_list : list[bool] = []
        range_circle = None
        tower_selected = None
        right_side = True
        tower_tier = 0
        for sprite in towers: # type: ignore
            sprite.wait += 1 # type: ignore
            money_script(True, int(sprite.find_closest_enemy()[1])) # type: ignore
            sprite.unfire() # type: ignore
            sprite.rotate() # type: ignore
            open_list += [sprite.open_upgrades(upgrade_rect)] # type: ignore
            range_circle_test = sprite.show_range() # type: ignore
            if range_circle_test != None:
                range_circle = range_circle_test # type: ignore
                tower_selected = sprite.tower # type: ignore
                tower_tier = sprite.tier #type: ignore

                if sprite.x > 640: # type: ignore
                    right_side = False

        tower_group = towers.sprites() # type: ignore

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
        upgrade_info = [0, "", 0.0]
        for sprite in upgrades: # type: ignore
            if sprite.upgrade == "upgradeui": # type: ignore
                sprite.hovering(open, right_side) # type: ignore
                upgrade_rect = sprite.rect # type: ignore
            else:
                if open_list.count(True) > 0:
                    upgrade_info = sprite.upgrades(open, tower_selected, tower_tier, right_side, tower_group[open_list.index(True)].upgrades_bought[tower_group[open_list.index(True)].tier]) # type: ignore
                else:
                    upgrade_info = sprite.upgrades(open, tower_selected, tower_tier, right_side, [False, False]) # type: ignore

        # the stat being upgraded
        upgrading = upgrade_info[1]

        if open_list.count(True) > 0 and upgrading != "":
            # subtracts the cost of the money from your money
            upgrade_cost : int = int(upgrade_info[0])
            money_script(False, upgrade_cost)

            current_stat = getattr(tower_group[open_list.index(True)], upgrading) # type: ignore
            setattr(tower_group[open_list.index(True)], upgrading, current_stat*upgrade_info[2]) # type: ignore
            if str(upgrade_info[3]).find(".1") != -1:
                tower_group[open_list.index(True)].upgrades_bought[tower_group[open_list.index(True)].tier][0] = True # type: ignore
            elif str(upgrade_info[3]).find(".2") != -1:
                tower_group[open_list.index(True)].upgrades_bought[tower_group[open_list.index(True)].tier][1] = True # type: ignore





        # cycles through all the necessary commands for the shop group
        hovering_list : list[bool] = []
        for sprite in shop: # type: ignore
            found = False
            # only runs hovering function for the panel type in the shop group
            if sprite.shop == "shopui": # type: ignore
                open = bool(sprite.hovering()) # type: ignore
            
            # runs normally for all other types in the shop group
            elif sprite.shop != "shopui" and sprite.shop != "towerui": # type: ignore
                if not found and not placing_tower:
                    temp_pkg = sprite.showing(open) # type: ignore
                    hovering_on_tower = bool(temp_pkg[1]) # type: ignore
                    if hovering_on_tower:
                        tower_stats = temp_pkg[3] # type: ignore
                        found = True

                if not placing_tower:
                    placing_tower = bool(temp_pkg[0]) # type: ignore
        
                if placing_tower:
                    tower_being_bought = str(temp_pkg[4]) # type: ignore
                    if tower_being_bought == sprite.shop: # type: ignore
                        placing_tower = bool(sprite.place_tower()) # type: ignore

                if not placing_tower:
                    found = False
                    money_script(False, int(temp_pkg[2])) # type: ignore

                hovering_list += [hovering_on_tower]
            else:
                if hovering_list.count(True) > 0:
                    hovering_on_tower = True

                sprite.show_stats(open, hovering_on_tower, tower_stats) # type: ignore


        money = money_script(None, 0)
        stats(money, hp)

        x += 1
        if x > 100:
            enemies.add(Enemies("basic", 8, 280)) # type: ignore
            x = -1000

        pygame.display.flip()
        clock.tick(60)
        #print(clock.get_fps())

    pygame.quit()