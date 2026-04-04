import numpy


if __name__ == "__main__":
    import pygame, os, psutil

    # initiates pygame
    pygame.init()
    pygame.font.init()

    from enum import Enum
    from enemy import Enemies, enemies
    from tower import Towers, towers
    from shop import Shop, shop
    from upgrade import Upgrades, upgrades
    from money import money_script
    from tower_projectiles import tower_projectiles
    from mouse import mouse_info, clicked_and_released
    from fonts import font_30, font_50
    from map_sys import select_map, map
    from constants import stat_constants, TowerConstants, ShopType, UpgradeType, EnemyType

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

    initialized = False

    # sets screen width and height
    screen = pygame.display.set_mode((1280, 720))  # in pixels

    clock = pygame.time.Clock()
    running = True

    class GameScreen(Enum):
        MAIN_MENU = 0
        IN_GAME = 1
        SETTINGS = 2

    game_screen = GameScreen.IN_GAME

    # just defining variables, nothing to look at
    placing_tower = False
    health_points = stat_constants()[1]

    # loads map info
    current_map = select_map()
    path, movement_nodes, map_offsets = map(current_map)

    for i in range(0):
        towers.add(Towers(TowerConstants.BASIC, 640, 360))

    shop.add(Shop(ShopType.SHOPUI, 640, 900))
    for i, tower in enumerate(TowerConstants):
        shop.add(Shop(tower, 100 + 150 * i, 540))
    shop.add(Shop(ShopType.TOWERUI, 0, 0))  # KEEP THIS AT END OF SHOP ITEMS

    upgrades.add(Upgrades(UpgradeType.UPGRADEUI, 1180, 360))
    upgrades.add(Upgrades(UpgradeType.UPGRADES, 1160, 360))

    x = 0
    upgrade_info: list[int | str | float] = [0, "", 0.0]
    upgrading: str = ""
    upgrade_rect: pygame.Rect = pygame.Rect(0, 0, 0, 0)

    hovering_on_tower = False
    tower_being_bought: ShopType | None = None
    tower_stats: list[pygame.Surface] = []
    money_spent = 0
    temp_pkg = []
    clicked = False
    hovering_list: list[bool] = []
    open_list: list[bool] = []
    range_circle: tuple[pygame.Surface, list[float]] | None = None
    tower_selected: TowerConstants | None = None

    enemy_cap = 10000

    enemy_x = numpy.zeros(10000, dtype=numpy.float32)
    enemy_y = numpy.zeros(10000, dtype=numpy.float32)
    enemy_movement_vector = numpy.zeros([10000, 2], dtype=numpy.float32)
    # grouping = numpy.zeros([10000, 2], dtype=numpy.float32)

    play = font_50.render("Play", True, "black").convert_alpha()
    play_location = [
        int(screen.get_width() / 2 - play.get_width() / 2),
        int(screen.get_height() / 2 - play.get_height()),
    ]
    play_rect = pygame.Rect(
        play_location[0] - 100,
        play_location[1] - 10,
        play.get_width() + 200,
        play.get_height() + 20,
    )
    border = play_rect.inflate(20, 20)
    settings_rect = pygame.Rect(10, 10, 50, 50)

    initialized = True

    def stats(money: int, health_points: int):
        text = font_30.render(f"Money: ${money}", True, "black")
        screen.blit(text, (5, 0))
        text = font_30.render(f"Health: {health_points}", True, "black")
        screen.blit(text, (5, 35))

    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    print(f"Current memory usage: {mem_info.rss / (1024 * 1024):.2f} MB")

    frame_check = 0

    # fps_list = numpy.array([99.9])

    # and so begins the main script
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if game_screen is not GameScreen.IN_GAME:
            screen.fill((255, 255, 255))
            if frame_check < 100:
                frame_check += 1

        if game_screen is GameScreen.MAIN_MENU:
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

        elif game_screen is GameScreen.SETTINGS:
            pygame.draw.rect(screen, (180, 180, 180), settings_rect)
            mouse = mouse_info()
            pressed, clicked = clicked_and_released(mouse[1], clicked)
            if settings_rect.collidepoint(mouse[0]) and pressed:
                game_screen = GameScreen.MAIN_MENU
            # TODO: add settings

        elif game_screen is GameScreen.IN_GAME:
            screen.fill((50, 200, 20))  # background
            screen.blit(path, (-4, 200))  # map

            # -------------------------------------------------------------- #
            # cycles through all the necessary commands for the enemies group
            # -------------------------------------------------------------- #
            if len(enemies) > enemy_cap:
                enemy_group = enemies.sprites()
                for i in range(len(enemies) - enemy_cap):
                    enemy_group[i].kill()

            for i, sprite in enumerate(enemies):
                enemy_movement_vector[i] = sprite.pathfind(screen)
                # try:
                # if grouping != 0:
                #    enemy_movement_vector[i][0] = grouping[0]
                #    enemy_movement_vector[i][1] = grouping[1]
                # except:
                #    pass
                enemy_x[i] = sprite.rect.centerx
                enemy_y[i] = sprite.rect.centery
                # pygame.draw.rect(screen, "red", (sprite.xy[0], sprite.xy[1], 5, 5))
            # --------------------------------------------------------------------- #

            tower_list = towers.sprites()
            # ------------------------------------------------------------------- #
            # cycles through all the necessary commands for the tower projectiles
            # ------------------------------------------------------------------- #
            for sprite in tower_projectiles:
                enemy_death_info = sprite.move(enemy_x, enemy_y, enemy_movement_vector)
                if enemy_death_info[0] != [0, 0]:
                    tower_list[int(enemy_death_info[1])].enemies_killed[enemy_death_info[0][0]] += 1
            # ---------------------------------------------------------------------------------------- #

            # ------------------------------------------------------------- #
            # cycles through all the necessary commands for the towers group
            # ------------------------------------------------------------- #
            range_circle = None  # resets showing range
            open_list.clear()
            right_side = True
            tower_tier = 0
            for sprite in towers:
                sprite.wait += 1
                sprite.rotate()
                money_script(True, int(sprite.find_closest_enemy(enemy_x, enemy_y)[1]))
                open_list += [sprite.open_upgrades(upgrade_rect)]
                range_circle_test = sprite.show_range()
                if range_circle_test is not None:
                    range_circle = range_circle_test
                    screen.blit(range_circle[0], range_circle[1])
                    tower_selected = sprite.tower
                    tower_tier = sprite.tier

                    if sprite.x > 640:
                        right_side = False

            open = False
            if True in open_list:
                open = True

            # ---------------------------------------------------------------- #
            # cycles through all the necessary commands for the upgrades group
            # ---------------------------------------------------------------- #
            upgrade_info = [0, "", 0.0]
            open_index = next(
                (i for i, open in enumerate(open_list) if open), None
            )  # if True is found in open_list, returns index of True, else returns None
            for sprite in upgrades:
                if sprite.upgrade == UpgradeType.UPGRADEUI:
                    sprite.hovering(open, right_side)  # opens and closes upgrade menu
                    upgrade_rect = sprite.rect
                elif tower_selected is not None:
                    if open_index is not None:
                        upgrades_bought = tower_list[open_index].upgrades_bought[
                            tower_list[open_index].tier
                        ]  # gets the upgrades bought for the tier of the currently selected tower
                        upgrade_info = sprite.upgrades(
                            open,
                            tower_selected,
                            tower_tier,
                            right_side,
                            upgrades_bought,
                        )
                    else:
                        upgrade_info = sprite.upgrades(
                            open,
                            tower_selected,
                            tower_tier,
                            right_side,
                            [False, False],
                        )

            upgrading = str(upgrade_info[1])  # the stat being upgraded

            if open_index is not None and upgrading != "":
                # subtracts the cost of the money from your money
                upgrade_cost: int = int(upgrade_info[0])
                money_script(False, upgrade_cost)

                current_stat = getattr(tower_list[open_index], upgrading)  # gets the stat that's being upgraded
                setattr(
                    tower_list[open_index],
                    upgrading,
                    current_stat * upgrade_info[2],
                )  # multiplies the stat by the upgrade' stat modifier

                if str(upgrade_info[3]).find(".1") != -1:
                    tower_list[open_index].upgrades_bought[tower_list[open_index].tier][0] = True
                elif str(upgrade_info[3]).find(".2") != -1:
                    tower_list[open_index].upgrades_bought[tower_list[open_index].tier][1] = True
            # ------------------------------------------------------------------------------------ #

            # ------------------------------------------------------------ #
            # cycles through all the necessary commands for the shop group
            # ------------------------------------------------------------ #
            hovering_list.clear()
            for sprite in shop:
                # only runs hovering function for the panel type in the shop group
                if sprite.shop is ShopType.SHOPUI:
                    open = bool(sprite.hovering(screen))

                elif sprite.tower:  # checks if the shop item is a tower
                    if not placing_tower:
                        temp_pkg = sprite.showing(screen, open)
                        placing_tower = temp_pkg[0]
                        hovering_on_tower = temp_pkg[1]
                        money_spent = temp_pkg[2]

                        if hovering_on_tower:
                            tower_stats = temp_pkg[3]

                        if placing_tower:
                            tower_being_bought = temp_pkg[4]

                    if tower_being_bought is sprite.shop and placing_tower:
                        placing_tower = bool(sprite.place_tower(screen))

                    if not placing_tower:
                        money_script(False, money_spent)

                    hovering_list += [hovering_on_tower]
                else:
                    if True in hovering_list:
                        sprite.show_stats(screen, open, tower_stats)
            # ------------------------------------------------------------------------------- #

            money = money_script(None, 0)  # finds the current amount of money
            stats(money, health_points)

            x += 1
            if x > 10:
                for i in range(10):
                    enemies.add(Enemies(EnemyType.BASIC, 8, 280))
                x = 10

        pygame.display.flip()
        # pygame.display.update()
        clock.tick(60)
        fps = clock.get_fps()
        print(fps, len(enemies))
        # print(fps)
        if fps < 5 and frame_check == 100:
            print("GAME CRASHED")
            running = False
            pygame.quit()

    pygame.quit()
