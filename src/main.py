if __name__ == "__main__":

    import pygame

    from enum import Enum
    from enemy import Enemies, enemies
    from tower import Towers, towers
    from shop import Shop, shop
    from upgrade import Upgrades, upgrades
    from money import money_script
    from image_loader import TowerType
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



        
        
    def stats(money : int, health_points : int):
        text = font_30.render(f'Money: ${money}', True, "black")
        screen.blit(text, (5, 0))
        text = font_30.render(f'Health: {health_points}', True, "black")
        screen.blit(text, (5, 35))


    towers.add(Towers("basic", 640, 360))

    shop.add(Shop("shopui", 640, 900))
    for i in range(len(TowerType)):
        shop.add(Shop(TowerType._member_names_[i].lower(), 100+150*i, 540))
    shop.add(Shop("towerui", 0, 0)) # KEEP THIS AT END OF SHOP ITEMS

    upgrades.add(Upgrades("upgradeui", 1180, 360))
    upgrades.add(Upgrades("basicupgrades", 1160, 360))
    
    x = 0
    upgrade_info : list[int|str|float] = [0, "", 0.0]
    upgrading : str = ""
    upgrade_rect : pygame.Rect = pygame.Rect(0, 0, 0, 0)

    hovering_on_tower = False
    tower_being_bought = False
    tower_stats = None
    money_spent = 0
    temp_pkg = []
    clicked = False
    
    play = font_50.render("Play", True, "black")
    play_location = [int(screen.get_width()/2-play.get_width()/2), int(screen.get_height()/2-play.get_height())]
    play_rect = pygame.Rect(play_location[0]-100, play_location[1]-10, play.get_width()+200, play.get_height()+20)
    border = play_rect.inflate(20, 20)

    settings_rect = pygame.Rect(10, 10, 50, 50)


    # and so begins the main script
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if game_screen != GameScreen.IN_GAME:
            screen.fill((255, 255, 255))

        if game_screen == GameScreen.MAIN_MENU:
            pygame.draw.rect(screen, "gray", play_rect, border_radius=15)
            pygame.draw.rect(screen, (100, 100, 100), border, 10, 25)
            pygame.draw.rect(screen, (180, 180, 180), settings_rect)
            screen.blit(play, play_location)
            mouse = mouse_info()
            pressed, clicked = clicked_and_released(mouse[1], clicked)
            if play_rect.collidepoint(mouse[0]) and pressed:
                game_screen = GameScreen.IN_GAME
            elif settings_rect.collidepoint(mouse[0]) and pressed:
                game_screen = GameScreen.SETTINGS

        elif game_screen == GameScreen.SETTINGS:
            pygame.draw.rect(screen, (180, 180, 180), settings_rect)
            mouse = mouse_info()
            pressed, clicked = clicked_and_released(mouse[1], clicked)
            if settings_rect.collidepoint(mouse[0]) and pressed:
                game_screen = GameScreen.MAIN_MENU
            # TODO: add settings

        elif game_screen == GameScreen.IN_GAME:
            screen.fill((50, 200, 20)) # background
            screen.blit(path, (-4, 200)) # map

            for sprite in tower_projectiles:
                sprite.move()

            # cycles through all the necessary commands for the towers group
            open_list : list[bool] = []
            range_circle = None
            tower_selected = None
            right_side = True
            tower_tier = 0
            for sprite in towers:
                sprite.wait += 1
                money_script(True, int(sprite.find_closest_enemy()[1]))
                sprite.unfire()
                sprite.rotate()
                open_list += [sprite.open_upgrades(upgrade_rect)]
                range_circle_test = sprite.show_range()
                if range_circle_test != None:
                    range_circle = range_circle_test
                    tower_selected = sprite.tower
                    tower_tier = sprite.tier

                    if sprite.x > 640:
                        right_side = False

            tower_group = towers.sprites()

            if range_circle != None:
                screen.blit(range_circle[0], range_circle[1])

            # -------------------------------------------------------------- #
            # cycles through all the necessary commands for the enemies group
            # -------------------------------------------------------------- #
            for sprite in enemies:
                health_points -= int(sprite.pathfind())
                pygame.draw.rect(screen, "red", (sprite.x, sprite.y, 5, 5))






            open = False
            if True in open_list:
                open = True

            # cycles through all the necessary commands for the upgrades group
            upgrade_info = [0, "", 0.0]
            for sprite in upgrades:
                if sprite.upgrade == "upgradeui":
                    sprite.hovering(open, right_side) # opens and closes upgrade menu
                    upgrade_rect = sprite.rect
                elif open_list.count(True) > 0: # needed because .index raises a ValueError if the value is not found
                    upgrades_bought = tower_group[open_list.index(True)].upgrades_bought[tower_group[open_list.index(True)].tier] # gets the upgrades bought for the tier of the currently selected tower
                    upgrade_info = sprite.upgrades(open, tower_selected, tower_tier, right_side, upgrades_bought)
                else:
                    upgrade_info = sprite.upgrades(open, tower_selected, tower_tier, right_side, [False, False])

            upgrading = upgrade_info[1] # the stat being upgraded

            if open_list.count(True) > 0 and upgrading != "":
                # subtracts the cost of the money from your money
                upgrade_cost : int = int(upgrade_info[0])
                money_script(False, upgrade_cost)

                current_stat = getattr(tower_group[open_list.index(True)], upgrading)
                setattr(tower_group[open_list.index(True)], upgrading, current_stat*upgrade_info[2]) # multiplies the stat by the upgrade' stat modifier
                print(getattr(tower_group[open_list.index(True)], upgrading))
                if str(upgrade_info[3]).find(".1") != -1:
                    tower_group[open_list.index(True)].upgrades_bought[tower_group[open_list.index(True)].tier][0] = True
                elif str(upgrade_info[3]).find(".2") != -1:
                    tower_group[open_list.index(True)].upgrades_bought[tower_group[open_list.index(True)].tier][1] = True





            # cycles through all the necessary commands for the shop group
            hovering_list : list[bool] = []
            for sprite in shop:
                # only runs hovering function for the panel type in the shop group
                if sprite.shop == "shopui":
                    open = bool(sprite.hovering())
                
                # runs normally for all other types in the shop group
                elif sprite.shop != "towerui":
                    if not placing_tower:
                        temp_pkg = sprite.showing(open)
                        placing_tower = temp_pkg[0]
                        hovering_on_tower = temp_pkg[1]
                        money_spent = temp_pkg[2]

                        if hovering_on_tower:
                            tower_stats = temp_pkg[3]
            
                        if placing_tower:
                            tower_being_bought = str(temp_pkg[4])
                        
                    if tower_being_bought == sprite.shop and placing_tower:
                        placing_tower = bool(sprite.place_tower())

                    if not placing_tower:
                        money_script(False, money_spent)

                    hovering_list += [hovering_on_tower]
                else:
                    if hovering_list.count(True) > 0:
                        hovering_on_tower = True

                    sprite.show_stats(open, hovering_on_tower, tower_stats)


            money = money_script(None, 0)
            stats(money, health_points)

            x += 1
            if x > 10:
                enemies.add(Enemies("basic", 8, 280))
                x = -100

        pygame.display.flip()
        clock.tick(60)
        #print(clock.get_fps())

    pygame.quit()