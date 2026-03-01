if __name__ == "__main__":

    import pygame, threading, os, psutil

    from enum import Enum
    from enemy import Enemies, enemies
    from tower import Towers, towers
    from shop import Shop, shop
    from upgrade import Upgrades, upgrades
    from money import money_script
    from image_loader import TowerType, ShopType, UpgradeType, EnemyType
    from tower_projectiles import tower_projectiles
    from mouse import mouse_info, clicked_and_released
    from fonts import font_30, font_50
    from map_sys import select_map, map
    from constants import stat_constants

    # TODO LIST
    # bruh. clean up code bc I'm lazy and don't want to make art
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
    class LoadGame():
        pygame.init()
        pygame.font.init()

        # sets screen width and height
        screen = pygame.display.set_mode((1280, 720)) # in pixels

        clock = pygame.time.Clock()
        running = True
        
        class GameScreen(Enum):
            MAIN_MENU = 0
            IN_GAME = 1
            SETTINGS = 2

        game_screen = GameScreen.MAIN_MENU

        # just defining variables, nothing to look at
        placing_tower = False
        health_points = stat_constants()[1]

        # loads map info
        current_map = select_map()
        path, movement_nodes, map_offsets = map(current_map)

        for i in range(1):
            towers.add(Towers(TowerType.BASIC, 640, 360))

        shop.add(Shop(ShopType.SHOPUI, 640, 900))
        for i in range(len(TowerType)):
            shop.add(Shop(TowerType._value2member_map_[i], 100+150*i, 540))
        shop.add(Shop(ShopType.TOWERUI, 0, 0)) # KEEP THIS AT END OF SHOP ITEMS

        upgrades.add(Upgrades(UpgradeType.UPGRADEUI, 1180, 360))
        upgrades.add(Upgrades(UpgradeType.UPGRADES, 1160, 360))
        
        x = 0
        upgrade_info : list[int|str|float] = [0, "", 0.0]
        upgrading : str = ""
        upgrade_rect : pygame.Rect = pygame.Rect(0, 0, 0, 0)

        hovering_on_tower = False
        tower_being_bought : ShopType | None = None
        tower_stats : list[pygame.Surface] = []
        money_spent = 0
        temp_pkg = []
        clicked = False
        hovering_list : list[bool] = []
        open_list : list[bool] = []
        range_circle : tuple[pygame.Surface, list[float]] | None = None
        tower_selected : TowerType | None = None
        
        play = font_50.render("Play", True, "black")
        play_location = [int(screen.get_width()/2-play.get_width()/2), int(screen.get_height()/2-play.get_height())]
        play_rect = pygame.Rect(play_location[0]-100, play_location[1]-10, play.get_width()+200, play.get_height()+20)
        border = play_rect.inflate(20, 20)

        settings_rect = pygame.Rect(10, 10, 50, 50)

    def stats(money : int, health_points : int):
        text = font_30.render(f'Money: ${money}', True, "black")
        LoadGame.screen.blit(text, (5, 0))
        text = font_30.render(f'Health: {health_points}', True, "black")
        LoadGame.screen.blit(text, (5, 35))


    loading_game = threading.Thread(target=LoadGame)
    loading_game.start()
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    print(f"Current memory usage: {mem_info.rss / (1024 * 1024):.2f} MB")
    loading_game.join(3.0)
    task_terminated = loading_game.is_alive()
    if task_terminated:
        print("Failed to load game, timed out")

    # and so begins the main script
    while LoadGame.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                LoadGame.running = False

        if LoadGame.game_screen != LoadGame.GameScreen.IN_GAME:
            LoadGame.screen.fill((255, 255, 255))

        if LoadGame.game_screen == LoadGame.GameScreen.MAIN_MENU:
            pygame.draw.rect(LoadGame.screen, "gray", LoadGame.play_rect, border_radius=15)
            pygame.draw.rect(LoadGame.screen, (100, 100, 100), LoadGame.border, 10, 25)
            pygame.draw.rect(LoadGame.screen, (180, 180, 180), LoadGame.settings_rect)
            LoadGame.screen.blit(LoadGame.play, LoadGame.play_location)
            mouse = mouse_info()
            pressed, LoadGame.clicked = clicked_and_released(mouse[1], LoadGame.clicked)

            if LoadGame.play_rect.collidepoint(mouse[0]) and pressed:
                LoadGame.game_screen = LoadGame.GameScreen.IN_GAME
            elif LoadGame.settings_rect.collidepoint(mouse[0]) and pressed:
                LoadGame.game_screen = LoadGame.GameScreen.SETTINGS

        elif LoadGame.game_screen == LoadGame.GameScreen.SETTINGS:
            pygame.draw.rect(LoadGame.screen, (180, 180, 180), LoadGame.settings_rect)
            mouse = mouse_info()
            pressed, LoadGame.clicked = clicked_and_released(mouse[1], LoadGame.clicked)
            if LoadGame.settings_rect.collidepoint(mouse[0]) and pressed:
                LoadGame.game_screen = LoadGame.GameScreen.MAIN_MENU
            # TODO: add settings

        elif LoadGame.game_screen == LoadGame.GameScreen.IN_GAME:
            LoadGame.screen.fill((50, 200, 20)) # background
            LoadGame.screen.blit(LoadGame.path, (-4, 200)) # map




            tower_list = towers.sprites()
            for sprite in tower_projectiles:
                enemy_death_info = sprite.move()
                tower_list[int(enemy_death_info[1])].enemies_killed[enemy_death_info[0][0]] += 1





            # cycles through all the necessary commands for the towers group
            LoadGame.range_circle = None # resets showing range
            LoadGame.open_list.clear()
            right_side = True
            tower_tier = 0
            for sprite in towers:
                sprite.wait += 1
                money_script(True, int(sprite.find_closest_enemy()[1]))
                #sprite.unfire()
                sprite.rotate()
                LoadGame.open_list += [sprite.open_upgrades(LoadGame.upgrade_rect)]
                range_circle_test = sprite.show_range()
                if range_circle_test != None:
                    LoadGame.range_circle = range_circle_test
                    LoadGame.screen.blit(LoadGame.range_circle[0], LoadGame.range_circle[1])
                    LoadGame.tower_selected = sprite.tower
                    tower_tier = sprite.tier

                    if sprite.x > 640:
                        right_side = False

            #if LoadGame.range_circle != None:
                

            # -------------------------------------------------------------- #
            # cycles through all the necessary commands for the enemies group
            # -------------------------------------------------------------- #
            for sprite in enemies:
                LoadGame.health_points -= int(sprite.pathfind())
                pygame.draw.rect(LoadGame.screen, "red", (sprite.x, sprite.y, 5, 5))






            open = False
            if True in LoadGame.open_list:
                open = True

            # cycles through all the necessary commands for the upgrades group
            LoadGame.upgrade_info = [0, "", 0.0]
            open_index = next((i for i, open in enumerate(LoadGame.open_list) if open), None) # if True is found in open_list, returns index of True, else returns None
            for sprite in upgrades:
                if sprite.upgrade == UpgradeType.UPGRADEUI:
                    sprite.hovering(open, right_side) # opens and closes upgrade menu
                    LoadGame.upgrade_rect = sprite.rect
                elif LoadGame.tower_selected != None:
                    if open_index != None:
                        upgrades_bought = tower_list[open_index].upgrades_bought[tower_list[open_index].tier] # gets the upgrades bought for the tier of the currently selected tower
                        LoadGame.upgrade_info = sprite.upgrades(open, LoadGame.tower_selected, tower_tier, right_side, upgrades_bought)
                    else:
                        LoadGame.upgrade_info = sprite.upgrades(open, LoadGame.tower_selected, tower_tier, right_side, [False, False])

            LoadGame.upgrading = str(LoadGame.upgrade_info[1]) # the stat being upgraded

            if open_index != None and LoadGame.upgrading != "":
                # subtracts the cost of the money from your money
                upgrade_cost : int = int(LoadGame.upgrade_info[0])
                money_script(False, upgrade_cost)

                current_stat = getattr(tower_list[open_index], LoadGame.upgrading)
                setattr(tower_list[open_index], LoadGame.upgrading, current_stat*LoadGame.upgrade_info[2]) # multiplies the stat by the upgrade' stat modifier
        
                if str(LoadGame.upgrade_info[3]).find(".1") != -1:
                    tower_list[open_index].upgrades_bought[tower_list[open_index].tier][0] = True
                elif str(LoadGame.upgrade_info[3]).find(".2") != -1:
                    tower_list[open_index].upgrades_bought[tower_list[open_index].tier][1] = True





            # cycles through all the necessary commands for the shop group
            LoadGame.hovering_list.clear()
            for sprite in shop:
                # only runs hovering function for the panel type in the shop group
                if sprite.shop == ShopType.SHOPUI:
                    open = bool(sprite.hovering())
                
                elif sprite.tower: # checks if the shop item is a tower
                    if not LoadGame.placing_tower:
                        temp_pkg = sprite.showing(open)
                        LoadGame.placing_tower = temp_pkg[0]
                        LoadGame.hovering_on_tower = temp_pkg[1]
                        LoadGame.money_spent = temp_pkg[2]

                        if LoadGame.hovering_on_tower:
                            LoadGame.tower_stats = temp_pkg[3]
            
                        if LoadGame.placing_tower:
                            LoadGame.tower_being_bought = temp_pkg[4]
                        
                    if LoadGame.tower_being_bought == sprite.shop and LoadGame.placing_tower:
                        LoadGame.placing_tower = bool(sprite.place_tower())

                    if not LoadGame.placing_tower:
                        money_script(False, LoadGame.money_spent)

                    LoadGame.hovering_list += [LoadGame.hovering_on_tower]
                else:
                    if LoadGame.hovering_list.count(True) > 0:
                        sprite.show_stats(open, LoadGame.tower_stats)


            money = money_script(None, 0) # finds the current amount of money
            stats(money, LoadGame.health_points)

            LoadGame.x += 1
            if LoadGame.x > 10:
                enemies.add(Enemies(EnemyType.BASIC, 8, 280))
                LoadGame.x = -10000

        pygame.display.flip()
        LoadGame.clock.tick(60)
        print(LoadGame.clock.get_fps())

    pygame.quit()